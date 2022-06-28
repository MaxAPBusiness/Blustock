import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import sqlite3 as db
import os
from gestion_herramientas import GestionHerramientas
from gestion_herramientas2 import GestionHerramientas1
try:
    con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
except:
    os.chdir("../../..")
    con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")

cur=con.cursor()

# Creamos la ventana principal
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 1024)

        menuIzquierdo = qtw.QToolBar()
        menuIzquierdo.setOrientation(qtc.Qt.Orientation.Vertical)
        menuIzquierdo.addWidget(qtw.QLineEdit())
        menuIzquierdo.setFloatable(False)
        menuIzquierdo.setMovable(False)
        menuIzquierdo.addWidget(qtw.QLabel("Gestiones"))
        gestion1=qtw.QRadioButton('Gestión de herramientas')
        gestion2=qtw.QRadioButton('Gestión de herramientas (DUPLICADO)')
        menuIzquierdo.addWidget(gestion1)
        menuIzquierdo.addWidget(gestion2)
        # Creamos la colección de pantallas
        stack = qtw.QStackedWidget()

        self.herramientas=GestionHerramientas()
        self.prueba=GestionHerramientas1()
        
        self.addToolBar(qtc.Qt.ToolBarArea.LeftToolBarArea, menuIzquierdo)

        # Añadimos las pantallas a la colección
        for i in [self.herramientas, self.prueba]:
            stack.addWidget(i)
        
        gestion1.toggled.connect(lambda:stack.setCurrentIndex(0))
        gestion2.toggled.connect(lambda:stack.setCurrentIndex(1))

        # Añadimos la colección a la ventana
        self.setCentralWidget(stack)
        stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/gestion.qss", 'r') as css:
        window.setStyleSheet(css.read())
    window.show()
    app.exec()
