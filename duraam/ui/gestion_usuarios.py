# gestion_herramientas.py: la gestión de herramientas. Contiene una tabla, que muestra 
#                          la tabla de la base de datos; una barra de buscador; botones para 
#                          ordenar alfabéticamente la tabla por nombre, grupo y subgrupo de 
#                          herramientas; botones para editar y eliminar los datos; un botón
#                          para agregar herramientas. 
#                          Para editar y agregar, aparece un submenú con los datos a introducir.

# Se importan las librerías.
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

# Se importa la función m.mostrarMensaje.
import db.inicializar_bbdd as db
import mostrar_mensaje as m
from registrar_cambios import registrarCambios


# clase GestiónHerramientas: ya explicada. Es un widget que después se ensambla en un stackwidget en main.py.
class GestionDeUsuarios(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        self.titulo=qtw.QLabel("Gestión de usuarios")
        self.titulo.setObjectName("titulo")

        # Se crea la tabla.
        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")

        # Se crean los títulos de las columnas de la tabla y se introducen en esta.
        self.campos = ["Usuario", "Nombre y Apellido", "", ""]      
                                
        # Se establece el número de columnas que va a tener. 
        self.tabla.setColumnCount(len(self.campos))
        # Se introducen los títulos en la tabla.
        self.tabla.setHorizontalHeaderLabels(self.campos)

        # Se esconden los números de fila de la tabla que vienen por defecto para evitar confusión con el campo ID.
        self.tabla.verticalHeader().hide()
        # Se cambia el ancho de las dos últimas columnas, porque son las que van a tener los botones de editar y eliminar.
        self.tabla.setColumnWidth(1, 125)
        self.tabla.setColumnWidth(2, 35)
        self.tabla.setColumnWidth(3, 35)

        # Se muestran los datos.
        self.mostrarDatos()

        # Se crea el layout y se le añaden todos los widgets anteriores.
        layout = qtw.QGridLayout()
        layout.addWidget(self.titulo, 0, 0)
        layout.addWidget(self.tabla, 1, 0, 1, 9)

        # Se le da el layout al widget central
        self.setLayout(layout)


# Función mostrar datos: busca los datos de la tabla de la base de datos y los muestra en la tabla con la que el usuario puede interactuar. Parámetro:
    # - consulta: muestra los datos de forma distinta según el tipo de consulta. Es opcional y, si no se introduce, su valor por defecto es normal. Valores:
    # - - Normal: valor por defecto. Muestra todos los datos de la tabla de la base de datos.
    # - - Buscar: Busca en la tabla de la base de datos las filas que contengan lo buscado.
    # - - Nombre: Muestra todos los datos de la tabla de la base de datos ordenados por su nombre.
    # - - Grupo: Muestra todos los datos de la tabla de la base de datos ordenados por su grupo.
    # - - Subgrupo: Muestra todos los datos de la tabla de la base de datos ordenados por su subgrupo.
    def mostrarDatos(self):
        db.cur.execute("SELECT usuario, nombre_apellido FROM usuarioS")
        # Se guarda la consulta en una variable.
        consulta = db.cur.fetchall()

        # Se establece la cantidad de filas que va a tener la tabla
        self.tabla.setRowCount(len(consulta))
        # Bucle: por cada fila de la consulta obtenida, se guarda su id y se genera otro bucle que inserta todos los datos en la fila de la tabla de la ui.
        # Además, se insertan dos botones al costado de cada tabla: uno para editarla y otro para eliminarla.
        for i in range(len(consulta)):

            # Bucle: se introduce en cada celda el elemento correspondiente de la fila.
            for j in range(len(consulta[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(consulta[i][j])))

            self.tabla.setRowHeight(i, 35)

            # Se crea el boton de editar, se le da la función de editar y se lo introduce después de introducir los datos.
            botonHacerAdmin = qtw.QPushButton()
            botonHacerAdmin.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/ascender.png")))
            botonHacerAdmin.setIconSize(qtc.QSize(25, 25))
            botonHacerAdmin.setObjectName("aceptar")

            botonHacerAdmin.clicked.connect(lambda: self.hacerAdmin())
            botonHacerAdmin.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, len(self.campos)-2, botonHacerAdmin)

            # Se crea el boton de eliminar, se le da la función de eliminar la tabla con su id correspondiente y se introduce el boton al final de la fila.
            botonEliminar = qtw.QPushButton()
            botonEliminar.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/eliminar.png")))
            botonEliminar.setIconSize(qtc.QSize(25, 25))
            botonEliminar.setObjectName("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar())
            botonEliminar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, len(self.campos)-1, botonEliminar)

    def hacerAdmin(self):
        # se le pregunta al usuario si desea eliminar la fila.
        resp = m.mostrarMensaje("Pregunta", "Advertencia",
                              "¿Está seguro que desea eliminar estos datos?")
        # si pulsó el boton de sí:
        if resp == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            # luego se obtiene la posicion del boton.
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd=posicion.sibling(posicion.row(), 0).data()
            db.cur.execute("SELECT * FROM usuarioS WHERE usuario = ?", (idd,)) 
            datos=db.cur.fetchall()[0]
            db.cur.execute("INSERT INTO administradores VALUES (?, ?, ?, ?)", datos)
            db.cur.execute("DELETE FROM usuarioS WHERE usuario = ?", (datos[1],))
            registrarCambios("Ascenso", "Usuarios Administradores", datos[0], f"{datos}", f"{datos}")
            db.con.commit()
            self.mostrarDatos()

    def eliminar(self):
        # se le pregunta al usuario si desea eliminar la fila.
        resp = m.mostrarMensaje("Pregunta", "Advertencia",
                "¿Está seguro que desea eliminar el usuario? No podrá volver a acceder al sistema.")
        # si pulsó el boton de sí:
        if resp == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            # luego se obtiene la posicion del boton.
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd=posicion.sibling(posicion.row(), 0).data()
            # elimina la fila con el id correspondiente de la tabla de la base de datos.
            db.cur.execute("SELECT * FROM usuarioS WHERE ID = ?", (idd,))
            datosEliminados=db.cur.fetchall()[0]
            db.cur.execute("DELETE FROM usuarioS WHERE usuario = ?", (idd,))
            registrarCambios("Eliminación simple", "Usuarios", idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()