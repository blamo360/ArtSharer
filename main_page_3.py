from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk



class Start(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x700")

        self.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(Image.open('img/icon.jpg')))

        self.call("source", "assets/themes/Azure-ttk-theme-2.1.0/azure.tcl")
        self.call("set_theme", "dark")

        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(1,weight=1)

        self.main_page()
        self.menu_bar()
        self.search_bar()
        self.main_filter_bar()
        self.minor_filter_bar()

    def kill():
        root.destroy()
        import login_page_1

    def main_page(self):
        self.menu_bar_frame = ttk.Frame(self,style = "Card.TFrame")
        self.menu_bar_frame.grid(row=0, column=0, columnspan= 2, sticky= "WE", padx= 5, pady= (5,0))

        self.main_filter_frame = ttk.Frame(self,style = "Card.TFrame")
        self.main_filter_frame.grid(row=1, column=0, sticky = "NSWE", padx= (5,0), pady = 5)

        self.main_window_frame = ttk.Frame(self, style = "Card.TFrame")
        self.main_window_frame.grid(row=1, column=1, sticky = "NSWE", padx= 5, pady= 5)

        self.main_window_frame.rowconfigure(1, weight= 1)
        self.main_window_frame.columnconfigure(0, weight= 1)

        self.minor_filter_frame = ttk.Frame(self.main_window_frame)
        self.minor_filter_frame.grid(row=0, column=0,sticky="NSWE", padx=5, pady=5)

        self.gallery_seperator = ttk.Separator(self.main_window_frame)
        self.gallery_seperator.grid(row = 1, sticky="NWE", pady=5)

        self.gallery = ttk.Frame(self.main_window_frame, style = "Card.TFrame")
        self.gallery.grid(row=2, column=0,sticky="NSWE", padx=5, pady=5)

    def menu_bar(self):
        self.menu_opt = ["quan", "too", "quan", "quan"]
        self.menu_bar_frame.columnconfigure(list(range(0,len(self.menu_opt))), weight=1)

        for i in range(len(self.menu_opt)):
            self.btn1 = ttk.Button(self.menu_bar_frame, text = self.menu_opt[i])
            self.btn1.grid(row=0,column=i,sticky="WE", padx= 10, pady= 10)

    def search_bar(self):
        self.searchbar = ttk.Entry(self.menu_bar_frame)
        self.searchbar.grid(row=1, column= 0, sticky="NSWE", columnspan = len(self.menu_opt) - 1, padx = 5, pady= 5)
        searchbtn = ttk.Button(self.menu_bar_frame, command=self.kill, text= "search")
        searchbtn.grid(row=1, column=len(self.menu_opt) - 1, sticky="NSWE", padx=20, pady=5)

    def main_filter_bar(self):
        mainfilterselect = ["quknhjhan", "too", "too", "too", "too", "too", "too", "too", "too", "too"]
        frame2len = list(range(0,len(mainfilterselect)))
        self.main_filter_frame.rowconfigure(frame2len, weight=1)
        self.main_filter_frame.columnconfigure(0, weight=1)

        for i in range(len(mainfilterselect)):
            btn1 = ttk.Button(self.main_filter_frame, text = mainfilterselect[i])
            btn1.grid(row=i,column=0,sticky="WE", padx= 10, pady= 10)

    def minor_filter_bar(self):
        minorfilters = ["quan", "too", "too", "too", "too", "too", "too", "too", "too", "too"]
        for i in range(len(minorfilters)):
            filterframe = Frame(self.minor_filter_frame)
            filterframe.grid(row=0, column=i, sticky="WE", padx=5, pady=5)
            filtertext = ttk.Label(filterframe, text = minorfilters[i])
            filtertext.grid(row=0, column=0)
            minorfilterclose = ttk.Button(filterframe, text="x")
            minorfilterclose.grid(row=0, column= 1)




    

if __name__ == "__main__":
    root = Start()
    root.mainloop()
