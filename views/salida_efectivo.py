import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from database.salida_efectivo_db import guardar_salida


COLOR_FONDO = "#ffffff"
COLOR_BOTON = "#A9B7C0"
COLOR_BOTON_HOVER = "#8F9BA3"
COLOR_BOTON_TEXTO = "#1F2937"

class Salida_efectivo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.widgets()

    def widgets(self): 

        frame = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=0)
        frame.place(x=0,y=0,width=400,height=300)   

        lblcantidad = tk.Label(frame,text="Cantidad:",font=("sans",15,"bold"),bg=COLOR_FONDO)
        lblcantidad.place(x=78,y=15,)
        self.entry_cantidad = ctk.CTkEntry(frame,font=("sans", 19, "bold"),corner_radius=10,width=250, height=40)
        self.entry_cantidad.place(relx=0.5,y=50,anchor="n")
        self.entry_cantidad.bind("<KeyRelease>",self.formatear_cantidad)

        lblmotivo = tk.Label(frame,text="Motivo:",font=("sans",15,"bold"),bg=COLOR_FONDO)
        lblmotivo.place(x=78,y=110,)
        self.entry_motivo = ctk.CTkEntry(frame,font=("sans", 19, "bold"),corner_radius=10,width=250, height=40)
        self.entry_motivo.place(relx=0.5,y=145,anchor="n")

        btnguardar = ctk.CTkButton(frame,text="Guardar",fg_color=COLOR_BOTON,font=("sans",16,"bold"),hover_color=COLOR_BOTON_HOVER,text_color=COLOR_BOTON_TEXTO,
            corner_radius=10,width=190,height=40,command=self.guardar)
        btnguardar.place(x=100,y=220)

    def formatear_cantidad(self, event):
        entry = event.widget
        texto = entry.get().replace(",", "").strip()
        if texto.isdigit():
            texto_formateado = "{:,}".format(int(texto))
            entry.delete(0, tk.END)
            entry.insert(0, texto_formateado)
            entry.icursor(tk.END)    

    def guardar(self):   
        cantidad = self.entry_cantidad.get().strip()
        motivo = self.entry_motivo.get().strip()

        if not cantidad or not motivo:
            messagebox.showerror("Error", "Debe completar todos los campos",parent=self)
            return
        if motivo.replace(" ", "").isalpha() is False:
            messagebox.showerror("Error", "El motivo solo debe contener texto", parent=self)
            return
        try:
            monto = float(cantidad.replace(",",""))
        except ValueError:
            messagebox.showerror("Error", "Cantidad no válida", parent=self) 
            return  

        if guardar_salida(monto,motivo):
            self.entry_cantidad.delete(0, tk.END)
            self.entry_motivo.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Salida registrada correctamente", parent=self)
        else:
            messagebox.showerror("Error", "No se pudo guardar la salida", parent=self)         

