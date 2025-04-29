import customtkinter as ctk
from tkinter import Canvas

class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Create a canvas
        self.canvas = Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Add a vertical scrollbar to the canvas
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        
        # Add the scrollable frame to the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind the configure event of the scrollable frame to update the scroll region
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        
        # Bind the mousewheel event to the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        for i in range(40):
            ctk.CTkLabel(self.scrollable_frame, text=f"Label {i+1}").pack()
        
    def on_frame_configure(self, event):
        # Update the scroll region of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_mousewheel(self, event):
        # Scroll the canvas with the mouse wheel
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")