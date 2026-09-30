import os                                        # Para manejar rutas y archivos
import sys                                         # Para saber si corremos en Windows, Mac o Linux
import subprocess                                  # Para abrir el PDF con el programa por defecto del sistema
import tempfile                                   # Para crear archivos temporales que no se acumulan
import re                                         # Para limpiar el nombre del producto (quitar caracteres raros)
from reportlab.graphics.barcode import code128   # Para dibujar el código de barras tipo Code128
from reportlab.pdfgen import canvas              # Para crear el PDF
from reportlab.lib.units import mm               # Para usar medidas en milímetros

def crear_codigo_barras(codigo, altura_mm=11.5, ancho_etiqueta_mm=30):
    try:
        max_width = ancho_etiqueta_mm * mm
        bar_width = 1.0
        while bar_width > 0.3:
            barcode = code128.Code128(codigo, barHeight=altura_mm * mm, barWidth=bar_width, humanReadable=False)
            if barcode.width <= max_width:
                return barcode
            bar_width -= 0.05
        return code128.Code128(codigo, barHeight=altura_mm * mm, barWidth=0.3, humanReadable=False)        
    except Exception as e:
        print(f"Error al crear código de barras: {e}")
        return None

def generar_pdf_etiqueta(codigo, nombre_producto, precio):
    try:
        etiqueta_alto = 20 * mm
        ancho_total = 60 * mm

        archivo_temp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        nombre_archivo = archivo_temp.name
        archivo_temp.close()

        c = canvas.Canvas(nombre_archivo, pagesize=(ancho_total, etiqueta_alto))
        y_barra = 6 * mm
        y_nombre = 2.5 * mm
        y_precio = 0.5 * mm

        # Etiqueta izquierda
        barcode1 = crear_codigo_barras(codigo)
        x_izq = (30 * mm - barcode1.width) / 2
        barcode1.drawOn(c, x_izq, y_barra)
        c.setFont("Helvetica", 5.8)
        c.drawCentredString(15 * mm, y_nombre, nombre_producto[:22])
        c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(15 * mm, y_precio, f"${precio:,.0f}")

        # Etiqueta derecha
        barcode2 = crear_codigo_barras(codigo)
        x_der = 30 * mm + (30 * mm - barcode2.width) / 2
        barcode2.drawOn(c, x_der, y_barra)
        c.setFont("Helvetica", 5.8)
        c.drawCentredString(30 * mm + 15 * mm, y_nombre, nombre_producto[:22])
        c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(30 * mm + 15 * mm, y_precio, f"${precio:,.0f}")
        c.save()

        if sys.platform.startswith("win"):
            os.startfile(nombre_archivo)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", nombre_archivo])
        else:
            subprocess.Popen(["xdg-open", nombre_archivo])

        return nombre_archivo
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return None    

    