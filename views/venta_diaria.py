import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from datetime import datetime
from database.reportes_db import obtener_ventas_del_dia, obtener_totales_del_dia

COLOR_FONDO = "#F1F5F9"
COLOR_TARJETA = "#ffffff"
COLOR_TITULO = "#1E6091"
COLOR_TEXTO  = "#6B7280"
COLOR_VARIOS = "#2563EB"
COLOR_HOVER = "#1D4ED8"
COLOR_SECUNDARIO = "#E8ECEF" 
COLOR_SECUNDARIO_HOVER = "#D4DCDE"
COLOR_TEXTO_BTN = "#1F2937"

class VentaDiaria():
    def __init__(self, ventas):
        self.ventas = ventas
        self.abrir_ventana_diaria()
        

    def abrir_ventana_diaria(self):
        self.ventana_diaria = tk.Toplevel(self.ventas)
        self.ventana_diaria.title("Ventas diarias")
        self.ventana_diaria.geometry("1275x810+5+20")
        self.ventana_diaria.config(bg=COLOR_FONDO)
        self.ventana_diaria.resizable(False, False) 

        frame1 = tk.Frame(self.ventana_diaria,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=0)
        frame1.place(x=0,y=0,width=1275,height=80) 

        titulo = tk.Label(self.ventana_diaria,text="Venta diaria",bg=COLOR_FONDO,fg=COLOR_TITULO,font="sans 30 bold",anchor="w")
        titulo.place(x=20,y=10,width=1275,height=70) 

        frame2 = tk.Frame(self.ventana_diaria,bg=COLOR_FONDO,highlightbackground=COLOR_FONDO,highlightthickness=1)
        frame2.place(x=0,y=71,width=1275,height=748)  

        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        label_fecha = tk.Label(frame2, text=f"📅 Ventas del {fecha_actual}", font="sans 14 bold", bg=COLOR_FONDO, fg=COLOR_TEXTO)
        label_fecha.place(x=20, y=70)
        
        # TREEVIEW
        treeframe = tk.Frame(frame2,bg=COLOR_SECUNDARIO)           
        treeframe.place(x=20,y=140,width=1240,height=400) 

        # BLOQUE SCROLLBAR ////////////////////////////////
        scrol_y = ttk.Scrollbar(treeframe,orient=tk.VERTICAL)
        scrol_y.pack(side=tk.RIGHT,fill=tk.Y)

        scrol_x = ttk.Scrollbar(treeframe,orient=tk.HORIZONTAL)
        scrol_x.pack(side=tk.BOTTOM,fill=tk.X) 

        # TREEVIEW CREACION CAMPOS////////////////////////////// 
        style = ttk.Style(self.ventana_diaria)
        style.configure("Treeview", font=("sans", 14), rowheight=25)
        style.configure("Treeview.Heading", font=("sans", 13))
        
        self.tree = ttk.Treeview(treeframe,yscrollcommand=scrol_y.set,xscrollcommand=scrol_x.set,height=40,
            columns=("ID", "FACTURA","PRODUCTO","CANTIDAD","PRECIO","TOTAL","TIPO PAGO","GANANCIA",),
            show = "headings")  

        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)  

        self.tree.heading("ID",text="Id")
        self.tree.heading("FACTURA",text="Factura")
        self.tree.heading("PRODUCTO",text="Producto")
        self.tree.heading("CANTIDAD",text="Cantidad")
        self.tree.heading("PRECIO",text="Precio")
        self.tree.heading("TOTAL",text="Total")
        self.tree.heading("TIPO PAGO",text="Tipo Pago")
        self.tree.heading("GANANCIA",text="Ganancia")
        
        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("FACTURA", width=80, anchor="center")
        self.tree.column("PRODUCTO", width=250, anchor="w")
        self.tree.column("CANTIDAD", width=70, anchor="center")
        self.tree.column("PRECIO", width=100, anchor="e")
        self.tree.column("TOTAL", width=100, anchor="e")
        self.tree.column("TIPO PAGO", width=100, anchor="center")
        self.tree.column("GANANCIA", width=100, anchor="e")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        # FRAMES INFERIORES

        # BLOQUE TOTAL VENTAS //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                border_color="#E5E7EB",border_width=2)
        lblframe.place(x=100,y=580)

        titulo_info = ctk.CTkLabel(lblframe,text="Cantidad total \n vendida:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info.place(x=35,y=15)
        self.total_ventas = ctk.CTkLabel(lblframe,text="0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_ventas.place(relx=0.5,y=75,anchor="center")
    
        # BLOQUE TOTAL EFECTIVO //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                        border_color="#E5E7EB",border_width=2)
        lblframe.place(x=320,y=580)

        titulo_info1 = ctk.CTkLabel(lblframe,text="Efectivo:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info1.place(x=60,y=15)
        self.total_efectivo = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_efectivo.place(relx=0.5,y=75,anchor="center")

        # BLOQUE TOTAL QR //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                                border_color="#E5E7EB",border_width=2)
        lblframe.place(x=540,y=580)

        titulo_info2 = ctk.CTkLabel(lblframe,text="QR:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info2.place(x=75,y=15)
        self.total_qr = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_qr.place(relx=0.5,y=75,anchor="center")

        # BLOQUE TOTAL TARJETA //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                                border_color="#E5E7EB",border_width=2)
        lblframe.place(x=760,y=580)

        titulo_info3 = ctk.CTkLabel(lblframe,text="Tarjeta:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_TEXTO)
        titulo_info3.place(x=60,y=15)
        self.total_tarjeta = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_TEXTO_BTN)
        self.total_tarjeta.place(relx=0.5,y=75,anchor="center")

        # BLOQUE TOTAL VENDIDO //////////////////////////////////////////////////////
        lblframe = ctk.CTkFrame(frame2,fg_color=COLOR_TARJETA,corner_radius=10,width=170,height=130,
                                        border_color="#E5E7EB",border_width=2)
        lblframe.place(x=980,y=580)

        titulo_info4 = ctk.CTkLabel(lblframe,text="Total Vendido:",fg_color=COLOR_TARJETA,font=("sans",15,"bold"),text_color=COLOR_VARIOS)
        titulo_info4.place(x=40,y=15)
        self.total_total_vendido = ctk.CTkLabel(lblframe,text="$ 0",font=("sans",20,"bold"),fg_color=COLOR_TARJETA,text_color=COLOR_VARIOS)
        self.total_total_vendido.place(relx=0.5,y=75,anchor="center")

        self.cargar_ventas_del_dia()

    def cargar_ventas_del_dia(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        ventas = obtener_ventas_del_dia()

        for venta in ventas:
            id_detalle = venta[0]
            factura = venta[1]
            producto = venta[2]
            cantidad = venta[3]
            precio = f"{venta[4]:,.0f}"
            total = f"{venta[5]:,.0f}"
            tipo_pago = self.calcular_tipo_pago(venta[6], venta[7], venta[8])
            ganancia = f"{venta[9]:,.0f}" if venta[9] is not None else "0"

            self.tree.insert("", "end", values=(
                id_detalle, factura, producto, cantidad, precio, total, tipo_pago, ganancia
            ))

        totales = obtener_totales_del_dia()

        self.total_ventas.configure(text=f"{totales['cantidad_total']}")
        self.total_efectivo.configure(text=f"$ {totales['efectivo']:,.0f}")
        self.total_qr.configure(text=f"$ {totales['qr']:,.0f}")
        self.total_tarjeta.configure(text=f"$ {totales['tarjeta']:,.0f}")
        self.total_total_vendido.configure(text=f"$ {totales['total_vendido']:,.0f}")    
        
    def calcular_tipo_pago(self, pago_efectivo, pago_qr, pago_tarjeta):
        metodos = []
        if pago_efectivo > 0:
            metodos.append("Efecitvo")
        if pago_qr > 0:
            metodos.append("QR")
        if pago_tarjeta > 0:
            metodos.append("Tarjeta")
        return "/".join(metodos)    

        



