# main.py: es el archivo principal, que ensambla todo el código y lo ejecuta. 
# Lo que hace, en detalle, lo siguiente:
# 1. Crea la base de datos (si no estaba creada antes) con la función crearBBDD de db.py.
# 2. Crea la ventana principal del programa:
#     2.1: Crea tres secciones dentro de la ventana: 
#     2.1.1: la cabecera, que importa de cabecera.py.
#     2.1.2: el menú izquierdo, que permite navegar por las gestiones de la pantalla principal.
#            de menu_izquierdo.py
#     2.1.3: la pantalla principal, que contiene todas las gestiones. Para hacerla, importa todas
#            las gestiones de la ui.
# 3. Importa y establece los estilos de la gestion.
# 4. Ejecuta la ventana.

# Importamos las librerías
import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import sqlite3 as db
import os

# Importamos las pantallas y el codigo de BD
from db.db import crearBBDD
from ui.gestion_movimientos_herramientas import GestionMovimientosHerramientas
from ui.gestion_herramientas import GestionHerramientas
from ui.gestion_herramientas2 import GestionHerramientas1
from ui.gestion_turnos import GestionTurnos
from ui.cabecera import Cabecera
from ui.menu_izquierdo import MenuIzquierdo
from ui.gestion_alumnos import GestionAlumnos
from ui.gestion_profesores import GestionProfesores

# Se crea la base de datos
crearBBDD()

os.chdir(f"{os.path.abspath(__file__)}/../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()

# Creamos la ventana principal
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 1024)
        self.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))
        # Se crea el título (el nombre de la app que va al lado del logo en la barra superior).
        cabecera=Cabecera()
        cabecera.setObjectName("cabecera")
        menuIzquierdo=MenuIzquierdo()
        
        # Creamos la colección de pantallas
        stack = qtw.QStackedWidget()

        self.herramientas=GestionHerramientas()
        self.prueba=GestionHerramientas1()
        self.movimientos=GestionMovimientosHerramientas()
        self.turnos=GestionTurnos()
        self.alumnos=GestionAlumnos()
        self.profesores=GestionProfesores()

        self.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, cabecera)
        self.addToolBar(qtc.Qt.ToolBarArea.LeftToolBarArea, menuIzquierdo)

        # Añadimos las pantallas a la colección
        for i in [self.herramientas, self.movimientos, self.turnos, self.alumnos,self.profesores]:
            stack.addWidget(i)
        
        menuIzquierdo.gestion1.toggled.connect(lambda:stack.setCurrentIndex(0))
        menuIzquierdo.gestion2.toggled.connect(lambda:stack.setCurrentIndex(1))
        menuIzquierdo.gestion3.toggled.connect(lambda:stack.setCurrentIndex(2))
        menuIzquierdo.gestion4.toggled.connect(lambda:stack.setCurrentIndex(3))
        menuIzquierdo.gestion5.toggled.connect(lambda:stack.setCurrentIndex(4))
        # Añadimos la colección a la ventana
        self.setCentralWidget(stack)
        stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding,)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/gestion.qss", 'r') as qss:
        app.setStyleSheet(qss.read())
    window.show()
    app.exec()