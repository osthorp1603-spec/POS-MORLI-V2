import tkinter as tk
from core.container import Container
from utils.rutas import ruta_base
import os


COLOR_FONDO = "#c6d9e3"

class Manager(tk.Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.withdraw()
        self.title("Sistema POS Morli v2.0")
        self.iconbitmap(os.path.join(ruta_base(), "icono.ico"))
        self.resizable(False,False)
        self.configure(bg=COLOR_FONDO)
        self.geometry("1000x480+120+20")    #CAMBIAR TAMAÑO, PERO NO SOLO AQUI SINO EN CONTAINER TAMBIEN 800X400 VIEJO

        self.container = tk.Frame(self,bg=COLOR_FONDO)
        self.container.pack(fill="both",expand=True)

        self.frames = {
            Container: None
        }

        self.load_frames()
        self.show_frames(Container)
        self.deiconify()

    def load_frames(self):
        for FrameClass in self.frames.keys():    
            frame = FrameClass(self.container,self)
            self.frames[FrameClass] = frame

    def show_frames(self,frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


  
