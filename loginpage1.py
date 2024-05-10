from tkinter import *
from PIL import Image, ImageTk

root = Tk()

root.geometry("700x500")
root.configure(bg="#555555")
root.resizable(False, False)

fr1 = Frame(root, bg = "#cccccc")

img1 = Image.open("img/images.png")
img2 = img1.resize((700, 500))
img3 = ImageTk.PhotoImage(img2)
img4 = Label(root, image = img3)

img2 = img1.resize((500, 300))
img6 = ImageTk.PhotoImage(img2)
img5 = Label(fr1, image = img6)


img4.place(relx= 0.5, rely= 0.5, anchor= CENTER)
fr1.place(relx=0.5, rely=0.5, width=500, height=300, anchor = CENTER)
fr1.lift()


root.mainloop()
