from Tkinter import *
import os


root = Tk()

#
dirlist = os.listdir('imgs/')
print dirlist

for image in dirlist:
    try:
        w = Label(root, image=image)
        w.pack()
        
        
    except Exception, e:
        pass

root.mainloop()
