import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from ttkthemes import ThemedStyle
from database.decoraciones_db import guardar_decoracion, obtener_productos_para_decoracion, obtener_costo_por_id
from database.inventario_db import buscar_productos_completos_por_nombre


COLOR_FONDO = "#F1F5F9"
COLOR_TITULO = "#1E6091"
COLOR_TEXTO  = "#6B7280"
COLOR_BOTON1 = "#2563EB"
COLOR_HOVER1 = "#1D4ED8"
COLOR_BOTON2 = "#2D8A56"            
COLOR_HOVER2 = "#246E44" 
COLOR_SECUNDARIO = "#E8ECEF" 


class Decoraciones(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.widgets()

    def widgets(self):  
        # FRAME TITULO   SE NECESITA EL FRAME 1 PARA QUE TAPE EL PEDAZO DE FONOD QEU VIEN DEL CONTAINER
        frame1 = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=0)
        frame1.place(x=0,y=0,width=740,height=70)      

        # CAPA QEU CONTINEE EL TITULO
        titulo = tk.Label(self,text="Asignar codigos de barra",bg=COLOR_FONDO,fg=COLOR_TITULO,font="sans 30 bold",anchor="w")
        titulo.place(x=20,y=10,width=740,height=60)

        # FRAME TODA LA VENTANTA
        frame2 = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=1)
        frame2.place(x=0,y=63,width=740,height=737)  

        
        lblproducto = tk.Label(frame2,text="Buscar producto:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lblproducto.place(x=30,y=38)
        self.entry_producto = ctk.CTkEntry(frame2,font=("sans",16,"bold"),corner_radius=10,width=300,height=38)
        self.entry_producto.place(x=30,y=68)
        self.entry_producto.bind("<KeyRelease>", self.filtrar)

        lbldecoracion = tk.Label(frame2,text="Nombre decoracion:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lbldecoracion.place(x=30,y=130)
        self.entry_decoracio = ctk.CTkEntry(frame2,font=("sans",16,"bold"),corner_radius=10,width=300,height=38)
        self.entry_decoracio.place(x=30,y=160)

        lblprecio = tk.Label(frame2,text="Precio para venta:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lblprecio.place(x=400,y=130)
        self.entry_precio = ctk.CTkEntry(frame2,font=("sans",16,"bold"),corner_radius=10,width=300,height=38)
        self.entry_precio.place(x=400,y=160)

        lbltreeview1 = tk.Label(frame2,text="Seleccion productos",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lbltreeview1.place(x=30,y=220)

        lblcantidad = tk.Label(frame2,text="Cantidad:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lblcantidad.place(x=545,y=270)
        self.entry_cantidad= ctk.CTkEntry(frame2,font=("sans",16,"bold"),corner_radius=10,width=140,height=38)
        self.entry_cantidad.place(x=545,y=300)
        
        self.btnagregar = ctk.CTkButton(frame2,text="Agregar",fg_color=COLOR_BOTON1,hover_color=COLOR_HOVER1,
            font=("sans",18,"bold"),corner_radius=10,width=100,height=43,command=self.agregar_producto)
        self.btnagregar.place(x=545,y=350)

        self.btnguardar = ctk.CTkButton(frame2,text="Guardar dec",fg_color=COLOR_BOTON2,hover_color=COLOR_HOVER2,
                font=("sans",18,"bold"),corner_radius=10,width=100,height=43,command=self.guardar_decoracion_click)
        self.btnguardar.place(x=545,y=545)
        

        # TREEVIEW
        treeframe = tk.Frame(frame2,bg=COLOR_SECUNDARIO)           
        treeframe.place(x=25,y=250,width=500,height=200) 

        # BLOQUE SCROLLBAR ////////////////////////////////
        scrol_y = ttk.Scrollbar(treeframe,orient=tk.VERTICAL)
        scrol_y.pack(side=tk.RIGHT,fill=tk.Y)

        scrol_x = ttk.Scrollbar(treeframe,orient=tk.HORIZONTAL)
        scrol_x.pack(side=tk.BOTTOM,fill=tk.X) 

        # TREEVIEW CREACION CAMPOS////////////////////////////// 
        style = ttk.Style(self)
        style.configure("Treeview", font=("sans", 14), rowheight=25)
        style.configure("Treeview.Heading", font=("sans", 13))        

        self.tree1 = ttk.Treeview(treeframe,yscrollcommand=scrol_y.set,xscrollcommand=scrol_x.set,height=40,
            columns=("ID","PRODUCTO","STOCK","PRECIO"),
            show = "headings")
        
        scrol_y.config(command=self.tree1.yview)
        scrol_x.config(command=self.tree1.xview)  

        self.tree1.heading("ID",text="Id")
        self.tree1.heading("PRODUCTO",text="Producto")
        self.tree1.heading("STOCK",text="Stock")
        self.tree1.heading("PRECIO",text="Precio")

        self.tree1.column("ID", width=0, stretch=False)
        self.tree1.column("PRODUCTO", width=200, anchor="w")
        self.tree1.column("STOCK", width=80, anchor="center")
        self.tree1.column("PRECIO", width=100, anchor="e")

        self.tree1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        lbltreeview2 = tk.Label(frame2,text="Productos agregados",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lbltreeview2.place(x=30,y=470)

        # TREEVIEW 2
        treeframe = tk.Frame(frame2,bg=COLOR_SECUNDARIO)           
        treeframe.place(x=25,y=500,width=500,height=150) 

        # BLOQUE SCROLLBAR ////////////////////////////////
        scrol_y = ttk.Scrollbar(treeframe,orient=tk.VERTICAL)
        scrol_y.pack(side=tk.RIGHT,fill=tk.Y)

        scrol_x = ttk.Scrollbar(treeframe,orient=tk.HORIZONTAL)
        scrol_x.pack(side=tk.BOTTOM,fill=tk.X) 

        # TREEVIEW CREACION CAMPOS////////////////////////////// 
        style = ttk.Style(self)
        style.configure("Treeview", font=("sans", 14), rowheight=25)
        style.configure("Treeview.Heading", font=("sans", 13))        

        self.tree2 = ttk.Treeview(treeframe,yscrollcommand=scrol_y.set,xscrollcommand=scrol_x.set,height=40,
            columns=("ID","PRODUCTO","STOCK","PRECIO"),
            show = "headings")
        
        scrol_y.config(command=self.tree2.yview)
        scrol_x.config(command=self.tree2.xview) 

        self.tree2.heading("ID",text="Id")
        self.tree2.heading("PRODUCTO",text="Producto")
        self.tree2.heading("STOCK",text="Stock")
        self.tree2.heading("PRECIO",text="Precio")

        self.tree2.column("ID", width=0, stretch=False)
        self.tree2.column("PRODUCTO", width=200, anchor="w")
        self.tree2.column("STOCK", width=80, anchor="center")
        self.tree2.column("PRECIO", width=100, anchor="e")

        self.tree2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lblprecio_bruto = tk.Label(frame2,text="Precio bruto: $ 0",bg=COLOR_FONDO,font="sans 14 bold")
        self.lblprecio_bruto.place(x=30,y=650)

        self.lblcosto = tk.Label(frame2,text="Costo total: $ 0",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        self.lblcosto.place(x=30,y=680)
        
        self.mostrar()

    def mostrar(self):
        for item in self.tree1.get_children():
            self.tree1.delete(item)
        productos = obtener_productos_para_decoracion()
        for producto in productos:
            precio = f"{float(producto[3]):,.0f}" if producto[3] else ""
            self.tree1.insert("", "end", values=(
                producto[0], producto[1], producto[2], precio
            ))    

    def filtrar(self, event=None):
        texto = self.entry_producto.get().strip()
        for item in self.tree1.get_children():
            self.tree1.delete(item)
        if not texto:
            self.mostrar()
            return
        productos = buscar_productos_completos_por_nombre(texto)
        for producto in productos:
            precio = f"{float(producto[3]):,.0f}" if producto[3] else ""
            self.tree1.insert("", "end", values=(
                producto[0], producto[1], producto[5], precio
            ))        

    def agregar_producto(self):
        seleccion = self.tree1.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto.", parent=self)
            return
        try:
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.", parent=self)
            return
        valores = self.tree1.item(seleccion[0])["values"]
        id_producto = valores[0]
        nombre = valores[1]
        stock = valores[2]
        precio = valores[3]
        if cantidad > int(stock):
            messagebox.showerror("Error", "Cantidad supera stock disponible.", parent=self)
            return
        for item in self.tree2.get_children():
            vals = self.tree2.item(item)["values"]
            if str(vals[0]) == str(id_producto):
                nueva_cant = int(vals[2]) + cantidad
                self.tree2.item(item, values=(id_producto, nombre, nueva_cant, precio))
                self.actualizar_totales()
                self.entry_cantidad.delete(0, "end")
                return
        self.tree2.insert("", "end", values=(id_producto, nombre, cantidad, precio))
        self.actualizar_totales()
        self.entry_cantidad.delete(0, "end")   

    def actualizar_totales(self):
        precio_bruto = 0
        costo_total = 0
        for item in self.tree2.get_children():
            vals = self.tree2.item(item)["values"]
            id_producto = vals[0]
            precio_unitario = float(str(vals[3]).replace(",", ""))
            cantidad = int(vals[2])
            precio_bruto += precio_unitario * cantidad
            costo_unitario = obtener_costo_por_id(id_producto)
            if costo_unitario:
                costo_total += float(costo_unitario) * cantidad
        self.lblprecio_bruto.config(text=f"Precio bruto: $ {precio_bruto:,.0f}")
        self.lblcosto.config(text=f"Costo total: $ {costo_total:,.0f}")        

    def guardar_decoracion_click(self):
        nombre = self.entry_decoracio.get().strip()
        precio = self.entry_precio.get().strip()
        if not nombre or not precio:
            messagebox.showwarning("Guardar", "Complete el nombre y el precio.", parent=self)
            return
        if not self.tree2.get_children():
            messagebox.showwarning("Guardar", "Agregue al menos un producto.", parent=self)
            return
        try:
            precio = float(precio.replace(",", ""))
        except ValueError:
            messagebox.showerror("Guardar", "Precio inválido.", parent=self)
            return

        componentes = []
        for item in self.tree2.get_children():
            vals = self.tree2.item(item)["values"]
            id_componente = int(vals[0])
            cantidad = int(vals[2])
            componentes.append((id_componente, cantidad))

        costo_total = 0
        for id_comp, cant in componentes:
            costo_unitario = obtener_costo_por_id(id_comp)
            if costo_unitario:
                costo_total += float(costo_unitario) * cant

        id_decoracion = guardar_decoracion(nombre, precio, costo_total, componentes)
        if id_decoracion:
            messagebox.showinfo("Éxito", "Decoración guardada correctamente.", parent=self)
        else:
            messagebox.showerror("Error", "No se pudo guardar la decoración.", parent=self)     

