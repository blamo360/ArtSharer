from tkinter import *
import customtkinter
from PIL import Image, ImageTk, ImageOps
import sqlite3
import subprocess

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x700")
        self.configure(bg="#555555")

        self.tk.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(Image.open("img/placeholders/iconn.png"))) # type: ignore

        customtkinter.set_appearance_mode("dark")
        self.login()
        self.resizable(False, False)

    def login(self):
        self.frame1 = customtkinter.CTkFrame(self, width=300, height=500)
        self.frame1.place(relx=0.5, rely=0.5, anchor = CENTER)

        self.loginframe = customtkinter.CTkFrame(self.frame1, width=300, height=450, fg_color="transparent")
        self.loginframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.logoimg = ImageTk.PhotoImage(ImageOps.contain(Image.open("img/placeholders/iconn.png"), (100, 100)))

        self.logo = Label(self.loginframe, image=self.logoimg) # type: ignore
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

        self.registerbtn = customtkinter.CTkButton(self.loginframe, text="Register", command=self.reg)
        self.registerbtn.grid(row=3, column=0, columnspan=2, pady=(10,10))

    def reg(self):
        self.destroy()
        subprocess.run(["python","register_page_f.py"])

    def logindb(self):
        connection = sqlite3.connect("users/artsharer.db")
        cur = connection.cursor()
        email = self.emailinput.get()
        password = self.passwordinput.get()

        cur.execute("SELECT userID FROM loginfo WHERE email='{}' and password='{}'".format(email, password))
        userID = cur.fetchone()[0]

        if userID is None:
            print("Invalid email or password")
        
        else:
            cur.close()
            self.destroy()
            subprocess.run(["python", "main_page_f.py"])

if __name__ == "__main__":
    root = Login()
    root.mainloop()