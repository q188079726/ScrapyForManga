import os
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas

base_path = '/Users/LeeShow/Pictures/kingdom/'
base_dir = os.path.dirname(base_path)
error_log = os.path.join(base_dir,'error_log')

for dir in os.listdir(base_dir):
    path = os.path.join(base_path,dir)
    if not os.path.isdir(path):
        continue
    pdf_path = base_path+dir.split('.')[0]+'.pdf'
    (w,h) = portrait(A4)
    c = canvas.Canvas(pdf_path,pagesize=(w,h))
    
    list = os.listdir(path)

    l = sorted(list,key=lambda string: int(string.split('.')[0]))
    for file_name in l:
        file_path = os.path.join(path,file_name)
        try:
             c.drawImage(file_path,0,0,w,h)
             c.showPage()
        except Exception as e:
            print(file_path)
            with open(error_log,'a') as f:
                f.write('wrong file is:'+file_path)
    c.save()
    print('ok')


