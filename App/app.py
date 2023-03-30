import os
from flask import Flask, jsonify, json, render_template,request
from roboflow import Roboflow
import easyocr
from PIL import Image
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import fitz, io

from Modules import Database, Crop, Table_Extraction, Clean_Data, Pdf_to_Img


UPLOAD_FOLDER = r'C:\\Users\\chand\\OneDrive\\Desktop\\Flask\\FAER\\Uploaded_Files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


user_id = 1

class User(db.Model):
    User_Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20),nullable=False,unique=True)
    Password = db.Column(db.String(80),nullable=False)
    invoice = db.relationship('Invoice',backref='user')

class Invoice(db.Model):
    User_Id = db.Column(db.Integer, db.ForeignKey('user.User_Id'))
    Invoice_No = db.Column(db.Integer, primary_key=True)
    Invoice_Name = db.Column(db.String(50))
    Description = db.Column(db.String(100))
    invoice_items = db.relationship('Invoice_Items',backref='invoice')

class Invoice_Items(db.Model):
    Item_id = db.Column(db.Integer, primary_key=True)
    Invoice_No = db.Column(db.Integer, db.ForeignKey('invoice.Invoice_No'))
    Product_Name = db.Column(db.String(100))
    Quantity = db.Column(db.String(20))
    Price = db.Column(db.String(20))
    Total = db.Column(db.String(20))



def add_invoice(user_id, invoice_no, invoice_name, description):
    new_invoice = Invoice(User_Id=user_id, Invoice_No=invoice_no, Invoice_Name=invoice_name, Description=description)
    db.session.add(new_invoice)
    db.session.commit()


def add_items(items):
    for item in items:
        new_item = Invoice_Items(Invoice_No=item[0], Product_Name=item[1], Quantity=item[4], Price=item[2], Total=item[3])
        db.session.add(new_item)
        db.session.commit()

def extract_from_db(invoice_no):
    invoice_no = str(invoice_no)
    con = sqlite3.connect('instance/database.db')
    cursor = con.cursor()
    cursor.execute("select Product_Name,Quantity,Price,Total  from Invoice__Items WHERE Invoice_No="+invoice_no)
    data = cursor.fetchall()
    list_data=[]
    for i in data:
        temp=[]
        for j in i:
            temp.append(j)
        list_data.append(temp)
    dict_data={}
    dict_data['items'] = list_data
    return dict_data


def roboflow(filepath, filename):
    rf = Roboflow(api_key="p6ULMmvcwzyrdE53WdqW")
    project = rf.workspace().project("table-detection-zowgr")
    model = project.version(3).model
    # model.predict("C:\\Users\\chand\\OneDrive\\Desktop\\images\\Final Images\\invoice1.jpg", confidence=40, overlap=30).save("prediction.jpg")
    tablejson = model.predict(filepath, confidence=40, overlap=30).json()

    #Code for Seperating Table and Image
    height = int(tablejson["predictions"][0]["height"])
    width = int(tablejson["predictions"][0]["width"])
    x = int(tablejson["predictions"][0]["x"])
    y = int(tablejson["predictions"][0]["y"])
    invoice_image = Image.open(filepath)
    Crop.crop_table(invoice_image, x, y, width, height)

    #Code for extracting data from invoice other than table

    #Code for extracting data from table image
    filename = os.path.splitext(filename)[0]
    tablename = filename + "_table.jpg"
    tablepath = os.path.join(app.config['UPLOAD_FOLDER'], tablename)
    reader = easyocr.Reader(['en'])
    table = reader.readtext(tablepath)
    # reader = easyocr.Reader(['en'], gpu = True)
    # table = reader.readtext(tablepath, width_ths=0.9, height_ths=0.9)
    tabledata = Table_Extraction.table_data(table)      

    return tabledata





@app.route('/list')
def home():
    id = str(user_id)
    con = sqlite3.connect('instance/database.db')
    cursor = con.cursor()
    cursor.execute('select Invoice_No, Invoice_Name from Invoice where User_Id='+id)
    data = cursor.fetchall()
    final_data=[]
    for i in data:
        dict_data ={}
        dict_data['no'] = i[0]
        dict_data['name'] = i[1]
        final_data.append(dict_data)

    return final_data


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    invoice_no = request.form['invoice_no']
    invoice_name = request.form['invoice_name']
    description = request.form['description']

    filepath, filename = Pdf_to_Img.convert(file, app.config['UPLOAD_FOLDER'])
    # filename = os.path.splitext(file.filename)[0] + '.png'
    filedata = roboflow(filepath, filename)
    print(filedata)

    cleaned_filedata = Clean_Data.clean_data(filedata)
    print(cleaned_filedata)

    invoice_items = Database.get_invoice_items(cleaned_filedata, invoice_no)
    add_invoice(user_id, invoice_no, invoice_name, description)
    add_items(invoice_items)

    return jsonify({'msg':'Uploaded Sucessfully'})


@app.route('/invoice', methods=['POST'])
def invoice():
    invoice_no = request.get_json(force=True)
    invoice_data = extract_from_db(invoice_no)
    return jsonify(invoice_data)


    

if __name__ == "__main__":
    app.run(debug = True)
    # app.run(host='192.168.143.85', debug = True)

