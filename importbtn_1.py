import tkinter
import customtkinter
import sqlite3
from tkinter import filedialog as fd

class importbtn(customtkinter.CTkButton):
    name= fd.askopenfilename() 
    print(name)
    
