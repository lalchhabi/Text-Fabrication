import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from color_picker import ColorApp
from main import create_data
import pickle


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self, image_path):
        super().__init__()

        # configure window
        self.title("Data Fabrication")
        self.geometry(f"{1200}x{600}")
        #loading image
        self.load_image(image_path)

        # self.img_path = image_path 
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)        
        
        # create sidebar frame with widgets
        ##=================left side bar frame andbutton=========================##
        self.sidebar_frame = ctk.CTkFrame(self, width=200,height=600, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)
        self.rsidebar_frame = ctk.CTkFrame(self, width=200,height=600, corner_radius=0)
        self.rsidebar_frame.grid(row=0, column=2, rowspan=5, sticky="nsew")
        self.rsidebar_frame.grid_rowconfigure(9, weight=1)

        self.load_image_button = ctk.CTkButton(self.sidebar_frame, text="load image",command=self.imagetobe_fabricated,width=200)
        self.load_image_button.grid(row=0, column=0, padx=10, pady=10,columnspan=2, sticky="ew")

        self.font_button = ctk.CTkButton(self.sidebar_frame, text="Choose Font",command=self.load_font,width=200)
        self.font_button.grid(row=1, column=0, padx=10, pady=10,columnspan=2,sticky="ew")

        
        
        self.x1_entry_label=ctk.CTkLabel(self.sidebar_frame,text="Enter the value of X1 :")
        self.x1_entry_label.grid(row=2, column=0,  padx=10, pady=10,sticky="ew")
        self.x1_entry = ctk.CTkEntry(self.sidebar_frame,width=150)
        self.x1_entry.grid(row=2, column=1, padx=10, pady=10,sticky="ew")
        self.x2_entry_label=ctk.CTkLabel(self.sidebar_frame,text="Enter the value of X2 :")
        self.x2_entry_label.grid(row=3, column=0,  padx=10, pady=10,sticky="ew")
        self.x2_entry = ctk.CTkEntry(self.sidebar_frame,width=150)
        self.x2_entry.grid(row=3, column=1, padx=10, pady=10,sticky="ew")
        self.y1_entry_label=ctk.CTkLabel(self.sidebar_frame,text="Enter the value of Y1 :")
        self.y1_entry_label.grid(row=4, column=0,  padx=10, pady=10,sticky="ew")
        self.y1_entry = ctk.CTkEntry(self.sidebar_frame,width=150)
        self.y1_entry.grid(row=4, column=1, padx=10, pady=10,sticky="ew")
        self.y2_entry_label=ctk.CTkLabel(self.sidebar_frame,text="Enter the value of Y2 :")
        self.y2_entry_label.grid(row=5, column=0, padx=10, pady=10,sticky="ew")
        self.y2_entry = ctk.CTkEntry(self.sidebar_frame,width=150)
        self.y2_entry.grid(row=5, column=1, padx=10, pady=10,sticky="ew")

        self.color_button = ctk.CTkButton(self.sidebar_frame, command=self.colorpicker,text="Choose Color",width=200)
        self.color_button.grid(row=6, column=0, padx=10, pady=10,columnspan=2,sticky="ew")
        
        
        # self.color_label=ctk.CTkLabel(self.sidebar_frame,text="Color Value (R, G, B) :")
        # self.color_label.grid(row=7, column=0, padx=10, pady=10,sticky="ew")
        # self.color_entry = ctk.CTkEntry(self.sidebar_frame,width=150)
        # self.color_entry.grid(row=7, column=1, padx=10, pady=10,sticky="ew")

        self.image_number_label=ctk.CTkLabel(self.sidebar_frame,text="Number of image to generate :")
        self.image_number_label.grid(row=8, column=0,  padx=10, pady=10,sticky="ew")
        self.image_number_entry = ctk.CTkEntry(self.sidebar_frame,width=150)
        self.image_number_entry.grid(row=8, column=1, padx=10, pady=10,sticky="ew")

        self.font_button = ctk.CTkButton(self.sidebar_frame, text="Generate Fabricated Data",command=self.generate_data,width=200)
        self.font_button.grid(row=9, column=0,columnspan = 2,  padx=10, pady=10,sticky="ew")

        self.coordinate_label=ctk.CTkLabel(self.rsidebar_frame,text="Coordinate(X1,Y1)")
        self.coordinate_label.grid(row=0, column=3,  padx=5, pady=5,sticky="ew")
        self.coordinate_entry=ctk.CTkEntry(self.rsidebar_frame,width=150)
        self.coordinate_entry.grid(row=1,column=3,padx=5,pady=5,sticky='ew')

    def on_press(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        pixels = int(x),int(y)
        
        self.coordinate_entry.delete(0,ctk.END)
        self.coordinate_entry.insert(0,str(pixels))
        self.x1_entry.delete(0,ctk.END)
        self.x1_entry.insert(0,str(int(x)))
        self.y1_entry.delete(0,ctk.END)
        self.y1_entry.insert(0,str(int(y)))


    def colorpicker(self):
        ColorApp(self.imagename)


    def imagetobe_fabricated(self):
        self.imagename=ctk.filedialog.askopenfilename(initialdir="/Desktop/",title="open images",filetypes=(("png files","*.png"),("jpg files","*.jpg"),("jpeg files","*.jpeg")))
        self.load_image(self.imagename)
    
    def load_font(self):
        self.font = ctk.filedialog.askopenfilenames(title="choose font",filetypes=[("ttf files","*.ttf")])
    
    def complete(self):
        CTkMessagebox(message="Data Fabrication Completed",icon="check", option_1="Ok")
    
    def generate_data(self):
        try:
            font=''.join([str(x) for x in self.font])
            create_data(self.imagename,self.x1_entry.get(),self.x2_entry.get(),self.y1_entry.get(),self.y2_entry.get(),int(self.image_number_entry.get()),font=font)
            CTkMessagebox(message="Data Fabrication Completed",icon="check", option_1="Ok")
            print("====data fabrication complete======")

        except Exception as e:
            print("Select the font first")
            print(e)

        
        
        # obj.mainloop()
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
        self.frame.grid(row=1, column=1,padx=50, sticky="w"+"n")

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

  
if __name__ == "__main__":
    image_path =r"C:\Users\shres\OneDrive\Desktop\Office\data_fabrication\Text-Fabrication\blank_image.png"
    app = App(image_path)

    app.mainloop()

