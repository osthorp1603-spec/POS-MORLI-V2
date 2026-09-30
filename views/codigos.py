import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from ttkthemes import ThemedStyle
from database.codigos_db import verificar_codigo_existe, insertar_codigo
from database.inventario_db import (obtener_todos_los_productos, buscar_productos_completos_por_nombre, verificar_codigo_duplicado,
    actualizar_codigo_barras,obtener_precio_por_id )
from utils.generador import generar_pdf_etiqueta

COLOR_FONDO = "#F1F5F9"
COLOR_TITULO = "#1E6091"
COLOR_TEXTO  = "#6B7280"
COLOR_BOTON1 = "#2563EB"
COLOR_HOVER1 = "#1D4ED8"
COLOR_BOTON2 = "#2D8A56"            
COLOR_HOVER2 = "#246E44" 
COLOR_SECUNDARIO = "#E8ECEF" 


class Codigos(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.widgets()

    def widgets(self):  
        # FRAME TITULO   SE NECESITA EL FRAME 1 PARA QUE TAPE EL PEDAZO DE FONOD QEU VIEN DEL CONTAINER
        frame1 = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=0)
        frame1.place(x=0,y=0,width=1100,height=70)      

        # CAPA QEU CONTINEE EL TITULO
        titulo = tk.Label(self,text="Asignar codigos de barra",bg=COLOR_FONDO,fg=COLOR_TITULO,font="sans 30 bold",anchor="w")
        titulo.place(x=20,y=10,width=1100,height=60)

        # FRAME TODA LA VENTANTA
        frame2 = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=1)
        frame2.place(x=0,y=64,width=1100,height=577) 

        lblnuevocodigo = tk.Label(frame2,text="Nuevo Codigo:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lblnuevocodigo.place(x=240,y=30)
        self.entrynuevocodigo = ctk.CTkEntry(frame2,font=("sans",16,"bold"),corner_radius=10,width=220,height=38)
        self.entrynuevocodigo.place(x=240,y=64)
        
        lblbuscarproducto = tk.Label(frame2,text="Buscar producto:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lblbuscarproducto.place(x=650,y=30)
        self.entrybuscarproducto = ctk.CTkEntry(frame2,font=("sans",16,"bold"),corner_radius=10,width=220,height=38)
        self.entrybuscarproducto.place(x=650,y=64)
        self.entrybuscarproducto.bind("<KeyRelease>", self.filtrar)
        
        # TREEVIEW
        treeframe = tk.Frame(frame2,bg=COLOR_SECUNDARIO)           
        treeframe.place(x=20,y=140,width=1040,height=260) 

        # BLOQUE SCROLLBAR ////////////////////////////////
        scrol_y = ttk.Scrollbar(treeframe,orient=tk.VERTICAL)
        scrol_y.pack(side=tk.RIGHT,fill=tk.Y)

        scrol_x = ttk.Scrollbar(treeframe,orient=tk.HORIZONTAL)
        scrol_x.pack(side=tk.BOTTOM,fill=tk.X) 

        # TREEVIEW CREACION CAMPOS////////////////////////////// 
        style = ttk.Style(self)
        style.configure("Treeview", font=("sans", 14), rowheight=25)
        style.configure("Treeview.Heading", font=("sans", 13))
        

        self.tree = ttk.Treeview(treeframe,yscrollcommand=scrol_y.set,xscrollcommand=scrol_x.set,height=40,
            columns=("ID","PRODUCTO","CODIGO BARRAS","STOCK"),
            show = "headings")
        
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)  

        self.tree.heading("ID",text="Id")
        self.tree.heading("PRODUCTO",text="Producto")
        self.tree.heading("CODIGO BARRAS",text="Codigo de barras")
        self.tree.heading("STOCK",text="Stock")

        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("PRODUCTO", width=100, anchor="w")
        self.tree.column("CODIGO BARRAS", width=100, anchor="center")
        self.tree.column("STOCK", width=70, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar)

        btnasignar = ctk.CTkButton(frame2,text="Asignar e imprimir",fg_color=COLOR_BOTON1,text_color="white",font=("sans",15,"bold"),
            corner_radius=10,width=200,height=100,hover_color=COLOR_HOVER1,command=self.asignar_codigo)
        btnasignar.place(x=220,y=430)  

        btnimprimir = ctk.CTkButton(frame2,text="Imprimir",fg_color=COLOR_BOTON2,text_color="white",font=("sans",15,"bold"),
                    corner_radius=10,width=200,height=100,hover_color=COLOR_HOVER2,command=self.imprimir_codigo)
        btnimprimir.place(x=700,y=430)  

        self.mostrar()

    def mostrar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        productos = obtener_todos_los_productos()
        for producto in productos:
            codigo = producto[7] if producto[7] else "-"
            self.tree.insert("", "end", values=(
                producto[0], producto[1], codigo, producto[5]
            ))     

    def filtrar(self, event=None):
        texto = self.entrybuscarproducto.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not texto:
            self.mostrar()
            return
        productos = buscar_productos_completos_por_nombre(texto)
        for producto in productos:
            codigo = producto[7] if producto[7] else "-"
            self.tree.insert("", "end", values=(
                producto[0], producto[1], codigo, producto[5]
            ))

    def al_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        valores = self.tree.item(seleccion)["values"]
        self.entrynuevocodigo.delete(0, "end")
        codigo = valores[2]
        if codigo and codigo != "-":
            self.entrynuevocodigo.insert(0, codigo)

    def asignar_codigo(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Asignar código", "Seleccione un producto.", parent=self)
            return
        codigo = self.entrynuevocodigo.get().strip()
        if not codigo:
            messagebox.showwarning("Asignar código", "Ingrese un código válido.", parent=self)
            return
        producto_id = self.tree.item(seleccion)["values"][0]
        nombre_duplicado = verificar_codigo_duplicado(codigo, producto_id)
        if nombre_duplicado:
            messagebox.showwarning("Código existente", f"El código '{codigo}' ya está asignado al producto: '{nombre_duplicado}'.", parent=self)
            return
        if not verificar_codigo_existe(codigo):
            insertar_codigo(codigo)

        if actualizar_codigo_barras(producto_id, codigo):
            self.entrynuevocodigo.delete(0, "end")
            nombre = self.tree.item(seleccion[0])["values"][1]
            precio = obtener_precio_por_id(producto_id)
            self.mostrar()
            if precio:
                generar_pdf_etiqueta(codigo, nombre, float(precio))
            messagebox.showinfo("Éxito", "Código asignado correctamente.", parent=self)
        else:
            messagebox.showerror("Error", "No se pudo asignar el código.", parent=self)

    def imprimir_codigo(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Imprimir", "Seleccione un producto.", parent=self)
            return
        valores = self.tree.item(seleccion[0])["values"]
        codigo = valores[2]
        if not codigo or codigo == "-":
            messagebox.showwarning("Imprimir", "Este producto no tiene código asignado.", parent=self)
            return
        producto_id = valores[0]
        nombre = valores[1]
        precio = obtener_precio_por_id(producto_id)
        if precio:
            generar_pdf_etiqueta(codigo, nombre, float(precio))
            messagebox.showinfo("Imprimir", f"Etiqueta del código '{codigo}' generada.", parent=self)
        else:
            messagebox.showerror("Error", "No se pudo obtener el precio del producto.", parent=self)         


