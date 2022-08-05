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
import datetime as dt

os.chdir(f"{os.path.abspath(__file__)}/../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()

# Importamos las pantallas y el codigo de BD
from db.db import crearBBDD
from ui.cabecera import Cabecera
from gestiones_panol.inicio import Inicio

# Se crea la base de datos
crearBBDD()

# Creamos la ventana principal
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 1024)
        self.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))
        # Se crea el título (el nombre de la app que va al lado del logo en la barra superior).
        cabecera=Cabecera()
        cabecera.setObjectName("cabecera")
        self.inicio=Inicio()
        # Creamos la colección de pantallas
        stack = qtw.QStackedWidget()

        self.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, cabecera)

        self.inicio.confirmar.clicked.connect(lambda:self.confirmar())
        # Añadimos las pantallas a la colección
        for i in [self.inicio]:
            stack.addWidget(i)
 
        # Añadimos la colección a la ventana
        self.setCentralWidget(stack)
        stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding,)

    def confirmar(self):
        fecha=dt.date.today()
        fecha.replace("-", "/")
        hora=dt.datetime.now().strftime("%H:%M")
        cur.execute("INSERT INTO TURNO_PANOL VALUES(NULL, ?, ?, ?, NULL, ?, NULL)", (fecha, self.inicio.alumno.currentText(), hora, self.inicio.profesor.currentText()))
        con.commit()
        cur.execute("SELECT ID FROM TURNO_PANOL ORDER BY ID DESC LIMIT 1")
        self.id=cur.fetchall()[0][0]



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/gestion.qss", 'r') as qss:
        app.setStyleSheet(qss.read())
    window.show()
    app.exec()