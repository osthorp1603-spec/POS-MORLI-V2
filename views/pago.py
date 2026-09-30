import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from PIL import Image
from database.ventas_db import guardar_venta, guardar_detalle_venta
from database.inventario_db import (restar_stock_producto,obtener_umbral_producto,obtener_stock_producto,
    restar_stock_con_componentes)
from utils.rutas import ruta_base
import os
from core.impresora import imprimir_ticket_pos
from datetime import datetime


COLOR_FONDO = "#c6d9e3"
COLOR_BOTON = "#F1EFE8"
COLOR_BOTON_HOVER = "#DCD9D0"
COLOR_TEXTO_BOTON = "#2C2C2A"
COLOR_ACENTO_EFECTIVO = "#0F6E56"
COLOR_EFECTIVO_HOVER = "#0B5946"
COLOR_ACENTO_QR = "#185fa5"
COLOR_QR_HOVER = "#124B84"
COLOR_ACENTO_TARJETA = "#B5651D"
COLOR_TARJETA_HOVER = "#8F4F19"

class Pago():
        
    def __init__(self, ventas):
        self.ventas = ventas
        self.abrir_ventana_pago()

    def abrir_ventana_pago(self):
            if not self.ventas.tree.get_children():
                messagebox.showerror("Error", "No hay artículos para pagar",parent=self.ventas)
                return

            self.ventana_pago = tk.Toplevel(self.ventas)
            self.ventana_pago.title("Realizar pago")
            self.ventana_pago.geometry("1050x650+150+20")
            self.ventana_pago.config(bg=COLOR_FONDO)
            self.ventana_pago.resizable(False, False) 
            self.ventana_pago.grab_set()
            total = self.ventas.obtener_total()

            label_total = tk.Label(self.ventana_pago, bg=COLOR_FONDO, text=f"Total a pagar: ${total:,.0f}", font="sans 40 bold")
            label_total.place(relx=0.5, y=40,anchor="n")

            label_cantidad_pagada = tk.Label(self.ventana_pago, bg=COLOR_FONDO, text="Cantidad pagada:", font="sans 16 bold")
            label_cantidad_pagada.place(relx=0.5, y=150,anchor="n")

            self.entry_cantidad_pagado = ctk.CTkEntry(self.ventana_pago,font=("sans",30,"bold"),corner_radius=10,width=300,height=45,justify="center")
            self.entry_cantidad_pagado.place(relx=0.5,y=185,anchor="n")

            self.label_cambio = tk.Label(self.ventana_pago, bg=COLOR_FONDO, text="Cambio: $ ", font="sans 20 bold")
            self.label_cambio.place(relx=0.5, y=250,anchor="n")

            def calcular_cambio(event):
                texto = self.entry_cantidad_pagado.get().replace(",", "").strip()
                if texto.isdigit():
                    texto_formateado = "{:,}".format(int(texto))
                    self.entry_cantidad_pagado.delete(0, tk.END)
                    self.entry_cantidad_pagado.insert(0, texto_formateado)
                    self.entry_cantidad_pagado.icursor(tk.END)
                try:
                    cantidad_pagada = float(self.entry_cantidad_pagado.get().replace(",", ""))
                    total = self.ventas.obtener_total()
                    cambio = cantidad_pagada - total
                    if cambio < 0:
                        self.label_cambio.config(text="Cambio: $ 0")
                        return
                    self.label_cambio.config(text=f"Cambio: $ {cambio:,.0f}")
                except ValueError:
                    self.label_cambio.config(text="")
            self.entry_cantidad_pagado.bind("<KeyRelease>", calcular_cambio)  

            def usar_billete(valor):
                self.entry_cantidad_pagado.delete(0, tk.END)
                self.entry_cantidad_pagado.insert(0, str(valor))
                calcular_cambio(None)

            valores_billetes = [2000, 5000, 10000, 20000, 50000, 100000]
            x_inicial = 60
            espacio = 155
            y_billetes = 340

            for i, valor in enumerate(valores_billetes):
                btn = ctk.CTkButton(self.ventana_pago, text=f"${valor:,}", font=("sans",17,"bold"), text_color=COLOR_TEXTO_BOTON, fg_color=COLOR_BOTON,
                width=140, height=55,border_width=2,corner_radius=10,hover_color=COLOR_BOTON_HOVER, command=lambda v=valor: usar_billete(v))
                btn.place(x=x_inicial + i * espacio, y=y_billetes)

            # BOTONES DE PAGOS
            self.icon_ef = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/efectivo.png")), size=(50, 50))
            btn_efectivo = ctk.CTkButton(self.ventana_pago,image=self.icon_ef,compound="left", text="Efectivo", font=("sans",15,"bold"),
            text_color=COLOR_TEXTO_BOTON, fg_color=COLOR_BOTON,corner_radius=10,
            border_width=2, border_color=COLOR_ACENTO_EFECTIVO,hover_color=COLOR_EFECTIVO_HOVER,
            width=280, height=100,command=lambda: self.pagar("Efectivo"))
            btn_efectivo.place(x=60, y=450)

            self.icon_qr = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/qr.png")), size=(50, 50))
            btn_qr = ctk.CTkButton(self.ventana_pago,image=self.icon_qr,compound="left", text="Qr", font=("sans",15,"bold"),
            text_color=COLOR_TEXTO_BOTON, fg_color=COLOR_BOTON,corner_radius=10,
            border_width=2, border_color=COLOR_ACENTO_QR,hover_color=COLOR_QR_HOVER,
            width=280, height=100,command=lambda: self.pagar("QR"))
            btn_qr.place(x=400, y=450)

            self.icon_tar = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/tarjeta.png")), size=(50, 50))
            btn_tarjeta = ctk.CTkButton(self.ventana_pago, image=self.icon_tar,compound="left",text="Tarjeta", font=("sans",15,"bold"),
            text_color=COLOR_TEXTO_BOTON, fg_color=COLOR_BOTON,corner_radius=10,
            border_width=2, border_color=COLOR_ACENTO_TARJETA,hover_color=COLOR_TARJETA_HOVER,
            width=280, height=100,command=lambda: self.pagar("Tarjeta"))
            btn_tarjeta.place(x=740, y=450)

            self.icon_div = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/dividido.png")), size=(25, 25))
            btn_pagodividido = ctk.CTkButton(self.ventana_pago,image=self.icon_div,compound="left", text="Pago dividido", font=("sans",15,"bold"),
            text_color=COLOR_TEXTO_BOTON, fg_color=COLOR_BOTON,corner_radius=10,
            border_width=2,hover_color=COLOR_BOTON_HOVER,
            width=200, height=50,command=self.abrir_pago_dividido)
            btn_pagodividido.place(x=440, y=570)

    
    def pagar(self, tipo_pago):
        total = self.ventas.obtener_total()
        if tipo_pago == "Efectivo":
            try:
                cantidad_pagada = float(self.entry_cantidad_pagado.get().replace(",", ""))
            except ValueError:
                messagebox.showerror("Error", "Monto no válido", parent=self.ventana_pago)
                return
        else:
            cantidad_pagada = total
        
        if cantidad_pagada < total:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente", parent=self.ventana_pago)
            return

        if tipo_pago == "Efectivo":
            pago_efectivo = cantidad_pagada
            pago_qr = 0
            pago_tarjeta = 0
            cambio = cantidad_pagada - total
        elif tipo_pago == "QR":
            pago_efectivo = 0
            pago_qr = total
            pago_tarjeta = 0
            cambio = 0
        else:  # Tarjeta
            pago_efectivo = 0
            pago_qr = 0
            pago_tarjeta = total
            cambio = 0

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        factura = int(self.ventas.numero_factura.get())

        venta_id = guardar_venta(factura, fecha, total, pago_efectivo, pago_qr, pago_tarjeta, cambio)

        productos_en_umbral = []
        for child in self.ventas.tree.get_children():
            item = self.ventas.tree.item(child,"values")
            nombre_articulo = item[0]
            valor_articulo = float(item[1].replace(",", ""))
            cantidad = int(item[2])
            subtotal = float(item[3].replace(",", ""))
            guardar_detalle_venta(venta_id, nombre_articulo, valor_articulo, cantidad, subtotal)
            restar_stock_con_componentes(nombre_articulo, cantidad)

            umbral = obtener_umbral_producto(nombre_articulo)
            stock_actual = obtener_stock_producto(nombre_articulo)
            if umbral is not None and stock_actual is not None and stock_actual <= umbral:
                productos_en_umbral.append(f"{nombre_articulo} (stock: {stock_actual}, umbral: {umbral})")
        
    # IMPRESORA 
        productos_ticket = []
        for child in self.ventas.tree.get_children():
            item = self.ventas.tree.item(child, "values")
            nombre_articulo = item[0]
            valor_articulo = float(item[1].replace(",", ""))
            cantidad = int(item[2])
            subtotal = float(item[3].replace(",", ""))
            productos_ticket.append((nombre_articulo, valor_articulo, cantidad, subtotal))

        imprimir_ticket_pos(
            productos_ticket,
            total,
            tipo_pago,
            cambio,
            cantidad_pagada,
            factura,
            fecha
        )
        self.ventas.tree.delete(*self.ventas.tree.get_children())
        
    # LIMPIAR PANTALLA Y CERRAR VENTANTA DE PAGO    
        self.ventas.actualizar_total()
        self.ventana_pago.destroy()
        self.ventas.actualizar_numero_factura()
        self.ventas.entry_pistola.focus_set()
                
    #//////////////////////////////////////////////////////////////////

    def abrir_pago_dividido(self):
        ventana_dividido = tk.Toplevel(self.ventana_pago)
        ventana_dividido.title("Pago Dividido")
        ventana_dividido.geometry("400x375+500+170")
        ventana_dividido.config(bg="white")
        ventana_dividido.resizable(False, False)
        ventana_dividido.transient(self.ventana_pago)
        ventana_dividido.grab_set()
        ventana_dividido.focus_force()

        tk.Label(ventana_dividido, text="Ingrese los montos:",fg="#1E6091", font="sans 14 bold", bg="white").pack(pady=10)

        frame_campos = tk.Frame(ventana_dividido, bg="white")
        frame_campos.pack(pady=10)

        def formatear_entry(event):
            entry = event.widget
            texto = entry.get().replace(",", "").strip()
            if texto.isdigit():
                texto_formateado = "{:,}".format(int(texto))
                entry.delete(0, tk.END)
                entry.insert(0, texto_formateado)
                entry.icursor(tk.END)

        ctk.CTkLabel(frame_campos, text="💵 Efectivo:", font=("sans", 13, "bold"), text_color="black", fg_color="transparent").grid(row=0, column=0, sticky="w", pady=5)
        entry_efectivo = ctk.CTkEntry(frame_campos, font=("sans", 15), justify="center", width=180, height=32, corner_radius=8)
        entry_efectivo.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(frame_campos, text="📱 QR:", font=("sans", 13, "bold"), text_color="black", fg_color="transparent").grid(row=1, column=0, sticky="w", pady=5)
        entry_qr = ctk.CTkEntry(frame_campos, font=("sans", 15), justify="center", width=180, height=32, corner_radius=8)
        entry_qr.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(frame_campos, text="💳 Tarjeta:", font=("sans", 13, "bold"), text_color="black", fg_color="transparent").grid(row=2, column=0, sticky="w", pady=5)
        entry_tarjeta = ctk.CTkEntry(frame_campos, font=("sans", 15), justify="center", width=180, height=32, corner_radius=8)
        entry_tarjeta.grid(row=2, column=1, pady=5)

        self.label_falta = tk.Label(ventana_dividido, text="Falta: $0", fg="#A32D2D", font="sans 14 bold", bg="white")
        self.label_falta.place(relx=0.5, y=245, anchor="center")

        def calcular_falta(*args):
            def leer(entry):
                texto = entry.get().replace(",", "").strip()
                return float(texto) if texto else 0.0
            
            efectivo = leer(entry_efectivo)
            qr = leer(entry_qr)
            tarjeta = leer(entry_tarjeta)
            falta = self.ventas.obtener_total() - (efectivo + qr + tarjeta)
            
            if falta <= 0:
                self.label_falta.config(text="Falta: $0", fg="#2D8A56")
            else:
                self.label_falta.config(text=f"Falta: ${falta:,.0f}", fg="#A32D2D") 

        entry_efectivo.bind("<KeyRelease>", formatear_entry)
        entry_qr.bind("<KeyRelease>", formatear_entry)           # BLOQUE PARA EL FORMATO MIL
        entry_tarjeta.bind("<KeyRelease>", formatear_entry)
        entry_efectivo.bind("<KeyRelease>", calcular_falta, add="+")
        entry_qr.bind("<KeyRelease>", calcular_falta, add="+")
        entry_tarjeta.bind("<KeyRelease>", calcular_falta, add="+")

        btn_finalizar = ctk.CTkButton(
        ventana_dividido,
        text="Finalizar Pago Dividido",
        font=("sans", 14, "bold"),
        fg_color="#2D8A56",
        hover_color="#246E44",
        width=200, height=45,
        corner_radius=10,
        command=lambda: self.procesar_pago_dividido(ventana_dividido, entry_efectivo, entry_qr,
        entry_tarjeta)
        )
        btn_finalizar.place(relx=0.5,y=300,anchor="n")

    def procesar_pago_dividido(self, ventana_dividido, entry_efectivo, entry_qr, entry_tarjeta):
        def leer(entry):
            texto = entry.get().replace(",", "").strip()
            return float(texto) if texto else 0.0

        try:
            efectivo = leer(entry_efectivo)
            qr = leer(entry_qr)
            tarjeta = leer(entry_tarjeta)
        except ValueError:
            messagebox.showerror("Error", "Algún monto no es válido", parent=ventana_dividido)
            return

        total_pago = efectivo + qr + tarjeta
        total = self.ventas.obtener_total()

        if total_pago != total:
            messagebox.showerror(
                "Error",
                f"La suma de los montos (${total_pago:,.0f}) no coincide con el total (${total:,.0f})",
                parent=ventana_dividido
            )
            return

        self.guardar_venta_dividida(efectivo, qr, tarjeta, total)

        ventana_dividido.destroy()

    def guardar_venta_dividida(self, efectivo, qr, tarjeta, total):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        factura = int(self.ventas.numero_factura.get())

        venta_id = guardar_venta(factura, fecha, total, efectivo, qr, tarjeta, 0)

        for child in self.ventas.tree.get_children():
            item = self.ventas.tree.item(child, "values")
            nombre_articulo = item[0]
            valor_articulo = float(item[1].replace(",", ""))
            cantidad = int(item[2])
            subtotal = float(item[3].replace(",", ""))
            guardar_detalle_venta(venta_id, nombre_articulo, valor_articulo, cantidad, subtotal)
            restar_stock_con_componentes(nombre_articulo, cantidad)   

        self.ventas.tree.delete(*self.ventas.tree.get_children())
        self.ventas.actualizar_total()
        self.ventana_pago.destroy()
        self.ventas.actualizar_numero_factura()
        self.ventas.entry_pistola.focus_set()
        self.ventas.lift()
        self.ventas.focus_force()