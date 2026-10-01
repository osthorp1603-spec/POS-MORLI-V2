import tkinter as tk
from tkinter import messagebox,simpledialog
from views.ventas import Ventas 
from views.inventario import Inventario
from views.salida_efectivo import Salida_efectivo
from views.reportes import Reportes
from views.codigos import Codigos
from views.decoraciones import Decoraciones
from views.factura_electronica import FacturaElectronica
from core.cortez import generar_corte_z
from utils.rutas import ruta_base
import os
from PIL import Image,ImageTk                       #PARA LAS IMAGENES
import customtkinter as ctk                         #BOTONES MODERNSO
from datetime import datetime                       #para copyright




COLOR_FONDO = "#FAFAFA"  #c6d9e3          # Blanco cálido suave
COLOR_PRINCIPAL = "#B84272"        # Rosa magenta vibrante
COLOR_PRINCIPAL_HOVER = "#96325A"
COLOR_PRINCIPAL_TEXTO = "#FFFFFF"  # Texto blanco
COLOR_SECUNDARIO = "#E8ECEF"       # Gris suave neutro
COLOR_SECUNDARIO_TEXTO = "#1F2937" # Texto gris oscuro
COLOR_PELIGRO = "#8B0000"          # Rojo granate/vino
COLOR_PELIGRO_HOVER = "#660000"
COLOR_PELIGRO_TEXTO = "#FFFFFF"    # Texto blanco

