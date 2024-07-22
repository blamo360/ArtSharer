from PIL import Image, ImageTk
import tkinter
import customtkinter
import sqlite3
import login_page_4
from login_page_4 import Login


class Start(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x700")

        self.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(Image.open('img/icon.jpg')))

        self.call("source", "assets/themes/Azure-ttk-theme-2.1.0/azure.tcl")
        self.call("set_theme", "dark")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #User info

        self.main_page()
        self.menu_bar()
        self.search_bar()
        self.main_filter_bar()
        self.minor_filter_bar()
        self.add_button()

        self.loginpanel = Login()

    def main_page(self):
        self.menu_bar_frame = customtkinter.CTkFrame(self)
        self.menu_bar_frame.grid(row=0, column=0, columnspan= 2, sticky= "WE", padx= 5, pady= (5,0))

        self.main_filter_frame = customtkinter.CTkFrame(self)
        self.main_filter_frame.grid(row=1, column=0, sticky = "NSWE", padx= (5,0), pady = 5)

        self.main_window_frame = customtkinter.CTkFrame(self)
        self.main_window_frame.grid(row=1, column=1, sticky = "NSWE", padx= 5, pady= 5)

        self.main_window_frame.rowconfigure(1, weight= 1)
        self.main_window_frame.columnconfigure(0, weight= 1)

        self.minor_filter_frame = customtkinter.CTkFrame(self.main_window_frame)
        self.minor_filter_frame.grid(row=0, column=0,sticky="NWE", padx=5, pady=5)

        self.gallery = customtkinter.CTkScrollableFrame(self.main_window_frame)
        self.gallery.grid(row=1, column=0,sticky="NSWE", padx=5, pady=5)

    def menu_bar(self):
        self.menu_opt = [("menu", "main_page.py"), ("too", "main_page.py"), ("quan", "main_page.py"), ("wa", "main_page.py")]
        self.menu_bar_frame.columnconfigure(list(range(0,len(self.menu_opt)+1)), weight=1)

        i=0
        for x,y in self.menu_opt:
            
            self.btn1 = customtkinter.CTkButton(self.menu_bar_frame, text = x)
            self.btn1.grid(row = 0,column = i,sticky="EW", padx= 10, pady= 10,)
            print(i)
            i=i+1

        #login frames
        self.loginFrame = customtkinter.CTkFrame(self.menu_bar_frame, width= 300, height= 30)
        self.loginFrame.grid(row=0,column=(len(self.menu_opt)),sticky="WE", padx= (0,10), pady= 10)

        self.login = customtkinter.CTkButton(self.loginFrame, text = "Sign In")
        self.login.grid(row = 0, column = 0, sticky = "W", padx= 10, pady= 10)

        self.login = customtkinter.CTkButton(self.loginFrame, text = "Sign Up")
        self.login.grid(row = 0, column = 1, sticky = "W", padx= (0,10), pady= 10)
        

    def search_bar(self):
        self.searchbar = customtkinter.CTkEntry(self.menu_bar_frame)
        self.searchbar.grid(row=1, column= 0, sticky="NSWE", columnspan = len(self.menu_opt), padx = 5, pady= (0,10))
        searchbtn = customtkinter.CTkButton(self.menu_bar_frame, text= "search")
        searchbtn.grid(row=1, column=len(self.menu_opt), sticky="NSWE", padx=20, pady=(0,10))

    def main_filter_bar(self):
        mainfilterselect = ["quknhjhan", "too", "too", "too", "too", "too", "too", "too", "too", "too"]
        frame2len = list(range(0,len(mainfilterselect)))
        self.main_filter_frame.rowconfigure(frame2len, weight=1)
        self.main_filter_frame.columnconfigure(0, weight=1)

        for i in range(len(mainfilterselect)):
            btn1 = customtkinter.CTkButton(self.main_filter_frame, text = mainfilterselect[i])
            btn1.grid(row=i,column=0,sticky="W", padx= 10, pady= 10)

    def minor_filter_bar(self):
        minorfilters = ["quan", "too", "too", "too", "too", "too", "too", "too", "too", "too"]
        for i in range(len(minorfilters)):
            filterframe = customtkinter.CTkFrame(self.minor_filter_frame)
            filterframe.grid(row=0, column=i, sticky="WE", padx=5, pady=5)
            filtertext = customtkinter.CTkLabel(filterframe, text = minorfilters[i])
            filtertext.grid(row=0, column=0, padx=10)
            minorfilterclose = customtkinter.CTkButton(filterframe, text="x", width=0, fg_color="transparent")
            minorfilterclose.grid(row=0, column= 1, padx=(0,5), pady=2)

    def add_button(self):
        addbtn = customtkinter.CTkButton(self.main_window_frame, text="+", width=75, height=75)
        addbtn.place(anchor = "se", relx = 1, rely = 1, x = -30, y = -30)  
        addbtn.lift()


if __name__ == "__main__":
    root = Start()
    root.mainloop()
