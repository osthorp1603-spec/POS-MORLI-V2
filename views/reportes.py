import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from ttkthemes import ThemedStyle
from tkcalendar import DateEntry
from datetime import datetime
from database.inventario_db import obtener_proveedores,obtener_tipos_producto
from database.reportes_db import obtener_ventas_reporte,obtener_totales_reporte

COLOR_FONDO = "#F1F5F9"
COLOR_TARJETA = "#ffffff"
COLOR_TITULO = "#1E6091"
COLOR_TEXTO  = "#6B7280"
COLOR_VARIOS = "#2563EB"
COLOR_HOVER = "#1D4ED8"
COLOR_SECUNDARIO = "#E8ECEF" 
COLOR_SECUNDARIO_HOVER = "#D4DCDE"
COLOR_TEXTO_BTN = "#1F2937"

class Reportes(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.widgets()

    def widgets(self):  
        # FRAME TITULO   SE NECESITA EL FRAME 1 PARA QUE TAPE EL PEDAZO DE FONOD QEU VIEN DEL CONTAINER
        frame1 = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=0)
        frame1.place(x=0,y=0,width=1273,height=80)  

        # CAPA QEU CONTINEE EL TITULO
        titulo = tk.Label(self,text="Reporte de ventas",bg=COLOR_FONDO,fg=COLOR_TITULO,font="sans 30 bold",anchor="w")
        titulo.place(x=20,y=10,width=1275,height=70)

        # FRAME TODA LA VENTANTA
        frame2 = tk.Frame(self,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=1)
        frame2.place(x=0,y=71,width=1275,height=748)    

        lblproveedor = tk.Label(frame2,text="Proveedor:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lblproveedor.place(x=420,y=46)
        self.combo_proveedor = ctk.CTkComboBox(frame2,font=("sans",16,"bold"),corner_radius=10,width=220,height=38)
        self.combo_proveedor.place(x=420,y=80)
        self.combo_proveedor.bind("<KeyRelease>", self.filtrar_combo_proveedor)

        lblproducto = tk.Label(frame2,text="Tipo de producto:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lblproducto.place(x=702,y=46)
        self.combo_producto = ctk.CTkComboBox(frame2,font=("sans",16,"bold"),corner_radius=10,width=220,height=38)
        self.combo_producto.place(x=702,y=80)
        self.combo_producto.bind("<KeyRelease>", self.filtrar_combo_producto)

        lbldesde = tk.Label(frame2,text="Desde:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lbldesde.place(x=18,y=46) 
        self.date_desde = DateEntry(frame2,font=("sans",18,"bold"),width=8, background="#C6D9E3", 
                                    foreground="white", borderwidth=1)
        self.date_desde.place(x=18,y=80)

        lblhasta = tk.Label(frame2,text="Hasta:",bg=COLOR_FONDO,fg=COLOR_TEXTO,font="sans 13 bold")
        lblhasta.place(x=200,y=46)
        self.date_hasta = DateEntry(frame2,font=("sans",18,"bold"),width=8, background="#C6D9E3", 
                                            foreground="white", borderwidth=1)
        self.date_hasta.place(x=200,y=80)

        self.btnfiltrar = ctk.CTkButton(frame2,text="Filtrar",fg_color=COLOR_VARIOS,hover_color=COLOR_HOVER,
            font=("sans",18,"bold"),corner_radius=10,width=100,height=43,command=self.cargar_treeview )
        self.btnfiltrar.place(x=960,y=80)

        
        self.btnmostrar = ctk.CTkButton(frame2,text="Mostra Todo",fg_color=COLOR_SECUNDARIO,hover_color=COLOR_SECUNDARIO_HOVER,
            text_color=COLOR_TEXTO_BTN,font=("sans",18,"bold"),corner_radius=10,width=100,height=43,command=self.mostrar_todo )
        self.btnmostrar.place(x=1100,y=80)

        # TREEVIEW
        treeframe = tk.Frame(frame2,bg=COLOR_SECUNDARIO)           
        treeframe.place(x=20,y=140,width=1240,height=400) 

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
            columns=("ID", "FACTURA","FECHA","PRODUCTO","TIPO","PROVEEDOR","CANTIDAD","PRECIO","TOTAL","GANANCIA","TIPO PAGO"),
            show = "headings")
        
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)  

        self.tree.heading("ID",text="Id")
        self.tree.heading("FACTURA",text="Factura")
        self.tree.heading("FECHA",text="Fecha")
        self.tree.heading("PRODUCTO",text="Producto")
        self.tree.heading("TIPO",text="Tipo")
        self.tree.heading("PROVEEDOR",text="Proveedor")
        self.tree.heading("CANTIDAD",text="Cantidad")
        self.tree.heading("PRECIO",text="Precio")
        self.tree.heading("TOTAL",text="Total")
        self.tree.heading("GANANCIA",text="Ganancia")
        self.tree.heading("TIPO PAGO",text="Tipo Pago")

        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("FACTURA", width=80, anchor="center")
        self.tree.column("FECHA", width=150, anchor="center")
        self.tree.column("PRODUCTO", width=290, anchor="w")
        self.tree.column("TIPO", width=110, anchor="w")
        self.tree.column("PROVEEDOR", width=140, anchor="w")
        self.tree.column("CANTIDAD", width=70, anchor="center")
        self.tree.column("PRECIO", width=100, anchor="e")
        self.tree.column("TOTAL", width=100, anchor="e")
        self.tree.column("GANANCIA", width=100, anchor="e")
        self.tree.column("TIPO PAGO", width=100, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # FRAMES INFERIORES

        # BLOQUE TOTAL VENTAS //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                border_color="#E5E7EB",border_width=2)
        lblframe.place(x=20,y=580)

        titulo_info = ctk.CTkLabel(lblframe,text="Cantidad total \n vendida:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info.place(x=35,y=15)
        self.total_ventas = ctk.CTkLabel(lblframe,text="0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_ventas.place(relx=0.5,y=75,anchor="center")
    
        # BLOQUE TOTAL EFECTIVO //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                        border_color="#E5E7EB",border_width=2)
        lblframe.place(x=225,y=580)

        titulo_info1 = ctk.CTkLabel(lblframe,text="Efectivo:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info1.place(x=60,y=15)
        self.total_efectivo = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_efectivo.place(relx=0.5,y=75,anchor="center")

        # BLOQUE TOTAL QR //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                                border_color="#E5E7EB",border_width=2)
        lblframe.place(x=430,y=580)

        titulo_info2 = ctk.CTkLabel(lblframe,text="QR:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info2.place(x=75,y=15)
        self.total_qr = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_qr.place(relx=0.5,y=75,anchor="center")

        # BLOQUE TOTAL TARJETA //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                                border_color="#E5E7EB",border_width=2)
        lblframe.place(x=635,y=580)

        titulo_info3 = ctk.CTkLabel(lblframe,text="Tarjeta:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info3.place(x=60,y=15)
        self.total_tarjeta = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_tarjeta.place(relx=0.5,y=75,anchor="center")

        # BLOQUE TOTAL VENDIDO //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                        border_color="#E5E7EB",border_width=2)
        lblframe.place(x=840,y=580)

        titulo_info4 = ctk.CTkLabel(lblframe,text="Total Vendido:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info4.place(x=40,y=15)
        self.total_total_vendido = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_total_vendido.place(relx=0.5,y=75,anchor="center")

        # BLOQUE TOTAL VENDIDO //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                        border_color="#E5E7EB",border_width=2)
        lblframe.place(x=1045,y=580)

        titulo_info5 = ctk.CTkLabel(lblframe,text="Ganancia:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info5.place(x=50,y=15)
        self.total_venta_neta = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_VARIOS)
        self.total_venta_neta.place(relx=0.5,y=75,anchor="center")   
        
        self.cargar_combos()  
     

    def cargar_combos(self):
        proveedores = obtener_proveedores()
        lista_proveedores = []
        for p in proveedores:
            lista_proveedores.append(p[0])
        self.combo_proveedor.configure(values=lista_proveedores)
        self.combo_proveedor.set("")

        tipos = obtener_tipos_producto()
        lista_tipos = []
        for t in tipos:
            lista_tipos.append(t[0])
        self.combo_producto.configure(values=lista_tipos)
        self.combo_producto.set("") 

    def cargar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        proveedor = self.combo_proveedor.get().strip()
        tipo_producto = self.combo_producto.get().strip()
        fecha_desde = self.date_desde.get_date().strftime("%Y-%m-%d")
        fecha_hasta = self.date_hasta.get_date().strftime("%Y-%m-%d")

        ventas = obtener_ventas_reporte(proveedor, tipo_producto, fecha_desde, fecha_hasta)

        for venta in ventas:
            id_detalle = venta[0]
            factura = venta[1]
            fecha = venta[2]
            producto = venta[3]
            tipo = venta[4] if venta[4] else "-"
            proveedor_v = venta[5] if venta[5] else "-"
            cantidad = venta[6]
            precio = f"{venta[7]:,.0f}"
            total = f"{venta[8]:,.0f}"
            ganancia = f"{venta[9]:,.0f}" if venta[9] is not None else "0"
            tipo_pago = self.calcular_tipo_pago(venta[10], venta[11], venta[12])

            self.tree.insert("", "end", values=(
                id_detalle, factura, fecha, producto, tipo, proveedor_v,
                cantidad, precio, total, ganancia, tipo_pago
            ))

        totales = obtener_totales_reporte(proveedor, tipo_producto, fecha_desde, fecha_hasta)

        self.total_ventas.configure(text=f"{totales['cantidad_total']}")
        self.total_efectivo.configure(text=f"$ {totales['efectivo']:,.0f}")
        self.total_qr.configure(text=f"$ {totales['qr']:,.0f}")
        self.total_tarjeta.configure(text=f"$ {totales['tarjeta']:,.0f}")
        self.total_total_vendido.configure(text=f"$ {totales['total_vendido']:,.0f}")
        
        self.total_venta_neta.configure(text=f"$ {totales['ganancia_total']:,.0f}")
            
    def calcular_tipo_pago(self, pago_efectivo, pago_qr, pago_tarjeta):
        metodos = []
        if pago_efectivo > 0:
            metodos.append("Efectivo")
        if pago_qr > 0:
            metodos.append("QR")
        if pago_tarjeta > 0:
            metodos.append("Tarjeta")
        return "/".join(metodos)
    
    def mostrar_todo(self):
        self.combo_proveedor.set("")
        self.combo_producto.set("")
        self.cargar_treeview()

    def filtrar_combo_proveedor(self, event):
        if event.keysym in ["Up", "Down", "Return", "Left", "Right", "Tab"]:
            return
        texto = self.combo_proveedor.get().strip()
        if not texto:
            return
        proveedores = obtener_proveedores()
        coincidencias = [p[0] for p in proveedores if texto.lower() in p[0].lower()]
        self.abrir_listbox_filtro(coincidencias, self.combo_proveedor)

    def filtrar_combo_producto(self, event):
        if event.keysym in ["Up", "Down", "Return", "Left", "Right", "Tab"]:
            return
        texto = self.combo_producto.get().strip()
        if not texto:
            return
        tipos = obtener_tipos_producto()
        coincidencias = [t[0] for t in tipos if texto.lower() in t[0].lower()]
        self.abrir_listbox_filtro(coincidencias, self.combo_producto)    

    def abrir_listbox_filtro(self, coincidencias, combo_destino):
        if hasattr(self, "toplevel_filtro") and self.toplevel_filtro.winfo_exists():
            self.toplevel_filtro.destroy()

        if not coincidencias:
            return

        self.toplevel_filtro = tk.Toplevel(self)
        self.toplevel_filtro.title("Filtrar")
        x = combo_destino.winfo_rootx()
        y = combo_destino.winfo_rooty() + combo_destino.winfo_height()
        self.toplevel_filtro.geometry(f"250x200+{x}+{y}")
        self.toplevel_filtro.transient(self)
        self.toplevel_filtro.resizable(False, False)

        self.listbox_filtro = tk.Listbox(self.toplevel_filtro, font="sans 12")
        self.listbox_filtro.pack(fill=tk.BOTH, expand=True)

        for c in coincidencias:
            self.listbox_filtro.insert(tk.END, c)

        self.listbox_filtro.bind("<Return>", lambda e: self.seleccionar_filtro(combo_destino))
        self.listbox_filtro.bind("<Button-1>", lambda e: self.seleccionar_filtro(combo_destino))
        combo_destino.focus_set()    

    def seleccionar_filtro(self, combo_destino):
        seleccion = self.listbox_filtro.curselection()
        if not seleccion:
            return
        valor = self.listbox_filtro.get(seleccion[0])
        combo_destino.set(valor)
        self.toplevel_filtro.destroy()
   