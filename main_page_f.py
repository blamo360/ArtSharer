import customtkinter
from tkinter import *
import sqlite3
from tkinter import filedialog as fd
import json
import shutil
import os
import subprocess
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk, ImageOps


def signup_win():
    #opens registration page
    subprocess.run(["python", "register_page_f.py"])


def loginwin():
    #opens login page
    subprocess.run(["python", "login_page_f.py"])

class Start(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.tag_input = None
        self.caption_input = None
        self.name_input = None
        self.add = None
        self.search_display = None
        self.img_title = None
        self._w = None
        self.searchbar = None
        self.gallery = None
        self.main_window_frame = None
        self.menu_bar_frame = None

        self.geometry("1000x700")

        self.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(
            Image.open('img/icon.jpg')))  # type: ignore

        customtkinter.set_default_color_theme("assets/themes/customtheme.json")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.page_num = 0
        self.search_compiled = []
        self.upload = None
        self.post_window = None

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
        self.main_window_frame.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)

        self.main_window_frame.rowconfigure(0, weight=1)
        self.main_window_frame.columnconfigure(0, weight=1)

        self.gallery = customtkinter.CTkScrollableFrame(self.main_window_frame)
        self.gallery.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

    def menu_bar(self):

        search_frame = customtkinter.CTkFrame(self.menu_bar_frame)
        search_frame.grid(row=0, column=0, sticky="EW", padx=10, pady=10)
        search_frame.grid_columnconfigure(0, weight=10)

        self.searchbar = customtkinter.CTkEntry(search_frame)
        self.searchbar.grid(row=0, column=0, sticky="WE", padx=5, pady=10)

        search_btn = customtkinter.CTkButton(
            search_frame, text="search", command=self.search)
        search_btn.grid(row=0, column=1, sticky="WE", padx=20, pady=10)

        # login frames
        login_frame = customtkinter.CTkFrame(
            self.menu_bar_frame, width=300, height=30)
        login_frame.grid(row=0, column=2, sticky="WE", padx=(0, 10), pady=10)

        login = customtkinter.CTkButton(
            login_frame, text="Sign In", command=loginwin)
        login.grid(row=0, column=1, sticky="W", padx=10, pady=10)

        login = customtkinter.CTkButton(
            login_frame, text="Sign Up", command=signup_win)
        login.grid(row=0, column=2, sticky="W", padx=(0, 10), pady=10)

    def search(self):
        # returns list(img_ids)
        searchcompare = 0
        search_num = 0
        self.page_num = 0
        searchstring = self.searchbar.get()
        if searchstring == "":
            search_list = []
        else:
            search_list = (searchstring.lower()).split(" ")
            for i in search_list:
                search_list[i] = search_list[i].replace(" ", "")

        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()

        # compiles image IDs to search for
        if not search_list:
            cur.execute("SELECT imgid FROM imginfo")
            self.search_compiled = cur.fetchall()
            self.search_compiled = [i[0] for i in self.search_compiled]

        elif len(search_list) == 1:
            # for single searches
            print(
                f"SELECT imgids FROM taginfo WHERE tagName = {search_list[0]}")
            cur.execute(
                f"SELECT imgids FROM taginfo WHERE tagName = {search_list[0]}")
            tag = cur.fetchone()

            if tag is None:
                # tag does not exist
                CTkMessagebox(message="tag does not exist!")

            else:
                tag = json.loads(tag)
                self.search_compiled = tag
        else:
            # for multiple tags
            for i in search_list:
                cur.execute(f"SELECT imgids FROM taginfo WHERE tagName = {i}")
                tag = cur.fetchone()
                tag = json.loads(tag)

                if tag is None:
                    # tag does not exist
                    CTkMessagebox(message="tag(s) does not exist!")
                    break
                else:
                    if search_num == 0:
                        searchcompare = tag
                        search_num = search_num + 1
                    else:
                        search2 = tag

                        for j in searchcompare:
                            for k in search2:
                                if j == k:
                                    self.search_compiled.append(j)

        self.update_gallery()

    def update_gallery(self):
        # updates gallery grids
        x = 0
        y = 0
        self.search_display = self.search_compiled[self.page_num:(
            self.page_num + 20)]
        for i in self.search_display:
            if x <= 5:
                self.img_gallery(i, x, y)
                x = x + 1
            else:
                x = 0
                y = y + 1
                self.img_gallery(i, x, y)

    def img_gallery(self, imgid, x, y):
        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()

        cur.execute(f"SELECT img_title FROM imginfo WHERE imgid = {imgid}")
        img_title = (cur.fetchone())[0]

        img_frame = customtkinter.CTkFrame(self.gallery)
        title_name = customtkinter.CTkLabel(img_frame, text=img_title)

        # get image from
        cur.execute(f"SELECT img_file_name FROM imginfo WHERE imgid = {imgid}")
        img_file_name = cur.fetchone()
        img_file_name = img_file_name[0]

        image = Image.open(f"img/imguploads/{img_file_name}")

        resized = ImageOps.fit(image, (150, 150), centering=(0.5, 0.5))
        new_pic = ImageTk.PhotoImage(resized)
        img_label = customtkinter.CTkButton(img_frame, image=new_pic, text="", command=lambda: self.post_info(
            imgid), fg_color="transparent")  # type: ignore

        img_frame.grid(row=y, column=x, padx=3, pady=5)
        img_label.pack()
        title_name.pack(pady=(3, 5))

        connection.close()

    def post_info(self, imgid):
        if self.post_window is None or not self.post_window.winfo_exists():
            connection = sqlite3.connect("artsharer.db")
            cur = connection.cursor()

            cur.execute(
                f"SELECT imgFileName FROM imginfo WHERE imgid = {imgid}")
            img_file_name = cur.fetchone()
            img_file_name = img_file_name[0]

            cur.execute(f"SELECT img_title FROM imginfo WHERE imgid = {imgid}")
            self.img_title = (cur.fetchone())[0]
            cur.execute(f"SELECT imgTags FROM imginfo WHERE imgid = {imgid}")
            img_tags = (cur.fetchone())[0]
            cur.execute(
                f"SELECT imgCaptions FROM imginfo WHERE imgid = {imgid}")
            imgcaption = (cur.fetchone())[0]

            image = Image.open(f"img/imguploads/{img_file_name}")
            resized = ImageOps.contain(image, (500, 500))
            width, height = resized.size
            new_pic = ImageTk.PhotoImage(resized)

            image_dimensions = "%dx%d" % (width, height)

            self.grid_rowconfigure(1, weight=1)
            self.post_window = customtkinter.CTkToplevel(self)

            post_frame = customtkinter.CTkFrame(self.post_window)
            post_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

            image_label = customtkinter.CTkLabel(
                post_frame, image=new_pic, text="")  # type: ignore
            image_label.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
            size_label = customtkinter.CTkLabel(
                post_frame, text=image_dimensions)

            desc_frame = customtkinter.CTkFrame(post_frame)

            title = customtkinter.CTkLabel(desc_frame, text=self.img_title, font=(
                "", 25, "bold"), justify="left", anchor="w")
            caption = customtkinter.CTkLabel(
                desc_frame, text=imgcaption, justify="left", anchor="w")
            tag_title = customtkinter.CTkLabel(desc_frame, text="Tags", font=(
                "", 23, "bold"), justify="left", anchor="w")
            tags = customtkinter.CTkLabel(
                desc_frame, text=img_tags, justify="left", anchor="w")

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
        add_btn = customtkinter.CTkButton(
            self.main_window_frame, text="+", width=75, height=75, command=self.upload_page)
        add_btn.place(anchor="se", relx=1, rely=1, x=-30, y=-30)

    def upload_page(self):
        
        if self.upload is None or not self.upload.winfo_exists():
            # file upload
            self.add = fd.askopenfilename()

            image = Image.open(self.add)
            resized = ImageOps.contain(image, (500, 500))
            width, height = resized.size
            new_pic = ImageTk.PhotoImage(resized)

            image_dimensions = "%dx%d" % (width, height)

            self.upload = customtkinter.CTkToplevel(self)
            self.upload.geometry("530x%d" % (height + 270))

            image_frame = customtkinter.CTkFrame(self.upload)
            image_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

            image_frame.grid_rowconfigure(0, weight=1)
            image_frame.grid_columnconfigure(0, weight=2)
            image_frame.grid_columnconfigure(1, weight=8)

            image_label = customtkinter.CTkLabel(
                image_frame, image=new_pic, text="")  # type: ignore
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
                image_frame, text="Post", command=self.submit_post)

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

    def submit_post(self):
        #adds image information into the databases

        # database connection
        connection = sqlite3.connect("artsharer.db")
        cur = connection.cursor()

        # tag format: space = new tag, under-slash(_) = seperator

        img_file_name = os.path.basename(self.add)

        tags = (self.tag_input.get().lower()).split(" ")
        tags_json = json.dumps(tags)
        cur.execute("INSERT INTO imginfo (imgFileName, img_title,imgCaptions,imgTags) values('{}', '{}','{}','{}')".format(
            img_file_name, self.name_input.get(), self.caption_input.get('1.0', 'end-1c'), tags_json))
        connection.commit()

        cur.execute("SELECT imgid FROM imginfo ORDER BY imgid DESC LIMIT 1")
        imgid = cur.fetchone()
        imgid = imgid[0]

        for i in tags:
            # checking if tag exists in database
            tag_name = cur.execute(
                f"SELECT tagName FROM taginfo WHERE tagName = '{i}'")
            tag_name = tag_name.fetchone()
            if tag_name is None:
                # conversion to string representation of list for storing
                imgid_str = [imgid]
                imgid_str = json.dumps(imgid_str)
                # create new tag entry
                cur.execute("INSERT INTO taginfo(tagName,imgAmount,imgids) values('{}',{},'{}')".format(
                    i, 1, imgid_str))
                connection.commit()
            else:
                # string -> list
                tag_name = tag_name[0]
                cur.execute(
                    f"SELECT imgAmount FROM taginfo WHERE tagName = '{i}'")
                img_amount = cur.fetchone()
                img_amount = int(img_amount[0])
                img_amount = img_amount + 1
                cur.execute(
                    f"UPDATE taginfo SET imgAmount = {img_amount} WHERE tagName = '{tag_name}'")
                connection.commit()

                cur.execute(
                    "SELECT imgids FROM taginfo WHERE tagName = '{}'".format(tag_name))
                imgids = cur.fetchone()
                print(imgids)
                imgids = imgids[0]

                print(imgids)
                imgids = json.loads(imgids)
                imgids.append(imgid)
                imgids = json.dumps(imgids)
                print(imgids)
                cur.execute(
                    f"UPDATE taginfo SET imgids = '{imgids}' WHERE tagName = '{tag_name}'")
                connection.commit()

        shutil.copy2(self.add, "img/imguploads")

        connection.commit()
        connection.close()


if __name__ == "__main__":
    root = Start()
    root.mainloop()
