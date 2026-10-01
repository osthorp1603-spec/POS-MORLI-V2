import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
import webbrowser

COLOR_FONDO = "#ffffff"
COLOR_BOTON = "#A9B7C0"
COLOR_BOTON_HOVER = "#8F9BA3"
COLOR_BOTON_TEXTO = "#1F2937"

class FacturaElectronica(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.widgets()
        
    def widgets(self): 

        frame = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=0)
        frame.place(x=0,y=0,width=400,height=300)   

        btnprueba = ctk.CTkButton(frame,text="Guardar",fg_color=COLOR_BOTON,font=("sans",16,"bold"),hover_color=COLOR_BOTON_HOVER,text_color=COLOR_BOTON_TEXTO,
            corner_radius=10,width=190,height=40,command=lambda: webbrowser.open("https://www.youtube.com/"))
        btnprueba.place(x=30,y=50) 