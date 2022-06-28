import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import sqlite3 as db
import os

from pantallas.gestion_herramientas import GestionHerramientas
from pantallas.gestion_herramientas2 import GestionHerramientas1
from cabecera import Cabecera
from menu_izquierdo import MenuIzquierdo

os.chdir(f"{os.path.abspath(__file__)}/../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()

# Creamos la ventana principal
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 1024)

        # Se crea el título (el nombre de la app que va al lado del logo en la barra superior).
        cabecera=Cabecera()
        cabecera.setObjectName("cabecera")
        menuIzquierdo=MenuIzquierdo()
        
        # Creamos la colección de pantallas
        stack = qtw.QStackedWidget()

        self.herramientas=GestionHerramientas()
        self.prueba=GestionHerramientas1()
        
        self.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, cabecera)
        self.addToolBar(qtc.Qt.ToolBarArea.LeftToolBarArea, menuIzquierdo)

        # Añadimos las pantallas a la colección
        for i in [self.herramientas, self.prueba]:
            stack.addWidget(i)
        
        menuIzquierdo.gestion1.toggled.connect(lambda:stack.setCurrentIndex(0))
        menuIzquierdo.gestion2.toggled.connect(lambda:stack.setCurrentIndex(1))

        # Añadimos la colección a la ventana
        self.setCentralWidget(stack)
        stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/gestion.qss", 'r') as qss:
        app.setStyleSheet(qss.read())
    window.show()
    app.exec()
