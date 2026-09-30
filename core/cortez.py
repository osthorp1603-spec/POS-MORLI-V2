import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from database.corte_z_db import (obtener_resumen_ventas,obtener_resumen_rf,obtener_totales_corte,
        marcar_todo_cerrado)


def generar_corte_z():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    resumen_ventas = obtener_resumen_ventas()
    resumen_rf = obtener_resumen_rf()
    totales = obtener_totales_corte()

    ruta_pdf = generar_corte_z_pdf(resumen_ventas, resumen_rf, totales, fecha_hoy)

    marcar_todo_cerrado()

    try:
        import win32print
        nombre_impresora = "POSPrinter POS80"
        hPrinter = win32print.OpenPrinter(nombre_impresora)
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Abrir Cajón Corte Z", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, b"\x1B\x70\x00\x19\xFA")
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)
    except Exception as e:
        print(f"No se pudo abrir el cajón: {e}")

    os.startfile(os.path.abspath(ruta_pdf))
    return ruta_pdf


def generar_corte_z_pdf(resumen_ventas, resumen_rf, totales, fecha_hoy):
    width = 2.25 * inch
    height = 6 * inch

    base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
    carpeta = os.path.join(base_path, "corte_z")
    os.makedirs(carpeta, exist_ok=True)

    nombre_archivo = f"corte_{fecha_hoy.replace(':', '-')}.pdf"
    ruta_pdf = os.path.join(carpeta, nombre_archivo)

    c = canvas.Canvas(ruta_pdf, pagesize=(width, height))

    c.setFont("Helvetica-Bold", 8)
    c.drawString(10, height - 20, f"Corte Z - {fecha_hoy}")

    c.setFont("Helvetica-Bold", 7)
    c.drawString(10, height - 40, "Resumen:")
    y = height - 60
    c.setFont("Helvetica", 6)
    for tipo, cantidad, total in resumen_ventas:
        tipo = tipo if tipo else "Sin tipo"
        c.drawString(10, y, f"{tipo}: {cantidad} vendidos - ${total:,.0f}")
        y -= 10

    c.setFont("Helvetica-Bold", 8)
    c.drawString(10, y - 10, f"BRUTO: ${totales['total_vendido']:,.0f}")
    c.drawString(10, y - 20, f"Efectivo: ${totales['efectivo_neto']:,.0f}")
    c.drawString(10, y - 30, f"QR: ${totales['qr']:,.0f}")
    c.drawString(10, y - 40, f"Tarjeta: ${totales['tarjeta']:,.0f}")
    c.drawString(10, y - 50, f"TL: {totales['cantidad_total']}")

    y -= 70
    c.setFont("Helvetica-Bold", 7)
    c.drawString(10, y, f"Salida Efectivo: ${totales['total_salida']:,.0f}")
    y -= 10
    c.drawString(10, y, f"Efectivo Final: ${totales['efectivo_final']:,.0f}")
    y -= 20

    c.setFont("Helvetica-Bold", 7)
    c.drawString(10, y, "Ventas Canceladas (RF):")
    y -= 10
    c.setFont("Helvetica", 6)
    for tipo, cantidad, total in resumen_rf:
        tipo = tipo if tipo else "Sin tipo"
        c.drawString(10, y, f"{tipo}: {cantidad} cancelados - ${total:,.0f}")
        y -= 10

    c.setFont("Helvetica-Bold", 8)
    c.drawString(10, y, f"Total RF Cancelado: ${totales['total_rf']:,.0f}")

    c.save()
    return ruta_pdf