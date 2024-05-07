import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import yaml

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self, image_path):
        super().__init__()

        # configure window
        self.title("Labling Bounding box")
        self.geometry(f"{1200}x{600}")
        #loading image
        self.load_image(image_path)
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)        
        
        # create sidebar frame with widgets
        ##=================left side bar frame andbutton=========================##
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.entry=ctk.CTkLabel(self.sidebar_frame,text="RGB Color Code")
        self.entry.grid(row=0, column=0, padx=10, pady=5,sticky="w")
        self.entry = ctk.CTkEntry(self.sidebar_frame,width=200)
        self.entry.grid(row=0, column=1,sticky="w")
        self.entry1=ctk.CTkLabel(self.sidebar_frame,text="HEX Code")
        self.entry1.grid(row=1, column=0, padx=10, pady=5,sticky="w")
        self.entry1 = ctk.CTkEntry(self.sidebar_frame,width=200)
        self.entry1.grid(row=1, column=1, padx=0, pady=5,sticky="w")
       
        self.color_display = ctk.CTkButton(self.sidebar_frame, text=" ",width=200)
        self.color_display.grid(row=3, column=1, padx=0, pady=5,sticky="w")

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, command=self.save_color, text="Save Color",width=200)
        self.sidebar_button_2.grid(row=4, column=1, padx=10, pady=10,sticky="w")
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=10,sticky="w")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], width=200,command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=1, padx=10, pady=5,sticky="w")
        self.appearance_mode_optionemenu.set("Light")


    #####===================Changing the mode Light and Dark mode=============############
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    
    ####=============Image loading in canvas================#########
    def load_image(self,image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image,master=self)
        if self.image is None:
            print(f"Error: Unable to load image from {image_path}")
            return

        # create a scrollable frame
        self.frame = ctk.CTkFrame(self,width=self.photo.width(),height=self.photo.height())
        self.frame.grid(row=1, column=1,padx=(1, 0), pady=(1, 0), sticky="w"+"n")

        #creating scrollbar
        hsbar= tk.Scrollbar(self.frame, orient="horizontal")
        vsbar= tk.Scrollbar(self.frame, orient="vertical")

        self.canvas = ctk.CTkCanvas(self.frame,width=self.photo.width(),height=self.photo.height(),
                                    scrollregion=(0,0,self.photo.width(),self.photo.height()),
                                    xscrollcommand=hsbar.set, yscrollcommand=vsbar.set)
        

        hsbar.pack(side="bottom", fill='x')
        vsbar.pack(side="right", fill="y")

        self.canvas.pack(side="left",expand="yes",fill="both")


        hsbar.configure(command=self.canvas.xview)
        vsbar.configure(command=self.canvas.yview)
       
        # Load image onto canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        
        #button function on canvas
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
    def on_mousewheel(self, event):
        if event.state & 0x1:
            if event.delta < 0:  
                self.canvas.xview_scroll(1 , "units")     
            else:
                self.canvas.xview_scroll(-1 , "units")
        else:
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
    
    def from_rgb(self,rgb):
        return "#%02x%02x%02x" % rgb
 
    def on_press(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        pixels = self.image.getpixel((x, y))
        ds = self.from_rgb((pixels))
        color=ds
        self.entry.delete(0,ctk.END)
        self.entry.insert(0,str(pixels))
        #####=====Hex Code========#
        self.entry1.delete(0,ctk.END)
        self.entry1.insert(0,str(color))
        
        self.color_display.configure(hover_color=color,fg_color=color)
   
    ####===========saving color value=============##########
    def save_color(self):
        color=self.entry.get()
        with open("color.txt", "w") as f:
            f.write(f"{color}")
        print("Coordinates saved to rectangle_coordinates.txt")
        return(color)

if __name__ == "__main__":
    image_path = "C:/Users/shres/OneDrive/Desktop/Office/det/OCR_training/bounding box software/IMG1.bmp"
    app = App(image_path)
    app.mainloop()


def read_from_txt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        return None

file_path = "color.txt"
color_fill=read_from_txt_file(file_path)
color_fill_tuple = tuple(map(int, color_fill.strip('()').split(', ')))



