from tkinter import *
import customtkinter
from PIL import Image, ImageTk, ImageOps
import sqlite3
import main_page_4
import subprocess

customtkinter.set_appearance_mode("light")


class Login(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x700")
        self.configure(bg="#555555")

        self.tk.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(Image.open("img\placeholders\iconn.png")))

        self.login()
        self.resizable(False, False)

    def login(self):
        self.img1 = Image.open("img/placeholders/forest-1072828_640.jpg")
        self.img1 = self.img1.point(lambda p: p * 0.3)
        self.img1 = ImageOps.contain(self.img1, (10000, 700))
        self.bgimg = ImageTk.PhotoImage(self.img1)
        self.bg = Label(self, image = self.bgimg)

        self.frame1 = customtkinter.CTkFrame(self, width=300, height=500)

        self.bg.place(relx= 0.5, rely= 0.5, relheight= 1, relwidth=1, anchor= CENTER)
        self.frame1.place(relx=0.5, rely=0.5, anchor = CENTER)

        self.loginframe = customtkinter.CTkFrame(self.frame1, width=300, height=450, fg_color="transparent")
        self.loginframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.logoimg = ImageTk.PhotoImage(ImageOps.contain(Image.open("img\placeholders\iconn.png"), (100, 100)))

        self.logo = Label(self.loginframe, image=self.logoimg)
        self.logo.grid(row=0, column=0, columnspan=2, pady=10)

        self.loginlabel = customtkinter.CTkLabel(self.loginframe, text="Email")
        self.loginlabel.grid(row=1, column=0, padx=10, pady=10)

        self.passwordlabel = customtkinter.CTkLabel(self.loginframe, text="Password")
        self.passwordlabel.grid(row=2, column=0, padx=10, sticky="NWE")
        
        self.emailinput = customtkinter.CTkEntry(self.loginframe)
        self.emailinput.grid(row=1,column=1, sticky="NWE", padx = 10, pady=10)

        self.passwordinput = customtkinter.CTkEntry(self.loginframe)
        self.passwordinput.grid(row=2, column=1, sticky="NWE", padx = 10)

        self.loginbtn = customtkinter.CTkButton(self.loginframe, text="Login", command=self.logindb)
        self.loginbtn.grid(row=2, column=0, columnspan=2, pady=(200,10))

    def logindb(self):
        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()
        email = self.emailinput.get()
        password = self.passwordinput.get()

        cur.execute("SELECT * FROM loginfo Where email='{}' and password='{}'".format(email, password))
        loginver = cur.fetchone()

        if loginver == None:
            print("Invalid email or password")
        
        else:
            self.destroy()
            subprocess.run(["python","main_page_4.py"])

            
        


if __name__ == "__main__":
    root = Login()
    root.mainloop()

