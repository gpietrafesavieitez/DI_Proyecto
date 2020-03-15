from sqlite3 import dbapi2

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, PageBreak, TableStyle, Table)


class GenerarClientes():
    def __init__(self):
        listaInventario = []
        listaInventario.append(list(['Listado de Clientes', '', '', '', '']))
        listaInventario.append(list(['Identificación', 'Nombre', 'Primer apellido', 'Segundo apellido', 'Teléfono']))

        try:
            baseDatos = dbapi2.connect("base.dat")
            cursor = baseDatos.cursor()
            clientes = cursor.execute("select dni, name, apel1, apel2, tlf from clientes")
            for cliente in clientes:
                listaInventario.append(list([cliente[0], cliente[1], cliente[2], cliente[3], str(cliente[4])]))
        except (dbapi2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            baseDatos.close()

        doc = SimpleDocTemplate("export/listadoClientes.pdf", pagesize=A4)
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
    GenerarClientes()
