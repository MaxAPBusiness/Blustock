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

from crypt import encriptar, decriptar
from mostrar_mensaje import mostrarMensaje

from ui.cabecera import Cabecera
from ui.menu_izquierdo import MenuIzquierdo

from ui.iniciarSesion import IniciarSesion
from ui.registrarse import Registrarse
from ui.gestion_movimientos_herramientas import GestionMovimientosHerramientas
from ui.gestion_herramientas import GestionHerramientas
from ui.gestion_turnos import GestionTurnos
from ui.gestion_alumnos import GestionAlumnos
from ui.gestion_profesores import GestionProfesores
from ui.gestion_grupos import GestionGrupos
from ui.gestion_subgrupos import GestionSubgrupos

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
        self.menuIzquierdo=MenuIzquierdo()
        
        # Creamos la colección de pantallas
        self.stack = qtw.QStackedWidget()

        self.iniciarSesion=IniciarSesion()
        self.registrarse=Registrarse()
        self.herramientas=GestionHerramientas()
        self.movimientos=GestionMovimientosHerramientas()
        self.turnos=GestionTurnos()
        self.alumnos=GestionAlumnos()
        self.profesores=GestionProfesores()
        self.grupos=GestionGrupos()
        self.subgrupos=GestionSubgrupos()

        self.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, cabecera)

        # Añadimos las pantallas a la colección
        for i in [self.iniciarSesion, self.registrarse, self.herramientas, self.movimientos, self.turnos, self.alumnos,self.profesores, self.grupos, self.subgrupos]:
            self.stack.addWidget(i)

        self.iniciarSesion.registrarse.toggled.connect(lambda:self.stack.setCurrentIndex(1))
        self.iniciarSesion.confirmar.toggled.connect(lambda:self.confirmarInicio())

        self.registrarse.ingresar.toggled.connect(lambda:self.stack.setCurrentIndex(0))
        self.registrarse.confirmar.toggled.connect(lambda:self.registrarse)

        self.menuIzquierdo.gestion1.toggled.connect(lambda:self.stack.setCurrentIndex(2))
        self.menuIzquierdo.gestion2.toggled.connect(lambda:self.stack.setCurrentIndex(3))
        self.menuIzquierdo.gestion3.toggled.connect(lambda:self.stack.setCurrentIndex(4))
        self.menuIzquierdo.gestion4.toggled.connect(lambda:self.stack.setCurrentIndex(5))
        self.menuIzquierdo.gestion5.toggled.connect(lambda:self.stack.setCurrentIndex(6))
        self.menuIzquierdo.gestion6.toggled.connect(lambda:self.stack.setCurrentIndex(7))
        self.menuIzquierdo.gestion7.toggled.connect(lambda:self.stack.setCurrentIndex(8))
        # Añadimos la colección a la ventana
        self.setCentralWidget(self.stack)
        self.stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding,)
    
    def closeEvent(self, event):
        global app
        app.closeAllWindows()
    
            
    def confirmarInicio(self):
        truePass = decriptar(self.iniciarSesion.entry2.text())

        cur.execute("SELECT USUARIO, CONTRASENA, NOMBRE_APELLIDO FROM USUARIOS WHERE USUARIO=? AND CONTRASENA=?", (self.iniciarSesion.entry1.text(), truePass))
        query=cur.fetchall()
        if query:
            self.addToolBar(qtc.Qt.ToolBarArea.LeftToolBarArea, self.menuIzquierdo)
            self.stack.setCurrentIndex(2)
            mostrarMensaje("Aviso", "Aviso", f"Ha ingresado con éxito. Bienvenido, {query[0][2]}.")
        else: 
            mostrarMensaje("Advertencia", "Error",
            "El usuario y la contraseña no coinciden. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")
    
    def registrarse(self):
        if self.registrarse.entry3.text() == self.registrarse.entry4.text():
            cur.execute("SELECT USUARIO FROM USUARIOS WHERE USUARIO=?", (self.registrarse.entry2.text(),))
            if cur.fetchall():
                mostrarMensaje("Error", "Error", "El usuario ya está ingresado. Por favor, ingrese los datos nuevamente.")
                return

            cur.execute("SELECT * FROM USUARIOS")
            if cur.fetchall():
                cur.execute('INSERT INTO SOLICITUDES VALUES (?, ?, ?, "Pendiente")', 
                (self.registrarse.entry2.text(), self.registrarse.entry3.text(), self.registrarse.entry1.text(),))
                mostrarMensaje("Aviso", "Información", 
                "El registro se realizó correctamente. Recuerde que el administrador debe verificar su registro para que su usuario esté habilitado y pueda acceder.")
            else:
                cur.execute("INSERT INTO USUARIOS VALUES(NULL, ?, ?, ?)", 
                (self.registrarse.entry2.text(), self.registrarse.entry3.text(), self.registrarse.entry1.text(),))
                mostrarMensaje("Aviso", "Información", "El registro se realizó correctamente.")
            con.commit()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/gestion.qss", 'r') as qss:
        app.setStyleSheet(qss.read())
    window.show()
    app.exec()