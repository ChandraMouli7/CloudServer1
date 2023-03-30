import os
def crop_table(img, x, y, width, height):
    x-=int(width/2)
    y-=int(height/2)
    cropped_img = img.crop((x, y, x + width, y + height))
    cropped_img.show()
    actual_name = os.path.splitext(img.filename)[0]
    output_name = actual_name + "_table"
    cropped_img.save(f"{output_name}.jpg")

def crop_above(img, x, y, width, height):
    w,h = img.size
    y-=int(height/2)
    cropped_img = img.crop((0,0,w,y))
    cropped_img.show()    
    actual_name = os.path.splitext(img.filename)[0]
    output_name = actual_name + "_above"
    cropped_img.save(f"{output_name}.jpg")
    
def crop_below(img, x, y, width, height):
    w,h = img.size
    y+=int(height/2)
    cropped_img = img.crop((0,y,w,h))
    cropped_img.show()    
    actual_name = os.path.splitext(img.filename)[0]
    output_name = actual_name + "_below"
    cropped_img.save(f"{output_name}.jpg")