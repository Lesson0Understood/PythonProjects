from PIL import Image, ImageTk
import customtkinter as ctk
from constants import icons_dir , KitSelectionBar_Frame, Container_Frame , KitSelectionBar_Button

class KitSelectionBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,**KitSelectionBar_Frame)
        self.button_names = ["Reverse", "Web", "Crypto", "Forensics", "Pwn", "Osint"]
        self.icons = {}  # Store image references
        self.create_widgets()


    def create_widgets(self):
        container = ctk.CTkFrame(self, **Container_Frame)
        container.pack(expand=True, pady=5)
        for name in self.button_names:
            original_icon = Image.open(f"{icons_dir}/{name}.png")
            resized_icon = original_icon.resize((32, 32), Image.Resampling.LANCZOS)
            icon = ctk.CTkImage(resized_icon)  # Use CTkImage instead of PhotoImage
            self.icons[name] = icon  # Store the reference to the image object
            button = ctk.CTkButton(container,
                                   text=name,
                                   image=icon,
                                   compound="left",
                                   command=lambda name=name: self.open_kit(name),
                                   **KitSelectionBar_Button,
                                   )
            button.pack(side="left", padx=4, pady=5)

    def open_kit(self, title):
        window = ctk.CTkToplevel()
        window.title(title)
        window.geometry("500x500")
