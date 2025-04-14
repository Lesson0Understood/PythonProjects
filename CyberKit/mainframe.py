import customtkinter as ctk
from constants import *
from scrollable import ScrollableFrame
from sidepanel import SidePanel
from mainpanel import MainPanel


class MainFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent,**MainFrame_Design)

        self.create_widgets()


    def create_widgets(self):

        self.scrollable_panel = ScrollableFrame(self)
        self.scrollable_panel.pack(side="left",fill="y")


        self.main_panel = MainPanel(self)
        self.main_panel.pack(side="right",fill=ctk.BOTH,expand=True)