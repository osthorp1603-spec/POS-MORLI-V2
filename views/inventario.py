import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from ttkthemes import ThemedStyle  # ttktheme para el treeview
from database.inventario_db import (
    obtener_todos_los_productos,insertar_producto,eliminar_producto_por_id,actualizar_producto,
    buscar_productos_completos_por_nombre,buscar_producto_por_codigo,verificar_codigo_duplicado,
    actualizar_codigo_barras,actualizar_umbral_producto)

COLOR_FONDO = "#c6d9e3"            # fondo general de la ventana
COLOR_TARJETA = "#ECF2F6"          # fondo del panel lateral (Datos del producto)
COLOR_TABLA_FONDO = "#ECF2F6"      # fondo de la tabla y de los inputs
COLOR_TITULO = "#1E6091"           # azul del texto "INVENTARIOS"
COLOR_INGRESAR = "#2D8A56"         # verde, botón "Ingresar"
COLOR_INGRESAR_HOVER = "#246E44"
COLOR_SECUNDARIO = "#D1D5DB"       # gris, botones "Editar", "Actualizar Inventario", "Actualizar Min"
COLOR_SECUNDARIO_HOVER = "#9CA3AF"
COLOR_ELIMINAR = "#A32D2D"         # rojo vino, botón "Eliminar"
COLOR_ELIMINAR_HOVER = "#7A2222"

