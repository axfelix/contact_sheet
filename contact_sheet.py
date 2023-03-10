import os
import sys
from PIL import Image, ImageFont, ImageDraw
from PyPDF2 import PdfMerger
from shutil import copyfile

# Purpose: Create a contact sheet for a folder of images. Resize and label images, then arrange in a grid in a single file.
# Convert to pdf. Before running, ensure working directory is the folder with images to be processed.

# Function to add text to images (ie, label by fname)
def add_label(dir):
    os.makedirs("access")
    im_count = 0
    for filename in dir:
        ext = os.path.splitext(filename)[1].lower()
        e_list = ['.png', '.jpg', '.jpeg', '.tiff', '.gif', '.jp2', '.jpm', '.jpx', '.bmd', '.pct', '.psd', '.tga']
        if not ext in e_list: continue
        else:
            im_count += 1
            img = Image.open(filename)
            img.thumbnail((250,250))
            old_size = img.size
            new_size = (300,300)
            newim = Image.new("RGB", new_size)
            newim.paste(img, ((new_size[0]-old_size[0])//2,
                      (new_size[1]-old_size[1])//2))
            labelled = ImageDraw.Draw(newim)
            if sys.platform.startswith('darwin'):
                font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 38)
            elif sys.platform.startswith('win'):
                font = ImageFont.truetype('arial.ttf', 38)
            else:
                font = ImageFont.load_default()
            txt = str(im_count) + "_" + filename[:filename.index(".")]
            if len(txt) > 10:
                labelled.text((5,5), txt[0:10], font = font, fill = 'white')
            else:
                labelled.text((5,5), txt, font = font, fill = 'white')
            newim.save(os.path.join("access", (str(im_count)+"_"+filename)))
            newim.close()
            img.close()

# Get file names of images and run function
loc = input('Enter folder location:')
try:
    os.chdir(loc)
    dir = os.listdir(os.getcwd())
except:
    print('Error: invalid directory')
    quit()

add_label(dir)

#Tile the images
def contactsheet(imlist, n_col):
    n_img = len(imlist)   # number of  images
    q = n_img//n_col   # quotient, or number of full rows
    r = n_img%n_col   # remainder, or number of images in any partially filled rows    
    if r == 0: 
        n_row = q
    else:
        n_row = q + 1         
    size = (300*n_col, 300*n_row)    
    bg =  Image.new("RGB", size)
    for i in range(0, q):
        j=0        
        while j < n_col:
            im = Image.open(imlist[n_col*i+j])
            bg.paste(im, (300*j, 300*i))
            j += 1
            im.close()
        bg.save("contact_sheet.jpg")
    if r != 0:
        k = n_col*q
        count = 0
        for n in range(k, k+r):
            im = Image.open(imlist[n])
            bg.paste(im, (300*count, 300*q))
            count += 1
            bg.save("contact_sheet.jpg")
            im.close()
    bg.close()


os.chdir("access")
imlist = os.listdir(os.getcwd())
imlist.sort(key = lambda x: int(x.split("_")[0]))
contactsheet(imlist, 5)

#To divide long sheets into multi-page pdf
def multi_pg(cs):
    im = Image.open(cs)
    w,h = im.size
    p = h//1800 #max pixel length per page for letter size
    rem = h%1800
    if rem == 0:
        pgs = p
    else:
        pgs = p + 1
    for i in range(pgs):
        cr = im.crop((0, 1800*i, w, 1800+(1800*i)))
        filename = 'pg' + str(i+1) + '.pdf'
        cr.save(filename)
        cr.close()
    dir = os.listdir(os.getcwd())
    pdfs = []
    for file in dir:
        if file.endswith('.pdf'):
            pdfs.append(file)
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write((os.path.basename(loc)+"-contact_sheet.pdf"))
    merger.close()
    im.close()
    
multi_pg("contact_sheet.jpg")
copyfile((os.path.basename(loc)+"-contact_sheet.pdf"),
         os.path.join(loc, (os.path.basename(loc)+"-contact_sheet.pdf")))

#Clean up files
os.remove('contact_sheet.jpg')

dir2 = os.listdir(os.getcwd())

for filename in dir2:
    if filename in imlist:
        os.remove(filename)
    if filename.startswith('pg') and filename.endswith('.pdf'):
        os.remove(filename)
