#Para ahorrar selfs, pasa los datos como argumentos en vez de hacerlos globales




















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
import os

# Importamos las pantallas y el codigo de BD
import db.inicializar_bbdd as db
from crypt import encriptar, decriptar
import mostrar_mensaje as m
import registrar_cambios as rc


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
from ui.solicitudes import Solicitudes
from ui.gestion_usuarios import GestionDeUsuarios
from ui.gestion_administradores import GestionDeAdministradores
from ui.historial_de_cambios import HistorialDeCambios

# Creamos la ventana principal


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 1024)
        self.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))

        # Se crea el título (el nombre de la app que va al lado del logo en la barra superior).
        self.cabecera = Cabecera()
        self.cabecera.setObjectName("cabecera")

        self.menuIzquierdo = MenuIzquierdo()
        self.menuIzquierdo.setFixedWidth(300)

        self.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.cabecera)
        self.addToolBar(qtc.Qt.ToolBarArea.LeftToolBarArea, self.menuIzquierdo)

        self.menuIzquierdo.toggleViewAction().setChecked(False)
        self.menuIzquierdo.toggleViewAction().trigger()
        self.menuIzquierdo.toggleViewAction().trigger()

        # Creamos la colección de pantallas
        self.stack = qtw.QStackedWidget()

        self.iniciarSesion = IniciarSesion()
        self.registrarse = Registrarse()
        self.herramientas = GestionHerramientas()
        self.movimientos = GestionMovimientosHerramientas()
        self.turnos = GestionTurnos()
        self.alumnos = GestionAlumnos()
        self.profesores = GestionProfesores()
        self.grupos = GestionGrupos()
        self.subgrupos = GestionSubgrupos()
        self.alumnosHistoricos = GestionRegistroAlumnosHistoricos()
        self.profesoresHistoricos = GestionRegistroProfesoresHistoricos()
        self.solicitudes= Solicitudes()
        self.usuarios= GestionDeUsuarios()
        self.administradores=GestionDeAdministradores()
        self.historialDeCambios=HistorialDeCambios()

        # Añadimos las pantallas a la colección
        self.pantallas = [
            self.iniciarSesion, self.registrarse, self.herramientas, self.movimientos,
            self.turnos, self.alumnos, self.profesores, self.grupos, self.subgrupos,
            self.alumnosHistoricos, self.profesoresHistoricos, self.solicitudes, self.usuarios,
            self.administradores, self.historialDeCambios
                    ]
        for i in self.pantallas:
            self.stack.addWidget(i)

        self.iniciarSesion.registrarse.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.iniciarSesion.confirmar.clicked.connect(lambda: self.confirmarInicio())
        self.iniciarSesion.entry2.returnPressed.connect(lambda: self.confirmarInicio())

        self.registrarse.ingresar.clicked.connect(
            lambda: self.stack.setCurrentIndex(0))
        self.registrarse.confirmar.clicked.connect(lambda: self.registrar())

        self.menuIzquierdo.gestion1.toggled.connect(lambda: self.cambiarPantalla(2))
        self.menuIzquierdo.gestion2.toggled.connect(lambda: self.cambiarPantalla(3))
        self.menuIzquierdo.gestion3.toggled.connect(lambda: self.cambiarPantalla(4))
        self.menuIzquierdo.gestion4.toggled.connect(lambda: self.cambiarPantalla(5))
        self.menuIzquierdo.gestion5.toggled.connect(lambda: self.cambiarPantalla(6))
        self.menuIzquierdo.gestion6.toggled.connect(lambda: self.cambiarPantalla(7))
        self.menuIzquierdo.gestion7.toggled.connect(lambda: self.cambiarPantalla(8))
        self.menuIzquierdo.gestion8.toggled.connect(lambda: self.cambiarPantalla(9))
        self.menuIzquierdo.gestion9.toggled.connect(lambda: self.cambiarPantalla(10))
        self.menuIzquierdo.gestion10.toggled.connect(lambda: self.cambiarPantalla(11))
        self.menuIzquierdo.gestion11.toggled.connect(lambda: self.cambiarPantalla(12))
        self.menuIzquierdo.gestion12.toggled.connect(lambda: self.cambiarPantalla(13))
        self.menuIzquierdo.gestion13.toggled.connect(lambda: self.cambiarPantalla(14))
        # Añadimos la colección a la ventana
        self.setCentralWidget(self.stack)
        self.stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding,)

    def cambiarPantalla(self, nro):
        self.pantallas[nro].mostrarDatos()
        self.stack.setCurrentIndex(nro)
    
    def closeEvent(self, event):
        global app
        app.closeAllWindows()

    def confirmarInicio(self):
        db.cur.execute("SELECT usuario, CONTRASENA, nombre_apellido FROM administradores WHERE usuario = ?",
                    (self.iniciarSesion.entry1.text(),))
        consulta = db.cur.fetchall()
        if consulta:
            try:
                truePass=consulta[0][1].encode()
            except:
                truePass=consulta[0][1]
            
            if decriptar(truePass) == self.iniciarSesion.entry2.text():
                m.mostrarMensaje(
                    "Aviso", "Aviso", f"Ha ingresado con éxito. Bienvenido, {consulta[0][2]}.")
                self.menuIzquierdo.toggleViewAction().trigger()
                self.cabecera.containerLayout.addWidget(self.cabecera.usuario)
                self.cabecera.usuario.clicked.connect(
                    lambda: self.informacionUsuario(consulta[0][2], consulta[0][0]))
                self.menuIzquierdo.containerLayout.addWidget(self.menuIzquierdo.gestion10, self.menuIzquierdo.contador+2, 0)
                self.menuIzquierdo.containerLayout.addWidget(self.menuIzquierdo.gestion11, self.menuIzquierdo.contador+3, 0)
                self.menuIzquierdo.containerLayout.addWidget(self.menuIzquierdo.gestion12, self.menuIzquierdo.contador+4, 0)
                self.stack.setCurrentIndex(2)
                rc.userInfo=[consulta[0][0], 1]
                self.iniciarSesion.entry1.setText("")
                self.iniciarSesion.entry2.setText("")
                return

        db.cur.execute("SELECT usuario, CONTRASENA, nombre_apellido FROM usuarioS WHERE usuario = ?",
                    (self.iniciarSesion.entry1.text(),))
        consulta = db.cur.fetchall()
        if consulta:
            try:
                truePass=consulta[0][1].encode()
            except:
                truePass=consulta[0][1]
            
            if decriptar(truePass) == self.iniciarSesion.entry2.text():
                m.mostrarMensaje(
                    "Aviso", "Aviso", f"Ha ingresado con éxito. Bienvenido, {consulta[0][2]}.")
                self.menuIzquierdo.toggleViewAction().trigger()
                self.cabecera.containerLayout.addWidget(self.cabecera.usuario)
                self.cabecera.usuario.clicked.connect(
                    lambda: self.informacionUsuario(consulta[0][2], consulta[0][0]))
                self.stack.setCurrentIndex(2)
                rc.userInfo=[consulta[0][0], 0]
                self.iniciarSesion.entry1.setText("")
                self.iniciarSesion.entry2.setText("")
                return
        
        db.cur.execute("SELECT usuario, CONTRASENA, ESTADO FROM SOLICITUDES WHERE usuario = ?",
                    (self.iniciarSesion.entry1.text(),))
        consulta = db.cur.fetchall()
        if consulta:
            try:
                truePass=consulta[0][1].encode()
            except:
                truePass=consulta[0][1]
            
            
            if decriptar(truePass) == self.iniciarSesion.entry2.text():
                if consulta[0][2]:
                    return m.mostrarMensaje("Advertencia", "Aviso", 
                "Su cuenta todavía no fue verificada. Por favor, espere a que su cuenta sea verificada. Si tiene inconvenientes, póngase en contacto con algún administrador.")
                else:
                    m.mostrarMensaje("Advertencia", "Aviso", 
                "La solicitud de registro de su cuenta fue rechazada. Si tiene algún inconveniente, póngase en contacto con algún administrador.")
                    db.cur.execute("DELETE FROM SOLICITUDES WHERE usuario = ?", (consulta[0][0],))
            else:
                return m.mostrarMensaje("Advertencia", "Error",
                                        "El usuario y la contraseña no coinciden. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")
        else:
            return m.mostrarMensaje("Advertencia", "Error",
                                  "El usuario no está registrado. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")
        
        

    def registrar(self):
        if len(self.registrarse.entry2.text()) < 8:
            return m.mostrarMensaje("Error", "Aviso", "El usuario es demasiado corto. Por favor, ingrese uno más largo.")
        elif len(self.registrarse.entry3.text()) < 8:
            return m.mostrarMensaje("Error", "Aviso", "La contraseña es demasiado corta. Por favor, ingrese una más larga.")
        elif self.registrarse.entry3.text() != self.registrarse.entry4.text():
            return m.mostrarMensaje("Error", "Aviso", "Las contraseñas no coinciden. Por favor, revise los datos e ingrese nuevamente.")

        db.cur.execute("SELECT usuario FROM usuarioS WHERE usuario = ?",
                    (self.registrarse.entry2.text(),))
        usuarioEncontrado=db.cur.fetchall()
        db.cur.execute("SELECT usuario FROM SOLICITUDES WHERE usuario = ?",
                    (self.registrarse.entry2.text(),))
        solicitudEncontrada=db.cur.fetchall()
        db.cur.execute("SELECT usuario FROM administradores WHERE usuario = ?",
                    (self.registrarse.entry2.text(),))
        adminEncontrado=db.cur.fetchall()
        if usuarioEncontrado or solicitudEncontrada or adminEncontrado:
            return m.mostrarMensaje("Error", "Error", "El usuario ya está ingresado. Por favor, ingrese un usuario distinto.")

        db.cur.execute("SELECT * FROM usuarioS")
        password = encriptar(self.registrarse.entry3.text())
        if db.cur.fetchall():
            db.cur.execute("INSERT INTO SOLICITUDES VALUES (?, ?, ?, 'Pendiente')",
                        (self.registrarse.entry2.text(), password, self.registrarse.entry1.text().upper(),))
            m.mostrarMensaje("Aviso", "Información",
                           "El registro se realizó correctamente. Recuerde que el administrador debe verificar su registro para que su usuario esté habilitado y pueda acceder.")
        else:
            db.cur.execute("INSERT INTO usuarioS VALUES(NULL, ?, ?, ?)",
                        (self.registrarse.entry2.text(), password, self.registrarse.entry1.text().upper(),))
        db.con.commit()
        m.mostrarMensaje("Aviso", "Información",
                       "El registro se realizó correctamente.")

    def informacionUsuario(self, nombre, usuario):
        menu = qtw.QMenu(self)
        menu.setObjectName("menu")
        nombre = qtw.QLabel(nombre)
        usuario = qtw.QLabel(usuario)
        botonCerrarSesion = qtg.QAction("Cerrar sesión")
        botonCerrarSesion.triggered.connect(lambda: self.cerrarSesion())
        botonSalir=qtg.QAction("Salir")
        botonSalir.triggered.connect(lambda: self.salir())
        insertarNombre = qtw.QWidgetAction(menu)
        insertarUsuario = qtw.QWidgetAction(menu)
        insertarNombre.setDefaultWidget(nombre)
        insertarUsuario.setDefaultWidget(usuario)
        menu.addAction(insertarNombre)
        menu.addAction(insertarUsuario)
        menu.addSeparator()
        menu.addAction(botonCerrarSesion)
        menu.addAction(botonSalir)

        menu.exec(qtg.QCursor.pos())

    def cerrarSesion(self):
        self.cabecera.usuario.clicked.disconnect()
        resp = m.mostrarMensaje("Pregunta", "Advertencia",
                              "¿Está seguro de que desea cerrar la sesión?")
        if resp==qtw.QMessageBox.StandardButton.Yes:
            self.cabecera.usuario.setParent(None)
            self.menuIzquierdo.toggleViewAction().trigger()
            self.menuIzquierdo.containerLayout.removeWidget(self.menuIzquierdo.gestion10)
            self.menuIzquierdo.containerLayout.removeWidget(self.menuIzquierdo.gestion11)
            self.menuIzquierdo.containerLayout.removeWidget(self.menuIzquierdo.gestion12)
            self.stack.setCurrentIndex(0)
    
    def salir(self):
        global app
        resp = m.mostrarMensaje("Pregunta", "Advertencia",
                            "¿Está seguro de que desea salir?")
        if resp==qtw.QMessageBox.StandardButton.Yes:
            app.quit()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/gestion.qss", "r") as qss:
        app.setStyleSheet(qss.read())
    window.show()
    app.exec()
