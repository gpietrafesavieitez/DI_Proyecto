import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
from sqlite3 import dbapi2
from scripts.generarListadoClientes import GenerarClientes
from scripts.generarListadoProductos import GenerarProductos

base = "base.dat"

"""
    Programa principal
"""
def recargar():
    """ Función que ejecuta un cursor en la base de datos para seleccionar todos los clientes existentes.
            Parámetros:
                No tiene.
            Devoluciones:
                :return: Devuelve la lista de resultados.
            Excepciones:
                dbapi2.DatabaseError
    """
    devolver = list()
    try:
        bd = dbapi2.connect(base)
        cursor = bd.cursor()
        clientes = cursor.execute("SELECT * FROM clientes")
        for c in clientes:
            devolver.append(c)
    except(dbapi2.DatabaseError) as error:
        print(error)
        dialogo(0, "Ha habido un problema con la base de datos.")
    finally:
        cursor.close()
        bd.close()
    return devolver


def eliminar(pk):
    """ Función que ejecuta una sentencia de eliminación en la base de datos para un cliente concreto.
            Parámetros:
                :param pk -- Recibe clave primaria del cliente.
            Devoluciones:
                No tiene.
            Excepciones:
                dbapi2.DatabaseError
    """
    try:
        bd = dbapi2.connect(base)
        cursor = bd.cursor()
        cursor.execute("DELETE FROM clientes WHERE dni='" + pk + "'")
        bd.commit()
        dialogo(2, "Se ha eliminado el cliente satisfactoriamente.")
    except(dbapi2.DatabaseError) as error:
        print(error)
        dialogo(0, "Ha habido un problema con la base de datos.")
    finally:
        cursor.close()
        bd.close()


def validar(txt1, txt2, txt3, txt4, num):
    """ Función que filtra y sanitiza los formularios de entrada de texto, concretamente el de añadir un cliente.
            Parámetros:
                :param txt1 -- Recibe la primera entrada, en este caso el dni.
                :param txt2 -- Recibe la segunda entrada, en este caso el nombre.
                :param txt3 -- Recibe la tercera entrada, en este caso el primer apellido.
                :param txt4 -- Recibe la cuarta entrada, en este caso el segundo apellido.
                :param num -- Recibe la quinta entrada, en este caso el teléfono.
            Devoluciones:
                :return -- Devuelve mensajes en forma de lista.
            Excepciones:
                No tiene.
    """
    devolver = True
    msg = list()
    if txt1 and txt2 and txt3 and txt4 and num:
        if len(txt1) == 9 and txt1[8].isupper():
            print()
        else:
            devolver = False
            msg.append("\n\t- La identificación introducida no tiene un formato válido.")
        if num.isdigit() and len(num) == 9:
            print()
        else:
            devolver = False
            msg.append("\n\t- El teléfono introducido no tiene un formato válido.")
    else:
        devolver = False
        msg.append("\n\t- No puede haber campos vacíos.")
    if not devolver:
        dialog = Gtk.MessageDialog(flags=0, message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK, text="Aviso")
        s = ""
        for i in msg:
            s += str(i)
        dialog.format_secondary_text("Se han encontrado los siguientes problemas:" + s)
        dialog.run()
        dialog.destroy()
    return devolver


