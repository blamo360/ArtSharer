import customtkinter
import sqlite3
from tkinter import filedialog as fd
import json
import shutil
import os
import subprocess
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk, ImageOps


class Start(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.gallery = None
        self.main_window_frame = None
        self.menu_bar_frame = None
        self.geometry("1000x700")

        self.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(
            Image.open('img/icon.jpg')))  # type: ignore

        customtkinter.set_default_color_theme("assets/themes/customtheme.json")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.pagenum = 0
        self.searchcompiled = []
        self.upload = None
        self.postwindow = None

        self.main_page()
        self.menu_bar()
        self.upload_button()
        self.search()

    def main_page(self):
        #creates the main frames
        self.menu_bar_frame = customtkinter.CTkFrame(self)
        self.menu_bar_frame.grid(row=0, column=0, columnspan=2, sticky="WE", padx=5, pady=(5, 0))
        self.menu_bar_frame.grid_columnconfigure(0, weight=1)

        self.main_window_frame = customtkinter.CTkFrame(self)
        self.main_window_frame.grid(row=1, column=1, sticky="NSWE", padx=5, pady=5)

        self.main_window_frame.rowconfigure(0, weight=1)
        self.main_window_frame.columnconfigure(0, weight=1)

        self.gallery = customtkinter.CTkScrollableFrame(self.main_window_frame)
        self.gallery.grid(row=0, column=0, sticky="NSWE", padx=5, pady=5)

    def menu_bar(self):
        
        searchframe = customtkinter.CTkFrame(self.menu_bar_frame)
        searchframe.grid(row=0, column=0, sticky="EW", padx=10, pady=10)
        searchframe.grid_columnconfigure(0, weight=10)

        self.searchbar = customtkinter.CTkEntry(searchframe)
        self.searchbar.grid(row=0, column=0, sticky="WE", padx=5, pady=10)

        searchbtn = customtkinter.CTkButton(
            searchframe, text="search", command=self.search)
        searchbtn.grid(row=0, column=1, sticky="WE", padx=20, pady=10)

        # login frames
        login_frame = customtkinter.CTkFrame(
            self.menu_bar_frame, width=300, height=30)
        login_frame.grid(row=0, column=2, sticky="WE", padx=(0, 10), pady=10)

        login = customtkinter.CTkButton(
            login_frame, text="Sign In", command=self.loginwin)
        login.grid(row=0, column=1, sticky="W", padx=10, pady=10)

        login = customtkinter.CTkButton(
            login_frame, text="Sign Up", command=self.signupwin)
        login.grid(row=0, column=2, sticky="W", padx=(0, 10), pady=10)

    def loginwin(self):
        #opens login page
        subprocess.run(["python", "login_page_f.py"])

    def signupwin(self):
        #opens REgistration page
        subprocess.run(["python", "register_page_f.py"])

    def search(self):
        # returns list(imgIDs)
        searchnum = 0
        self.pagenum = 0
        searchstring = self.searchbar.get()
        if searchstring == "":
            searchlist = []
        else:
            searchlist = (searchstring.lower()).split(" ")
            for i in searchlist:
                i = i.replace(" ", "")

        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()

        # compiles image IDs to search for
        if searchlist == []:
            cur.execute("SELECT imgID FROM imginfo")
            self.searchcompiled = cur.fetchall()
            self.searchcompiled = [i[0] for i in self.searchcompiled]

        elif len(searchlist) == 1:
            # for single searches
            print(
                f"SELECT imgIDs FROM taginfo WHERE tagName = {searchlist[0]}")
            cur.execute(
                f"SELECT imgIDs FROM taginfo WHERE tagName = {searchlist[0]}")
            tag = cur.fetchone()

            if tag is None:
                # tag does not exist
                CTkMessagebox(message="tag does not exist!")

            else:
                tag = json.loads(tag)
                self.searchcompiled = tag
        else:
            # for multiple tags
            for i in searchlist:
                cur.execute(f"SELECT imgIDs FROM taginfo WHERE tagName = {i}")
                tag = cur.fetchone()
                tag = json.loads(tag)

                if tag is None:
                    # tag does not exist
                    CTkMessagebox(message="tag(s) does not exist!")
                    break
                else:
                    if searchnum == 0:
                        search1 = tag
                        searchnum = searchnum + 1
                    else:
                        search2 = tag

                        for j in search1:
                            for k in search2:
                                if j == k:
                                    self.searchcompiled.append(j)

        self.updategallery()

    def updategallery(self):
        # updates gallery grids
        x = 0
        y = 0
        self.searchdisplay = self.searchcompiled[self.pagenum:(
            self.pagenum + 20)]
        for i in self.searchdisplay:
            if x <= 5:
                self.imggallery(i, x, y)
                x = x + 1
            else:
                x = 0
                y = y + 1
                self.imggallery(i, x, y)

    def imggallery(self, imgID, x, y):
        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()

        cur.execute(f"SELECT imgTitle FROM imginfo WHERE imgID = {imgID}")
        imgtitle = (cur.fetchone())[0]

        imgframe = customtkinter.CTkFrame(self.gallery)
        titlename = customtkinter.CTkLabel(imgframe, text=imgtitle)

        # get image from
        cur.execute(f"SELECT imgFileName FROM imginfo WHERE imgID = {imgID}")
        imgFileName = cur.fetchone()
        imgFileName = imgFileName[0]

        image = Image.open(f"img/imguploads/{imgFileName}")

        resized = ImageOps.fit(image, (150, 150), centering=(0.5, 0.5))
        newpic = ImageTk.PhotoImage(resized)
        imglabel = customtkinter.CTkButton(imgframe, image=newpic, text="", command=lambda: self.postinfo(
            imgID), fg_color="transparent")  # type: ignore

        imgframe.grid(row=y, column=x, padx=3, pady=5)
        imglabel.pack()
        titlename.pack(pady=(3, 5))

        connection.close()

    def postinfo(self, imgID):
        if self.postwindow is None or not self.postwindow.winfo_exists():
            connection = sqlite3.connect("artsharer.db")
            cur = connection.cursor()

            cur.execute(
                f"SELECT imgFileName FROM imginfo WHERE imgID = {imgID}")
            imgFileName = cur.fetchone()
            imgFileName = imgFileName[0]

            cur.execute(f"SELECT imgTitle FROM imginfo WHERE imgID = {imgID}")
            self.imgtitle = (cur.fetchone())[0]
            cur.execute(f"SELECT imgTags FROM imginfo WHERE imgID = {imgID}")
            self.imgtags = (cur.fetchone())[0]
            cur.execute(
                f"SELECT imgCaptions FROM imginfo WHERE imgID = {imgID}")
            self.imgcaption = (cur.fetchone())[0]

            image = Image.open(f"img/imguploads/{imgFileName}")
            resized = ImageOps.contain(image, (500, 500))
            width, height = resized.size
            newpic = ImageTk.PhotoImage(resized)

            image_dimensions = "%dx%d" % (width, height)

            self.grid_rowconfigure(1, weight=1)
            self.postwindow = customtkinter.CTkToplevel(self)

            post_frame = customtkinter.CTkFrame(self.postwindow)
            post_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NWEW")

            image_label = customtkinter.CTkLabel(
                post_frame, image=newpic, text="")  # type: ignore
            image_label.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
            size_label = customtkinter.CTkLabel(
                post_frame, text=image_dimensions)

            desc_frame = customtkinter.CTkFrame(post_frame)

            title = customtkinter.CTkLabel(desc_frame, text=self.imgtitle, font=(
                "", 25, "bold"), justify="left", anchor="w")
            caption = customtkinter.CTkLabel(
                desc_frame, text=self.imgcaption, justify="left", anchor="w")
            tag_title = customtkinter.CTkLabel(desc_frame, text="Tags", font=(
                "", 23, "bold"), justify="left", anchor="w")
            tags = customtkinter.CTkLabel(
                desc_frame, text=self.imgtags, justify="left", anchor="w")

            post_frame.grid_rowconfigure(0, weight=1)

            size_label.grid(row=1, column=0, sticky="SEW", pady=5)
            desc_frame.grid(row=0, column=1, sticky="NSEW",
                            rowspan=2, padx=10, pady=10)
            title.grid(row=0, column=0, sticky="NEW", pady=(5, 20), padx=5)
            caption.grid(row=1, column=0, sticky="NSEW", pady=(5, 20), padx=5)
            tag_title.grid(row=2, column=0, sticky="NEW", padx=5)
            tags.grid(row=3, column=0, sticky="NEW", padx=5)

            cur.close()


    def upload_button(self):
        addbtn = customtkinter.CTkButton(
            self.main_window_frame, text="+", width=75, height=75, command=self.uploadimg)
        addbtn.place(anchor="se", relx=1, rely=1, x=-30, y=-30)

    def uploadimg(self):
        if self.upload is None or not self.upload.winfo_exists():
            # file upload
            self.add = fd.askopenfilename()

            image = Image.open(self.add)
            resized = ImageOps.contain(image, (500, 500))
            width, height = resized.size
            newpic = ImageTk.PhotoImage(resized)

            image_dimensions = "%dx%d" % (width, height)

            self.upload = customtkinter.CTkToplevel(self)
            self.upload.geometry("530x%d" % (height + 270))

            image_frame = customtkinter.CTkFrame(self.upload)
            image_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NWSE")

            image_frame.grid_rowconfigure(0, weight=1)
            image_frame.grid_columnconfigure(0, weight=2)
            image_frame.grid_columnconfigure(1, weight=8)

            image_label = customtkinter.CTkLabel(
                image_frame, image=newpic, text="")  # type: ignore
            image_label.grid(row=0, column=0, columnspan=2,
                             padx=10, pady=10, sticky="NSEW")

            size_label = customtkinter.CTkLabel(
                image_frame, text=image_dimensions)
            name_label = customtkinter.CTkLabel(image_frame, text="Title")
            self.name_input = customtkinter.CTkEntry(image_frame)
            caption_label = customtkinter.CTkLabel(image_frame, text="Caption")
            self.caption_input = customtkinter.CTkTextbox(
                image_frame, height=100)
            tag_label = customtkinter.CTkLabel(image_frame, text="Tags")
            self.tag_input = customtkinter.CTkEntry(image_frame)
            submit_btn = customtkinter.CTkButton(
                image_frame, text="Post", command=self.submitpost)

            size_label.grid(row=1, column=0, columnspan=2,
                            sticky="NEW", pady=5)
            name_label.grid(row=2, column=0, sticky="EW", pady=5)
            caption_label.grid(row=3, column=0, sticky="EW", pady=5)
            tag_label.grid(row=4, column=0, sticky="EW", pady=5)

            self.name_input.grid(row=2, column=1, sticky="EW")
            self.caption_input.grid(row=3, column=1, sticky="EW")
            self.tag_input.grid(row=4, column=1, sticky="EW")

            submit_btn.grid(row=5, column=0, columnspan=2, sticky="EW")

        else:
            self.upload.focus()

    def submitpost(self):
        # database connection
        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()

        # tag format: space = new tag, underslash(_) = seperator

        imgFileName = os.path.basename(self.add)

        tags = (self.tag_input.get().lower()).split(" ")
        tagsJSON = json.dumps(tags)
        cur.execute("INSERT INTO imginfo (imgFileName, imgTitle,imgCaptions,imgTags) values('{}', '{}','{}','{}')".format(
            imgFileName, self.name_input.get(), self.caption_input.get('1.0', 'end-1c'), tagsJSON))
        connection.commit()

        cur.execute("SELECT imgID FROM imginfo ORDER BY imgID DESC LIMIT 1")
        imgID = cur.fetchone()
        imgID = imgID[0]

        for i in tags:
            # checking if tag exists in database
            tagName = cur.execute(
                f"SELECT tagName FROM taginfo WHERE tagName = '{i}'")
            tagName = tagName.fetchone()
            if tagName == None:
                # conversion to string representation of list for storing
                imgIDstr = [imgID]
                imgIDstr = json.dumps(imgIDstr)
                # create new tag entry
                cur.execute("INSERT INTO taginfo(tagName,imgAmount,imgIDs) values('{}',{},'{}')".format(
                    i, 1, imgIDstr))
                connection.commit()
            else:
                # string -> list
                tagName = tagName[0]
                cur.execute(
                    f"SELECT imgAmount FROM taginfo WHERE tagName = '{i}'")
                imgAmount = cur.fetchone()
                imgAmount = int(imgAmount[0])
                imgAmount = imgAmount + 1
                cur.execute(
                    f"UPDATE taginfo SET imgAmount = {imgAmount} WHERE tagName = '{tagName}'")
                connection.commit()

                cur.execute(
                    "SELECT imgIDs FROM taginfo WHERE tagName = '{}'".format(tagName))
                imgIDs = cur.fetchone()
                print(imgIDs)
                imgIDs = imgIDs[0]

                print(imgIDs)
                imgIDs = json.loads(imgIDs)
                imgIDs.append(imgID)
                imgIDs = json.dumps(imgIDs)
                print(imgIDs)
                cur.execute(
                    f"UPDATE taginfo SET imgIDs = '{imgIDs}' WHERE tagName = '{tagName}'")
                connection.commit()

        tags = json.dumps(tags)
        shutil.copy2(self.add, "img/imguploads")

        connection.commit()
        connection.close()


if __name__ == "__main__":
    root = Start()
    root.mainloop()
