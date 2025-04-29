from kitselectionbar import KitSelectionBar
from hotbar import HotBar
from footer import Footer
import customtkinter as ctk
from mainframe import MainFrame


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CyberKit")
        self.geometry("1200x800")
        self.num_columns = 3
        self.num_rows = 4
    # Configure grid column weights
        for i in range(self.num_columns):
            self.grid_columnconfigure(i,weight=1)
        # Configure grid row weights
        for i in range(self.num_rows):
            if i == 2:
                self.grid_rowconfigure(i, weight=1)
            else:
                self.grid_rowconfigure(i, weight=0)


        self.create_widgets()
    
    def create_widgets(self):

        self.hotbar = HotBar(self)  # Replace with your custom implementation
        self.hotbar.grid(row=0,column=0,columnspan=self.num_columns,sticky="nswe")
        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=2,column=0,columnspan=self.num_columns,sticky="nswe")
        self.footer = Footer(self)
        self.footer.grid(row=3,column=0,columnspan=self.num_columns,sticky="nswe")  # Replace with your custom implementation
        #self.main_frame.pack(side="bottom",fill=ctk.BOTH,expand=True)


        # HotBar - Assuming this is a custom widget you created

        #self.hotbar.pack(side="top", fill="x")
        
        # KitSelectionBar - Assuming this is a custom widget you created
        self.kit_selection_bar = KitSelectionBar(self)  # Replace with your custom implementation
        self.kit_selection_bar.grid(row=1,column=0,columnspan=self.num_columns,sticky="nswe")
        #self.kit_selection_bar.pack(side="top", fill="x")

       

        # If there are any other widgets, add them similarly

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()