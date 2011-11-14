######################################################################################### 
#Babington plot'

# Joao Wilbert - 2011
# Code developed for educational purposes

#########################################################################################

from Tkinter import *
import os
from PIL import Image, ImageTk
import Tkinter

######################################################################################### 
# Class Definition


# http://zetcode.com/tutorials/tkintertutorial/layout/

class ImageFile():
    def __init__(self,image,xpos,ypos):
        
        self.image = image
        
        image1 = Image.open('captured/'+image) 
        tkpi = ImageTk.PhotoImage(image1)
        label_image = Tkinter.Label(root, image=tkpi)
        label_image.place(x=xpos,y=ypos,width=image1.size[0],height=image1.size[1])
        root.title(image)
        
        root.mainloop()

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.


######################################################################################### 
# Creating GUI

dirlist = os.listdir('captured/')

# Start GUI
root = Tk()

# Go Fullscreen
w = root.winfo_screenwidth()
h = root.winfo_screenheight()

root.geometry("%dx%d+0+0" % (w, h))
root.configure(background='black')
root.bind("<Button>", button_click_exit_mainloop)
#root.overrideredirect(1)


for img_file in dirlist:
    img = ImageFile(img_file,10,20)
    