class Container(tk.Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.place(x=0,y=0,width=1000,height=480)  #VENTANA PADRE - CAMBIAR TAMAÑO, PERO NO SOLO AQUI SINO EN MANAGER
        self.config(bg=COLOR_FONDO)                                # y en def widgett
        self.widgets()

    def show_frames(self,container,size):
        top_level = tk.Toplevel(self)
        top_level.withdraw()     # oculta la ventana al crearla              
        top_level.iconbitmap(os.path.join(ruta_base(),"icono.ico"))
        frame = container(top_level)
        frame.config(bg="#c6d9e3")          #INTEFAZ VENTANA PERO DE LAS OTRAS PANTALLAS
        frame.pack(fill="both",expand=True)
        top_level.geometry(size)
        top_level.resizable(False,False)
        top_level.deiconify()       # muestra al final, ya con el ícono puesto
        return top_level
        
    def ventas(self):
        self.show_frames(Ventas,"1100x660+120+20")

    def inventario(self):
        self.show_frames(Inventario,"1273x810+5+20") 

    def salida_efectivo(self):
        self.show_frames(Salida_efectivo,"400x300+500+170")  

    def reportes(self):
        self.winfo_toplevel().withdraw()
        ventana = self.show_frames(Reportes,"1273x810+5+20") 
        ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_reportes(ventana))

    def cerrar_reportes(self, ventana):
        ventana.destroy()
        self.winfo_toplevel().deiconify()

    def validar_password_reporte(self):
        password = tk.simpledialog.askstring("Autenticación","Ingrese la contraseña:",show="*")
        if password == "monioscar":  
            self.reportes()
        elif password is not None:
            messagebox.showerror("Acceso denegado", "Contraseña incorrecta.")      

    def codigos(self):
        self.show_frames(Codigos,"1100x640+120+20")   

    def decoraciones(self):
        self.show_frames(Decoraciones,"740x800+460+20")     

    def factura_electronica(self):
        self.show_frames(FacturaElectronica,"400x300+500+170")       

    def cierre_z(self):
        confirmar = messagebox.askyesno("Cierre Z", "¿Está seguro de hacer el Cierre Z?\n\nEsto cerrará todas las ventas pendientes.")
        if not confirmar:
            return
        try:
            generar_corte_z()
            messagebox.showinfo("Cierre Z", "Corte Z generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el Cierre Z:\n{e}") 

      
            

    def widgets(self):                        #INTERFAZ GRAFICA PANTALLA PRINCIPAL VALROVIEJRO 800X400
        frame1 =tk.Frame(self,bg=COLOR_FONDO)     
        frame1.place(x=0,y=0,width=1000,height=480)

        #BOTON VENTAS ///////////// VALOR VIEJO x=500,y=30,width=180,height=70
        self.icon_reg = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/regalo.png")), size=(50, 50))
        btnventas = ctk.CTkButton(frame1,image=self.icon_reg,compound="left",fg_color=COLOR_PRINCIPAL,text_color=COLOR_PRINCIPAL_TEXTO,font=("sans",20,"bold"),text="Ventas",corner_radius=10,width=560,height=60,hover_color=COLOR_PRINCIPAL_HOVER,command=self.ventas)    
        btnventas.place(x=400,y=30)

        #BOTON INVENTARIO /////////////// VALOR VIEJO x=500,y=130,width=210,height=70
        self.icon_inv = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/btninventario.png")), size=(50, 50))
        btninventario = ctk.CTkButton(frame1,image=self.icon_inv,compound="left",fg_color=COLOR_PRINCIPAL,text_color=COLOR_PRINCIPAL_TEXTO,font=("sans",20,"bold"),text="Inventario",corner_radius=10,width=560,height=60,hover_color=COLOR_PRINCIPAL_HOVER,command=self.inventario)
        btninventario.place(x=400,y=110)

        #BOTON REPORTE
        self.icon_reporte = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/btnreportes.png")), size=(25, 25))
        btnreporte = ctk.CTkButton(frame1,image=self.icon_reporte,compound="left",fg_color=COLOR_SECUNDARIO,text_color=COLOR_SECUNDARIO_TEXTO,font=("sans",15,"bold"),text="Reportes",corner_radius=10,width=270,height=45,hover_color=COLOR_FONDO,command=self.validar_password_reporte)
        btnreporte.place(x=400,y=190)

        #BOTON COD_BARRAS
        self.icon_cod = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/codigo.png")), size=(25, 25))
        btncod_barras = ctk.CTkButton(frame1,image=self.icon_cod,compound="left",fg_color=COLOR_SECUNDARIO,text_color=COLOR_SECUNDARIO_TEXTO,font=("sans",15,"bold"),text="Cod_Barra",corner_radius=10,width=270,height=45,hover_color=COLOR_FONDO,command=self.codigos)
        btncod_barras.place(x=690,y=190)

        #BOTON FACTURA ELECTRONICA
        self.icon_fe = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/contabilidad.png")), size=(25, 25))
        btnfe = ctk.CTkButton(frame1,image=self.icon_fe,compound="left",fg_color=COLOR_SECUNDARIO,text_color=COLOR_SECUNDARIO_TEXTO,font=("sans",15,"bold"),text="factura electronica",corner_radius=10,width=270,height=45,hover_color=COLOR_FONDO,command=self.factura_electronica)
        btnfe.place(x=400,y=250)

        #BOTON CLIENTES
        self.icon_cli = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/cliente.png")), size=(25, 25))
        btncliente = ctk.CTkButton(frame1,image=self.icon_cli,compound="left",fg_color=COLOR_SECUNDARIO,text_color=COLOR_SECUNDARIO_TEXTO,font=("sans",15,"bold"),text="Clientes",corner_radius=10,width=270,height=45,hover_color=COLOR_FONDO)
        btncliente.place(x=690,y=250)

        #BOTON DECORACIONES
        self.icon_dec = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/cesta.png")), size=(25, 25))
        btndecoracion = ctk.CTkButton(frame1,image=self.icon_dec,compound="left",fg_color=COLOR_SECUNDARIO,text_color=COLOR_SECUNDARIO_TEXTO,font=("sans",15,"bold"),text="Decoraciones",corner_radius=10,width=270,height=45,hover_color=COLOR_FONDO,command=self.decoraciones)
        btndecoracion.place(x=400,y=310)

        #BOTON SALIDA EFECTIVO
        self.icon_sal = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/dinero.png")), size=(25, 25))
        btnsalida_efectivo = ctk.CTkButton(frame1,image=self.icon_sal,compound="left",fg_color=COLOR_SECUNDARIO,text_color=COLOR_SECUNDARIO_TEXTO,font=("sans",15,"bold"),text="Salida Efectivo",corner_radius=10,width=270,height=45,hover_color=COLOR_FONDO,command=self.salida_efectivo)
        btnsalida_efectivo.place(x=690,y=310)

        #BOTON CIERRE (Z) - peligro, ancho completo, solo
        self.icon_z = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_base(),"assets/icons/cerrar.png")), size=(25, 25))
        btncierre = ctk.CTkButton(frame1,image=self.icon_z,compound="left",fg_color=COLOR_PELIGRO,text_color=COLOR_PELIGRO_TEXTO,font=("sans",18,"bold"),
            text="Cierre (Z)",corner_radius=10,width=360,height=45,hover_color=COLOR_PELIGRO_HOVER,command=self.cierre_z)
        btncierre.place(x=500,y=380)

        #IMAGNE LOGO ////////////VALORES VIEJOS x=100,y=30
        self.logo_image = Image.open(os.path.join(ruta_base(),"assets/images/logolocal.png"))
        self.logo_image = self.logo_image.resize((280,280))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1,image=self.logo_image,bg=COLOR_FONDO)
        self.logo_label.place(x=60,y=40,width=280,height=280)

        #COPYRIGHT //// VALORES VIEJOS x=180,y=350
        año = datetime.now().year
        copyright_label = tk.Label(frame1,text=f"© {año} MORLIGIFTSTORE \n todos los derechos reservados",font="sans 10 bold",bg=COLOR_FONDO,fg="gray")
        copyright_label.place(x=5,y=340,width=380,height=40)





