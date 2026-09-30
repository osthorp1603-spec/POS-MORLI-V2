#  MORLIGIFTSTORE POS — Versión 2
## Descripción
Sistema de punto de venta (POS) para la gestión integral de una tienda de regalos. Permite registrar ventas con lector de código de barras, controlar el inventario, gestionar clientes, crear anchetas/decoraciones, generar facturas e imprimir tickets en impresora térmica. Incluye un módulo para visualizar las ventas con su respectiva ganancia.

Versión 2.0 — Segunda iteración del sistema, con mejoras en la interfaz, optimización de procesos y nuevas funcionalidades.

## ¿Qué es la Versión 2?
Esta es la segunda versión del sistema. A diferencia de la Versión 1, se enfoca en:

- Código más limpio y organizado.
- Interfaz visualmente mejorada con CustomTkinter (ctk).
- Mayor robustez.

## Tecnologías utilizadas

- **Python** — lenguaje principal del proyecto.
- **Tkinter / CustomTkinter (ctk)** — interfaz gráfica de escritorio, con componentes modernos.
- **SQLite** — base de datos local.
- **ReportLab** — generación de facturas y etiquetas en PDF.
- **win32print** — impresión térmica POS y apertura del cajón.
- **Matplotlib** — gráficos para los reportes.
- **Arquitectura modular** — separación en UI, lógica y utilidades.

## Estructura del proyecto
```
POS MORLI/
│
├── assets/
│   ├── icons/
│   └── images/
│
├── core/
│   ├── container.py
│   ├── cortez.py
│   ├── impresora.py
│   ├── manager.py
│   └── rf.py
│
├── corte_z/
│
├── database/
│   ├── codigos_db.py
│   ├── conexion.py
│   ├── corte_z_db.py
│   ├── decoraciones_db.py
│   ├── inventario_db.py
│   ├── reportes_db.py
│   ├── rf_db.py
│   ├── salida_efectivo_db.py
│   └── ventas_db.py
│
├── utils/
│   ├── generador.py
│   └── rutas.py
│
├── views/
│   ├── codigos.py
│   ├── decoraciones.py
│   ├── inventario.py
│   ├── pago.py
│   ├── reportes.py
│   ├── salida_efectivo.py
│   ├── venta_diaria.py
│   └── ventas.py
│
├── database.db
├── icono.ico
├── index.py
├── POSMorli.spec
└── README.md

```
## Explicación técnica

El sistema fue desarrollado en Python, con interfaz gráfica en Tkinter y una base de datos local en SQLite.

El proyecto sigue una arquitectura modular que separa responsabilidades:

- **UI:** contiene las ventanas del sistema: ventas, inventario, clientes, anchetas, movimientos de inventario y las ventanas contables de interfaz.
- **Lógica:** contiene las operaciones de negocio y reportes: corte Z, cancelaciones (RF), generación de códigos de barras y todos los cálculos contables (utilidad, balance, estado de resultados, punto de equilibrio, etc.).
- **Utilidades:** herramientas auxiliares, como la impresión de tickets en la impresora térmica.

### Flujo general del sistema

1. El vendedor registra los productos mediante el lector de código de barras o por búsqueda manual.
2. Al cobrar, el sistema acepta pago en efectivo, QR, tarjeta o pago dividido.
3. La venta se guarda en la base de datos, se descuenta el stock y se genera la factura en PDF.
4. El ticket se imprime en la impresora térmica y, si el pago es en efectivo, se abre el cajón.
5. Al final del día se realiza el Corte Z, que genera el resumen de caja y cierra la jornada.
6. El administrador puede consultar reportes de utilidad, inventario y la contabilidad completa.

## Evidencias

![ventana_principal](evidencias/ventanaprincipal.png)
![ventana_de_compra](evidencias/ventanaventa.png)
![ventana_de_pago](evidencias/ventanapago.png)
![visualizar_ventas_diarias-mes](evidencias/filtroventas.png)
![ventana_inventario](evidencias/inventario.png)
![ventana_contable](evidencias/contable.png)