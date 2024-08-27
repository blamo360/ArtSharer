from tkinter import *
import customtkinter
import sqlite3
import subprocess
import random
from CTkMessagebox import CTkMessagebox
import time

customtkinter.set_appearance_mode("light")


class Login(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.password_conf_input = None
        self.password_input = None
        self.username_input = None
        self.email_input = None
        self.geometry("500x700")
        self.configure(bg="#555555")
        self.resizable(False, False)

        customtkinter.set_appearance_mode("dark")
        self.login()
        customtkinter.set_default_color_theme("assets/themes/customtheme.json")

    def login(self):
        main_frame = customtkinter.CTkFrame(self, width=300, height=500)
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        login_frame = customtkinter.CTkFrame(main_frame, width=300, height=450, fg_color="transparent")
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        #email
        email_label = customtkinter.CTkLabel(login_frame, text="Email")
        email_label.grid(row=0, column=0, padx=10, sticky="NWE")

        self.email_input = customtkinter.CTkEntry(login_frame)
        self.email_input.grid(row=0, column=1, sticky="NWE", padx=10)

        #username
        username_label = customtkinter.CTkLabel(login_frame, text="Username")
        username_label.grid(row=1, column=0, padx=10, pady=10)

        self.username_input = customtkinter.CTkEntry(login_frame)
        self.username_input.grid(row=1, column=1, sticky="NWE", padx=10, pady=10)

        #password plus confirmation
        password_label = customtkinter.CTkLabel(login_frame, text="Password")
        password_label.grid(row=2, column=0, padx=10, sticky="NWE")

        self.password_input = customtkinter.CTkEntry(login_frame)
        self.password_input.grid(row=2, column=1, sticky="NWE", padx=10, pady=(0, 10))

        password_conf_label = customtkinter.CTkLabel(login_frame, text="Confirm Password")
        password_conf_label.grid(row=3, column=0, padx=10, sticky="NWE")

        self.password_conf_input = customtkinter.CTkEntry(login_frame)
        self.password_conf_input.grid(row=3, column=1, sticky="NWE", padx=10)

        reg_btn = customtkinter.CTkButton(login_frame, text="Register", command=self.signup)
        reg_btn.grid(row=4, column=0, columnspan=2, pady=(120, 10))

        login_btn = customtkinter.CTkButton(login_frame, text="Login", command=self.login_btn)
        login_btn.grid(row=5, column=0, columnspan=2, pady=(10, 10))

    def login_btn(self):
        self.destroy()
        subprocess.run(["python", "login_page_f.py"])

    def signup(self):
        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()

        #usernname validation
        if not self.username_input.get().isalnum():
            CTkMessagebox(message='Only non-special characters allowed')

        else:
            user = cur.execute("SELECT username FROM loginfo WHERE username='{}'".format(self.username_input.get()))
            user_ver = user.fetchone()

            if user_ver is not None:
                CTkMessagebox(message="Username already exists")
            else:
                #password validation
                if " " in self.password_input.get():
                    CTkMessagebox(message="No spaces in password")

                elif len(self.password_input.get()) < 6:
                    CTkMessagebox(message="Password must be larger than six characters")

                elif self.password_input.get() != self.password_conf_input.get():
                    CTkMessagebox(message="Passwords do not match")

                else:
                    mail = cur.execute("SELECT email FROM loginfo WHERE email = '{}'".format(self.email_input.get()))
                    emailver = mail.fetchone()

                    if emailver is not None:
                        CTkMessagebox(message="Email already exists")

                    else:
                        #unique ID check
                        while True:
                            new_user_id = random.randint(0, 999999998)
                            user_id_ver = cur.execute(
                                "SELECT userID FROM loginfo WHERE userID = '{}'".format(new_user_id))
                            user_id_ver = user_id_ver.fetchone()
                            if user_id_ver is None:
                                break

                        #add info
                        cur.execute(
                            "INSERT INTO loginfo (userID,username,password,email) values({},'{}','{}','{}')".format(
                                new_user_id, self.username_input.get(), self.password_input.get(),
                                self.email_input.get()))

                        connection.commit()
                        connection.close()

                        CTkMessagebox(message="Registration successful!")
                        time.sleep(2)
                        self.destroy()
                        subprocess.run(["python", "main_page_f.py"])


if __name__ == "__main__":
    root = Login()
    root.mainloop()
