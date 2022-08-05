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
import datetime as dt

# Se importa la función mostrarMensaje.
from mostrar_mensaje import mostrarMensaje
from cursos import cursos
# Se hace una conexión a la base de datos
os.chdir(f"{os.path.abspath(__file__)}/../../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()


# clase GestiónHerramientas: ya explicada. Es un widget que después se ensambla en un stackwidget en main.py.
class Inicio(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        titulo=qtw.QLabel("""
        Bienvenido al sistema de gestión del pañol!
        Ingrese el pañolero.
        """)
        titulo.setObjectName("titulo") 
        label1=qtw.QLabel("Curso: ")
        label2=qtw.QLabel("Alumno: ")
        self.curso=qtw.QComboBox()
        self.curso.addItems(cursos)
        self.curso.currentIndexChanged.connect(lambda:self.busquedaAlumnos())
        self.alumno=qtw.QComboBox()
        self.busquedaAlumnos()
        self.confirmar=qtw.QPushButton("confirmar")
        layout=qtw.QGridLayout()
        layout.addWidget(titulo, 0, 0, 1, 2)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(self.curso, 1, 1)
        layout.addWidget(self.alumno, 2, 1)
        layout.addWidget(self.confirmar, 3, 1, 1, 2)
        self.setLayout(layout)
        
    def busquedaAlumnos(self):
        cur.execute("SELECT NOMBRE_APELLIDO FROM ALUMNOS WHERE CURSO=?", (self.curso.currentText(),))
        a=cur.fetchall()
        for i in a:
            for j in i:
                 self.alumno.addItem(j)
