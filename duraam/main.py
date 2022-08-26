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
from ui.gestion_registro_alumnos_historicos import GestionRegistroAlumnosHistoricos
from ui.gestion_registro_profesores_historicos import GestionRegistroProfesoresHistoricos

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
        self.cabecera=Cabecera()
        self.cabecera.usuario.hide()
        self.cabecera.setObjectName("cabecera")
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
        self.alumnosHistoricos=GestionRegistroAlumnosHistoricos()
        self.profesoresHistoricos=GestionRegistroProfesoresHistoricos()

        self.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.cabecera)

        # Añadimos las pantallas a la colección
        pantallas=[self.iniciarSesion, self.registrarse, self.herramientas, self.movimientos, 
                    self.turnos, self.alumnos, self.profesores, self.grupos, self.subgrupos, 
                    self.alumnosHistoricos, self.profesoresHistoricos]
        for i in pantallas:
            self.stack.addWidget(i)

        self.iniciarSesion.registrarse.clicked.connect(lambda:self.stack.setCurrentIndex(1))
        self.iniciarSesion.confirmar.clicked.connect(lambda:self.confirmarInicio())

        self.registrarse.ingresar.clicked.connect(lambda:self.stack.setCurrentIndex(0))
        self.registrarse.confirmar.clicked.connect(lambda:self.registrar())

        self.menuIzquierdo.gestion1.toggled.connect(lambda:self.stack.setCurrentIndex(2))
        self.menuIzquierdo.gestion2.toggled.connect(lambda:self.stack.setCurrentIndex(3))
        self.menuIzquierdo.gestion3.toggled.connect(lambda:self.stack.setCurrentIndex(4))
        self.menuIzquierdo.gestion4.toggled.connect(lambda:self.stack.setCurrentIndex(5))
        self.menuIzquierdo.gestion5.toggled.connect(lambda:self.stack.setCurrentIndex(6))
        self.menuIzquierdo.gestion6.toggled.connect(lambda:self.stack.setCurrentIndex(7))
        self.menuIzquierdo.gestion7.toggled.connect(lambda:self.stack.setCurrentIndex(8))
        self.menuIzquierdo.gestion8.toggled.connect(lambda:self.stack.setCurrentIndex(9))
        self.menuIzquierdo.gestion9.toggled.connect(lambda:self.stack.setCurrentIndex(10))
        # Añadimos la colección a la ventana
        self.setCentralWidget(self.stack)
        self.stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding,)
    
    def closeEvent(self, event):
        global app
        app.closeAllWindows()
    
            
    def confirmarInicio(self):
        cur.execute("SELECT USUARIO, CONTRASENA, NOMBRE_APELLIDO FROM USUARIOS WHERE USUARIO=?", (self.iniciarSesion.entry1.text(),))
        query=cur.fetchall()
        if not query:
            return mostrarMensaje("Advertencia", "Error",
            "El usuario no está registrado. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")
        try:
            if decriptar(query[0][1].encode('utf-8')) == self.iniciarSesion.entry2.text():
                mostrarMensaje("Aviso", "Aviso", f"Ha ingresado con éxito. Bienvenido, {query[0][2]}.")
                self.addToolBar(qtc.Qt.ToolBarArea.LeftToolBarArea, self.menuIzquierdo)
                self.stack.setCurrentIndex(2)
                self.cabecera.usuario.show()
                return
            else:
                return mostrarMensaje("Advertencia", "Error",
                "El usuario y la contraseña no coinciden. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")
        except AttributeError as e:
            print(e)
            return mostrarMensaje("Advertencia", "Error",
            "La contraseña es incorrecta. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")

    
    def registrar(self):
        if len(self.registrarse.entry2.text()) < 8:
            return mostrarMensaje("Error", "Aviso", "El usuario es demasiado corto. Por favor, ingrese uno más largo.")
        elif len(self.registrarse.entry3.text()) < 8:
            return mostrarMensaje("Error", "Aviso", "La contraseña es demasiado corta. Por favor, ingrese una más larga.")
        elif self.registrarse.entry3.text() != self.registrarse.entry4.text():
            return mostrarMensaje("Error", "Aviso", "Las contraseñas no coinciden. Por favor, revise los datos e ingrese nuevamente.")

        cur.execute("SELECT USUARIO FROM USUARIOS WHERE USUARIO=?", (self.registrarse.entry2.text(),))
        if cur.fetchall():
            return mostrarMensaje("Error", "Error", "El usuario ya está ingresado. Por favor, ingrese los datos nuevamente.")

        cur.execute("SELECT * FROM USUARIOS")
        password=encriptar(self.registrarse.entry3.text())
        if cur.fetchall():
            cur.execute('INSERT INTO SOLICITUDES VALUES (?, ?, ?, "Pendiente")', 
            (self.registrarse.entry2.text(), password, self.registrarse.entry1.text().upper(),))
            mostrarMensaje("Aviso", "Información", 
            "El registro se realizó correctamente. Recuerde que el administrador debe verificar su registro para que su usuario esté habilitado y pueda acceder.")
        else:
            cur.execute("INSERT INTO USUARIOS VALUES(NULL, ?, ?, ?)", 
            (self.registrarse.entry2.text(), password, self.registrarse.entry1.text().upper(),))
        con.commit()
        mostrarMensaje("Aviso", "Información", "El registro se realizó correctamente.")


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/gestion.qss", 'r') as qss:
        app.setStyleSheet(qss.read())
    window.show()
    app.exec()