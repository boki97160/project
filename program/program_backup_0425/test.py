
import numpy as np
import cv2
import fitz    
pdffile = '../popular_pattern/ANTLERTOQUE-tincanknits.pdf'
doc = fitz.open(pdffile)
for page_index in range(doc.page_count):
    page = doc.load_page(page_index)  
    pix = page.get_pixmap(dpi=300)
    nppix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
    cv2.imwrite('page'+str(page_index)+'.png',nppix)