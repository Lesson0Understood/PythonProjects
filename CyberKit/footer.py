import customtkinter as ctk
from constants import Footer_Frame, icons_dir
from PIL import Image, ImageTk

class Footer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,**Footer_Frame)
        self.create_widgets()
    
    def create_widgets(self):
        self.image = Image.open(f"{icons_dir}/MainIcon.png")
        self.image = self.image.resize((32, 32), Image.LANCZOS)  # Resize the image
        self.icon = ImageTk.PhotoImage(self.image)
        self.copyright = ctk.CTkLabel(self,
                                      text="Islam - 2024 | Sponsored By JordanSec Team",
                                      image=self.icon,
                                      compound="right",
                                      )
        self.copyright.pack(side="bottom",pady=5)