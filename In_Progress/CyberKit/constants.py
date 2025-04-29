# Directories


icons_dir = "assets/images/icons"

# Colors
# Add temporary debug colors
KitSelectionBar_Frame = {
    "fg_color": "#222B33",
    "corner_radius": 0,
    "border_width": 2,
    "border_color": "#AAAAAA",
    "bg_color": "#222B33"  # Add debug color
}

Container_Frame = {
    "fg_color": KitSelectionBar_Frame["fg_color"],
    "corner_radius": 0,
    "bg_color": KitSelectionBar_Frame["fg_color"]  # Add debug color
}

KitSelectionBar_Button = {
    "height": 45,
    "fg_color" : "#2D8286",
    "border_color": "#FFFFFF",
    "border_width": 2,
    "corner_radius": 10,
    "background_corner_colors": (KitSelectionBar_Frame["fg_color"],)*4,
    "text_color": "#FFFFFF",
    "hover_color": "#0078DB",
    "font": ("Arial",20,"bold")
}

HotBar_Frame = {"fg_color": "#263748",
                "bg_color": KitSelectionBar_Frame["fg_color"],
                "corner_radius": 0,}

HotBar_Frame_Debug = {
                "fg_color": "#222B33",
                "corner_radius": 0,
                "border_width": 2,
                "border_color": "#AAAAAA",
                "bg_color": "#222B33"  # Add debug color
                }
HotBar_Button = {"fg_color":"#263748",
                 "hover_color":"#345B63",
                 "width": 40,
                 "font": ("Arial",16),
                 }
MainFrame_Design = {"fg_color": "#2B2F33",
             "corner_radius": 0,
             }
MainPanel_Frame = {"fg_color": "#2B2F33",
                   "bg_color":"#2B2F33",
                   }


SidePanel_Frame = {"fg_color": "#263748"}


AppName_Label = {"bg_color": KitSelectionBar_Frame["fg_color"]}


Footer_Frame = {"fg_color": "#2D8286",
                "bg_color": "#2D8286",
                "border_color":"#FFFFFF",
                "border_width": 0,
                "corner_radius": 0}
CopyRight_TFrame = {"bg_color": "#263748"}
