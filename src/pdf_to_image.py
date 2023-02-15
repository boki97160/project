from pdf2image import convert_from_path
images = convert_from_path("src/Nurmilintu_revised_eng.pdf",300,poppler_path=r'C:\Program Files\poppler-0.67.0\bin')
for i, image in enumerate(images):
    fname = 'resized_image'+str(i)+'.png'
    image.save(fname, "PNG")