from tkinter import *
from PIL import Image, ImageTk
import subprocess


root = Tk()
root.geometry("1000x700")
root.configure(bg= "#aaaaaa")
root.resizable(False, False)

root.grid_columnconfigure((0,1),weight=1)
root.grid_rowconfigure((0,1),weight=1)

frame1 = Frame(root, bg = "#cccccc")
#frame1.grid(row = 0, column = 0, columnspan = 2)
frame1.place(x = 10, y = 10, width=980, height=50, anchor = NW)

frame2 = Frame(root, bg = "#cccccc")
#frame1.grid(row = 1, column = 0)
frame2.place(x = 10, y = 70, width=130, height= 620, anchor = NW)

frame3 = Frame(root, bg = "#dddddd")
#frame1.grid(row = 1, column = 1)
frame3.place(x = 150, y = 70, width=840, height= 620, anchor = NW)

def send():
    subprocess.run(["python", "archive/loginpage1.py"])


#top menu
menuselect = ["quan", "too", "quan", "quan"]

frame1len = list(range(0,len(menuselect)))
frame1.columnconfigure(frame1len, weight=1)

for i in range(len(menuselect)):
    btn1 = Button(frame1, text = menuselect[i])
    btn1.grid(row=0,column=i,sticky="WE", padx= 10, pady= 10)

#main filters
mainfilterselect = ["quan", "too", "too", "too", "too", "too", "too", "too", "too", "too"]

frame2len = list(range(0,len(mainfilterselect)))
frame2.rowconfigure(frame2len, weight=1)
frame2.columnconfigure(0, weight=1)

for i in range(len(mainfilterselect)):
    btn1 = Button(frame2, text = mainfilterselect[i])
    btn1.grid(row=i,column=0,sticky="WE", padx= 10, pady= 10)

searchbar = Entry(frame1)
searchbar.grid(row=1, column=0, sticky="WE", columnspan = len(menuselect))

root.mainloop()