class Inventario(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.widgets()
    
    def widgets(self): 
    # FRAME DEL ENCABEZADO    --- EN VNTAS S EJDA LO QUE HABIA AQEUI PERO NO ES NECASRI ES SOLO PAR RECORDAR                            
        titulo = tk.Label(self,text="INVENTARIOS",bg=COLOR_FONDO,fg=COLOR_TITULO,font="sans 30 bold",anchor="center")
        titulo.place(x=5,y=5,width=1265,height=70)

    # FRAME DE LA VENTANA INVENTARIO //////////
        frame2 = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=1)
        frame2.place(x=0,y=80,width=1273,height=729)

    # FRAME LABEL LATERAL    
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=290,height=710)
        lblframe.place(x=20,y=10)
        titulo_info = ctk.CTkLabel(lblframe,text="Datos del producto",font=("sans",22,"bold"))
        titulo_info.place(x=20,y=1)

    # LABELS DE ETIQUETAS 

        lblnombre = tk.Label(lblframe,text="Nombre:",font=("sans",13,"bold"),bg=COLOR_TARJETA)
        lblnombre.place(x=20,y=48)
        self.entry_nombre = ctk.CTkEntry(lblframe,font=("sans",18,"bold"),corner_radius=10,width=240,height=39)
        self.entry_nombre.place(x=20,y=75)

        lblproveedor = tk.Label(lblframe,text="Proveedor:",font=("sans",13,"bold"),bg=COLOR_TARJETA)
        lblproveedor.place(x=20,y=125)
        self.entry_proveedor = ctk.CTkEntry(lblframe,font=("sans",18,"bold"),corner_radius=10,width=240,height=39)
        self.entry_proveedor.place(x=20,y=152)

        lblprecio = tk.Label(lblframe,text="Precio:",font=("sans",13,"bold"),bg=COLOR_TARJETA)
        lblprecio.place(x=20,y=202)
        self.entry_precio = ctk.CTkEntry(lblframe,font=("sans",18,"bold"),corner_radius=10,width=240,height=39)
        self.entry_precio.place(x=20,y=229)

        lblcosto = tk.Label(lblframe,text="Costo:",font=("sans",13,"bold"),bg=COLOR_TARJETA)
        lblcosto.place(x=20,y=279)
        self.entry_costo = ctk.CTkEntry(lblframe,font=("sans",18,"bold"),corner_radius=10,width=240,height=39)
        self.entry_costo.place(x=20,y=306)

        lblstock = tk.Label(lblframe,text="Stock:",font=("sans",13,"bold"),bg=COLOR_TARJETA)
        lblstock.place(x=20,y=356)
        self.entry_stock = ctk.CTkEntry(lblframe,font=("sans",18,"bold"),corner_radius=10,width=240,height=39)
        self.entry_stock.place(x=20,y=383)

        lbltipo = tk.Label(lblframe,text="Tipo Producto:",font=("sans",13,"bold"),bg=COLOR_TARJETA)
        lbltipo.place(x=20,y=433)
        self.entry_tipo = ctk.CTkEntry(lblframe,font=("sans",18,"bold"),corner_radius=10,width=240,height=39)
        self.entry_tipo.place(x=20,y=460)

    # BOTONES FRAME LATERAL

        btningresar = ctk.CTkButton(lblframe,text="Ingresar",fg_color=COLOR_INGRESAR,text_color="white",
            font=("sans",16,"bold"),corner_radius=10,width=240,height=45,hover_color=COLOR_INGRESAR_HOVER,command=self.ingresar_producto)
        btningresar.place(x=20,y=525)

        btneditar = ctk.CTkButton(lblframe,text="Editar",fg_color=COLOR_SECUNDARIO,text_color="#1F2937",
            font=("sans",16,"bold"),corner_radius=10,width=240,height=45,hover_color=COLOR_SECUNDARIO_HOVER,command=self.editar_producto)
        btneditar.place(x=20,y=590)

        btneliminar = ctk.CTkButton(lblframe,text="Eliminar",fg_color=COLOR_ELIMINAR,text_color="white",
            font=("sans",16,"bold"),corner_radius=10,width=240,height=45,hover_color=COLOR_ELIMINAR_HOVER,command=self.eliminar_producto)
        btneliminar.place(x=20,y=655 )   

    # LABEL BUSCAR PDORUCTO - ASIGNAR CODIGO - MINIMO
        
        frame3 = ctk.CTkFrame(frame2, fg_color=COLOR_TABLA_FONDO, corner_radius=10, width=930, height=87)
        frame3.place(x=330, y=10)

    # BUSCAR PRODUCTO 
        lblbuscar = tk.Label(frame3, text="Buscar Producto:", font=("sans", 14, "bold"), bg=COLOR_TABLA_FONDO)
        lblbuscar.place(x=15, y=10)

        self.entry_buscar = ctk.CTkEntry(frame3, font=("sans", 19, "bold"), corner_radius=10, width=250, height=40)
        self.entry_buscar.place(x=15, y=40)
        self.entry_buscar.bind("<KeyRelease>", self.filtrar)

        btnlimpiar = ctk.CTkButton(frame3, text="Limpiar", font=("sans", 14, "bold"),
                                    fg_color=COLOR_SECUNDARIO, text_color="#1F2937",
                                    hover_color=COLOR_SECUNDARIO_HOVER,
                                    corner_radius=10, width=60, height=34,
                                    command=self.limpiar_busqueda)
        btnlimpiar.place(x=276, y=40)        

    # ASIGNAR CODIGO 
        lblcodigo = tk.Label(frame3, text="Asignar Código:", font=("sans", 14, "bold"), bg=COLOR_TABLA_FONDO)
        lblcodigo.place(x=390, y=10)

        self.entry_codigo = ctk.CTkEntry(frame3, font=("sans", 19, "bold"), corner_radius=10, width=170, height=40)
        self.entry_codigo.place(x=390, y=40)   

        btnguardar = ctk.CTkButton(frame3, text="Guardar", font=("sans", 14, "bold"),
                                    fg_color=COLOR_SECUNDARIO, text_color="#1F2937",
                                    hover_color=COLOR_SECUNDARIO_HOVER,
                                    corner_radius=10, width=60, height=34,
                                    command=self.guardar_codigo_barras)
        btnguardar.place(x=570, y=40)         

    #  EDICION MINIMOS
        lblumbral = tk.Label(frame3, text="Editar Min:", font=("sans", 14, "bold"), bg=COLOR_TABLA_FONDO)
        lblumbral.place(x=730, y=10)

        self.entry_umbral = ctk.CTkEntry(frame3, font=("sans", 19, "bold"), corner_radius=10, width=58, height=40)
        self.entry_umbral.place(x=740, y=40)

        btnumbral = ctk.CTkButton(frame3, text="Aplicar", font=("sans", 14, "bold"),
                                fg_color=COLOR_SECUNDARIO, text_color="#1F2937",
                                hover_color=COLOR_SECUNDARIO_HOVER,
                                corner_radius=10, width=60, height=34,
                                command=self.actualizar_umbral)
        btnumbral.place(x=810, y=40)            
        
    # TREEVIEW VENTANA
        treframe = tk.Frame(frame2,bg=COLOR_TABLA_FONDO)
        treframe.place(x=345,y=117, width=915,height=600) 

    # BLOQUE SCROLLBAR ////////////////////////////////
        scrol_y = ttk.Scrollbar(treframe,orient=tk.VERTICAL)
        scrol_y.pack(side=tk.RIGHT,fill=tk.Y)

        scrol_x = ttk.Scrollbar(treframe,orient=tk.HORIZONTAL)
        scrol_x.pack(side=tk.BOTTOM,fill=tk.X)   

    # TREEVIEW CREACION CAMPOS////////////////////////////// 
        style = ThemedStyle(self)
        style.set_theme("vista")    
        style.configure("Treeview", font=("sans", 14), rowheight=28)
        style.configure("Treeview.Heading", font=("sans", 14)) 

        self.tre = ttk.Treeview(treframe,yscrollcommand=scrol_y.set,xscrollcommand=scrol_x.set,height=40,
            columns=("ID", "PRODUCTO","PROVEEDOR","PRECIO","COSTO","STOCK", "TIPO PRODUCTO","CODIGO BARRAS","UMBRAL STOCK"),
            show = "headings")

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)  

        self.tre.heading("ID",text="Id")
        self.tre.heading("PRODUCTO",text="Producto")
        self.tre.heading("PROVEEDOR",text="Proveedor")
        self.tre.heading("PRECIO",text="Precio")
        self.tre.heading("COSTO",text="Costo")
        self.tre.heading("STOCK",text="Stock")
        self.tre.heading("TIPO PRODUCTO",text="Tipo producto")
        self.tre.heading("CODIGO BARRAS",text="Cod barras")
        self.tre.heading("UMBRAL STOCK",text="Umbral stock")

        self.tre.column("ID", width=0, stretch=False)
        self.tre.column("PRODUCTO", width=220, anchor="w")
        self.tre.column("PROVEEDOR", width=120, anchor="w")
        self.tre.column("PRECIO", width=100, anchor="e")
        self.tre.column("COSTO", width=100, anchor="e")
        self.tre.column("STOCK", width=70, anchor="center")
        self.tre.column("TIPO PRODUCTO", width=120, anchor="w")
        self.tre.column("CODIGO BARRAS", width=110, anchor="center")
        self.tre.column("UMBRAL STOCK", width=70, anchor="center")
                
        self.tre.pack(expand=True,fill=tk.BOTH)
        self.mostrar()

    # LECTOR PISTOLA 
      

 #("ID", "PRODUCTO","PROVEEDOR","PRECIO","COSTO","STOCK", "TIPO PRODUCTO","CODIGO BARRAS","UMBRAL STOCK")
    def mostrar(self):
        for item in self.tre.get_children():
            self.tre.delete(item)


        productos = obtener_todos_los_productos()
        for producto in productos:
            precio = f"{float(producto[3]):,.0f}" if producto[3] else ""  
            costo  = f"{float(producto[4]):,.0f}" if producto[4] else ""  
            codigo = producto[7] if producto[7] is not None else "-"
            umbral = producto[8] if producto[8] is not None else "-"
            self.tre.insert("","end",values=(
                producto[0],producto[1],producto[2],precio,costo,
                producto[5],producto[6],codigo,umbral              
            ))

    def ingresar_producto(self):
        nombre = self.entry_nombre.get().strip()
        proveedor = self.entry_proveedor.get().strip()
        precio = self.entry_precio.get().strip()
        costo = self.entry_costo.get().strip()
        stock = self.entry_stock.get().strip()
        tipo_producto = self.entry_tipo.get().strip()

        if not (nombre and proveedor and precio and costo and stock and tipo_producto):
            messagebox.showwarning("Error","Ningun campo debe estar vacio",parent=self)
            return
        try:
            float(precio)
            float(costo)
            int(stock)
        except ValueError:
            messagebox.showwarning("Error", "Precio, costo y stock deben ser números válidos",parent=self)
            return
        if insertar_producto(nombre, proveedor,float(precio),float(costo),int(stock),tipo_producto):
            self.mostrar()
            self.entry_nombre.delete(0, "end")
            self.entry_proveedor.delete(0, "end")
            self.entry_precio.delete(0, "end")
            self.entry_costo.delete(0, "end")
            self.entry_stock.delete(0, "end")
            self.entry_tipo.delete(0, "end")
        else:
            messagebox.showerror("Error", "No se pudo guardar el producto",parent=self)

    def eliminar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar producto", "Seleccione un producto para eliminar.",parent=self)
            return

        item_id = self.tre.item(seleccion)["values"][0]
        nombre_producto = self.tre.item(seleccion)["values"][1]

        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar '{nombre_producto}'?",parent=self)
        if not confirmacion:
            return

        if eliminar_producto_por_id(item_id):
            self.mostrar()
            messagebox.showinfo("Producto eliminado", f"El producto '{nombre_producto}' ha sido eliminado correctamente.",parent=self)
        else:
            messagebox.showerror("Error", "No se pudo eliminar el producto.",parent=self)        

    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar producto", "Seleccione un producto para editar.", parent=self)
            return

        item_values = self.tre.item(seleccion)["values"]

        ventana_editar = tk.Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("480x530")
        ventana_editar.config(bg=COLOR_FONDO)
        ventana_editar.resizable(False, False)

        # Nombre
        ctk.CTkLabel(ventana_editar, text="Nombre:", bg_color=COLOR_FONDO, font=("sans", 20, "bold")).place(x=20, y=20)
        entry_nombre = ctk.CTkEntry(ventana_editar, font=("sans", 19, "bold"), corner_radius=10, width=300, height=39)
        entry_nombre.place(x=130, y=20)
        entry_nombre.insert(0, item_values[1])

        # Proveedor
        ctk.CTkLabel(ventana_editar, text="Proveedor:", bg_color=COLOR_FONDO, font=("sans", 20, "bold")).place(x=20, y=90)
        entry_proveedor = ctk.CTkEntry(ventana_editar, font=("sans", 19, "bold"), corner_radius=8, width=300, height=39)
        entry_proveedor.place(x=130, y=90)
        entry_proveedor.insert(0, item_values[2])

        # Precio
        ctk.CTkLabel(ventana_editar, text="Precio:", bg_color=COLOR_FONDO, font=("sans", 20, "bold")).place(x=20, y=160)
        entry_precio = ctk.CTkEntry(ventana_editar, font=("sans", 19, "bold"), corner_radius=8, width=300, height=39)
        entry_precio.place(x=130, y=160)
        entry_precio.insert(0, str(item_values[3]).replace(",", ""))

        # Costo
        ctk.CTkLabel(ventana_editar, text="Costo:", bg_color=COLOR_FONDO, font=("sans", 20, "bold")).place(x=20, y=230)
        entry_costo = ctk.CTkEntry(ventana_editar, font=("sans", 19, "bold"), corner_radius=8, width=300, height=39)
        entry_costo.place(x=130, y=230)
        entry_costo.insert(0, str(item_values[4]).replace(",", ""))

        # Stock
        ctk.CTkLabel(ventana_editar, text="Stock:", bg_color=COLOR_FONDO, font=("sans", 20, "bold")).place(x=20, y=300)
        entry_stock = ctk.CTkEntry(ventana_editar, font=("sans", 19, "bold"), corner_radius=8, width=300, height=39)
        entry_stock.place(x=130, y=300)
        entry_stock.insert(0, item_values[5])

        # Tipo Producto
        ctk.CTkLabel(ventana_editar, text="Tipo Prod:", bg_color=COLOR_FONDO, font=("sans", 20, "bold")).place(x=20, y=370)
        entry_tipo = ctk.CTkEntry(ventana_editar, font=("sans", 19, "bold"), corner_radius=8, width=300, height=39)
        entry_tipo.place(x=130, y=370)
        entry_tipo.insert(0, item_values[6])    

        def guardar_cambios():
            nombre = entry_nombre.get().strip()
            proveedor = entry_proveedor.get().strip()
            precio = entry_precio.get().strip()
            costo = entry_costo.get().strip()
            stock = entry_stock.get().strip()
            tipo_producto = entry_tipo.get().strip()

            if not (nombre and proveedor and precio and costo and stock and tipo_producto):
                messagebox.showwarning("Guardar cambios", "Rellene todos los campos.", parent=ventana_editar)
                return

            try:
                precio = float(precio.replace(",", ""))
                costo = float(costo.replace(",", ""))
                stock = int(stock)
            except ValueError:
                messagebox.showwarning("Guardar cambios", "Precio, costo y stock deben ser números válidos.", parent=ventana_editar)
                return

            producto_id = item_values[0]
            if actualizar_producto(producto_id, nombre, proveedor, precio, costo, stock, tipo_producto):
                self.mostrar()
                ventana_editar.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto.", parent=ventana_editar)

        ctk.CTkButton(ventana_editar, text="Guardar cambios", font=("sans", 16, "bold"),
                    fg_color=COLOR_INGRESAR, hover_color=COLOR_INGRESAR_HOVER,
                    corner_radius=10, width=240, height=45,
                    command=guardar_cambios).place(x=120, y=450)

    def filtrar(self, event=None):
        texto = self.entry_buscar.get().strip()

        if event and event.keysym == "Return":
            resultado = buscar_producto_por_codigo(texto)
            if resultado:
                nombre, _ = resultado
                for item in self.tre.get_children():
                    self.tre.delete(item)
                for producto in buscar_productos_completos_por_nombre(nombre):
                    precio = f"{float(producto[3]):,.0f}" if producto[3] else ""
                    costo  = f"{float(producto[4]):,.0f}" if producto[4] else ""
                    codigo_tv = producto[7] if producto[7] is not None else "-"
                    umbral = producto[8] if producto[8] is not None else "-"
                    self.tre.insert("", "end", values=(
                        producto[0], producto[1], producto[2], precio, costo,
                        producto[5], producto[6], codigo_tv, umbral
                    ))
                self.entry_buscar.delete(0, tk.END)
            return

        for item in self.tre.get_children():
            self.tre.delete(item)

        if not texto:
            self.mostrar()
            return

        productos = buscar_productos_completos_por_nombre(texto)
        for producto in productos:
            precio = f"{float(producto[3]):,.0f}" if producto[3] else ""
            costo  = f"{float(producto[4]):,.0f}" if producto[4] else ""
            codigo = producto[7] if producto[7] is not None else "-"
            umbral = producto[8] if producto[8] is not None else "-"
            self.tre.insert("", "end", values=(
                producto[0], producto[1], producto[2], precio, costo,
                producto[5], producto[6], codigo, umbral
            ))
    
    def limpiar_busqueda(self):
        self.entry_buscar.delete(0, "end")
        self.mostrar()    

    def guardar_codigo_barras(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Asignar código", "Seleccione un producto para asignar el código.", parent=self)
            return

        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Asignar código", "Ingrese un código de barras válido.", parent=self)
            return

        producto_id = self.tre.item(seleccion)["values"][0]

        nombre_duplicado = verificar_codigo_duplicado(codigo, producto_id)
        if nombre_duplicado:
            messagebox.showwarning("Código existente", f"El código '{codigo}' ya está asignado al producto: '{nombre_duplicado}'.", parent=self)
            return

        if actualizar_codigo_barras(producto_id, codigo):
            self.entry_codigo.delete(0, "end")
            self.mostrar()
            messagebox.showinfo("Éxito", "Código de barras actualizado correctamente.", parent=self)
        else:
            messagebox.showerror("Error", "No se pudo actualizar el código.", parent=self)   

    def actualizar_umbral(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar Min", "Seleccione un producto para actualizar su umbral.", parent=self)
            return

        nuevo_umbral = self.entry_umbral.get().strip()
        if not nuevo_umbral.isdigit():
            messagebox.showwarning("Editar Min", "Ingrese un número válido para el umbral.", parent=self)
            return

        nuevo_umbral = int(nuevo_umbral)
        producto_id = self.tre.item(seleccion)["values"][0]

        if actualizar_umbral_producto(producto_id, nuevo_umbral):
            self.entry_umbral.delete(0, "end")
            self.mostrar()
            messagebox.showinfo("Éxito", "Umbral actualizado correctamente.", parent=self)
        else:
            messagebox.showerror("Error", "No se pudo actualizar el umbral.", parent=self)      