def dialogo(tipo, msg):
    """ Función que genera una ventana emergente para mostrar un mensaje personalizado.
            Parámetros:
                :param tipo -- Recibe el tipo del mensaje (información, aviso o error).
                :param msg -- Recibe el texto del mensaje.
            Devoluciones:
                No tiene.
            Excepciones:
                No tiene.
    """
    if tipo == 0:
        dialog = Gtk.MessageDialog(flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text="Error")
    if tipo == 1:
        dialog = Gtk.MessageDialog(flags=0, message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK, text="Aviso")
    if tipo == 2:
        dialog = Gtk.MessageDialog(flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Información")
    dialog.format_secondary_text(msg)
    dialog.run()
    dialog.destroy()


class Ventana(Gtk.Window):
    """ Clase principal de la aplicación que actuará como ventana.
            Constructor:
                __init__ -- Genera los componentes esenciales de la ventana.
            Métodos:
                on_celdaText2_edited -- Función que se dispara cuando se modifica la columna de los nombres.
                on_celdaText3_edited -- Función que se dispara cuando se modifica la columna de los teléfonos.
                on_vista_changed -- Función que se dispara cada vez que se selecciona un cliente en el modelo.
                on_btnAñadir_clicked -- Añade un cliente a la base de datos con la información proporcionada en el formulario.
                on_btnModificar_clicked -- Modifica un cliente en la base de datos con la nueva información proporcionada para un cliente concreto seleccionado.
                on_btnEliminar_clicked  -- Elimina el cliente que se haya seleccionado de la base de datos.
                on_btnGenerar_clicked -- Genera los listados de clientes y productos de la información recogida en la base de datos.
    """
    def __init__(self):
        # Propiedades de la ventana principal
        Gtk.Window.__init__(self, title="Desarrollo de Interfaces en Python con Gtk3")
        self.set_border_width(10)
        self.set_default_size(1024, 576)
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Desarrollo de Interfaces en Python con Gtk3"
        self.set_titlebar(header_bar)
        self.btnGenerar = Gtk.Button()
        icon = Gio.ThemedIcon(name="text-x-generic-template")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.btnGenerar.add(image)
        header_bar.pack_end(self.btnGenerar)
        self.btnGenerar.connect("clicked", self.on_btnGenerar_clicked)
        # Notebook
        self.notebook = Gtk.Notebook()
        # Primera página
        self.page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.page1.set_border_width(10)
        self.notebook.append_page(self.page1, Gtk.Label(label="Gestión de clientes"))
        # Caja vertical que representa la mitad superior
        cajaV1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # Caja horizontal que alberga los labels
        cajaH1_V1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lblIden = Gtk.Label(label="Identificación")
        lblNombre = Gtk.Label(label="Nombre")
        lblApel1 = Gtk.Label(label="Primer apellido")
        lblApel2 = Gtk.Label(label="Segundo apellido")
        lblTel = Gtk.Label(label="Teléfono")
        cajaH1_V1.pack_start(lblIden, True, True, 0)
        cajaH1_V1.pack_start(lblNombre, True, True, 0)
        cajaH1_V1.pack_start(lblApel1, True, True, 0)
        cajaH1_V1.pack_start(lblApel2, True, True, 0)
        cajaH1_V1.pack_start(lblTel, True, True, 0)
        # Caja horizontal que alberga los entries
        # Cajas horizontales que albergan labels
        cajaH2_V1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.txtIden = Gtk.Entry()
        self.txtNombre = Gtk.Entry()
        self.txtApel1 = Gtk.Entry()
        self.txtApel2 = Gtk.Entry()
        self.txtTel = Gtk.Entry()
        self.txtIden.set_placeholder_text("01234567A")
        self.txtNombre.set_placeholder_text("Juan")
        self.txtApel1.set_placeholder_text("González")
        self.txtApel2.set_placeholder_text("Rodríguez")
        self.txtTel.set_placeholder_text("987654321")
        cajaH2_V1.pack_start(self.txtIden, True, True, 0)
        cajaH2_V1.pack_start(self.txtNombre, True, True, 0)
        cajaH2_V1.pack_start(self.txtApel1, True, True, 0)
        cajaH2_V1.pack_start(self.txtApel2, True, True, 0)
        cajaH2_V1.pack_start(self.txtTel, True, True, 0)
        # Añadimos ambas cajas horizontales hijas a la cajaH1 vertical padre
        cajaV1.pack_start(cajaH1_V1, True, True, 0)
        cajaV1.pack_start(cajaH2_V1, True, True, 0)
        # Añadimos el conjunto a la página
        self.page1.pack_start(cajaV1, True, True, 0)
        # Justo debajo un botón para añadir clientes
        self.btnAñadir = Gtk.Button(label="Añadir cliente")
        self.page1.pack_start(self.btnAñadir, True, True, 0)
        # Genero el modelo que será el esqueleto para los datos recogidos de la BD. Simboliza la mitad inferior
        self.modelo = Gtk.ListStore(str, str, int)
        # Listo todos los clientes
        clientes = recargar()
        if clientes != 0:
            self.modelo.clear()
            for cliente in clientes:
                self.modelo.append([cliente[1], cliente[2] + " " + cliente[3] + " " + cliente[4], cliente[5]])
        # Caja horizontal que contendrá la tabla y una caja vertical para los botones
        cajaH1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vista = Gtk.TreeView(model=self.modelo)
        # Añado la tabla a la caja horizontal padre
        scrollTree = Gtk.ScrolledWindow()
        scrollTree.add(self.vista)
        cajaH1.pack_start(scrollTree, True, True, 0)
        # Caja vertical que contiene botones
        cajaV1_H1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.btnModificar = Gtk.Button(label="Modificar cliente")
        cajaV1_H1.pack_start(self.btnModificar, True, True, 0)
        self.btnEliminar = Gtk.Button(label="Eliminar cliente")
        cajaV1_H1.pack_start(self.btnEliminar, True, True, 0)
        # Añado la caja vertical hija a la caja horizontal padre
        cajaH1.pack_start(cajaV1_H1, True, True, 0)
        # Añado a continuacion la caja horizontal padre después de la caja vertical padre
        self.page1.pack_start(cajaH1, True, True, 0)
        # Estructura del Treeview:
        celdaText1 = Gtk.CellRendererText()
        celdaText1.props.xalign = 0.5
        colDni = Gtk.TreeViewColumn("Identificación", celdaText1, text=0)
        colDni.set_alignment(0.5)
        colDni.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        colDni.set_resizable(True)
        colDni.set_reorderable(True)
        colDni.set_sort_column_id(0)
        self.vista.append_column(colDni)
        celdaText2 = Gtk.CellRendererText()
        celdaText2.set_property("editable", True)
        celdaText2.props.xalign = 0.5
        celdaText2.connect("edited", self.on_celdaText2_edited)
        colNombre = Gtk.TreeViewColumn("Nombre completo", celdaText2, text=1)
        colNombre.set_alignment(0.5)
        colNombre.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        colNombre.set_resizable(True)
        colNombre.set_reorderable(True)
        colNombre.set_sort_column_id(1)
        self.vista.append_column(colNombre)
        celdaText3 = Gtk.CellRendererText()
        celdaText3.set_property("editable", True)
        celdaText3.props.xalign = 0.5
        celdaText3.connect("edited", self.on_celdaText3_edited)
        colTlf = Gtk.TreeViewColumn("Teléfono", celdaText3, text=2)
        colTlf.set_alignment(0.5)
        colTlf.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        colTlf.set_resizable(True)
        colTlf.set_reorderable(True)
        colTlf.set_sort_column_id(2)
        colDni.set_min_width(120)
        colDni.set_max_width(160)
        colNombre.set_min_width(200)
        colNombre.set_max_width(600)
        colTlf.set_min_width(50)
        colTlf.set_max_width(200)
        self.selection = self.vista.get_selection()
        self.vista.append_column(colTlf)
        # Conexiones
        self.selection.connect("changed", self.on_vista_changed)
        self.btnAñadir.connect("clicked", self.on_btnAñadir_clicked)
        self.btnModificar.connect("clicked", self.on_btnModificar_clicked)
        self.btnEliminar.connect("clicked", self.on_btnEliminar_clicked)
        self.connect("destroy", Gtk.main_quit)
        self.add(self.notebook)
        self.show_all()

    def on_celdaText2_edited(self, widget, path, text):
        """ Comprueba si el nombre del cliente que se ha modificado se corresponden con un nombre completo.
                    Parámetros:
                        :param path -- Recibe la referencia del modelo.
                        :param text -- Recibe el texto del campo que se ha modificado.
                    Devoluciones:
                        No tiene.
                    Excepciones:
                        No tiene.
        """
        campos = text.split()
        if len(campos) == 3:
            self.modelo[path][1] = text
        else:
            dialogo(1, "Porfavor, introduzca el nombre completo.")

    def on_celdaText3_edited(self, widget, path, text):
        """ Comprueba si el teléfono que se ha modificado tiene el formato correcto.
                    Parámetros:
                        :param path -- Recibe la referencia del modelo.
                        :param text -- Recibe el texto del campo que se ha modificado.
                    Devoluciones:
                        No tiene.
                    Excepciones:
                        OverflowError
                        ValueError
        """
        try:
            self.modelo[path][2] = int(text)
        except(OverflowError, ValueError) as error:
            print(error)
            dialogo(1, "Porfavor, introduzca un número de teléfono válido.")

    def on_vista_changed(self, selection):
        """ Obtiene la selección del cliente actual.
                    Parámetros:
                        :param selection -- Recibe la referencia de la selección actual en el modelo.
                    Devoluciones:
                        No tiene.
                    Excepciones:
                        No tiene.
        """
        (model, iter) = selection.get_selected()

    def on_btnAñadir_clicked(self, button):
        """ Obtiene los datos del formulario y se conecta a la base de datos para realizar la inserción de un nuevo cliente.
                    Parámetros:
                        No tiene.
                    Devoluciones:
                        No tiene.
                    Excepciones:
                        dbapi2.DatabaseError
        """
        iden = self.txtIden.get_text()
        nombre = self.txtNombre.get_text()
        apel1 = self.txtApel1.get_text()
        apel2 = self.txtApel2.get_text()
        tel = self.txtTel.get_text()
        if validar(iden, nombre, apel1, apel2, tel):
            try:
                bd = dbapi2.connect(base)
                cursor = bd.cursor()
                cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('" + iden + "', '" + nombre + "', '" + apel1 + "', '" + apel2 + "', " + tel + ")")
                bd.commit()
                # self.modelo.append([iden, nombre + " " + apel1 + " " + apel2, int(tel)])
                clientes = recargar()
                if clientes != 0:
                    self.modelo.clear()
                    for cliente in clientes:
                        self.modelo.append([cliente[1], cliente[2] + " " + cliente[3] + " " + cliente[4], cliente[5]])
            except(dbapi2.DatabaseError) as error:
                print(error)
                dialogo(0, "Ha habido un problema con la base de datos.")
            finally:
                cursor.close()
                bd.close()

    def on_btnModificar_clicked(self, button):
        """ Obtiene los datos de clientes que se hayan modificado y se conecta a la base de datos para realizar la modificación pertinente.
                    Parámetros:
                        No tiene.
                    Devoluciones:
                        No tiene.
                    Excepciones:
                        dbapi2.DatabaseError
        """
        if len(self.modelo) != 0:
            (model, iter) = self.selection.get_selected()
            if iter is not None:
                askDiag = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO, text="Pregunta")
                askDiag.format_secondary_text("¿Está seguro/a de que desea modificar este cliente?")
                if askDiag.run() == Gtk.ResponseType.YES:
                    try:
                        iden = model[iter][0]
                        nombre = model[iter][1]
                        lista = nombre.split()
                        tel = model[iter][2]
                        bd = dbapi2.connect(base)
                        cursor = bd.cursor()
                        cursor.execute(
                            "UPDATE clientes SET name='" + lista[0] + "', apel1='" + lista[1] + "', apel2='" +
                            lista[2] + "', tlf=" + str(tel) + " WHERE dni='" + iden + "'")
                        bd.commit()
                        clientes = recargar()
                        if clientes != 0:
                            self.modelo.clear()
                            for cliente in clientes:
                                self.modelo.append(
                                    [cliente[1], cliente[2] + " " + cliente[3] + " " + cliente[4], cliente[5]])
                        dialogo(2, "Se ha modificado el cliente satisfactoriamente.")
                    except(dbapi2.DatabaseError) as error:
                        print(error)
                        dialogo(0, "Ha habido un problema con la base de datos.")
                    finally:
                        cursor.close()
                        bd.close()
                askDiag.destroy()
            else:
                dialogo(1, "Porfavor, seleccione primero un cliente para poder modificarlo.")
        else:
            dialogo(1, "No existen clientes para modificar.")

    def on_btnEliminar_clicked(self, button):
        """ Obtiene los datos del cliente que se haya seleccionado y se conecta a la base de datos para realizar la eliminación del mismo.
                    Parámetros:
                        No tiene.
                    Devoluciones:
                        No tiene.
                    Excepciones:
                        dbapi2.DatabaseError
        """
        if len(self.modelo) != 0:
            (model, iter) = self.selection.get_selected()
            if iter is not None:
                askDiag = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO, text="Pregunta")
                askDiag.format_secondary_text("¿Está seguro/a de que desea eliminar este cliente?")
                if askDiag.run() == Gtk.ResponseType.YES:
                    eliminar(self.modelo[iter][0])
                    clientes = recargar()
                    if clientes != 0:
                        self.modelo.clear()
                        for cliente in clientes:
                            self.modelo.append(
                                [cliente[1], cliente[2] + " " + cliente[3] + " " + cliente[4], cliente[5]])
                askDiag.destroy()
            else:
                dialogo(1, "Porfavor, seleccione primero un cliente para poder eliminarlo.")
        else:
            dialogo(1, "No existen clientes para eliminar.")

    def on_btnGenerar_clicked(self, button):
        """ Llama a los scripts que generan los listados de clientes y productos.
                    Parámetros:
                        No tiene.
                    Devoluciones:
                        No tiene.
                    Excepciones:
                        No tiene.
        """
        GenerarClientes()
        GenerarProductos()


if __name__ == "__main__":
    Ventana()
    Gtk.main()