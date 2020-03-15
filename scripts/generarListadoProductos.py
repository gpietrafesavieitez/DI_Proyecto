from sqlite3 import dbapi2

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, PageBreak, TableStyle, Table)


class GenerarProductos():
    def __init__(self):
        listaInventario = []
        listaInventario.append(list(['Listado de Productos', '', '', '']))
        listaInventario.append(list(['Nombre', 'Descripción', 'Precio', 'Stock']))

        try:
            baseDatos = dbapi2.connect("base.dat")
            cursor = baseDatos.cursor()
            productos = cursor.execute("select name, desc, precio, stock from productos")
            for producto in productos:
                listaInventario.append(list([producto[0], producto[1], str(producto[2]), str(producto[3])]))
        except (dbapi2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            baseDatos.close()

        doc = SimpleDocTemplate("export/listadoProductos.pdf", pagesize=A4)
        guion = []
        taboa = Table(listaInventario, colWidths=150, rowHeights=30)
        taboa.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.green),
            ('TEXTCOLOR', (0, 4), (-1, -1), colors.black),
            # ('BOX', (0, 2), (-1, -4), 1, colors.black),
            ('INNERGRID', (0, 2), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))
        guion.append(taboa)
        guion.append(PageBreak())
        doc.build(guion)


if __name__ == "__main__":
    GenerarProductos()
