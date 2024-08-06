from CTkMessagebox import CTkMessagebox
from tkinter import *
from PIL import Image, ImageTk, ImageOps
import customtkinter
import sqlite3
from login_page_4 import Login
from tkinter import filedialog as fd
import random
import json
import shutil
from pathlib import Path
import os


class Start(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x700")

        self.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(Image.open('img/icon.jpg')))

        self.call("source", "assets/themes/Azure-ttk-theme-2.1.0/azure.tcl")
        self.call("set_theme", "dark")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.pagenum = 0
        self.searchcompiled =[]

        self.main_page()
        self.menu_bar()
        self.search_bar()
        self.main_filter_bar()
        self.minor_filter_bar()
        self.upload_button()

        self.upload = None

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
        searchbtn = customtkinter.CTkButton(self.menu_bar_frame, text= "search", command = self.search)
        searchbtn.grid(row=1, column=len(self.menu_opt), sticky="NSWE", padx=20, pady=(0,10))

    def search(self):
        searchnum = 0
        searchstring = self.searchbar.get()
        if searchstring == "":
            searchlist = []
        else:
            searchlist = (searchstring.lower()).split(" ")
        
        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()
        
        #compile image IDs to search for
        if searchlist == []:
            break
        elif searchlist.count() == 1:
            cur.execute(f"SELECT imgIDs FROM taginfo WHERE tagName = {searchlist[0]}")
            tag = cur.fetchall()

            if tag is None:
                #tag does not exist
                CTkMessagebox(message = "tag does not exist!")

            else:
                self.searchcompiled = tag
        else:
            for i in searchlist:
                cur.execute(f"SELECT imgIDs FROM taginfo WHERE tagName = {i}")
                tag = cur.fetchall()

                if tag is None:
                    #tag does not exist
                    break
                else:
                    if searchnum == 0:
                        search1 = tag
                        searchnum = searchnum + 1
                    else:
                        search2 = tag

                        for j in search1:
                            for n in search2:
                                if j == n:
                                    self.searchcompiled.append(j)
                            else:
                                continue

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

    def upload_button(self):
        addbtn = customtkinter.CTkButton(self.main_window_frame, text="+", width=75, height=75, command=self.uploadimg)
        addbtn.place(anchor = "se", relx = 1, rely = 1, x = -30, y = -30)

    def imggallery(self):
        imgframe = customtkinter.CTkFrame(self.gallery)
        
        
    def uploadimg(self):
        if self.upload is None or not self.upload.winfo_exists():

            #file upload
            self.add = fd.askopenfilename()

            image = Image.open(self.add)
            resized = ImageOps.contain(image, (500, 500))
            width, height = resized.size
            newpic = ImageTk.PhotoImage(resized)

            image_dimensions = "%dx%d" % (width, height)
            
            self.upload = customtkinter.CTkToplevel(self)
            self.upload.geometry("530x%d" % (height + 270))

            image_frame = customtkinter.CTkFrame(self.upload)
            image_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "NWSE")

            image_frame.grid_rowconfigure(0, weight = 1)
            image_frame.grid_columnconfigure(0, weight = 2)
            image_frame.grid_columnconfigure(1, weight = 8)

            image_label = customtkinter.CTkLabel(image_frame, image=newpic, text="") # type: ignore
            image_label.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = "NSEW")
            
            size_label = customtkinter.CTkLabel(image_frame, text = image_dimensions)
            name_label = customtkinter.CTkLabel(image_frame, text = "Title")
            self.name_input = customtkinter.CTkEntry(image_frame)
            caption_label = customtkinter.CTkLabel(image_frame, text = "Caption")
            self.caption_input = customtkinter.CTkTextbox(image_frame, height = 100)
            tag_label = customtkinter.CTkLabel(image_frame, text = "Tags")
            self.tag_input = customtkinter.CTkEntry(image_frame)
            submit_btn = customtkinter.CTkButton(image_frame, text = "Post", command = self.get_post_info)
            
            size_label.grid(row = 1, column = 0, columnspan = 2, sticky = "NEW", pady = 5)
            name_label.grid(row = 2, column = 0, sticky = "EW", pady = 5)
            caption_label.grid(row = 3, column = 0, sticky = "EW", pady = 5)
            tag_label.grid(row = 4, column = 0, sticky = "EW", pady = 5)
            
            self.name_input.grid(row = 2, column = 1, sticky = "EW")
            self.caption_input.grid(row = 3, column = 1, sticky = "EW")
            self.tag_input.grid(row = 4, column = 1, sticky = "EW")

            submit_btn.grid(row = 5, column = 0, columnspan = 2, sticky = "EW")

        else:
            self.upload.focus()

    def get_post_info(self):
            #database connection
            connection = sqlite3.connect("artsharer.db")
            cur = connection.cursor()
            
            #tag format: space = new tag, underslash(_) = seperator

            imgFileName = os.path.basename(self.add)

            tags = (self.tag_input.get().lower()).split(" ")
            tagsJSON = json.dumps(tags)
            cur.execute("INSERT INTO imginfo (imgFileName, imgTitle,imgCaptions,imgTags) values('{}', '{}','{}','{}')".format(imgFileName, self.name_input.get(), self.caption_input.get('1.0', 'end-1c'), tagsJSON))
            connection.commit()
            
            cur.execute("SELECT imgID FROM imginfo ORDER BY userID DESC LIMIT 1")
            imgID = cur.fetchone()

            for i in tags:
                #checking if tag exists in database
                tagName = cur.execute(f"SELECT tagName FROM taginfo WHERE tagName = '{i}'")
                tagName = tagName.fetchone()
                if tagName == None:
                    #conversion to string representation of list for storing
                    imgIDstr = [imgID]
                    imgIDstr = json.dumps(imgIDstr)
                    #create new tag entry
                    cur.execute("INSERT INTO taginfo(tagName,imgAmount,imgIDs) values('{}',{},'{}')".format(i, 1, imgIDstr))
                else:
                    #string -> list
                    cur.execute(f"SELECT imgAmount FROM taginfo WHERE tagName = '{i}'")
                    imgAmount = cur.fetchone()
                    imgAmount = imgAmount + 1
                    cur.execute(f"UPDATE taginfo SET imgAmount = {imgAmount} WHERE tagName = {i}")

                    cur.execute("SELECT imgIDs FROM taginfo WHERE tagName = '{}'".format(tagName))
                    imgIDs = cur.fetchone()

                    imgIDs = json.loads(imgIDs)
                    imgIDs.append(imgID)
                    imgIDs = json.dumps(imgIDs)
                    cur.execute(f"UPDATE taginfo SET imgIDs = {imgIDs} WHERE tagName = {i}")

            tags = json.dumps(tags)
            shutil.copy2(self.add, "img/imguploads")
            
            connection.commit()
            connection.close()


if __name__ == "__main__":
    root = Start()
    root.mainloop()
