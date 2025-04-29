import customtkinter as ctk
from constants import *
from PIL import Image, ImageTk

class HotBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, **HotBar_Frame)
        self.button_names = ["file", "edit", "about", "help"]
        self.icons = []
        self.create_widgets()
    
    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1,minsize=250)
        self.grid_columnconfigure(1, weight=1,minsize=250)
        self.grid_columnconfigure(2, weight=1,minsize=150)
        self.grid_rowconfigure(0, weight=0)
        # Create a frame for buttons
        self.buttons_frame = ctk.CTkFrame(self, **HotBar_Frame)
        self.buttons_frame.grid(row=0, column=0, columnspan=1, sticky="ew")

        # Create and place buttons in the buttons_frame
        for i, name in enumerate(self.button_names):
            button = ctk.CTkButton(self.buttons_frame,
                                   text=name,
                                   command=self.open_settings,
                                   **HotBar_Button)
            if i == 0:
                button.grid(row=0, column=i, padx=(5,5), pady=(7, 5))
            else:
                button.grid(row=0, column=i, padx=(5,0), pady=(7, 5))

        # Create and place the app name label
        self.app_name_frame = ctk.CTkFrame(self,**HotBar_Frame,border_width=2,border_color=HotBar_Frame["fg_color"])
        self.app_name = ctk.CTkLabel(self.app_name_frame,
                                     text="CyberKit",
                                     font=ctk.CTkFont("Arial", size=30, weight="bold"),
                                     text_color="#FFFFFF",
                                     pady=5,fg_color="#263748",padx=20)
        self.app_name_frame.grid(row=0, column=1,sticky="nswe")
        self.app_name.pack(padx=(0,110))


        # Configure grid weights to ensure proper alignment


    def open_settings(self):
        window = ctk.CTkToplevel(self)
        window.title("Settings")
        window.geometry("500x500")
