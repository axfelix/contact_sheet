import os
from PIL import Image, ImageFont, ImageDraw, ImageColor

# Purpose: Create a contact sheet for a folder of images. Resize and label images, then arrange in a grid in a single file. Convert to pdf. Before running, ensure working directory is the folder with images to be processed.

# Function to add text to images (ie, label by fname)
def add_label(dir):
    os.makedirs("LabelledImages")
    for filename in dir:
        f = filename.lower()
        ext = f.split('.')[len(f.split('.'))-1]
        e_list = ['png', 'jpg', 'tiff', 'gif', 'jp2', 'jpm', 'jpx', 'bmd', 'pct', 'psd', 'tga']
        if not ext in e_list: continue
        else:            
            img = Image.open(filename)
            img.thumbnail((300,300))
            old_size = img.size
            new_size = (350,350)
            newim = Image.new("RGB", new_size, color = 'white')
            newim.paste(img, ((new_size[0]-old_size[0])//2,
                      (new_size[1]-old_size[1])//2))
            labelled = ImageDraw.Draw(newim)
            font = ImageFont.truetype('arial.ttf', 38)
            txt = str(dir.index(filename)+1)+ "_" + filename[:filename.index(".")]
            if len(txt) > 10:
                labelled.text((5,5), txt[0:10], font = font, fill = 'black')
            else:
                labelled.text((5,5), txt, font = font, fill = 'black')
            newim.save("LabelledImages\\"+"L_"+filename)
            newim.close()
            img.close()

# Get file names of images and run function
dir = os.listdir(os.getcwd())
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
        
    size = (350*n_col, 350*n_row)    
    bg =  Image.new("RGB", size, color = 'white')
    for i in range(0, q):
        j=0        
        while j < n_col:
            im = Image.open(imlist[n_col*i+j])
            bg.paste(im, (350*j, 350*i))
            j += 1
        bg.save("contact_sheet.pdf")
    if r != 0:
        k = n_col*q
        count = 0
        for n in range(k, k+r):
            im = Image.open(imlist[n])
            bg.paste(im, (350*count, 350*q))
            count += 1
            bg.save("contact_sheet.pdf")
    bg.close()
    im.close()

os.chdir("LabelledImages")
imlist = os.listdir(os.getcwd())

contactsheet(imlist, 5)