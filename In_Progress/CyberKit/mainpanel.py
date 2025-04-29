import customtkinter as ctk
from constants import MainPanel_Frame


class MainPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,**MainPanel_Frame)
        self.create_widgets()
    
    def create_widgets(self):
        self.top_frame = ctk.CTkFrame(self)

        self.MainLabel = ctk.CTkLabel(self.top_frame,text="Welcome To CyberKit")
        self.SubMainLabel = ctk.CTkLabel(self.top_frame,text="Welcome To CyberKit")