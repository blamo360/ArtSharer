from tkinter import *  

root = Tk()  

root.geometry("200x200")  

#here define your f1 window
def f1():  
    top = Toplevel(root)
    top.geometry("400x400")
    top.title("I am f1 window smaller than f2 but bigger than root")    
    top.mainloop() 

#Similarly here define your f2 window
def f2():  
    top = Toplevel(root)
    top.geometry("500x500")
    top.title("I am f2 window bigger than f1")  
    top.mainloop()
    

btn1 = Button(root, text = "open f1", command = f1)  
btn2 = Button(root, text = "open f2", command = f2)  


btn1.place(x=75,y=50)
btn2.place(x=75,y=20)  


root.mainloop()