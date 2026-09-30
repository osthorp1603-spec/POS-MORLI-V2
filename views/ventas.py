import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from ttkthemes import ThemedStyle  # ttktheme para el treeview
from PIL import Image
from database.inventario_db import (obtener_precio_producto,buscar_productos_por_nombre,obtener_stock_producto,
    buscar_producto_por_codigo,hay_stock_suficiente)
from database.ventas_db import obtener_siguiente_factura
from core.rf import mover_a_rf_registros
from views.pago import Pago
from views.venta_diaria import VentaDiaria
from utils.rutas import ruta_base
import os
from datetime import datetime


# Paleta 
COLOR_FONDO = "#C6D9E3"            
COLOR_TITULO = "#1E6091"           
COLOR_TABLA_FONDO = "#ECF2F6"     
# Botón Principal de Cobro 
COLOR_PAGAR = "#2D8A56"            
COLOR_PAGAR_HOVER = "#246E44"     
# Botones Secundarios
COLOR_SECUNDARIO = "#D1D5DB"       
COLOR_SECUNDARIO_HOVER = "#9CA3AF" 
COLOR_SECUNDARIO_TEXTO = "#1F2937" 
# Alerta y Cancelación
COLOR_CANCELAR = "#A32D2D"         
COLOR_CANCELAR_HOVER = "#7A2222"   
COLOR_CANCELAR_TEXTO = "#FFFFFF"   

