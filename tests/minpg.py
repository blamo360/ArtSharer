import customtkinter

class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")

class MenuFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_1 = customtkinter.CTkButton(self, text="ragh")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        self.checkbox_2 = customtkinter.CTkButton(self, text="rag")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")

class GalleryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("500x300")

        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.checkbox_frame = MyCheckboxFrame(self)
        self.checkbox_frame.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="nsew", columnspan=2)
        self.menu_frame = MenuFrame(self)
        self.menu_frame.grid(row=1, column=0, padx=(5,0), pady=(5, 0), sticky="nsew")
        self.gallery_frame = GalleryFrame(self)
        self.gallery_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=(5, 0))


    def button_callback(self):
        print("button pressed")

app = App()
app.mainloop()