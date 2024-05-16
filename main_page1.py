from tkinter import *
from PIL import Image, ImageTk
import subprocess


root = Tk()
root.geometry("1000x700")
root.configure(bg= "#aaaaaa")

root.tk.call('wm', 'iconphoto', root._w, ImageTk.PhotoImage(Image.open('img/icon.jpg')))


root.grid_columnconfigure(1,weight=1)
root.grid_rowconfigure(1,weight=1)

def kill():
    root.destroy()
    import login_page1

frame1 = Frame(root, bg = "#cccccc")
#frame1.grid(row = 0, column = 0, columnspan = 2)
frame1.grid(row=0, column=0, columnspan= 2, sticky= "WE", padx= 5, pady= (5,0))

frame2 = Frame(root, bg = "#cccccc")
#frame1.grid(row = 1, column = 0)
frame2.grid(row=1, column=0, sticky = "NSWE", padx= (5,0), pady = 5)

frame3 = Frame(root, bg = "#dddddd")
#frame1.grid(row = 1, column = 1)
frame3.grid(row=1, column=1, sticky = "NSWE", padx= 5, pady= 5)

frame3.rowconfigure(1, weight= 1)
frame3.columnconfigure(0, weight= 1)

selectedfilter = Frame(frame3, bg = "#444444")
selectedfilter.grid(row=0, column=0,sticky="NSWE", padx=5, pady=5)

gallery = Frame(frame3, bg = "#444444")
gallery.grid(row=1, column=0,sticky="NSWE", padx=5, pady=5)

#top menu
menuselect = ["quan", "too", "quan", "quan"]

frame1len = list(range(0,len(menuselect)))
frame1.columnconfigure(frame1len, weight=1)

for i in range(len(menuselect)):
    btn1 = Button(frame1, text = menuselect[i])
    btn1.grid(row=0,column=i,sticky="WE", padx= 10, pady= 10)

#main filters
mainfilterselect = ["quknhjhan", "too", "too", "too", "too", "too", "too", "too", "too", "too"]

frame2len = list(range(0,len(mainfilterselect)))
frame2.rowconfigure(frame2len, weight=1)
frame2.columnconfigure(0, weight=1)

for i in range(len(mainfilterselect)):
    btn1 = Button(frame2, text = mainfilterselect[i])
    btn1.grid(row=i,column=0,sticky="WE", padx= 10, pady= 10)

searchbar = Entry(frame1)
searchbar.grid(row=1, column= 0, sticky="NSWE", columnspan = len(menuselect) - 1, padx = 5, pady= 5)
searchbtn = Button(frame1, command=kill, text= "search")
searchbtn.grid(row=1, column=len(menuselect) - 1, sticky="NSWE", padx=20, pady=5)

#searchedfilters

minorfilters = ["quan", "too", "too", "too", "too", "too", "too", "too", "too", "too"]
for i in range(len(minorfilters)):
    filterframe = Frame(selectedfilter, bg = "#999999")
    filterframe.grid(row=0, column=i, sticky="WE", padx=5, pady=5)
    filtertext = Label(filterframe, text = minorfilters[i])
    filtertext.grid(row=0, column=0)
    minorfilterclose = Button(filterframe, text="x")
    minorfilterclose.grid(row=0, column= 1)

root.mainloop()
