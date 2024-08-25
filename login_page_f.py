from tkinter import *
import customtkinter
from PIL import Image, ImageTk, ImageOps
import sqlite3
import subprocess

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.passwordinput = None
        self.email_input = None
        self.geometry("500x700")
        self.configure(bg="#555555")

        self.tk.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(Image.open("img/placeholders/iconn.png"))) # type: ignore

        customtkinter.set_appearance_mode("dark")
        self.login()
        self.resizable(False, False)

    def login(self):
        main_frame = customtkinter.CTkFrame(self, width=300, height=500)
        main_frame.place(relx=0.5, rely=0.5, anchor = CENTER)

        login_frame = customtkinter.CTkFrame(main_frame, width=300, height=450, fg_color="transparent")
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        logo_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("img/placeholders/iconn.png"), (100, 100)))

        logo = Label(login_frame, image=logo_img) # type: ignore
        logo.grid(row=0, column=0, columnspan=2, pady=10)

        login_label = customtkinter.CTkLabel(login_frame, text="Email")
        login_label.grid(row=1, column=0, padx=10, pady=10)

        password_label = customtkinter.CTkLabel(login_frame, text="Password")
        password_label.grid(row=2, column=0, padx=10, sticky="NWE")
        
        self.email_input = customtkinter.CTkEntry(login_frame)
        self.email_input.grid(row=1, column=1, sticky="NWE", padx = 10, pady=10)

        self.passwordinput = customtkinter.CTkEntry(login_frame)
        self.passwordinput.grid(row=2, column=1, sticky="NWE", padx = 10)

        login_btn = customtkinter.CTkButton(login_frame, text="Login", command=self.login_db)
        login_btn.grid(row=2, column=0, columnspan=2, pady=(200, 10))

        register_btn = customtkinter.CTkButton(login_frame, text="Register", command=self.reg)
        register_btn.grid(row=3, column=0, columnspan=2, pady=(10, 10))

    def reg(self):
        self.destroy()
        subprocess.run(["python","register_page_f.py"])

    def login_db(self):
        connection = sqlite3.connect("users/artsharer.db")
        cur = connection.cursor()
        email = self.email_input.get()
        password = self.passwordinput.get()

        cur.execute("SELECT userID FROM loginfo WHERE email='{}' and password='{}'".format(email, password))
        user_id = cur.fetchone()[0]

        if user_id is None:
            print("Invalid email or password")
        
        else:
            cur.close()
            self.destroy()
            subprocess.run(["python", "main_page_f.py"])

if __name__ == "__main__":
    root = Login()
    root.mainloop()