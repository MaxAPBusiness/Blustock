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
import sqlite3 as db
import os

# Se importa la función mostrarMensaje.
from mostrar_mensaje import mostrarMensaje

# Se hace una conexión a la base de datos
os.chdir(f"{os.path.abspath(__file__)}/../../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()


# clase GestiónHerramientas: ya explicada. Es un widget que después se ensambla en un stackwidget en main.py.
class Solicitudes(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        self.titulo=qtw.QLabel("Solicitudes de usuario")
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
        cur.execute("SELECT USUARIO, nombre_apellido FROM SOLICITUDES WHERE ESTADO='Pendiente'")
        # Se guarda la consulta en una variable.
        consulta = cur.fetchall()

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
            botonAceptar = qtw.QPushButton()
            botonAceptar.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/aceptar.png")))
            botonAceptar.setIconSize(qtc.QSize(25, 25))
            botonAceptar.setObjectName("aceptar")

            botonAceptar.clicked.connect(lambda: self.aceptar(consulta[i][0]))
            botonAceptar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, len(self.campos)-2, botonAceptar)

            # Se crea el boton de eliminar, se le da la función de eliminar la tabla con su id correspondiente y se introduce el boton al final de la fila.
            botonRechazar = qtw.QPushButton()
            botonRechazar.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/rechazar.png")))
            botonRechazar.setIconSize(qtc.QSize(25, 25))
            botonRechazar.setObjectName("rechazar")
            botonRechazar.clicked.connect(lambda: self.rechazar(consulta[i][0]))
            botonRechazar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, len(self.campos)-1, botonRechazar)

    def aceptar(self, idd):
                # se obtiene la función definida fuera de la clase.
        global mostrarMensaje
        # se le pregunta al usuario si desea eliminar la fila.
        resp = mostrarMensaje("Pregunta", "Advertencia",
"¿Está seguro que desea aceptar la solicitud? El usuario podrá acceder a todas las bases de datos.")
        if resp == qtw.QMessageBox.StandardButton.Yes:
            cur.execute("SELECT USUARIO, CONTRASENA, nombre_apellido FROM SOLICITUDES WHERE USUARIO = ?", (idd,)) 
            datos=cur.fetchall()
            cur.execute("INSERT INTO USUARIOS VALUES (NULL, ?, ?, ?)", datos[0])
            cur.execute("DELETE FROM SOLICITUDES WHERE USUARIO = ?", (datos[0][0],))
            con.commit()
            self.mostrarDatos()

    def rechazar(self, idd):
        # se obtiene la función definida fuera de la clase.
        global mostrarMensaje
        # se le pregunta al usuario si desea eliminar la fila.
        resp = mostrarMensaje("Pregunta", "Advertencia",
                              "¿Está seguro que desea rechazar la solicitud?")
        # si pulsó el boton de sí:
        if resp == qtw.QMessageBox.StandardButton.Yes:
            cur.execute("UPDATE SOLICITUDES SET ESTADO='Rechazado' WHERE USUARIO = ?", (idd,))
            con.commit()
            self.mostrarDatos()
