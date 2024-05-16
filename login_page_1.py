from tkinter import *
from PIL import Image, ImageTk, ImageOps
import pymysql

root = Tk()

root.geometry("500x700")
root.configure(bg="#555555")

img1 = Image.open("img/placeholders/forest-1072828_640.jpg")
img1 = img1.point(lambda p: p * 0.3)
img1 = ImageOps.contain(img1, (10000, 700))
bgimg = ImageTk.PhotoImage(img1)
bg = Label(root, image = bgimg)

frame1 = Frame(root, bg = "#cccccc")

bg.place(relx= 0.5, rely= 0.5, relheight= 1, relwidth=1, anchor= CENTER)
frame1.place(relx=0.5, rely=0.5, width=300, height=500, anchor = CENTER)



artsharer = pymysql.connect(
    host="localhost",
    user="root",
    password="Linc0646!",
    database="artsharer"
)

cur = artsharer.cursor()

root.mainloop()

