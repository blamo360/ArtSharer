from tkinter import *
import customtkinter
from PIL import Image, ImageTk, ImageOps
import sqlite3
import subprocess
import random


customtkinter.set_appearance_mode("light")


class Login(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x700")
        self.configure(bg="#555555")
        self.resizable(False, False)

        self.tk.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(Image.open("img\placeholders\iconn.png")))

        customtkinter.set_appearance_mode("dark")
        self.login()
  

    def login(self):
        self.frame1 = customtkinter.CTkFrame(self, width=300, height=500)
        self.frame1.place(relx=0.5, rely=0.5, anchor = CENTER)

        self.loginframe = customtkinter.CTkFrame(self.frame1, width=300, height=450, fg_color="transparent")
        self.loginframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.logoimg = ImageTk.PhotoImage(ImageOps.contain(Image.open("img\placeholders\iconn.png"), (100, 100)))

        self.logo = Label(self.loginframe, image=self.logoimg) # type: ignore
        self.logo.grid(row=0, column=0, columnspan=2, pady=10)

        #email
        self.emaillabel = customtkinter.CTkLabel(self.loginframe, text="Email")
        self.emaillabel.grid(row=1, column=0, padx=10, sticky="NWE")
        
        self.emailinput = customtkinter.CTkEntry(self.loginframe)
        self.emailinput.grid(row=1, column=1, sticky="NWE", padx = 10)

        #username
        self.usernamelabel = customtkinter.CTkLabel(self.loginframe, text="Username")
        self.usernamelabel.grid(row=2, column=0, padx=10, pady=10)
        
        self.usernameinput = customtkinter.CTkEntry(self.loginframe)
        self.usernameinput.grid(row=2,column=1, sticky="NWE", padx = 10, pady=10)

        #password plus confirmation
        self.passwordlabel = customtkinter.CTkLabel(self.loginframe, text="Password")
        self.passwordlabel.grid(row=3, column=0, padx=10, sticky="NWE")
        
        self.passwordinput = customtkinter.CTkEntry(self.loginframe)
        self.passwordinput.grid(row=3, column=1, sticky="NWE", padx = 10, pady=(0,10))

        self.passwordconflabel = customtkinter.CTkLabel(self.loginframe, text="Confirm Password")
        self.passwordconflabel.grid(row=4, column=0, padx=10, sticky="NWE")
        
        self.passwordconfinput = customtkinter.CTkEntry(self.loginframe)
        self.passwordconfinput.grid(row=4, column=1, sticky="NWE", padx = 10)

        self.loginbtn = customtkinter.CTkButton(self.loginframe, text="Register", command=self.signup)
        self.loginbtn.grid(row=5, column=0, columnspan=2, pady=(120,10))

        self.loginbtn = customtkinter.CTkButton(self.loginframe, text="Login", command=self.loginbwtn)
        self.loginbtn.grid(row=6, column=0, columnspan=2, pady=(200,10))

    def loginbwtn(self):
        self.destroy()
        subprocess.run(["python","login_page_f.py"])
    
    def signup(self):
        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()

        #usernname validation
        if not self.usernameinput.get().isalnum():
            print("false")

        
        else:
            user = cur.execute("SELECT username FROM loginfo WHERE username='{}'".format(self.usernameinput.get()))
            userver = user.fetchone()


            if userver != None:
                print("Username already exists")
            else:
                #password validation
                if " " in self.passwordinput.get():
                    print("No spaces in password")

                elif len(self.passwordinput.get()) < 6:
                    print("Password must be larger than six characters")

                elif self.passwordinput.get() != self.passwordconfinput.get():
                    print("Passwords do not match")

                else:
                    mail = cur.execute("SELECT email FROM loginfo WHERE email = '{}'".format(self.emailinput.get()))
                    emailver = mail.fetchone()

                    if emailver != None:
                        print("Email already exists")

                    else:
                        #unique ID check
                        while True:
                            newUserID = random.randint(0, 999999998)
                            UserIDver = cur.execute("SELECT userID FROM loginfo WHERE userID = '{}'".format(newUserID))
                            UserIDver = UserIDver.fetchone()
                            print(newUserID)
                            if UserIDver == None:
                                break

                        #add info
                        cur.execute("INSERT INTO loginfo (userID,username,password,email) values({},'{}','{}','{}')".format(newUserID, self.usernameinput.get(), self.passwordinput.get(), self.emailinput.get()))
                        
                        connection.commit()
                        connection.close()

                        print("Registration successful!")
                
if __name__ == "__main__":
    root = Login()
    root.mainloop()

