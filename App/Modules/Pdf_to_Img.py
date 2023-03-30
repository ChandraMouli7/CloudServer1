from PIL import Image
import os, fitz, io

def convert(file, path):
    print(file.filename) 
    if file.filename.endswith('.pdf'):   
        pdf_doc = fitz.open(stream=io.BytesIO(file.read()), filetype='pdf')
        page = pdf_doc[0]
        pix = page.get_pixmap(alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        filename = os.path.splitext(file.filename)[0] + '.png'
        filepath = os.path.join(path, filename)
        img.save(filepath)
    
    else:
        filename = file.filename
        filepath = os.path.join(path, filename)
        file.save(filepath)

    return filepath, filename


    # for page_idx in range(pdf_doc.page_count):
    #     page = pdf_doc[page_idx]   
    #     pix = page.get_pixmap(alpha=False)
    #     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    #     img.save(f"{os.path.splitext(file.filename)[0]}_{page_idx+1}.png")