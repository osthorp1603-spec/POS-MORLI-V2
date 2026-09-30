from tkinter import messagebox
from database.rf_db import guardar_rf


def mover_a_rf_registros(tree, actualizar_total, factura_provisional):
    seleccion = tree.selection()

    if not seleccion:
        messagebox.showwarning("Cancelar Venta", "Seleccione un producto para cancelar.", parent=tree)
        return

    item = tree.item(seleccion)["values"]
    if not item:
        messagebox.showerror("Error", "No se pudo obtener la información del producto.", parent=tree)
        return

    nombre_articulo = item[0]
    valor_articulo = float(item[1].replace(",", ""))
    cantidad = int(item[2])
    subtotal = float(item[3].replace(",", ""))

    confirmar = messagebox.askyesno("Confirmar Cancelación", f"¿Está seguro de cancelar '{nombre_articulo}'?", parent=tree)
    if not confirmar:
        return

    if guardar_rf(factura_provisional, nombre_articulo, valor_articulo, cantidad, subtotal):
        tree.delete(seleccion)
        actualizar_total()
        messagebox.showinfo("Venta Cancelada", "El producto ha sido cancelado y enviado a RF Registros.", parent=tree)
    else:
        messagebox.showerror("Error", "No se pudo guardar la cancelación en RF.", parent=tree)