class Ventas(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.widgets() 

    def widgets(self):
    # FRAME DEL ENCABEZADO    
        titulo = tk.Label(self,text="VENTAS",bg=COLOR_FONDO,fg=COLOR_TITULO,font="sans 30 bold",anchor="center")
        titulo.place(x=5,y=5,width=1090,height=90)

    # FRAME DE LA VENTANA VENTAS ////////// PODRIA HABERSE LLAMADO frame1, pero PORQUE YA SE CREARON VARIAS
        frame2 = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=1)
        frame2.place(x=0,y=100,width=1100,height=550)

    #FRAME LABEL FRAME////////////////    
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TABLA_FONDO,corner_radius=10,width=1080,height=90)
        lblframe.place(x=10,y=10)
        titulo_info = ctk.CTkLabel(lblframe,text="INFORMACION VENTAS",font=("sans",13,"bold"))
        titulo_info.place(x=15,y=8)
        
    # LABEL DE FACTURA NO - ENTRY DE FACUTRA /////   
        label_numero_factura = tk.Label(lblframe,text="Factura No: ",bg=COLOR_TABLA_FONDO,font="sans 13 bold")
        label_numero_factura.place(x=18,y=46)
        self.numero_factura = tk.StringVar()
    #//////////////////////////////////////////////////    
        self.entry_numero_factura = ctk.CTkEntry(lblframe,textvariable=self.numero_factura,state="disabled",font=("sans",19,"bold"),corner_radius=10,width=80,height=42,justify="center")
        self.entry_numero_factura.place(x=118,y=38)

    # LABEL DE PRODUCTOS - ENTRY PRODUCTOS //////////
        label_producto = tk.Label(lblframe,text="Producto: ",bg=COLOR_TABLA_FONDO,font="sans 13 bold") 
        label_producto.place(x=220,y=46)  
    #////////////////////////////////////////////////
        self.entry_producto = ctk.CTkEntry(lblframe,font=("sans",19,"bold"),corner_radius=10,width=270,height=42)
        self.entry_producto.place(x=310,y=38)
        self.entry_producto.bind("<KeyRelease>", self.filtrar_productos)

    # LABEL DE PRECIO - ENTRY PRECIO //////////    
        label_precio = tk.Label(lblframe,text="Precio: ",bg=COLOR_TABLA_FONDO,font="sans 13 bold") 
        label_precio.place(x=610,y=46)  
    # //////////////////////////////////////////////////
        self.entry_precio = ctk.CTkEntry(lblframe,font=("sans",19,"bold"),corner_radius=10,width=130,height=42,justify="center")
        self.entry_precio.place(x=680,y=38)


     # LABEL DE CANTIDAD - ENTRY CANTIDAD /////////////
        label_cantidad = tk.Label(lblframe,text="Cantidad: ",bg=COLOR_TABLA_FONDO,font="sans 13 bold") 
        label_cantidad.place(x=852,y=46)  
    # //////////////////////////////////////////////////
        self.entry_cantidad = ctk.CTkEntry(lblframe,font=("sans",19,"bold"),corner_radius=10,width=100,height=42,justify="center")
        self.entry_cantidad.place(x=945,y=38)

    # TREEVIEW VENTANA//////////////////////////////
        treframe = tk.Frame(frame2,bg=COLOR_FONDO)           
        treframe.place(x=10,y=120,width=1080,height=200) 

    # BLOQUE SCROLLBAR ////////////////////////////////
        scrol_y = ttk.Scrollbar(treframe,orient=tk.VERTICAL)
        scrol_y.pack(side=tk.RIGHT,fill=tk.Y)

        scrol_x = ttk.Scrollbar(treframe,orient=tk.HORIZONTAL)
        scrol_x.pack(side=tk.BOTTOM,fill=tk.X)

    # TREEVIEW CREACION CAMPOS//////////////////////////////   
        style = ThemedStyle(self)
        style.set_theme("breeze")  
        style.configure("Treeview", font=("sans", 15), rowheight=30)
        self.tree = ttk.Treeview(treframe,columns=("Producto","Precio","Cantidad","Total"),
                                show="headings",height=12,yscrollcommand=scrol_y.set,xscrollcommand=scrol_x.set)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)  

        self.tree.heading("#1",text="Producto")
        self.tree.heading("#2",text="Precio")
        self.tree.heading("#3",text="Cantidad")
        self.tree.heading("#4",text="Total")

        self.tree.column("Producto",anchor="center")
        self.tree.column("Precio",anchor="center")
        self.tree.column("Cantidad",anchor="center")
        self.tree.column("Total",anchor="center")

        self.tree.pack(expand=True,fill=tk.BOTH)

    # LABEL VISUALIZACION DE TOTAL
        lblframe2 = ctk.CTkFrame(frame2,fg_color=COLOR_TABLA_FONDO,corner_radius=10,width=1080,height=70) 
        lblframe2.place(x=10, y=333)   
        self.suma_total = ctk.CTkLabel(lblframe2,text="Total a pagar: $ 0",font=("sans",25,"bold"))
        self.suma_total.place(relx=0.5, rely=0.5, anchor="center")

    # LABEL FRAME INFERIOR
        lblframe1 = ctk.CTkFrame(frame2,fg_color=COLOR_TABLA_FONDO,corner_radius=10,width=1080,height=140)
        lblframe1.place(x=10,y=416)

        titulo_opciones = ctk.CTkLabel(lblframe1,text="Opciones",font=("sans",12,"bold"))
        titulo_opciones.place(x=15,y=8)  

    #BOTONES LABEL FRAME INFERIOR   
        self.icon_add = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/agregar.png")), size=(30, 30))
        self.btnagregar = ctk.CTkButton(lblframe1,image=self.icon_add,compound="left",text="Agregar",fg_color=COLOR_SECUNDARIO,text_color=COLOR_SECUNDARIO_TEXTO,
            font=("sans",15,"bold"),corner_radius=10,width=330,height=45,hover_color=COLOR_SECUNDARIO_HOVER,command=self.registrar)
        self.btnagregar.place(x=30,y=35)

        self.icon_pag = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/compra.png")), size=(35, 35))
        btnpagar = ctk.CTkButton(lblframe1,image=self.icon_pag,compound="left",text="Pagar",fg_color=COLOR_PAGAR,text_color="white",font=("sans",15,"bold"),
            corner_radius=10,width=330,height=45,hover_color=COLOR_PAGAR_HOVER,command=self.abrir_pago)
        btnpagar.place(x=375,y=35)

        self.icon_vd = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/reporte.png")), size=(30, 30))
        btnventa_diaria = ctk.CTkButton(lblframe1,image=self.icon_vd,compound="left",text="Venta Diaria",fg_color=COLOR_SECUNDARIO,text_color=COLOR_SECUNDARIO_TEXTO,
            font=("sans",15,"bold"),corner_radius=10,width=330,height=45,hover_color=COLOR_SECUNDARIO_HOVER,command=self.abrir_venta_diaria)
        btnventa_diaria.place(x=720,y=35)

        self.icon_rf = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/borrar.png")), size=(25, 25))
        btncancelar = ctk.CTkButton(lblframe1,image=self.icon_rf,compound="left",text="Cancelar venta (RF)",fg_color=COLOR_CANCELAR,
            text_color=COLOR_CANCELAR_TEXTO,font=("sans",14,"bold"),corner_radius=10,width=325,height=45,
            hover_color=COLOR_CANCELAR_HOVER,
            command=lambda: mover_a_rf_registros(self.tree, self.actualizar_total, int(self.numero_factura.get())))
        btncancelar.place(x=380,y=85)

        self.actualizar_numero_factura()

        # LECTOR DE PISTOLA
        self.entry_pistola = ctk.CTkEntry(self, width=1, height=1)
        self.entry_pistola.place(x=-100, y=-100)
        self.entry_pistola.bind("<Return>", self.leer_codigo_barras)
        self.entry_pistola.focus_set()
            
       # BLOQUE METODOS ////////////////////////////////////////////////////////////////////
    def actualizar_numero_factura(self):
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        siguiente = obtener_siguiente_factura(fecha_hoy)
        self.numero_factura.set(str(siguiente))

    def filtrar_productos(self, event):
        texto = self.entry_producto.get().strip()
        if not texto:
            if hasattr(self, "toplevel_filtro") and self.toplevel_filtro.winfo_exists():
                self.toplevel_filtro.destroy()
            return

        productos = buscar_productos_por_nombre(texto)
        nombres = [p[0] for p in productos]

        if not hasattr(self, "toplevel_filtro") or not self.toplevel_filtro.winfo_exists():
            self.toplevel_filtro = tk.Toplevel(self)
            self.toplevel_filtro.title("Filtrar productos")
            self.toplevel_filtro.geometry("300x200+400+250")
            self.toplevel_filtro.transient(self)
            self.toplevel_filtro.resizable(False, False)
            self.listbox_filtro = tk.Listbox(self.toplevel_filtro, font="sans 12")
            self.listbox_filtro.pack(fill=tk.BOTH, expand=True)
            self.listbox_filtro.bind("<<ListboxSelect>>", self.seleccionar_producto_filtro)

        self.listbox_filtro.delete(0, tk.END)
        for nombre in nombres:
            self.listbox_filtro.insert(tk.END, nombre)

    def seleccionar_producto_filtro(self, event):
        seleccion = self.listbox_filtro.curselection()
        if not seleccion:
            return
        nombre = self.listbox_filtro.get(seleccion[0])
        self.entry_producto.delete(0, tk.END)
        self.entry_producto.insert(0, nombre)
        self.toplevel_filtro.destroy()
        self.actualizar_precio(nombre)        

    def actualizar_precio(self,seleccion):
        precio = obtener_precio_producto(seleccion)
        self.entry_precio.configure(state="normal")
        self.entry_precio.delete(0,tk.END)
        if precio is not None and precio != 0:
            self.entry_precio.insert(0,f"{precio:,.0f}")
            self.entry_precio.configure(state="disabled")
        elif precio == 0:
            self.entry_precio.configure(state="normal")    
        else:
            self.entry_precio.insert(0,"Precio no disponible")
            self.entry_precio.configure(state="disabled")
          

    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            valor = self.tree.item(child,"values")[3] 
            subtotal = float(valor.replace(",",""))   
            total += subtotal
        self.suma_total.configure(text=f"Total a pagar: $ {total:,.0f}")   

    def registrar(self):
        self.btnagregar.configure(state="disabled")
        producto = self.entry_producto.get().strip()
        precio = self.entry_precio.get().strip()
        cantidad = self.entry_cantidad.get().strip()
       
        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)
                cantidad_en_carrito = 0
                for item in self.tree.get_children():
                    valores = self.tree.item(item, "values")
                    if valores[0] == producto:
                        cantidad_en_carrito += int(valores[2])
                if not hay_stock_suficiente(producto, cantidad + cantidad_en_carrito):
                    messagebox.showerror("Error", "Sin Stock", parent=self)
                    self.btnagregar.configure(state="normal")
                    return 
                precio = float(precio.replace(",",""))
                if precio == 0:
                    messagebox.showerror("Error","Debe ingresar un precio válido", parent=self)
                    self.btnagregar.configure(state="normal")
                    return
                total = cantidad * precio
                total = cantidad * precio                

                self.tree.insert("","end",values=(producto,f"{precio:,.0f}",cantidad,f"{total:,.0f}"))
                self.entry_producto.delete(0,tk.END)
                self.entry_precio.configure(state="normal")
                self.entry_precio.delete(0,tk.END)
                self.entry_precio.configure(state="disabled")
                self.entry_cantidad.delete(0,tk.END)
 
                self.actualizar_total()
            except ValueError:
                messagebox.showerror("Error","Cantidad o precio no validos", parent=self)
        else:
            messagebox.showerror("Error","Debe completar todos los campos", parent=self)    
        self.entry_pistola.focus_set()      
        self.btnagregar.configure(state="normal")

    def verificar_stock(self,nombre,cantidad):
        stock = obtener_stock_producto(nombre)
        if stock is not None and stock >= cantidad:
            return True
        return False

    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            valor = self.tree.item(child,"values")[3]
            subtotal = float(valor.replace(",",""))
            total += subtotal
        return total

    def abrir_pago(self):
        for child in self.tree.get_children():
            valores = self.tree.item(child, "values")
            nombre = valores[0]
            cantidad = int(valores[2])
            if not hay_stock_suficiente(nombre, cantidad):
                messagebox.showwarning("Sin stock", f"No hay stock suficiente de '{nombre}'. Verifique antes de pagar.", parent=self)
                return
        Pago(self)

    def abrir_venta_diaria(self):
        VentaDiaria(self)    

    def leer_codigo_barras(self, event=None):
        codigo = self.entry_pistola.get().strip()
        self.entry_pistola.delete(0, tk.END)
        if not codigo:
            return

        resultado = buscar_producto_por_codigo(codigo)
        if not resultado:
            return

        nombre, precio = resultado

        encontrado = False
        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            if valores[0] == nombre:
                cantidad_actual = int(valores[2])
                nueva_cantidad = cantidad_actual + 1
                nuevo_total = nueva_cantidad * precio
                self.tree.item(item, values=(nombre, f"{precio:,.0f}", nueva_cantidad, f"{nuevo_total:,.0f}"))
                encontrado = True
                break

        if not encontrado:
            self.tree.insert("", "end", values=(nombre, f"{precio:,.0f}", 1, f"{precio:,.0f}"))

        self.actualizar_total()

  

        
    #/////////////////////////////////////////////////////////////////////////////////////////////////////      