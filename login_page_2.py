from tkinter import *
from PIL import Image, ImageTk, ImageOps
import pymysql

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x700")
        self.configure(bg="#555555")

        self.login()

    def login(self):
        self.img1 = Image.open("img/placeholders/forest-1072828_640.jpg")
        self.img1 = self.img1.point(lambda p: p * 0.3)
        self.img1 = ImageOps.contain(self.img1, (10000, 700))
        self.bgimg = ImageTk.PhotoImage(self.img1)
        self.bg = Label(self, image = self.bgimg)

        self.frame1 = Frame(self, bg = "#cccccc")

        self.bg.place(relx= 0.5, rely= 0.5, relheight= 1, relwidth=1, anchor= CENTER)
        self.frame1.place(relx=0.5, rely=0.5, width=300, height=500, anchor = CENTER)

artsharer = pymysql.connect(
    host="localhost",
    user="root",
    password="Linc0646!",
    database="artsharer"
)

cur = artsharer.cursor()

if __name__ == "__main__":
    root = Login()
    root.mainloop()

