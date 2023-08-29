"""El archivo principal. Genera la ventana principal y ejecuta la 
aplicación.

Clases:
    MainWindow(qtw.QMainWindow): crea la ventana principal.

Objetos:
    mainWindow: la ventana principal.
    app: la aplicación principal.
"""
# Antes de arrancar, establecemos el path con el que la app trabajará 
# para evitar problemas de importar módulos
import os
os.chdir(f"{os.path.abspath(__file__)}{os.sep}..")

# Ahora sí, hacemos todos los imports
from PyQt6 import QtWidgets, QtCore, QtGui, uic
from ui.presets.Toolbotoon import toolboton
from ui.presets.param_edit import ParamEdit
from ui.presets.popup import PopUp
from dal.dal import dal
from db.bdd import bdd
from datetime import datetime
from textwrap import dedent
from unidecode import unidecode
import core
import pandas as pd
from types import FunctionType as function
import sys


class MainWindow(QtWidgets.QMainWindow):
    """Esta clase crea la ventana principal.

    Hereda: PyQt6.QtWidgets.QMainWindow

    Métodos
    -------
        __init__(self):
            El constructor de la clase MainWindow.

            Crea la ventana principal con un menú inicialmente
            escondido y una colección de pantallas.
        
        actualizarSug(self):
            Refresca las sugerencias de todos los campos con
            sugerencias del sistema.

        habilitarSaves(self, row: int | None = None,
                       col: int | None = None,
                       tabla: QtWidgets.QTableWidget | None = None):
            Habilita el botón de guardar de una fila de una tabla de
            una gestión.

        actualizarTotal(self, row: int, col: int,
                        tabla: QtWidgets.QTableWidget | None = None):
            Actualiza el campo total de la tabla stock cuando se
            modifican las cantidades.

        actualizarSugSubgrupos(self):
            Actualiza las sugerencias de los campos de subgrupos al
            editar lo ingresado en un campo de grupos relacionado, ya
            que las sugerencias de subgrupos deben estar relacionadas
            al grupo ingresado.
        
        fetchStock(self):
            Refresca la tabla y los filtros de la pantalla stock.
        
        saveOne(self, tabla: QtWidgets.QTableWidget,
                funcSave: function, funcFetch: function,
                datos: list | None = None):
            Guarda los cambios hechos en una fila de una tabla de una
            gestión.
        
        saveAll(self, tabla: QtWidgets.QTableWidget,
                funcSave: function, funcFetch: function,
                datos: list | None = None):
            Guarda todos los cambios hechos en una tabla de una gestión
        
        deleteStock(self, datos: list | None = None) -> None:
            Elimina una fila de la tabla de la gestión stock.
        
        printStock(self):
            Genera un spreadsheet a partir de la tabla de la pantalla
            stock.
        
        cargarPlanillaAlumnos(self):
            Crea un dataframe para la carga de datos de una spreadsheet
            en la base de datos de la gestión alumnos.
        
        fetchAlumnos(self):
            Refresca la gestión de alumnos.
        
        deleteAlumnos(self, datos: list | None = None) -> None:
            Elimina una fila de la tabla de la gestión alumnos.
        
        fetchMovs(self):
            Refresca el listado de movimientos.
        
        fetchGrupos(self):
            Refresca la gestión de grupos.
        
        deleteGrupos(self, datos: list | None = None):
            Elimina una fila de la tabla de la gestión de grupos.
        
        fetchOtroPersonal(self):
            Refresca la gestión del personal.
        
        deleteOtroPersonal(self, datos: list | None = None):
            Elimina una fila de la tabla de la gestión del personal.
        
        fetchSubgrupos(self):
            Refresca la gestión subgrupos.
        
        deleteSubgrupos(self, datos: list | None = None):
            Elimina una fila de la tabla de la gestión subgrupos.
        
        fetchTurnos(self):
            Refresca el listado de turnos.
        
        fetchUsuarios(self):
            Refresca la gestión usuarios.
        
        deleteUsuarios(self, datos: list | None = None):
            Elimina una fila de la tabla de la gestión usuarios.
        
        fetchClases(self):
            Refresca la gestión clases.
        
        fetchUbis(self):
            Refresca la gestión ubicaciones.
        
        deleteUbis(self, datos: list | None = None):
            Elimina una fila de la tabla de la gestión ubicaciones.
        
        fetchReps(self):
            Refresca el listado de reparaciones.
        
        deleteClases(self, datos: list | None = None):
            Elimina una fila de la tabla de la gestión clases.
        
        fetchHistorial(self):
            Refresca el historial.
        
        fetchDeudas(self):
            Refresca el listado de deudas.
        
        fetchResumen(self):
            Refresca el resumen de deudas.
    """
    def __init__(self):
        """El constructor, crea la ventana principal con un menú
        inicialmente escondido y una colección de pantallas."""
        # Inicializamos la clase heredada
        super().__init__()

        # Inicializamos el menú principal
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}main.ui'), self)

        # Escondemos el menú para que no se pueda acceder apenas
        # se inicia la aplicación.
        self.menubar.hide()

        # Empezamos a crear todas las pantallas:
        # # Creamos un widget vacío
        self.pantallaAlumnos = QtWidgets.QWidget()
        # # Guardamos el path al archivo ui
        pathAlumnos = os.path.join(os.path.abspath(os.getcwd()),
                                 f'ui{os.sep}screens_uis{os.sep}alumnos.ui')
        # # Cargamos el ui al widget vacío
        uic.loadUi(pathAlumnos, self.pantallaAlumnos)
        # Hacemos lo mismo con el resto de las pantallas.
        self.pantallaGrupos = QtWidgets.QWidget()
        pathGrupos = os.path.join(os.path.abspath(os.getcwd()),
                                  f'ui{os.sep}screens_uis{os.sep}grupos.ui')
        uic.loadUi(pathGrupos, self.pantallaGrupos)
        self.pantallaStock = QtWidgets.QWidget()
        pathStock = os.path.join(os.path.abspath(os.getcwd()),
                                 f'ui{os.sep}screens_uis{os.sep}stock.ui')
        uic.loadUi(pathStock, self.pantallaStock)
        self.pantallaHistorial = QtWidgets.QWidget()
        pathHistorial = os.path.join(
            os.path.abspath(os.getcwd()),
            f'ui{os.sep}screens_uis{os.sep}historial.ui')
        uic.loadUi(pathHistorial, self.pantallaHistorial)
        self.pantallaMovs = QtWidgets.QWidget()
        pathMovs = os.path.join(
            os.path.abspath(os.getcwd()),
            f'ui{os.sep}screens_uis{os.sep}movimientos.ui')
        uic.loadUi(pathMovs, self.pantallaMovs)
        self.pantallaOtroPersonal = QtWidgets.QWidget()
        pathOtroPersonal = os.path.join(
            os.path.abspath(os.getcwd()),
            f'ui{os.sep}screens_uis{os.sep}otro_personal.ui')
        uic.loadUi(pathOtroPersonal, self.pantallaOtroPersonal)
        self.pantallaSubgrupos = QtWidgets.QWidget()
        pathSubgrupos = os.path.join(
            os.path.abspath(os.getcwd()),
            f'ui{os.sep}screens_uis{os.sep}subgrupos.ui')
        uic.loadUi(pathSubgrupos, self.pantallaSubgrupos)
        self.pantallaTurnos = QtWidgets.QWidget()
        pathTurnos = os.path.join(os.path.abspath(os.getcwd()),
                                  f'ui{os.sep}screens_uis{os.sep}turnos.ui')
        uic.loadUi(pathTurnos, self.pantallaTurnos)
        self.pantallaUsuarios = QtWidgets.QWidget()
        pathUsuarios = os.path.join(
            os.path.abspath(os.getcwd()),
            f'ui{os.sep}screens_uis{os.sep}usuarios.ui')
        uic.loadUi(pathUsuarios, self.pantallaUsuarios)
        self.pantallaLogin = QtWidgets.QWidget()
        pathLogin = os.path.join(os.path.abspath(os.getcwd()),
                                 f'ui{os.sep}screens_uis{os.sep}login.ui')
        uic.loadUi(pathLogin, self.pantallaLogin)
        self.pantallaClases = QtWidgets.QWidget()
        pathClases = os.path.join(os.path.abspath(os.getcwd()),
                                  f'ui{os.sep}screens_uis{os.sep}clases.ui')
        uic.loadUi(pathClases, self.pantallaClases)
        self.pantallaReps = QtWidgets.QWidget()
        pathReps = os.path.join(
            os.path.abspath(os.getcwd()),
            f'ui{os.sep}screens_uis{os.sep}reparaciones.ui')
        uic.loadUi(pathReps, self.pantallaReps)
        self.pantallaUbis = QtWidgets.QWidget()
        pathUbis = os.path.join(
            os.path.abspath(os.getcwd()),
            f'ui{os.sep}screens_uis{os.sep}ubicaciones.ui')
        uic.loadUi(pathUbis, self.pantallaUbis)
        self.pantallaRealizarMov = QtWidgets.QWidget()
        pathRealizarMov = os.path.join(
            os.path.abspath(os.getcwd()),
            f'ui{os.sep}screens_uis{os.sep}n-movimiento.ui')
        uic.loadUi(pathRealizarMov, self.pantallaRealizarMov)
        self.pantallaDeudas = QtWidgets.QWidget()
        pathDeudas = os.path.join(os.path.abspath(os.getcwd()),
                                  f'ui{os.sep}screens_uis{os.sep}deudas.ui')
        uic.loadUi(pathDeudas, self.pantallaDeudas)
        self.pantallaResumen = QtWidgets.QWidget()
        pathResumen = os.path.join(os.path.abspath(os.getcwd()),
                                   f'ui{os.sep}screens_uis{os.sep}resumen.ui')
        uic.loadUi(pathResumen, self.pantallaResumen)

        # Queremos aplicar cambios a todas las pantallas
        # # Primero, hacemos una tupla que contenga todas las tablas.
        pantallas = (self.pantallaLogin, self.pantallaAlumnos,
                     self.pantallaGrupos, self.pantallaStock,
                     self.pantallaMovs, self.pantallaOtroPersonal,
                     self.pantallaSubgrupos, self.pantallaTurnos,
                     self.pantallaUsuarios, self.pantallaHistorial,
                     self.pantallaClases, self.pantallaReps,
                     self.pantallaUbis, self.pantallaRealizarMov,
                     self.pantallaDeudas, self.pantallaResumen)
        # # Por cada pantalla ...
        for pantalla in pantallas:
            # # ... la añadimos al stackedwidget de la ventana
            # # principal
            self.stackedWidget.addWidget(pantalla)
            # #, intentamos...
            try:
                # # insertarle el logo de la barra de búsqueda
                path = f'ui{os.sep}rsc{os.sep}icons{os.sep}buscar.png'
                pixmap = QtGui.QPixmap(path)
                pantalla.label_2.setPixmap(pixmap)
                # # aplicar estilos y funcionalidad a todas las tablas
                pantalla.tableWidget.horizontalHeader().setFont(QtGui.QFont("Oswald", 13))
                pantalla.tableWidget.cellChanged.connect(self.habilitarSaves)
            # # Si ocurre algún error, es porque la pantalla no tenía
            # # una tabla. En ese caso, ignoramos la excepción.
            except BaseException:
                pass

        # Conectamos las opciones del menú a sus respectivas pantallas
        self.opcionStock.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(3))
        self.opcionSubgrupos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(6))
        self.opcionGrupos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))
        self.opcionAlumnos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.opcionOtroPersonal.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(5))
        self.opcionTurnos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(7))
        self.opcionMovimientos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(4))
        self.opcionUsuarios.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(8))
        self.GestionUbicaciones.triggered.connect(self.fetchUbis)
        self.GestionClases.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(10))
        self.realizarMovimientos.triggered.connect(self.realizarMovimiento)
        self.GestionReparacion.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(11))
        self.opcionHistorial.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(9))
        self.opcionDeudas.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(14))
        self.opcionResumen.triggered.connect(self.fetchResumen)
        
        #Pantalla login
        # Añadimos un botón de mostrar contraseña para la pantalla de
        # inicio de sesión.
        # Primero aplicamos el ícono.
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
        pixmap = QtGui.QPixmap(path)
        self.pantallaLogin.showPass.setIcon(QtGui.QIcon(QtGui.QIcon(pixmap)))
        self.pantallaLogin.showPass.setIconSize(QtCore.QSize(25, 25))
        # Le damos funcionalidad.
        self.pantallaLogin.showPass.clicked.connect(
            lambda: core.mostrarContrasena(
                self.pantallaLogin.showPass,
                self.pantallaLogin.passwordLineEdit))
        self.pantallaLogin.usuariosLineEdit.returnPressed.connect(
            lambda: self.pantallaLogin.passwordLineEdit.setFocus()
        )
        self.pantallaLogin.passwordLineEdit.returnPressed.connect(self.login)
        self.pantallaLogin.Ingresar.clicked.connect(self.login)
        #Creamos un boton que nos permite sacar o poner la flag para que la ventana este siempre arriba
        self.minimizar = QtWidgets.QPushButton()
        self.minimizar.setObjectName("mini")
        self.minimizar.setText("1")
        self.minimizar.setFixedSize(40, 40)
        self.minimizar.setVisible(True)
        self.minimizar.clicked.connect(self.desbloquear)
        #Creamos un boton que nos cerrar la aplicacion 
        boton = QtWidgets.QPushButton()
        boton.setObjectName("prueba")
        boton.setText("X")
        boton.setFixedSize(40, 40)
        boton.setVisible(True)
        boton.clicked.connect(lambda: self.close())
        self.pantallaLogin.gridLayout.addWidget(
            boton, 0, 1, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)
        self.pantallaLogin.gridLayout.addWidget(
            self.minimizar, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        # Empezamos a conectar los botones de agregar de todas las
        # gestiones.
        # Inicializamos las sugerencias.
        self.actualizarSug()
        # Conectamos el botón.
        self.pantallaStock.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaStock.tableWidget,
                lambda: self.saveOne(
                    self.pantallaStock.tableWidget, dal.saveStock),
                self.deleteStock, self.actualizarTotal, core.camposStock[0],
                (self.sGrupos, [], self.sUbis,),
                self.actualizarSugSubgrupos))
        # Conectamos el boton de guardar cambios
        self.pantallaStock.botonGuardar.clicked.connect(
            lambda: self.saveAll(self.pantallaStock.tableWidget,
                dal.saveStock, dal.obtenerDatos(
                    "stock", self.pantallaStock.lineEdit.text())))
        # Escondemos la primera columna. Esto es porque es la
        # columna id es necesaria para tener el número de fila pero no
        # queremos que la vean los usuarios porque no es info necesaria
        self.pantallaStock.tableWidget.setColumnHidden(0, True)
        self.pantallaStock.tableWidget.resizeColumnsToContents()
        self.pantallaStock.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaStock.tableWidget.horizontalHeader().setSectionResizeMode(
            7, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaStock.tableWidget.horizontalHeader().setSectionResizeMode(
            8, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        # Conectamos los cambios en la tabla stock para actualizar el
        # valor del campo total cada vez que se haga un cambio en una
        # cantidad.
        self.pantallaStock.tableWidget.cellChanged.connect(
            self.actualizarTotal)
        # Conectamos la barra de búsqueda
        self.pantallaStock.lineEdit.editingFinished.connect(
            lambda: core.refresh(self.pantallaStock.tableWidget,
                                 self.fetchStock))
        self.pantallaStock.listaUbi.currentIndexChanged.connect(
            lambda: core.refresh(self.pantallaStock.tableWidget,
                                 self.fetchStock))
        self.pantallaStock.botonRefresh.clicked.connect(
            lambda: core.refresh(self.pantallaStock.tableWidget,
                                 self.fetchStock))
        # Conectamos el botón de imprimir
        self.pantallaStock.botonImprimir.clicked.connect(self.printStock)

        # Hacemos lo mismo con las otras pantallas
        
        #Pantalla otroPersonal
        self.pantallaOtroPersonal.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaOtroPersonal.tableWidget, lambda: self.saveOne(
                    self.pantallaOtroPersonal.tableWidget,
                    dal.saveOtroPersonal), self.deleteOtroPersonal,
                self.habilitarSaves, core.camposOtroPersonal[0],
                [self.sClasesP]))
        self.pantallaOtroPersonal.botonPlanilla.clicked.connect(
            self.cargarPlanillaPersonal)
        self.pantallaOtroPersonal.botonGuardar.clicked.connect(
            lambda: self.saveAll(
                self.pantallaOtroPersonal.tableWidget, dal.saveOtroPersonal,
                dal.obtenerDatos(
                    "otro_personal", self.pantallaOtroPersonal.lineEdit.text()
                )))
        self.pantallaOtroPersonal.tableWidget.setColumnHidden(0, True)
        self.pantallaOtroPersonal.tableWidget.resizeColumnsToContents()
        self.pantallaOtroPersonal.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaOtroPersonal.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaOtroPersonal.lineEdit.editingFinished.connect(
            lambda: core.refresh(self.pantallaOtroPersonal.tableWidget,
                                 self.fetchOtroPersonal))
        self.pantallaOtroPersonal.botonRefresh.clicked.connect(
            lambda: core.refresh(self.pantallaOtroPersonal.tableWidget,
                                 self.fetchOtroPersonal))
        self.pantallaOtroPersonal.tableWidget.horizontalHeader().setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        #Pantalla subgrupos
        self.pantallaSubgrupos.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaSubgrupos.tableWidget,
                lambda: self.saveOne(
                    self.pantallaSubgrupos.tableWidget, dal.saveSubgrupos),
                self.deleteSubgrupos, self.habilitarSaves,
                core.camposSubgrupos[0], [self.sGruposS]))
        self.pantallaSubgrupos.botonGuardar.clicked.connect(
            lambda: self.saveAll(
                self.pantallaSubgrupos.tableWidget, dal.saveSubgrupos,
                dal.obtenerDatos(
                    "subgrupos", self.pantallaSubgrupos.lineEdit.text())))
        self.pantallaSubgrupos.tableWidget.setColumnHidden(0, True)
        self.pantallaSubgrupos.tableWidget.resizeColumnsToContents()
        self.pantallaSubgrupos.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaSubgrupos.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaSubgrupos.lineEdit.editingFinished.connect(
            lambda: core.refresh(self.pantallaSubgrupos.tableWidget,
                                 self.fetchSubgrupos))
        self.pantallaSubgrupos.botonRefresh.clicked.connect(
            lambda: core.refresh(self.pantallaSubgrupos.tableWidget,
                                 self.fetchSubgrupos))

        #Pantalla grupos
        self.pantallaGrupos.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaGrupos.tableWidget,
                lambda: self.saveOne(
                    self.pantallaGrupos.tableWidget, dal.saveGrupos),
                self.deleteGrupos, self.habilitarSaves, core.camposGrupos[0]))
        self.pantallaGrupos.botonGuardar.clicked.connect(
            lambda: self.saveAll(
                self.pantallaGrupos.tableWidget, dal.saveGrupos,
                dal.obtenerDatos(
                    "grupos", self.pantallaGrupos.lineEdit.text())))
        self.pantallaGrupos.tableWidget.setColumnHidden(0, True)
        self.pantallaGrupos.tableWidget.resizeColumnsToContents()
        self.pantallaGrupos.tableWidget.horizontalHeader(
        ).setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaGrupos.lineEdit.editingFinished.connect(
            lambda: core.refresh(self.pantallaGrupos.tableWidget,
                                 self.fetchGrupos))
        self.pantallaGrupos.botonRefresh.clicked.connect(
            lambda: core.refresh(self.pantallaGrupos.tableWidget,
                                 self.fetchGrupos))

        #Pantallas alumnos
        self.pantallaAlumnos.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaAlumnos.tableWidget,
                lambda: self.saveOne(
                    self.pantallaAlumnos.tableWidget, dal.saveAlumnos),
                self.deleteAlumnos,  self.habilitarSaves,
                core.camposAlumnos[0], [self.sClasesA]))
        self.pantallaAlumnos.botonGuardar.clicked.connect(
            lambda: self.saveAll(
                self.pantallaAlumnos.tableWidget, dal.saveAlumnos,
                dal.obtenerDatos(
                    "alumnos", self.pantallaAlumnos.lineEdit.text())))
        self.pantallaAlumnos.botonCargar.clicked.connect(
            self.cargarPlanillaAlumnos)
        self.pantallaAlumnos.tableWidget.setColumnHidden(0, True)
        self.pantallaAlumnos.tableWidget.resizeColumnsToContents()
        self.pantallaAlumnos.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaAlumnos.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaAlumnos.tableWidget.horizontalHeader().setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaAlumnos.lineEdit.editingFinished.connect(
            lambda: core.refresh(self.pantallaAlumnos.tableWidget,
                                 self.fetchAlumnos))
        self.pantallaAlumnos.botonRefresh.clicked.connect(
            lambda: core.refresh(self.pantallaAlumnos.tableWidget,
                                 self.fetchAlumnos))

        #Pantalla ubis
        self.pantallaUbis.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaUbis.tableWidget, lambda: self.saveOne(
                    self.pantallaUbis.tableWidget, dal.saveUbis),
                    self.deleteUbis, self.habilitarSaves,
                    core.camposUbis[0]))
        self.pantallaUbis.botonGuardar.clicked.connect(
            lambda: self.saveAll(
                self.pantallaUbis.tableWidget, dal.saveUbis, dal.obtenerDatos(
                    "ubicaciones", self.pantallaUbis.lineEdit.text())))
        self.pantallaUbis.tableWidget.setColumnHidden(0, True)
        self.pantallaUbis.tableWidget.resizeColumnsToContents()
        self.pantallaUbis.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaUbis.lineEdit.editingFinished.connect(
            lambda: core.refresh(self.pantallaUbis.tableWidget,
                                 self.fetchUbis))

        #Pantalla clases
        self.pantallaClases.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaClases.tableWidget, lambda: self.saveOne(
                self.pantallaClases.tableWidget, dal.saveClases),
                self.deleteClases, self.habilitarSaves,
                core.camposClases[0], [self.sCat]))
        self.pantallaClases.botonGuardar.clicked.connect(
            lambda: self.saveAll(
                self.pantallaClases.tableWidget, dal.saveClases,
                dal.obtenerDatos(
                    "clases", self.pantallaClases.lineEdit.text())))
        self.pantallaClases.tableWidget.setColumnHidden(0, True)
        self.pantallaClases.tableWidget.resizeColumnsToContents()
        self.pantallaClases.tableWidget.horizontalHeader(
        ).setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaClases.lineEdit.editingFinished.connect(
            lambda: core.refresh(self.pantallaClases.tableWidget,
                                 self.fetchClases))
        self.pantallaClases.botonRefresh.clicked.connect(
            lambda: core.refresh(self.pantallaClases.tableWidget,
                                 self.fetchClases))

       #Pantalla usuarios
        self.pantallaUsuarios.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaUsuarios.tableWidget, lambda: self.saveOne(
                    self.pantallaUsuarios.tableWidget, dal.saveUsuarios),
                self.deleteUsuarios, self.habilitarSaves,
                core.camposUsuarios[0], [self.sClasesU]))
        self.pantallaUsuarios.botonGuardar.clicked.connect(
            lambda: self.saveAll(
                self.pantallaUsuarios.tableWidget, dal.saveUsuarios,
                dal.obtenerDatos(
                    "usuarios", self.pantallaUsuarios.lineEdit.text())))
        self.pantallaUsuarios.tableWidget.setColumnHidden(0, True)
        self.pantallaUsuarios.tableWidget.resizeColumnsToContents()
        self.pantallaUsuarios.tableWidget.horizontalHeader(
        ).setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        #Pantalla movs
        self.pantallaMovs.tableWidget.resizeColumnsToContents()
        self.pantallaMovs.tableWidget.horizontalHeader().setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaMovs.lineEdit.editingFinished.connect(self.fetchMovs)
        self.pantallaMovs.nId.valueChanged.connect(self.fetchMovs)
        self.pantallaMovs.nTurno.valueChanged.connect(self.fetchMovs)
        self.pantallaMovs.botonRefresh.clicked.connect(self.fetchMovs)
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaMovs.hastaFecha.setDateTime(QtCore.QDateTime(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day(),
            QtCore.QTime.currentTime().hour(),
            QtCore.QTime.currentTime().minute(),
            QtCore.QTime.currentTime().second()))
        self.pantallaMovs.hastaFecha.setMaximumDateTime(QtCore.QDateTime(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day(),
            QtCore.QTime.currentTime().hour(),
            QtCore.QTime.currentTime().minute(),
            QtCore.QTime.currentTime().second()))
        self.pantallaMovs.hastaFecha.dateChanged.connect(self.fetchMovs)

        #Pantalla reparacion
        self.pantallaReps.tableWidget.resizeColumnsToContents()
        self.pantallaReps.tableWidget.horizontalHeader(
        ).setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaReps.tableWidget.horizontalHeader(
        ).setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaReps.tableWidget.horizontalHeader(
        ).setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaReps.lineEdit.editingFinished.connect(self.fetchReps)
        self.pantallaReps.botonRefresh.clicked.connect(self.fetchReps)
        self.pantallaReps.hastaFecha.setDate(QtCore.QDate(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day()))
        self.pantallaReps.hastaFecha.setMaximumDate(QtCore.QDate(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day()))
        self.pantallaReps.hastaFecha.dateChanged.connect(self.fetchReps)

        #Pantalla turnos
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaTurnos.lineEdit.editingFinished.connect(self.fetchTurnos)
        self.pantallaTurnos.nId.valueChanged.connect(self.fetchTurnos)
        self.pantallaTurnos.botonRefresh.clicked.connect(self.fetchTurnos)
        self.pantallaTurnos.desdeFecha.dateChanged.connect(self.fetchTurnos)
        self.pantallaTurnos.hastaFecha.dateChanged.connect(self.fetchTurnos)
        self.pantallaTurnos.hastaFecha.setDate(QtCore.QDate(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day()))
        self.pantallaTurnos.hastaFecha.setMaximumDate(QtCore.QDate(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day()))
        self.pantallaTurnos.hastaFecha.dateChanged.connect(self.fetchTurnos)
        
        #Pantalla Historial
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaHistorial.lineEdit.editingFinished.connect(
            self.fetchHistorial)
        self.pantallaHistorial.botonRefresh.clicked.connect(
            self.fetchHistorial)
        self.pantallaHistorial.hastaFecha.setDateTime(QtCore.QDateTime(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day(),
            QtCore.QTime.currentTime().hour(),
            QtCore.QTime.currentTime().minute(),
            QtCore.QTime.currentTime().second()))
        self.pantallaHistorial.hastaFecha.setMaximumDateTime(QtCore.QDateTime(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day(),
            QtCore.QTime.currentTime().hour(),
            QtCore.QTime.currentTime().minute(),
            QtCore.QTime.currentTime().second()))
        self.pantallaHistorial.hastaFecha.dateChanged.connect(
            self.fetchHistorial)
        
        #Pantalla RealizarMov
        self.pantallaRealizarMov.cursoComboBox.textActivated.connect(
            self.alumnos)
        self.pantallaRealizarMov.pushButton.clicked.connect(
            self.saveMovimiento)
        self.pantallaRealizarMov.ubicacionComboBox.textActivated.connect(
            self.herramientas)
        self.pantallaRealizarMov.Limpiar.clicked.connect(self.clear)
        self.pantallaRealizarMov.tipoDeMovimientoComboBox.textActivated.connect(
            self.check)
        self.pantallaRealizarMov.formLayout.setAlignment(self.pantallaRealizarMov.herramientasDisponiblesLineEdit, QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        #Pantalla Deudas
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaDeudas.lineEdit.editingFinished.connect(self.fetchDeudas)
        self.pantallaDeudas.botonRefresh.clicked.connect(self.fetchDeudas)
        self.pantallaDeudas.radioHerramienta.toggled.connect(self.fetchDeudas)
        self.pantallaDeudas.radioPersona.toggled.connect(self.fetchDeudas)
        self.pantallaDeudas.nMov.valueChanged.connect(self.fetchDeudas)
        self.pantallaDeudas.nTurno.valueChanged.connect(self.fetchDeudas)
        
        #Pantalla Resumen
        # Conectamos las otras barras de búsqueda y los otros filtros
        self.pantallaResumen.hastaFecha.setDate(QtCore.QDate(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day()))
        self.pantallaResumen.hastaFecha.setMaximumDate(QtCore.QDate(
            QtCore.QDate.currentDate().year()+1,
            QtCore.QDate.currentDate().month(),
            QtCore.QDate.currentDate().day()))
        self.pantallaResumen.hastaFecha.dateChanged.connect(self.fetchResumen)

        #ToolBoton
        self.boton = toolboton("usuario", self)
        self.boton.setIconSize(QtCore.QSize(60, 40))
        self.label = QtWidgets.QLabel(str("El pañolero en turno es: "))
        self.label.setObjectName("sopas")
        widget_with_layout = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget_with_layout)
        layout.addWidget(self.label)
        layout.addWidget(self.boton)
        self.menubar.setCornerWidget(
            widget_with_layout, QtCore.Qt.Corner.TopRightCorner)

        # Hacemos que la pantalla principal no se vea como ventana.
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        # Establecemos la pantalla del login como pantalla por defecto.
        self.stackedWidget.setCurrentIndex(0)
        # Cambiamos el titulo de la ventana y la hacemos pantalla completa.
        self.move(0, 0)
        self.setFixedSize(QtGui.QGuiApplication.primaryScreen().size())
        #Ponemos las flags
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        #Ponemos el ícono
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}blustock.ico'
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(path)))
        # Mostramos la ventana principal.
        self.show()
   
    #Esta funcion nos permite sacar o poner la flag para que la ventana este siempre arriba
    def desbloquear(self):
        if self.windowFlags() & QtCore.Qt.WindowType.WindowStaysOnTopHint:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self.minimizar.setText("2")

        else:    
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self.minimizar.setText("1")
        self.show()

    def actualizarSug(self):
        """Este método refresca las sugerencias de todos los campos
        con sugerencias del sistema."""
        self.sGrupos = [i[0] for i in bdd.cur.execute(
            'SELECT descripcion FROM grupos').fetchall()]
        self.sUbis = [i[0] for i in bdd.cur.execute(
            'SELECT descripcion FROM ubicaciones').fetchall()]
        sql = '''SELECT c.descripcion FROM clases c
               JOIN cats_clase cat ON c.id_cat=cat.id
               WHERE cat.descripcion='Personal' or c.descripcion='Director de Taller' or c.descripcion = 'Profesor de Taller';'''
        self.sClasesP = [i[0] for i in bdd.cur.execute(sql).fetchall()]
        self.sGruposS = [i[0] for i in bdd.cur.execute(
            'SELECT descripcion FROM grupos').fetchall()]
        sql = '''SELECT c.descripcion FROM clases c
               JOIN cats_clase cat ON c.id_cat=cat.id
               WHERE cat.descripcion='Alumno';'''
        self.sClasesA = [i[0] for i in bdd.cur.execute(sql).fetchall()]
        self.sCat = [i[0] for i in bdd.cur.execute(
            'SELECT descripcion FROM cats_clase').fetchall()]
        sql = '''SELECT c.descripcion FROM clases c
               JOIN cats_clase cat ON c.id_cat=cat.id
               WHERE cat.descripcion='Usuario';'''
        self.sClasesU = [i[0] for i in bdd.cur.execute(sql).fetchall()]

    #Con esta funcion re escribimos el evento que cierra la ventana principal para que solo se accione cuando se lo envia algun objeto de la app
    def closeEvent(self, event: QtGui.QCloseEvent):
        if self.sender() is not None:
            event.accept()
        else:
            event.ignore()

    #Este es el inicio de sesion verifica que todos el usuario y la contraseña esten bien si no te pone unos cartelitos segun lo que este mal, ademas verifica que no haya turnos activos, si los hay te pregunta que queres hacer con ese turno.
    def login(self):
        self.boton.show()
        bdd.cur.execute("SELECT count(*) FROM personal WHERE usuario = ?",
                        (self.pantallaLogin.usuariosLineEdit.text(),))
        check = bdd.cur.fetchone()
        if check[0] >= 1:
            bdd.cur.execute("SELECT count(*) FROM personal WHERE usuario = ? and contrasena = ?", (
                self.pantallaLogin.usuariosLineEdit.text(), self.pantallaLogin.passwordLineEdit.text(),))
            check = bdd.cur.fetchone()
            if check[0] == 1:
                self.usuario = bdd.cur.execute("SELECT dni FROM personal WHERE usuario = ? and contrasena = ?", (
                    self.pantallaLogin.usuariosLineEdit.text(), self.pantallaLogin.passwordLineEdit.text(),)).fetchall()[0][0]
                self.stackedWidget.setCurrentIndex(3)
                if bdd.cur.execute("SELECT c.descripcion FROM clases c join personal p on p.id_clase = c.id WHERE dni = ?", (self.usuario,)).fetchone()[0] != "Director de Taller":
                    self.menubar.actions()[4].setVisible(False)
                pañolero = bdd.cur.execute(
                    "select nombre_apellido from turnos join personal p on p.id = id_panolero WHERE fecha_egr is null").fetchone()
                if pañolero != None:
                    mensaje = "Hay un turno sin finalizar, desea continuarlo o finalizarlo?"
                    popup = PopUp("Turno", mensaje)

                    class sopas(QtCore.QObject):
                        def eventFilter(self, obj, event):
                            # ignora todos los eventos de teclas
                            if event.type() in [QtCore.QEvent.Type.KeyPress, QtCore.QEvent.Type.KeyRelease]:
                                return True  # Return True para indicar que el evento debe ser ignorado
                            return super().eventFilter(obj, event)

                    filtro = sopas(popup)
                    popup.installEventFilter(filtro)
                    popup.setWindowFlags(
                        QtCore.Qt.WindowType.CustomizeWindowHint)
                    popup.setWindowFlag(QtCore.Qt.WindowType.WindowTitleHint)
                    popup.button(
                        QtWidgets.QMessageBox.StandardButton.Cancel).hide()
                    popup = PopUp("Turno", mensaje).exec()
                    if popup == QtWidgets.QMessageBox.StandardButton.Yes:
                        self.label.setText(
                            "El pañolero en turno es: " + pañolero[0])
                        self.label.setObjectName("sopas")
                        self.boton.menu().actions()[2].setVisible(True)
                        self.boton.menu().actions()[6].setVisible(True)
                        self.boton.menu().actions()[4].setVisible(False)
                        self.boton.menu().actions()[0].setVisible(False)
                        for i in range(7):
                            if i != 1:
                                self.menubar.actions()[i].setVisible(False)

                    if popup == QtWidgets.QMessageBox.StandardButton.No:
                        profe = dal.obtenerDatos("usuarios", self.usuario,)
                        hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        bdd.cur.execute(
                            """UPDATE turnos SET fecha_egr = ?, id_prof_egr = ? WHERE fecha_egr is null""", (hora, profe[0][0],))
                        bdd.con.commit()
                        self.label.setText("Usuario: " + bdd.cur.execute(
                            "SELECT nombre_apellido FROM personal WHERE dni = ?", (self.usuario,)).fetchone()[0])
                        for i in range(7):
                            if i != 1:
                                self.menubar.actions()[i].setVisible(True)
                        self.boton.menu().actions()[2].setVisible(True)

                        if bdd.cur.execute("SELECT c.descripcion FROM clases c join personal p on p.id_clase = c.id WHERE dni = ?", (self.usuario,)).fetchone()[0] != "Director de Taller":
                            self.menubar.actions()[4].setVisible(False)
                        self.boton.menu().actions()[0].setVisible(True)
                        self.boton.menu().actions()[4].setVisible(True)
                        self.boton.menu().actions()[2].setVisible(False)

                else:
                    self.label.setText("Usuario: " + bdd.cur.execute(
                        "SELECT nombre_apellido FROM personal WHERE dni = ?", (self.usuario,)).fetchone()[0])
                    self.boton.menu().actions()[2].setVisible(False)                
                self.menubar.show()
                self.pantallaLogin.usuarioState.setText("")
                self.pantallaLogin.passwordState.setText("")

            else:
                self.pantallaLogin.passwordState.setText(
                    "contraseña incorrecta")
                self.pantallaLogin.usuarioState.setText("")

        else:
            self.pantallaLogin.usuarioState.setText("usuario incorrecto")
            self.pantallaLogin.passwordState.setText("")
    
    def clear(self):
        self.pantallaRealizarMov.tipoDeMovimientoComboBox.setCurrentIndex(-1)
        self.pantallaRealizarMov.herramientaComboBox.setCurrentIndex(-1)
        self.pantallaRealizarMov.estadoComboBox.setCurrentIndex(-1)
        self.pantallaRealizarMov.cursoComboBox.setCurrentIndex(-1)
        self.pantallaRealizarMov.alumnoComboBox.setCurrentIndex(-1)
        self.pantallaRealizarMov.ubicacionComboBox.setCurrentIndex(-1)
        self.pantallaRealizarMov.descripcionLineEdit.setText("")
        self.pantallaRealizarMov.herramientasDisponiblesLineEdit.setText("")
        self.pantallaRealizarMov.cantidadSpinBox.setValue(0)

    #Toma la cantidad en condiciones de la herramienta que selecciones
    # en nuevo movimiento y lo pone en una line edit para mostrarnos 
    # la cantida de herramientas en stock.
    def cant(self, mov: int, estado=None):
        if mov == 0:
            if not estado:
                return
            try:
                estado = estado[estado.index(" "):]
                estado = estado[1:]
            except:
                pass
            estado = unidecode(estado)
            estado = "cant_" + estado.lower()
            query = f"""SELECT {estado} FROM stock
                        WHERE descripcion = ? AND id_ubi = (
                            SELECT id FROM ubicaciones
                            WHERE descripcion = ?
                        )"""
            params = (self.pantallaRealizarMov.herramientaComboBox.currentText(),
                      self.pantallaRealizarMov.ubicacionComboBox.currentText())
            valor = bdd.cur.execute(query,params).fetchone()
            try:
                if not valor[0]:
                    valor = list(valor)
                    valor[0] = 0
            except:
                mensaje = "La herramienta que seleccionó no está registrada en el sistema. Por favor, ingrese una herramienta existente."
                self.pantallaRealizarMov.herramientaComboBox.setCurrentIndex(-1)
                return PopUp("Error", mensaje).exec()
            self.pantallaRealizarMov.cantidadSpinBox.setMaximum(valor[0])
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.setText(str(valor[0]))
        elif mov == 1:
            cant = bdd.cur.execute("SELECT sum(cantidad) FROM reparaciones where id_herramienta=(select id from stock where descripcion = ?)", (self.pantallaRealizarMov.herramientaComboBox.currentText(),)).fetchone()[0]
            self.pantallaRealizarMov.cantidadSpinBox.setMaximum(cant)
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.setText(str(cant))
        elif mov == 2:
            print(self.pantallaRealizarMov.herramientaComboBox.currentText(),self.pantallaRealizarMov.ubicacionComboBox.currentText(),self.pantallaRealizarMov.alumnoComboBox.currentText())
            cant = bdd.cur.execute(
                """
                SELECT sum(cant) FROM deudas WHERE id_mov = (
                    SELECT id FROM movimientos WHERE id_elem= (
                        SELECT id FROM stock WHERE descripcion = ?
                        AND id_ubi = (
                            SELECT id FROM ubicaciones WHERE descripcion = ?
                        )
                    ) AND id_persona IN (
                        SELECT id FROM personal WHERE nombre_apellido = ?
                    ))""",
                (self.pantallaRealizarMov.herramientaComboBox.currentText(),
                 self.pantallaRealizarMov.ubicacionComboBox.currentText(),
                self.pantallaRealizarMov.alumnoComboBox.currentText())).fetchone()[0]
            if cant not in {None,0}:
                self.pantallaRealizarMov.cantidadSpinBox.setMaximum(cant)
                self.pantallaRealizarMov.herramientasDisponiblesLineEdit.setText(str(cant))
            else:                
                self.pantallaRealizarMov.herramientasDisponiblesLineEdit.setText(str(0))
        elif mov == 3:
            cant = bdd.cur.execute(
                """SELECT cant_baja FROM stock
                   WHERE descripcion = ? AND id_ubi = (
                       SELECT id FROM ubicaciones WHERE descripcion = ?
                   )""",
                (self.pantallaRealizarMov.herramientaComboBox.currentText(),
                self.pantallaRealizarMov.ubicacionComboBox.currentText(),)).fetchone()
            try:
                cant = cant[0]
                if cant is None:
                    cant = 0
            except:
                mensaje = "La herramienta que seleccionó no está registrada en el sistema. Por favor, ingrese una herramienta existente."
                self.pantallaRealizarMov.herramientaComboBox.setCurrentIndex(-1)
                return PopUp("Error", mensaje).exec()
            self.pantallaRealizarMov.cantidadSpinBox.setMaximum(cant)
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.setText(
                str(cant))
        elif mov == 4:
            cantRep=bdd.cur.execute('''
            SELECT cantidad FROM reparaciones WHERE id_herramienta = (
                SELECT id FROM stock WHERE descripcion = ?
            ) AND fecha_regreso IS NULL ORDER BY id''', (
                self.pantallaRealizarMov.herramientaComboBox.currentText(),
                )).fetchone()
            try:
                cantRep=cantRep[0]
                if cantRep is None:
                    cantRep = 0
            except:
                mensaje = "La herramienta que seleccionó no está registrada en el sistema. Por favor, ingrese una herramienta existente."
                self.pantallaRealizarMov.herramientaComboBox.setCurrentIndex(-1)
            self.pantallaRealizarMov.cantidadSpinBox.setValue(cantRep)
            self.pantallaRealizarMov.cantidadSpinBox.setMaximum(cantRep)
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.setText(
                str(cantRep))
    #El completer que esta en core pero sin convertirte todo en un line edit
    def completar(self,sugerencias):
        cuadroSugerencias = QtWidgets.QCompleter(sugerencias, self)
        cuadroSugerencias.setCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive)
        cuadroSugerencias.setCompletionMode(
            QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        cuadroSugerencias.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        cuadroSugerencias.model().sort(0)
        return cuadroSugerencias
    
    def deactA(self):
        try:
            self.pantallaRealizarMov.alumnoComboBox.textActivated.disconnect()
        except:
            pass
        
    def deactB(self):
        try:
            self.pantallaRealizarMov.herramientaComboBox.textActivated.disconnect()
        except:
            pass
    
    def deactC(self):
        try:
            self.pantallaRealizarMov.cursoComboBox.textActivated.disconnect()
        except:
            pass

    def deactD(self):
        try:
            self.pantallaRealizarMov.ubicacionComboBox.textActivated.disconnect()
        except:
            pass

    def herramientasDeudadas(self):
        sugerencias = []
        for i in self.test:
            herramienta = i[2]
            herramienta = herramienta.replace(self.pantallaRealizarMov.ubicacionComboBox.currentText(), "").strip()
            if self.pantallaRealizarMov.herramientaComboBox.findText(str(herramienta))==-1 and self.pantallaRealizarMov.alumnoComboBox.currentText() == i[0]:
                self.pantallaRealizarMov.herramientaComboBox.addItem(herramienta)
                sugerencias.append(herramienta)
            self.pantallaRealizarMov.herramientaComboBox.setCompleter(self.completar(sugerencias))
            self.pantallaRealizarMov.herramientaComboBox.model().sort(0)
        self.pantallaRealizarMov.herramientaComboBox.setCurrentIndex(-1)

    def alumnosDeudores(self):
        sugerencias = []
        for i in self.test:
            if self.pantallaRealizarMov.alumnoComboBox.findText(str(i[0]))==-1 and self.pantallaRealizarMov.cursoComboBox.currentText() == i[1]:
                self.pantallaRealizarMov.alumnoComboBox.addItem(i[0])
                sugerencias.append(i[0])
            self.pantallaRealizarMov.alumnoComboBox.setCompleter(self.completar(sugerencias))
            self.pantallaRealizarMov.alumnoComboBox.model().sort(0)
        self.pantallaRealizarMov.alumnoComboBox.textActivated.connect(self.herramientasDeudadas)
        self.pantallaRealizarMov.alumnoComboBox.setCurrentIndex(-1)

    def deudasp(self):
        self.test = []
        self.pantallaRealizarMov.cursoComboBox.clear()
        sugerencias = []
        datos = dal.obtenerDatos("deudas1",(self.pantallaRealizarMov.ubicacionComboBox.currentText(),))
        if datos == []:
            self.pantallaRealizarMov.cursoComboBox.addItem("No hay retiros pendientes en este momento")
            self.pantallaRealizarMov.cursoComboBox.setCurrentIndex(0)

        else:
            for i in datos:
                partes = i[2].split(' ')
                sopas = ' '.join(partes[:-3])
                curso = ' '.join(partes[-3:])
                self.test.append((sopas,curso,i[0]))
                if self.pantallaRealizarMov.cursoComboBox.findText(str(curso))==-1:
                    self.pantallaRealizarMov.cursoComboBox.addItem(curso)
                    sugerencias.append(curso)
                
            self.pantallaRealizarMov.cursoComboBox.setCompleter(self.completar(sugerencias))
            self.pantallaRealizarMov.cursoComboBox.setCurrentIndex(-1)
            self.pantallaRealizarMov.cursoComboBox.textActivated.disconnect(self.alumnos)
            self.pantallaRealizarMov.cursoComboBox.textActivated.connect(self.alumnosDeudores)
            self.pantallaRealizarMov.cursoComboBox.model().sort(0)

    def reparadas(self,ubi):
        self.pantallaRealizarMov.herramientaComboBox.clear()
        sugerencias = []
        sql="""SELECT DISTINCT s.descripcion FROM reparaciones r
        JOIN stock s ON s.id = r.id_herramienta
        JOIN ubicaciones u ON u.id = s.id_ubi
        WHERE u.descripcion = ?
        AND r.fecha_regreso IS NULL"""
        datos = bdd.cur.execute(sql, (ubi,)).fetchall()

        if datos == []:
            self.pantallaRealizarMov.herramientaComboBox.addItem("No hay herramientas en enviadas a reparación")
            self.pantallaRealizarMov.herramientaComboBox.setCurrentIndex(0)
        else:
            for i in datos:
                self.pantallaRealizarMov.herramientaComboBox.addItem(i[0])
                sugerencias.append(i[0])
            self.pantallaRealizarMov.herramientaComboBox.setCompleter(self.completar(sugerencias))
            self.pantallaRealizarMov.herramientaComboBox.setCurrentIndex(-1)

    #Funcion que llena la combobox de alumnos en nuevo movimento
    def alumnos(self):
        sugerencias = []
        self.pantallaRealizarMov.alumnoComboBox.clear()
        for i in dal.obtenerDatos("alumnos", self.pantallaRealizarMov.cursoComboBox.currentText(),):
            self.pantallaRealizarMov.alumnoComboBox.addItem(i[1])
            sugerencias.append(i[1])
        for i in dal.obtenerDatos("otro_personal", self.pantallaRealizarMov.cursoComboBox.currentText(),):
            self.pantallaRealizarMov.alumnoComboBox.addItem(i[1])
            sugerencias.append(i[1])

        self.pantallaRealizarMov.alumnoComboBox.setCompleter(self.completar(sugerencias))
        self.pantallaRealizarMov.alumnoComboBox.setCurrentIndex(-1)

    def clases(self):
        self.pantallaRealizarMov.cursoComboBox.clear()
        print("xd")
        sugerencias=[]
        for i in dal.obtenerDatos("clases", ""):
            if i[2] not in {"Previas", "Egresado"}:
                index = self.pantallaRealizarMov.cursoComboBox.findText(str(i[2]))
                if index == -1:
                    self.pantallaRealizarMov.cursoComboBox.addItem(i[2])
                    sugerencias.append(i[2])
        self.pantallaRealizarMov.cursoComboBox.setCompleter(self.completar(sugerencias))
        self.pantallaRealizarMov.cursoComboBox.setCurrentIndex(-1)

    #Funcion que llena la combobox de herramientas en nuevo movimento
    def herramientas(self):
        self.pantallaRealizarMov.herramientaComboBox.clear()
        sugerencias = []
        for i in dal.obtenerDatos("stock", self.pantallaRealizarMov.ubicacionComboBox.currentText(),):
            self.pantallaRealizarMov.herramientaComboBox.addItem(i[1])
            sugerencias.append(i[1])
        self.pantallaRealizarMov.herramientaComboBox.setCompleter(self.completar(sugerencias))
        self.pantallaRealizarMov.herramientaComboBox.setCurrentIndex(-1)

    #Funcion que verifica y altera nmovimientos segun cual es el tipo de movimiento que se selecciona
    def check(self):
        for i in dal.obtenerDatos("estados", ""):
            index = self.pantallaRealizarMov.estadoComboBox.findText(i[1])
            if index == -1:
                self.pantallaRealizarMov.estadoComboBox.addItem(i[1])
        if self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText() == "Envío a Reparación":
            self.pantallaRealizarMov.cursoComboBox.hide()
            self.pantallaRealizarMov.alumnoComboBox.hide()
            self.pantallaRealizarMov.cursoLabel.hide()
            self.pantallaRealizarMov.alumnoLabel.hide()
            self.pantallaRealizarMov.estadoLabel.hide()
            self.pantallaRealizarMov.estadoComboBox.hide()
            try:
                self.pantallaRealizarMov.estadoComboBox.disconnect()
            except:
                pass
            self.pantallaRealizarMov.estadoComboBox.setCurrentIndex(
                self.pantallaRealizarMov.estadoComboBox.findText("De Baja"))
            self.pantallaRealizarMov.descripcionLabel.setText("Ubicacion de destino:")
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.show()
            self.pantallaRealizarMov.herramientasDisponiblesLabel.show()
            self.pantallaRealizarMov.herramientaComboBox.textActivated.connect(
                lambda: self.cant(3))
            self.pantallaRealizarMov.ubicacionComboBox.textActivated.connect(self.herramientas)
       
        elif self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText() == "Ingreso":
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.hide()
            self.pantallaRealizarMov.herramientasDisponiblesLabel.hide()
            self.pantallaRealizarMov.alumnoComboBox.hide()
            self.pantallaRealizarMov.alumnoLabel.hide()
            self.pantallaRealizarMov.descripcionLabel.setText("Descripcion:")
            self.pantallaRealizarMov.cursoComboBox.hide()
            self.pantallaRealizarMov.cursoLabel.hide()
            self.pantallaRealizarMov.descripcionLabel.setText("Descripcion:")
            self.pantallaRealizarMov.cantidadSpinBox.setMaximum(9999)
            self.pantallaRealizarMov.estadoComboBox.removeItem(
                self.pantallaRealizarMov.estadoComboBox.findText("En Reparación")
            )

        elif self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText() == "Retiro":
            self.pantallaRealizarMov.estadoComboBox.removeItem(
                self.pantallaRealizarMov.estadoComboBox.findText("En Reparación"))
            self.pantallaRealizarMov.estadoComboBox.removeItem(
                self.pantallaRealizarMov.estadoComboBox.findText("De Baja"))
            self.pantallaRealizarMov.cursoComboBox.show()
            self.pantallaRealizarMov.cursoLabel.show()
            self.pantallaRealizarMov.alumnoLabel.show()
            self.pantallaRealizarMov.alumnoComboBox.show()
            self.pantallaRealizarMov.descripcionLabel.setText("Descripcion:")
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.show()
            self.pantallaRealizarMov.herramientasDisponiblesLabel.show()

        elif self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText() == "Ingreso de Herramienta Reparada":
            self.pantallaRealizarMov.estadoComboBox.removeItem(
                self.pantallaRealizarMov.estadoComboBox.findText("En Reparación"))
            self.pantallaRealizarMov.estadoLabel.show()
            self.pantallaRealizarMov.estadoComboBox.show()
            self.pantallaRealizarMov.cursoComboBox.hide()
            self.pantallaRealizarMov.alumnoComboBox.hide()
            self.pantallaRealizarMov.cursoLabel.hide()
            self.pantallaRealizarMov.alumnoLabel.hide()
            self.pantallaRealizarMov.descripcionLabel.hide()
            self.pantallaRealizarMov.descripcionLineEdit.hide()
            self.pantallaRealizarMov.cantidadSpinBox.setMaximum(9999)
            self.pantallaRealizarMov.ubicacionComboBox.textActivated.connect(
                lambda: self.reparadas(self.pantallaRealizarMov.ubicacionComboBox.currentText()))
            self.pantallaRealizarMov.herramientaComboBox.textActivated.connect(
                lambda: self.cant(4)
            )
            try:
                self.pantallaRealizarMov.estadoComboBox.disconnect()
            except:
                pass

        elif self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText() == "Dar De Baja":
            if self.pantallaRealizarMov.estadoComboBox.findText("En Condiciones") == -1:
                self.pantallaRealizarMov.estadoComboBox.addItem("En Condiciones")
            self.pantallaRealizarMov.estadoComboBox.setCurrentIndex(
                self.pantallaRealizarMov.estadoComboBox.findText("En Condiciones"))
            self.pantallaRealizarMov.estadoLabel.hide()
            self.pantallaRealizarMov.estadoComboBox.hide()
            self.pantallaRealizarMov.cursoComboBox.hide()
            self.pantallaRealizarMov.alumnoComboBox.hide()
            self.pantallaRealizarMov.cursoLabel.hide()
            self.pantallaRealizarMov.alumnoLabel.hide()
            self.pantallaRealizarMov.descripcionLabel.setText("Motivo:")
            self.pantallaRealizarMov.descripcionLabel.show()
            self.pantallaRealizarMov.descripcionLineEdit.show()
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.show()
            self.pantallaRealizarMov.herramientasDisponiblesLabel.show()

        elif self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText() == "Devolución":
            self.pantallaRealizarMov.herramientasDisponiblesLineEdit.show()
            self.pantallaRealizarMov.herramientasDisponiblesLabel.show()
            self.pantallaRealizarMov.ubicacionComboBox.textActivated.disconnect()
            self.pantallaRealizarMov.ubicacionComboBox.textActivated.connect(self.deudasp)
            self.pantallaRealizarMov.herramientaComboBox.textActivated.connect(lambda: self.cant(2))
            self.pantallaRealizarMov.cursoComboBox.show()
            self.pantallaRealizarMov.cursoLabel.show()
            self.pantallaRealizarMov.alumnoLabel.show()
            self.pantallaRealizarMov.alumnoComboBox.show()
            try:
                self.pantallaRealizarMov.estadoComboBox.disconnect()
            except:
                pass
            self.pantallaRealizarMov.estadoComboBox.removeItem(
                self.pantallaRealizarMov.estadoComboBox.findText("En Reparación"))
            self.pantallaRealizarMov.descripcionLabel.setText("Descripción:")
        
        if self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText() not in {"Ingreso de Herramienta Reparada", "Devolución", "Envío a Reparación"}:
            self.deactA()
            self.deactB()
            self.deactC()
            self.deactD()
            self.herramientas()
            self.clases()
            self.pantallaRealizarMov.herramientaComboBox.textActivated.connect(lambda: self.cant(0,self.pantallaRealizarMov.estadoComboBox.currentText()))
            self.pantallaRealizarMov.estadoComboBox.textActivated.connect(lambda: self.cant(0,self.pantallaRealizarMov.estadoComboBox.currentText()))
            self.pantallaRealizarMov.cursoComboBox.textActivated.connect(self.alumnos)
            self.pantallaRealizarMov.ubicacionComboBox.textActivated.connect(self.herramientas)
            
        self.pantallaRealizarMov.ubicacionComboBox.setCurrentIndex(-1)
        self.pantallaRealizarMov.alumnoComboBox.setCurrentIndex(-1)
        
    #carga el resto de combobox de nuevo movimiento
    def realizarMovimiento(self, turno = None):
        if self.pantallaRealizarMov.tipoDeMovimientoComboBox.count()<3:

            for i in dal.obtenerDatos("tipos_mov", ""):
                index = self.pantallaRealizarMov.tipoDeMovimientoComboBox.findText(i[1])
                if index == -1:
                    self.pantallaRealizarMov.tipoDeMovimientoComboBox.addItem(i[1])

            for i in dal.obtenerDatos("estados", ""):
                index = self.pantallaRealizarMov.estadoComboBox.findText(i[1])
                if index == -1:
                    self.pantallaRealizarMov.estadoComboBox.addItem(i[1])

            self.clases()

            for i in dal.obtenerDatos("ubicaciones", ""):
                index = self.pantallaRealizarMov.tipoDeMovimientoComboBox.findText(i[1])
                if index == -1:
                    self.pantallaRealizarMov.ubicacionComboBox.addItem(i[1])

            self.pantallaRealizarMov.tipoDeMovimientoComboBox.setCurrentIndex(-1)
            
        if turno:
            self.pantallaRealizarMov.tipoDeMovimientoComboBox.removeItem(
                self.pantallaRealizarMov.tipoDeMovimientoComboBox.findText("Envío a Reparación")
            )
            self.pantallaRealizarMov.tipoDeMovimientoComboBox.removeItem(
                self.pantallaRealizarMov.tipoDeMovimientoComboBox.findText("Dar De Baja")
            )
            self.pantallaRealizarMov.tipoDeMovimientoComboBox.removeItem(
                self.pantallaRealizarMov.tipoDeMovimientoComboBox.findText("Ingreso")
            )
            self.pantallaRealizarMov.tipoDeMovimientoComboBox.removeItem(
                self.pantallaRealizarMov.tipoDeMovimientoComboBox.findText("Ingreso de Herramienta Reparada")
            )
        self.stackedWidget.setCurrentIndex(13)

    #Suma la cantidad de herramientas a la base de datos
    def sumar(self, cant, herramienta, estado):
        try:
            estado = estado[estado.index(" "):]
            estado = estado[1:]
        except:
            pass
        estado = unidecode(estado)
        estado = "cant_" + estado.lower()
        query = f"select {estado} from stock WHERE id = ?"
        params = (herramienta,)
        if bdd.cur.execute(query,params) ==None:
            query = f"UPDATE stock SET {estado} = 0 + ? WHERE id = ?"
        else:
            query = f"UPDATE stock SET {estado} = {estado} + ? WHERE id = ?"
            params = (cant, herramienta)
        self.sopas = True
        bdd.cur.execute(query, params)

    #Resta la cantidad de herramientas a la base de datos
    def restar(self, cant,herramienta,estado):
        try:
            estado = estado[estado.index(" "):]
            estado = estado[1:]
        except:
            pass
        estado = unidecode(estado)
        estado = "cant_" + estado.lower()
        query = f"select {estado} from stock WHERE id = ?"
        params = (herramienta,)
        try:
            resultado = bdd.cur.execute(query,params).fetchone()[0]
            if resultado is None:
                resultado = 0
        except:
            print("ERROR DE PROGRAMACION")
            return
        if resultado-cant >=0:
            query = f"UPDATE stock SET {estado} = {estado} - ? WHERE id = ?"
            params = (cant, herramienta)
            bdd.cur.execute(query, params)
            bdd.con.commit()
            self.sopas = True
        else:
            self.sopas = False

    #Guarda el movimiento
    def saveMovimiento(self):
        turno = bdd.cur.execute(
            "select id from turnos where fecha_egr IS NULL").fetchall()
        tipo = dal.obtenerDatos(
            "tipos_mov", self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText())
        cant = self.pantallaRealizarMov.cantidadSpinBox.value()
        estado = dal.obtenerDatos(
            "estados", self.pantallaRealizarMov.estadoComboBox.currentText())
        persona = bdd.cur.execute('''SELECT p.id 
            FROM personal p
            JOIN clases c ON c.id = p.id_clase
            WHERE p.nombre_apellido LIKE ?
            and c.descripcion LIKE ?;''', (self.pantallaRealizarMov.alumnoComboBox.currentText(), self.pantallaRealizarMov.cursoComboBox.currentText())).fetchone()
        ubicacion = dal.obtenerDatos(
            "ubicaciones", self.pantallaRealizarMov.ubicacionComboBox.currentText())
        herramienta = bdd.cur.execute(
            """SELECT s.id FROM STOCK s
            JOIN subgrupos sub ON s.id_subgrupo = sub.id
            JOIN grupos g ON sub.id_grupo=g.id
            JOIN ubicaciones u ON s.id_ubi=u.id
            where s.descripcion LIKE ? and s.id_ubi  LIKE ?""" , (self.pantallaRealizarMov.herramientaComboBox.currentText(), ubicacion[0][0])).fetchone()

        descripcion = self.pantallaRealizarMov.descripcionLineEdit.text()
        fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        texto = self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText()
        if texto == " " or texto == None or texto=="":
            mensaje = """Por favor ingrese el tipo de movimiento que desea realizar."""
            return PopUp("Error", mensaje).exec()
        else:
            if herramienta == " " or herramienta == None:
                mensaje = """Por favor ingrese la herramienta que desea mover."""
                return PopUp("Error", mensaje).exec()
            else:
                if cant == 0:
                    mensaje = """Por favor ingrese un valor mayor a 0."""
                    return PopUp("Error", mensaje).exec()
                else:
                    if texto in {"Dar De Baja", "Ingreso de Herramienta Reparada", "Envío a Reparación", "Ingreso"}:
                        persona = bdd.cur.execute("""SELECT id FROM personal where dni= ?""" , (self.usuario,)).fetchall()[0]
                    if (descripcion == " " or not descripcion) and texto in {"Envío a Reparacion", "Dar De Baja"}:
                        if texto=="Envío a Reparación":
                            mensaje = """Por favor ingrese la ubicacion a la que la herramienta será enviada"""
                        else:
                            mensaje = """Por favor ingrese el motivo por el que la herramienta se dió de baja"""
                        return PopUp("Error", mensaje).exec()
                    if persona:
                        try:
                            turno = turno[0][0]
                        except:
                            turno = None
                        if tipo[0][0] == 1:
                            bdd.cur.execute("INSERT INTO movimientos(id_turno,id_elem,id_estado,cant,id_persona,fecha_hora,id_tipo,descripcion) VALUES(?, ?, ?, ?, ?, ?, ?,?)",
                                        (turno, herramienta[0], estado[0][0], cant, persona[0], fecha, tipo[0][0], descripcion))
                            self.sumar(cant, herramienta[0], estado[0][1])
                        elif tipo[0][0] == 2:
                            usuario = bdd.cur.execute("""SELECT id FROM personal where dni= ?""" , (self.usuario,)).fetchall()[0][0]
                            self.restar(cant, herramienta[0], estado[0][1])
                            self.sumar(cant, herramienta[0],"reparacion")
                            bdd.cur.execute("INSERT INTO reparaciones(id_herramienta,cantidad,id_usuario,destino,fecha_envio) VALUES(?, ?, ?, ?, ?)",(herramienta[0],cant, usuario,descripcion, fecha[:10]))
                        elif tipo[0][0] == 3:
                            bdd.cur.execute("INSERT INTO movimientos(id_turno,id_elem,id_estado,cant,id_persona,fecha_hora,id_tipo,descripcion) VALUES(?, ?, ?, ?, ?, ?, ?,?)",
                                        (turno, herramienta[0], estado[0][0], cant, persona[0], fecha, tipo[0][0], descripcion))
                            self.restar(cant, herramienta[0],estado[0][1])
                            self.sumar(cant, herramienta[0],"prest")
                            bdd.cur.execute("INSERT INTO deudas (id_mov, cant) SELECT id, ? FROM movimientos ORDER BY id DESC LIMIT 1", (cant,))
                        elif tipo[0][0] == 4:
                            sql="""SELECT d.id_mov FROM deudas d 
                            join movimientos m on d.id_mov = m.id
                            where m.id_elem=? and m.id_persona=?"""
                            id = bdd.cur.execute(
                                    sql, (herramienta[0], persona[0])).fetchone()
                            if id:
                                self.sumar(cant, herramienta[0],estado[0][1])
                                self.restar(cant, herramienta[0],"prest")
                                bdd.cur.execute("DELETE FROM deudas WHERE id_mov = ?",(id[0],))
                            else:
                                mensaje = """No se ha encontrado el movimiento"""
                                return PopUp("Error", mensaje).exec()
                        elif tipo[0][0] == 5:
                            bdd.cur.execute("INSERT INTO movimientos(id_turno,id_elem,id_estado,cant,id_persona,fecha_hora,id_tipo,descripcion) VALUES(?, ?, ?, ?, ?, ?, ?,?)",
                                        (turno, herramienta[0], estado[0][0], cant, persona[0], fecha, tipo[0][0], descripcion))
                            self.restar(cant, herramienta[0], estado[0][1])
                            self.sumar(cant, herramienta[0], "baja")
                        elif tipo[0][0] == 6:
                            sql="""SELECT id
                            FROM reparaciones
                            WHERE id_herramienta = ?
                            AND cantidad = ?
                            AND fecha_regreso IS NULL
                            ORDER BY id"""
                            id = bdd.cur.execute(sql, (herramienta[0], cant,)).fetchone()
                            if id:
                                self.sumar(cant,herramienta[0],estado[0][1])
                                self.restar(cant, herramienta[0],"En reparacion")
                                sql="""UPDATE reparaciones
                                SET fecha_regreso = ?
                                WHERE cantidad = ? and id_herramienta = ?"""
                                bdd.cur.execute(sql, (datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 
                                                      cant, herramienta[0]))
                            else:
                                mensaje = """No se ha encontrado el movimiento"""
                                return PopUp("Error", mensaje).exec()

                        bdd.con.commit()
                        # Hermano que hiciste aca
                        if hasattr(self,"sopas"):
                            if self.sopas == True:
                                self.clear()                                
                                mensaje = """Movimiento realizado con exito."""
                                return PopUp("Aviso", mensaje).exec()
                            else:
                                mensaje = """Movimiento cancelado no hay suficientes herramientas para realizar el movimiento."""
                                return PopUp("Error", mensaje).exec()

                    else:
                        mensaje = """Por favor ingrese el nombre del alumno solicitante."""
                        return PopUp("Error", mensaje).exec()
                    
    def habilitarSaves(self, row: int | None = None, col: int | None = None,
                       tabla: QtWidgets.QTableWidget | None = None):
        """Este método habilita el botón de guardar de una fila de una
        tabla de una gestión.
        
        Parámetros
        ----------
            row: int | None = None
                La fila en la que está el boton.
                Default: None.
            col: int | None = None
                La columna de la que se ejecutó la función, no se usa
                pero es necesario declararla porque, si se ejecuta
                de una forma especial, esa ejecución pasa por defecto
                un parámetor de columna que, si no guardaramos en ese
                parámetro, estaría sobreescribiendo el parámetro tabla.
                Default: None.
            tabla: QtWidgets.QTableWidget | None = None
                La tabla en la que está el botón.
                Default:None
        """
        if tabla is None:
            tabla = self.sender()
        if row is None:
            row = tabla.indexAt(self.sender().pos()).row()
        tabla.cellWidget(row, tabla.columnCount()-2).setEnabled(True)
        tabla.parent().botonGuardar.setEnabled(True)

    def actualizarTotal(self, row: int, col: int,
                        tabla: QtWidgets.QTableWidget | None = None):
        """Este método actualiza el campo total de la tabla stock
        cuando se modifican las cantidades, y habilita el botón de 
        guardar de la fila modificada.
        
        Parámetros
        ----------
            row: int
                La fila del campo modificado.
            col: int
                La columna del campo modificado.
            tabla: QtWidgets.QTableWidget
                La tabla a la que se le actualizará el total.
                Default: None
        """
        # Si no se pasó una tabla por parámetro...
        if tabla is None:
            # ... se usa la tabla de la pantalla stock.
            tabla = self.pantallaStock.tableWidget
        tabla.setSortingEnabled(False)
        # Si esta función se ejecuta, significa que el usuario
        # modificó una fila de la tabla. Por eso, habilitamos los saves
        # de la fila para que el usuario pueda guardar los cambios.
        self.habilitarSaves(row, col, tabla)
        # Esta función se ejecuta siempre que el usuario modifique una
        # celda, sin distinguir la columna, por eso hay que checkear si
        # la columna modificada fue una de una cantidad antes de
        # ejecutar el código.
        # Si la columna modificada es de cantidad en condiciones,
        # cantidad en reparación o cantidad de baja...
        if col in (2, 3, 4, 5):
            #...inicializamos la variable del total
            total = 0
            # obtenemos las cantidades en una tupla
            cantidades = (tabla.item(row, 2).data(0),
                          tabla.item(row, 3).data(0),
                          tabla.item(row, 4).data(0),
                          tabla.item(row, 5).data(0),)
            # Por cada cantidad y su índice...
            for col, cantidad in enumerate(cantidades):
                try:
                    # Vemos si la cantidad es un entero. Si tira error
                    # es texto.
                    cantidad = int(cantidad)
                    # Si el número es negativo...
                    if cantidad < 0:
                        #...se ingresa un 0 en su lugar
                        tabla.item(row, col + 2).setData(0, 0)
                    # Si no...
                    else:
                        # ... se suma al total. 
                        total += int(cantidad)
                except:
                    # Se establece en 0
                    tabla.item(row, col + 2).setData(0, 0)
            # Creamos el item que vamos a meter en la tabla
            item = QtWidgets.QTableWidgetItem(str(total))
            # Hacemos que no sea editable
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                          QtCore.Qt.ItemFlag.ItemIsEnabled)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            # Lo insertamos a la tabla
            tabla.setItem(row, 6, item)
            tabla.setSortingEnabled(True)

    def actualizarSugSubgrupos(self):
        """Este método actualiza las sugerencias de los campos de
        subgrupos al editar lo ingresado en un campo de grupos
        relacionado, ya que las sugerencias de subgrupos deben estar
        relacionadas al grupo ingresado.
        """
        # Usamos la tabla de stock.
        tabla = self.pantallaStock.tableWidget
        # Obtenemos la fila del campo de grupos modificado.
        row = tabla.indexAt(self.sender().pos()).row()
        # Obtenemos los nuevos datos.
        grupo = tabla.cellWidget(row, 7).text()
        # Obtenemos el cuadro de sugerencias del campo subgrupos.
        completer = tabla.cellWidget(row, 8).completer()
        # Obtenemos sugerencias actualizadas.
        sugerencias =[i[0] for i in 
                     bdd.cur.execute('''SELECT s.descripcion FROM subgrupos s
                     JOIN grupos g ON s.id_grupo = g.id
                     WHERE g.descripcion LIKE ?''', (grupo,)).fetchall()]
        # Añadimos las sugerencias actualizadas al campo de subgrupos.
        completer.setModel(QtCore.QStringListModel(sugerencias))
        # Habilitamos el boton de guardar para que el usuario pueda
        # guardar los cambios.
        tabla.cellWidget(row, tabla.columnCount()-2).setEnabled(True)

    def fetchStock(self):
        """Este método refresca la tabla y los filtros de la pantalla
        stock.
        """
        # Los métodos de fetch son parecidos a este, por lo que solo
        # voy a documentar esta función. Si hay una acción especial
        # en algún otro método fetch, lo voy a documentar.
        # Obtenemos la tabla.
        tabla = self.pantallaStock.tableWidget
        # Desactivamos el sorting por defecto porque si alguien
        # refresca con el sorting activado se bugea.
        tabla.setSortingEnabled(False)
        # Desconectamos la tabla para que no ejecute funciones mientras
        # la refrescamos.
        try:
            tabla.disconnect()
        except:
            pass
        # Se refresca la tabla, eliminando todas las filas anteriores.
        tabla.setRowCount(0)
        
        # Obtenemos los filtros.
        barraBusqueda = self.pantallaStock.lineEdit

        listaUbi = self.pantallaStock.listaUbi
        # Desconectamos el filtro por la misma razón que la tabla.
        listaUbi.disconnect()
        # Obtenemos el texto seleccionado en el filtro.
        ubiSeleccionada = listaUbi.currentText()
        # Volvemos a buscar sugerencias.
        ubis = bdd.cur.execute("""SELECT DISTINCT u.descripcion
                                FROM stock s
                                JOIN ubicaciones u
                                ON u.id=s.id_ubi""").fetchall()
        # Limpiamos las sugerencias viejas.
        listaUbi.clear()
        # Añadimos el cuadro de sugerencias actualizado.
        listaUbi.addItem("Todas")
        for ubi in ubis:
            listaUbi.addItem(ubi[0])
        # Volvemos a seleccionar la opción que estaba seleccionada
        # desde antes de refrescar.
        listaUbi.setCurrentIndex(listaUbi.findText(ubiSeleccionada))
        # Si la ubi seleccionada es "todas", no aplicamos un filtro.
        if ubiSeleccionada == "Todas":
            filtroUbi = (None,)
        # Lo guardamos en una tupla porque la dal recibe por parámetro
        # una tupla.
        else:
            filtroUbi = (ubiSeleccionada,)

        # Se obtienen los datos de la base de datos.
        datos = dal.obtenerDatos("stock", barraBusqueda.text(), filtroUbi)

        # Por cada número de fila y los contenidos de ésta en los datos
        # obtenidos...
        for rowNum, rowData in enumerate(datos):
            # ...se añade una fila a la tabla.
            tabla.insertRow(rowNum)

            # Empezamos a añadir los items.
            item0 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            # Los centramos.
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            item1 = QtWidgets.QTableWidgetItem(str(rowData[1]))
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 1, item1)
            item2 = QtWidgets.QTableWidgetItem()
            # Los items numéricos los ponemos de esta forma para que qt
            # los reconozca como números y los ordene numéricamente.
            item2.setData(0, rowData[2])
            item2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 2, item2)
            item3 = QtWidgets.QTableWidgetItem()
            item3.setData(0, rowData[3])
            item3.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item3.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                           QtCore.Qt.ItemFlag.ItemIsEnabled)
            tabla.setItem(rowNum, 3, item3)
            item4 = QtWidgets.QTableWidgetItem()
            item4.setData(0, rowData[4])
            item4.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 4, item4)
            item5 = QtWidgets.QTableWidgetItem()
            item5.setData(0, rowData[5])
            item5.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item5.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                           QtCore.Qt.ItemFlag.ItemIsEnabled)
            tabla.setItem(rowNum, 5, item5)
            item6 = QtWidgets.QTableWidgetItem()
            item6.setData(0, rowData[6])
            item6.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item6.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                           QtCore.Qt.ItemFlag.ItemIsEnabled)
            tabla.setItem(rowNum, 6, item6)

            # Creamos el campo de sugerencias del campo grupos.
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute('SELECT descripcion FROM grupos'
                           ).fetchall()]
            # Creamos el campo con sugerencia.
            paramGrupos = ParamEdit(sugerencias, rowData[7])
            # Cuando termina de editarse, hacemos que actualice el
            # cuadro de sugerencias del campo grupos.
            paramGrupos.editingFinished.connect(self.actualizarSugSubgrupos)
            tabla.setCellWidget(rowNum, 7, paramGrupos)
            sql = '''SELECT s.descripcion FROM subgrupos s
                   JOIN grupos g ON s.id_grupo = g.id
                   WHERE g.descripcion LIKE ?'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql, (rowData[7],)).fetchall()]
            subgrupos = ParamEdit(sugerencias, rowData[8])
            subgrupos.textChanged.connect(
                lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(rowNum, 8, subgrupos)
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(
                           'SELECT descripcion FROM ubicaciones').fetchall()]
            ubicaciones = ParamEdit(sugerencias, rowData[9])
            ubicaciones.textChanged.connect(
                lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(rowNum, 9, ubicaciones)

            # Generamos los botones para la fila de la tabla
            core.generarBotones(
                lambda: self.saveOne(tabla, dal.saveStock, datos),
                lambda: self.deleteStock(datos), tabla, rowNum)

            # Cambiamos la altura de la fila.
            tabla.setRowHeight(rowNum, 35)
        # Hacemos que las columnas no puedan ser menos anchas que sus
        # contenidos.
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            7, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            8, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Hacemos que cada vez que se edite una celda de una tabla, se
        # ejecuta la función.
        tabla.cellChanged.connect(self.actualizarTotal)
        # Volvemos a habilitar el sorting.
        tabla.setSortingEnabled(True)
        # Volvemos a conectar el filtro.
        listaUbi.setMinimumWidth(
            listaUbi.minimumSizeHint().width() + 100
        )
        listaUbi.currentIndexChanged.connect(self.fetchStock)
        # Mostramos la pantalla de stock.
        self.stackedWidget.setCurrentIndex(3)

    def saveOne(self, tabla: QtWidgets.QTableWidget, funcSave: function,
                datos: list | None = None):
        """Este método guarda los cambios hechos en una fila de una
        tabla de una gestión.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la fila a guardar.
            funcSave: function
                La función de guardar relacionada a la gestión.
            funcFetch: function
                La función de refrescar relacionada a la gestión.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        # Obtenemos el id de la fila, que es la posición donde se
        # apretó el boton de guardar.
        row = tabla.indexAt(self.sender().pos()).row()
        # Preguntamos si el usuario quiere guardar los cambios.
        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila?"
        popup = PopUp("Pregunta", info).exec()
        # Si respondió que sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Se ejecuta la función de guardado.
            exito = funcSave(tabla, row, self.usuario, datos)
            # Si el guardado fue exitoso...
            if exito == True:
                # Se muestra que el guardado fue con éxito.
                tabla.cellWidget(row, tabla.columnCount()-2).setEnabled(False)
                info = "Los datos se han guardado con éxito."
                PopUp("Aviso", info).exec()
                self.actualizarSug()

    def saveAll(self, tabla: QtWidgets.QTableWidget, funcSave: function,
                datos: list | None = None):
        """Este método guarda todos los cambios hechos en una tabla de
        una gestión.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la fila a guardar.
            funcSave: function
                La función de guardar relacionada a la gestión.
            funcFetch: function
                La función de refrescar relacionada a la gestión.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        # Esta función es igual a saveOne, asi que solo documento
        # la diferencia.
        info = "Esta acción no se puede deshacer. ¿Desea guardar todos los cambios?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Inicializamos el exito de antes porque puede no
            # inicializarse.
            exito=True
            # Por cada fila de la tabla...
            for i in range(tabla.rowCount()):
                #...si se hicieron cambios en la fila...
                # Si el botón de guardar está habilitado, significa
                # que la fila fue modificada.
                if tabla.cellWidget(i, tabla.columnCount()-2).isEnabled():
                    # guardamos los cambios.
                    if not funcSave(tabla, i, self.usuario, datos):
                        exito=False
                    else:
                        tabla.cellWidget(i, tabla.columnCount()-2).setEnabled(False)

            if exito==True:
                info = "Los datos se han guardado con éxito."
                PopUp("Aviso", info).exec()
                self.actualizarSug()
            else:
                info = "Los datos se han guardado con errores. Revise los campos que quedaron sin guardar."
                PopUp("Advertencia", info).exec()

    def deleteStock(self, datos: list | None = None) -> None:
        """Este método elimina una fila de la tabla de la gestión
        stock.

        Parámetros
        ----------
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        # Obtenemos la tabla stock
        tabla = self.pantallaStock.tableWidget
        # Obtenemos la fila en la que se presionó el botón eliminar
        row = (tabla.indexAt(self.sender().pos())).row()
        idd = tabla.item(row, 0).text()
        # Si el id de la tabla está en blanco, significa que la tabla
        # fue recientemente agregada, entonces...
        if not idd:
            # ...no esta registrada en la base de datos, solo debemos
            # sacarla de la UI. Acá cortamos la función.
            return tabla.removeRow(row)
        # Transformamos el id en número.
        idd = int(idd)
        # Si está relacionada con la base de datos, antes de eliminar,
        # tenemos que verificar que la PK de la fila no
        # tenga relaciones foráneas con otras tablas. Si llegase a
        # tener, no podemos permitir una eliminación normal por dos
        # motivos. El primero, necesitamos registrar todos los campos
        # eliminados en el historial, y eliminar todo de una nos
        # complica registrar que tablas se eliminaron. El segundo, si
        # un profe se equivoca y elimina todo, no hay vuelta atrás.
        # Para esta verificación, llamamos a la función del dal.
        hayRelacion = dal.verifElimStock(idd)
        desc=tabla.item(row, 1).text()
        ubi=tabla.cellWidget(row, 9).text()
        if hayRelacion:
            mensaje = f"El elemento {desc} de la ubicación {ubi} tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar esta herramienta/insumo."
            return PopUp('Advertencia', mensaje).exec()

        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = f"Esta acción no se puede deshacer. ¿Desea eliminar el elemento {desc} de la ubicación {ubi}?"
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Obtenemos los datos para guardarlos en el historial.
            try:
                datosEliminados = [fila for fila in datos
                                   if fila[0] == idd][0]
            except TypeError:
                datosEliminados = []
                for numCol in range(tabla.columnCount() - 2):
                    if core.camposStock[1][numCol] < 2:
                        datosEliminados.append(tabla.item(row, numCol).text())
                    else:
                        datosEliminados.append(tabla.cellWidget(row, numCol).text())

            # Insertamos los datos en el historial para que quede registro.
            dal.insertarHistorial(
                self.usuario, "Eliminación", "Stock",
                f'{datosEliminados[1]} {datosEliminados[9]}',
                datosEliminados[2:])
            # Eliminamos los datos
            dal.eliminarDatos('stock', idd)
            tabla.removeRow(row)

    def printStock(self):
        """Este método genera un spreadsheet a partir de la tabla de la
        pantalla stock.
        """
        info = "Los cambios no guardados no se imprimirán. Guarde todos los cambios antes de imprimir."
        boton = PopUp('Advertencia', info).exec()
        # Si se cerro sin apretar ok, no se ejecuta.
        if boton == QtWidgets.QMessageBox.StandardButton.Ok:
            # Creamos la ventana filedialog.
            filename = QtWidgets.QFileDialog(self).getSaveFileName(self,
                'Guardar archivo', os.path.expanduser('~documents'),
                'Hoja de cálculo (*.xlsx)'
            );
            # Si no se abrió un archivo, corta la función
            if not filename[0]:
                return

            # Obtenemos los filtros
            barraBusqueda = self.pantallaStock.lineEdit
            listaUbi = self.pantallaStock.listaUbi
            # Obtenemos los datos de los filtros.
            if listaUbi.currentText() == "Todas":
                filtroUbi = (None,)
            else:
                filtroUbi = (listaUbi.currentText(),)

            # Obtenemos los datos usando los filtros ingresados.
            datos = dal.obtenerDatos(
                "stock", barraBusqueda.text(), filtroUbi)
            # Definimos las columnas de la spreadsheet en una lista
            columnas = ["Elemento", "Cant. en Condiciones",
                        "Cant. en Reparación", "Cant. de Baja",
                        "Cant. Prestadas", "Total", "Grupo", "Subgrupo",
                        "Ubicación"]
            # Creamos el dataframe. Usamos la list comprehension
            # para ignorar el campo id de las filas al generarlo.
            df = pd.DataFrame([i[1:] for i in datos], columns=columnas)
            # Intentamos...
            try:
                #... crear el xlsx a partir del dataframe.
                df.to_excel(filename[0])
                info = "Los datos se imprimieron exitosamente."
                PopUp('Aviso', info).exec()
            # Excepto que el sistema no permita la generación...
            except PermissionError:
                # suele ocurrir porque se quiere reemplazar un archivo
                # que está siendo usado por otra app, y windows no deja
                # hacer eso.
                info = "Ocurrió un error al imprimir la tabla. Esto pudo haber ocurrido porque intentó reemplazar un documento que tenía abierto o estaba siendo usado por otra app. Por favor, verifique que el documento que desea reemplazar esté cerrado y no esté siendo usado por ningún otra app."
                PopUp('Aviso', info).exec()

    def cargarPlanillaAlumnos(self):
        """Este método crea un dataframe para la carga de datos
        de una spreadsheet en la base de datos de la gestión alumnos.
        """
        info = '¿La planilla está en el formato de tutorvip?'
        formato = PopUp('Pregunta-Info', info).exec()
        # Si está en el formato de tutorvip...
        if formato == QtWidgets.QMessageBox.StandardButton.Yes:
            #...pregunta al usuario si quiere reemplazar el sistema de
            # cursos.
            info = 'El formato de los cursos del sistema puede ser diferente al del tutorvip.\n¿Desea reemplazar el formato de cursos actual con el formato de la planilla?'
            actualizarCursos = PopUp('Pregunta', info).exec()
            # Si el usuario respondio que si o que no...
            if actualizarCursos in (QtWidgets.QMessageBox.StandardButton.Yes,
                                    QtWidgets.QMessageBox.StandardButton.No):
                #...cargamos un valor bool de si respondio si o no.
                actualizarCursos = (QtWidgets.QMessageBox.StandardButton.Yes
                                    == actualizarCursos)
            # Si cerro sin responder, corta la función
            else:
                return
        # Si no usa el formato de tutorvip...
        elif formato == QtWidgets.QMessageBox.StandardButton.No:
            #...advierte al usuario.
            info = 'Esta acción no se puede deshacer. Los datos de la gestión se actualizarán en base al dni y se actualizarán los nombres y los cursos en base a los datos de la planilla. Asegúrese que los dni de la planilla y de la gestión alumnos sean correctos, de lo contrario se pueden originar alumnos duplicados. Además, asegúrese de que los datos (columnas) de la planilla esten en el siguiente orden: nombre, curso y dni.'
            # Si cerro sin responder, corta la función.
            if (PopUp('Advertencia', info).exec() !=
                QtWidgets.QMessageBox.StandardButton.Ok):
                return
            # Como se van a reemplazar los cursos si o si en esta
            # opción, inicializamos la variable como true.
            actualizarCursos = True
        # Si cerró sin responder (no respondío si ni no), corta.
        else:
            return
        # Cargamos formato con el valor bool de si usa el formato de
        # tutorvip o no.
        formato = formato == QtWidgets.QMessageBox.StandardButton.Yes

        # Creamos el dialog.
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(os.path.expanduser('~documents'))
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        dialog.setNameFilter(
            "Hoja de cálculo (*.xlsx *.xls *.xlsm *.xlsb *.xltx *.xltm *.xlt *.xlam *.xla *.xlw *.xlr)")
        dialog.setWindowTitle('Abrir archivo')
        # Si abrió un archivo el usuario...
        if dialog.exec():
            # Obtenemos el nombre
            filename = dialog.selectedFiles()[0]
        # Si no abrió un archivo, corta la función
        else:
            return
        
        # Intentamos hacer el dataframe a partir del excel
        try:
            df = pd.read_excel(filename)
        # Si el archivo no es válido, avisamos y cortamos la funcion.
        except:
            info = 'El archivo proporcionado no es válido como planilla. Proporcione un archivo válido.'
            return PopUp('Error', info).exec()
        # Obtenemos las columnas
        cols = list(df.columns.values)

        # Si la cantidad de columnas es menor a 3, corta
        if len(cols) != 3:
            info = 'La plantilla proporcionada tiene una cantidad de columnas distinta al formato requerido. Proporcione la cantidad justa de columnas.'
            return PopUp('Error', info).exec()

        # Si va con formato de tutorvip, cambiamos las columnas de 
        # orden
        if formato:
            df = df[[cols[2], cols[0], cols[1]]]
            cols = list(df.columns.values)

        # Si las columnas están en el orden incorrecto, corta
        if ("dni" in cols[0].lower() or "curso" in cols[0].lower()
            or "dni" in cols[1].lower() or "curso" in cols[2].lower()
                or "nombre" in cols[2].lower()):
            info = 'Los datos proporcionados no están ordenados correctamente. Ordene los datos de la planilla correctamente e intente nuevamente.'
            return PopUp('Error', info).exec()
        
        # Ejecutamos el cargar planilla del dal.
        dal.cargarPlanillaAlumnos(df.values.tolist(), actualizarCursos)
        # Refrescamos la gestión de alumnos.
        self.fetchAlumnos()
        PopUp('Aviso', 'La planilla se ha cargado con éxito.').exec()

    def cargarPlanillaPersonal(self):
        """Este método crea un dataframe para la carga de datos
        de una spreadsheet en la base de datos de la gestión personal.
        """
        info = 'Esta acción no se puede deshacer. Los datos de la gestión se actualizarán en base al dni y se actualizarán los nombres y las clases en base a los datos de la planilla. Asegúrese que los dni de la planilla y de la gestión personal sean correctos, de lo contrario se pueden originar personal duplicado. Además, asegúrese de que los datos (columnas) de la planilla esten en el siguiente orden: nombre, clase y dni.'
        # Si cerro sin responder, corta la función.
        if (PopUp('Advertencia', info).exec() !=
            QtWidgets.QMessageBox.StandardButton.Ok):
            return
        
        # Creamos el dialog.
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(os.path.expanduser('~documents'))
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        dialog.setNameFilter(
            "Hoja de cálculo (*.xlsx *.xls *.xlsm *.xlsb *.xltx *.xltm *.xlt *.xlam *.xla *.xlw *.xlr)")
        dialog.setWindowTitle('Abrir archivo')
        # Si abrió un archivo el usuario...
        if dialog.exec():
            # Obtenemos el nombre
            planilla = dialog.selectedFiles()[0]
        # Si no abrió un archivo, corta la función
        else:
            return
        
        # Intentamos hacer el dataframe a partir del excel
        try:
            df = pd.read_excel(planilla)
        # Si el archivo no es válido, avisamos y cortamos la funcion.
        except:
            info = 'El archivo proporcionado no es válido como planilla. Proporcione un archivo válido.'
            return PopUp('Error', info).exec()
        # Obtenemos las columnas
        cols = list(df.columns.values)

        # Si la cantidad de columnas es dsitinta a 3, corta
        if len(cols) != 3:
            info = 'La plantilla proporcionada tiene una cantidad de columnas distinta al formato requerido. Proporcione la cantidad justa de columnas.'
            return PopUp('Error', info).exec()

        # Si las columnas están en el orden incorrecto, corta
        if ("dni" in cols[0].lower() or "dni" in cols[1].lower() 
                                or "nombre" in cols[2].lower()):
            info = 'Los datos proporcionados no están ordenados correctamente. Ordene los datos de la planilla correctamente e intente nuevamente.'
            return PopUp('Error', info).exec()
        
        # Ejecutamos el cargar planilla del dal.
        dal.cargarPlanillaPersonal(df.values.tolist())
        # Refrescamos la gestión de alumnos.
        self.fetchOtroPersonal()
        PopUp('Aviso', 'La planilla se ha cargado con éxito.').exec()
    
    def fetchAlumnos(self):
        """Este método refresca la gestión de alumnos."""
        tabla = self.pantallaAlumnos.tableWidget
        barraBusqueda = self.pantallaAlumnos.lineEdit

        try:
            tabla.disconnect()
        except:
            pass
        tabla.setSortingEnabled(False)
        tabla.setRowCount(0)

        datos = dal.obtenerDatos("alumnos", barraBusqueda.text())

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            item0 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            item1 = QtWidgets.QTableWidgetItem(str(rowData[1]))
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 1, item1)
            sql ='''SELECT c.descripcion FROM clases c
            JOIN cats_clase cat ON c.id_cat=cat.id
            WHERE cat.descripcion='Alumno';'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql).fetchall()]
            cursos = ParamEdit(sugerencias, rowData[2])
            cursos.textChanged.connect(
                lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(rowNum, 2, cursos)
            item3 = QtWidgets.QTableWidgetItem(str(rowData[3]))
            item3.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 3, item3)

            core.generarBotones(
                lambda: self.saveOne(tabla, dal.saveAlumnos, datos),
                lambda: self.deleteAlumnos(datos), tabla, rowNum)
            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(1)

    def deleteAlumnos(self, datos: list | None = None) -> None:
        """Este método elimina una fila de la tabla de la gestión
        alumnos.

        Parámetros
        ----------
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        tabla = self.pantallaAlumnos.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()

        idd = tabla.item(row, 0).text()

        if not idd:
            return tabla.removeRow(row)

        idd = int(idd)

        hayRelacion = dal.verifElimAlumnos(idd)
        nombre=tabla.item(row, 1).text()
        if hayRelacion:
            mensaje = f"El alumno {nombre} tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este alumno."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = f"Esta acción no se puede deshacer. ¿Desea eliminar el alumno/a {nombre}?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                datosEliminados = [fila for fila in datos
                                   if fila[0] == idd][0]
            except TypeError:
                datosEliminados = []
                for numCol in range(tabla.columnCount() - 2):
                    if core.camposAlumnos[1][numCol] < 2:
                        datosEliminados.append(tabla.item(row, numCol).text())
                    else:
                        datosEliminados.append(tabla.cellWidget(row, numCol).text())
            dal.insertarHistorial(self.usuario, "Eliminación", "Alumnos",
                                  datosEliminados[1], datosEliminados[2:])

            dal.eliminarDatos('personal', idd)
            tabla.removeRow(row)

    def fetchMovs(self):
        """Este método refresca el listado de movimientos."""
        tabla = self.pantallaMovs.tableWidget
        barraBusqueda = self.pantallaMovs.lineEdit

        nId = self.pantallaMovs.nId
        listaElem = self.pantallaMovs.listaElem
        listaPersona = self.pantallaMovs.listaPersona
        desdeFecha = self.pantallaMovs.desdeFecha
        hastaFecha = self.pantallaMovs.hastaFecha
        nTurno = self.pantallaMovs.nTurno
        listaPanolero = self.pantallaMovs.listaPanolero

        try:
            tabla.disconnect()
        except:
            pass

        try:
            listaElem.disconnect()
            desdeFecha.disconnect()
            hastaFecha.disconnect()
            listaPersona.disconnect()
            listaPanolero.disconnect()
        except:
            pass

        desdeFecha.setMaximumDateTime(QtCore.QDateTime.currentDateTime())
        hastaFecha.setMinimumDateTime(QtCore.QDateTime.currentDateTime())

        elemSeleccionado = listaElem.currentText()
        elems = bdd.cur.execute("""SELECT DISTINCT s.descripcion
                                FROM movimientos m
                                JOIN stock s
                                ON s.id=m.id_elem""").fetchall()
        listaElem.clear()
        listaElem.addItem("Todos")
        for elem in elems:
            listaElem.addItem(elem[0])
        listaElem.setCurrentIndex(listaElem.findText(elemSeleccionado))

        personaSeleccionada = listaPersona.currentText()
        personas = bdd.cur.execute("""SELECT DISTINCT p.nombre_apellido || ' ' || c.descripcion 
                                FROM movimientos m
                                JOIN personal p
                                ON p.id=m.id_persona
                                JOIN clases c
                                ON p.id_clase = c.id""").fetchall()
        listaPersona.clear()
        listaPersona.addItem("Todas")
        for persona in personas:
            listaPersona.addItem(persona[0])
        listaPersona.setCurrentIndex(
            listaPersona.findText(personaSeleccionada))

        panoleroSeleccionado = listaPanolero.currentText()
        panoleros = bdd.cur.execute("""SELECT DISTINCT p.nombre_apellido || ' ' || c.descripcion
                                FROM movimientos m
                                JOIN turnos t
                                ON m.id_turno = t.id
                                JOIN personal p
                                ON p.id=t.id_panolero
                                JOIN clases c
                                ON p.id_clase = c.id""").fetchall()

        listaPanolero.clear()
        listaPanolero.addItem("Todos")
        for panolero in panoleros:
            listaPanolero.addItem(panolero[0])
        listaPanolero.setCurrentIndex(
            listaPanolero.findText(panoleroSeleccionado))

        filtros = []
        for i in (nId, nTurno):
            if i.value():
                filtros.append(i.value())
            else:
                filtros.append(None)

        if elemSeleccionado == "Todos":
            filtros.append(None)
        else:
            filtros.append(elemSeleccionado)

        if personaSeleccionada == "Todas":
            filtros.append(None)
        else:
            filtros.append(personaSeleccionada)

        if panoleroSeleccionado == "Todos":
            filtros.append(None)
        else:
            filtros.append(panoleroSeleccionado)

        datosCrudos = dal.obtenerDatos(
            "movimientos", barraBusqueda.text(), filtros)
        datos = []
        for rowData in datosCrudos:
            fecha = QtCore.QDateTime.fromString(
                rowData[8], 'yyyy/MM/dd HH:mm:ss')
            if fecha >= desdeFecha.dateTime() and fecha <= hastaFecha.dateTime():
                datos.append(rowData)

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            for cellNum, cellData in enumerate(rowData):
                if core.camposMovs[1][cellNum]:
                    item = QtWidgets.QTableWidgetItem(str(cellData))
                else:
                    item = QtWidgets.QTableWidgetItem()
                    item.setData(0, cellData)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum, cellNum, item)
            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);

        listaElem.setMinimumWidth(
            listaElem.minimumSizeHint().width() + 100
        )
        listaElem.currentIndexChanged.connect(self.fetchMovs)
        listaPersona.setMinimumWidth(
            listaPersona.minimumSizeHint().width() + 100
        )
        listaPersona.currentIndexChanged.connect(self.fetchMovs)
        listaPanolero.setMinimumWidth(
            listaPanolero.minimumSizeHint().width() + 100
        )
        listaPanolero.currentIndexChanged.connect(self.fetchMovs)
        desdeFecha.dateTimeChanged.connect(self.fetchMovs)
        hastaFecha.dateTimeChanged.connect(self.fetchMovs)

        self.stackedWidget.setCurrentIndex(4)

    def fetchGrupos(self):
        """Este método refresca la gestión de grupos."""
        tabla = self.pantallaGrupos.tableWidget
        barraBusqueda = self.pantallaGrupos.lineEdit

        try:
            tabla.disconnect()
        except:
            pass

        tabla.setSortingEnabled(False)

        datos = dal.obtenerDatos("grupos", barraBusqueda.text())
        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            item0 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            item1 = QtWidgets.QTableWidgetItem(str(rowData[1]))
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 1, item1)

            core.generarBotones(
                lambda: self.saveOne(tabla, dal.saveGrupos, datos),
                lambda: self.deleteGrupos(datos), tabla, rowNum)
                    
            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        self.pantallaGrupos.tableWidget.horizontalHeader(
        ).setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(2)

    def deleteGrupos(self, datos: list | None = None):
        """Este método elimina una fila de la tabla de la gestión de
        grupos.

        Parámetros
        ----------
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        tabla = self.pantallaGrupos.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()

        idd = tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd = int(idd)

        hayRelacion = dal.verifElimGrupos(idd)
        desc=tabla.item(row, 1).text()
        if hayRelacion:
            mensaje = f"El grupo {desc} tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este grupo."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = f"Esta acción no se puede deshacer. ¿Desea eliminar el grupo {desc}?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                datosEliminados = [fila for fila in datos
                                   if fila[0] == idd][0]
            except TypeError:
                datosEliminados = []
                for numCol in range(tabla.columnCount() - 2):
                    if core.camposGrupos[1][numCol] < 2:
                        datosEliminados.append(tabla.item(row, numCol).text())
                    else:
                        datosEliminados.append(tabla.cellWidget(row, numCol).text())
            dal.insertarHistorial(self.usuario, 'Eliminación', 'Grupos',
                                  datosEliminados[1], None)
            dal.eliminarDatos('grupos', idd)
            tabla.removeRow(row)

    def fetchOtroPersonal(self):
        """Este método refresca la gestión del personal."""
        tabla = self.pantallaOtroPersonal.tableWidget
        barraBusqueda = self.pantallaOtroPersonal.lineEdit

        try:
            tabla.disconnect()
        except:
            pass
        tabla.setSortingEnabled(False)
        tabla.setRowCount(0)

        datos = dal.obtenerDatos("otro_personal", barraBusqueda.text())

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            item0 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            item1 = QtWidgets.QTableWidgetItem(str(rowData[1]))
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 1, item1)
            sql ='''SELECT c.descripcion FROM clases c
            JOIN cats_clase cat ON c.id_cat=cat.id
            WHERE cat.descripcion='Personal';'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql).fetchall()]
            clases = ParamEdit(sugerencias, rowData[2])
            clases.textChanged.connect(
                lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(
                rowNum, 2, clases)
            item3 = QtWidgets.QTableWidgetItem(str(rowData[3]))
            item3.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 3, item3)

            core.generarBotones(
                lambda: self.saveOne(tabla, dal.saveOtroPersonal, datos),
                lambda: self.deleteOtroPersonal(datos), tabla, rowNum)

            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(5)

    def deleteOtroPersonal(self, datos: list | None = None):
        """Este método elimina una fila de la tabla de la gestión del
        personal.

        Parámetros
        ----------
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        tabla = self.pantallaOtroPersonal.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()

        idd = tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd = int(idd)

        hayRelacion = dal.verifElimOtroPersonal(idd)
        desc=tabla.item(row, 1).text()
        if hayRelacion:
            mensaje = f"El personal {desc} tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar el personal."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = f"Esta acción no se puede deshacer. ¿Desea eliminar el personal {desc}?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                datosEliminados = [fila for fila in datos
                                   if fila[0] == idd][0]
            except TypeError:
                datosEliminados = []
                for numCol in range(tabla.columnCount() - 2):
                    if core.camposOtroPersonal[1][numCol] < 2:
                        datosEliminados.append(tabla.item(row, numCol).text())
                    else:
                        datosEliminados.append(tabla.cellWidget(row, numCol).text())
            dal.insertarHistorial(self.usuario, 'Eliminación', 'Personal',
                                  datosEliminados[1], datosEliminados[2:])
            dal.eliminarDatos('personal', idd)
            tabla.removeRow(row)

    def fetchSubgrupos(self):
        """Este método refresca la gestión subgrupos."""
        tabla = self.pantallaSubgrupos.tableWidget
        barraBusqueda = self.pantallaSubgrupos.lineEdit

        try:
            tabla.disconnect()
        except:
            pass

        tabla.setSortingEnabled(False)
        datos = dal.obtenerDatos("subgrupos", barraBusqueda.text())
        tabla.setRowCount(0)
        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            item0 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            item1 = QtWidgets.QTableWidgetItem(str(rowData[1]))
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 1, item1)
            sugerencias =[i[0] for i in
                         bdd.cur.execute('SELECT descripcion FROM grupos'
                         ).fetchall()]
            grupos = ParamEdit(sugerencias, rowData[2])
            grupos.textChanged.connect(
                lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(rowNum, 2, grupos)

            core.generarBotones(
                lambda: self.saveOne(tabla, dal.saveSubgrupos, datos),
                lambda: self.deleteSubgrupos(datos), tabla, rowNum)

            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(6)

    def deleteSubgrupos(self, datos: list | None = None):
        """Este método elimina una fila de la tabla de la gestión
        subgrupos.

        Parámetros
        ----------
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        tabla = self.pantallaSubgrupos.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()

        idd = tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd = int(idd)
        hayRelacion = dal.verifElimSubgrupos(idd)
        desc = tabla.item(row, 1).text()
        if hayRelacion:
            mensaje = f"El subgrupo {desc} tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este subgrupo."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = f"Esta acción no se puede deshacer. ¿Desea eliminar el subgrupo {desc}?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                datosEliminados = [fila for fila in datos
                                   if fila[0] == idd][0]
            except TypeError:
                datosEliminados = []
                for numCol in range(tabla.columnCount() - 2):
                    if core.camposSubgrupos[1][numCol] < 2:
                        datosEliminados.append(tabla.item(row, numCol).text())
                    else:
                        datosEliminados.append(tabla.cellWidget(row, numCol).text())
            dal.insertarHistorial(self.usuario, 'Eliminación', 'Subgrupos',
                                  datosEliminados[1], datosEliminados[2:])
            dal.eliminarDatos('subgrupos', idd)
            tabla.removeRow(row)

    def fetchTurnos(self):
        """Este método refresca la gestión de turnos."""
        tabla = self.pantallaTurnos.tableWidget
        barraBusqueda = self.pantallaTurnos.lineEdit

        nId = self.pantallaTurnos.nId
        desdeFecha = self.pantallaTurnos.desdeFecha
        hastaFecha = self.pantallaTurnos.hastaFecha

        try:
            tabla.disconnect()
        except:
            pass
        try:
            desdeFecha.disconnect()
            hastaFecha.disconnect()
        except:
            pass

        desdeFecha.setMaximumDate(QtCore.QDate.currentDate())
        hastaFecha.setMinimumDate(QtCore.QDate.currentDate())

        if nId.value():
            filtro = (nId.value(),)
        else:
            filtro = (None,)

        tabla.setRowCount(0)
        datosCrudos = dal.obtenerDatos("turnos", barraBusqueda.text(), filtro)
        datos = []
        for rowData in datosCrudos:
            fecha = QtCore.QDate.fromString(rowData[2][:10], 'yyyy/MM/dd')
            if fecha >= desdeFecha.date() and fecha <= hastaFecha.date():
                datos.append(rowData)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            for cellNum, cellData in enumerate(rowData):
                if core.camposTurnos[1][cellNum]:
                    item = QtWidgets.QTableWidgetItem(str(cellData))
                else:
                    item = QtWidgets.QTableWidgetItem()
                    item.setData(0, cellData)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum, cellNum, item)
            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader(
        ).setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader(
        ).setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader(
        ).setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader(
        ).setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader(
        ).setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader(
        ).setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(7)

    def fetchUsuarios(self):
        """Este método refresca la gestión usuarios."""
        tabla = self.pantallaUsuarios.tableWidget
        barraBusqueda = self.pantallaUsuarios.lineEdit

        tabla.setSortingEnabled(False)
        try:
            tabla.disconnect()
        except:
            pass

        datos = dal.obtenerDatos("usuarios", barraBusqueda.text())

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            item0 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            item1 = QtWidgets.QTableWidgetItem(str(rowData[1]))
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 1, item1)
            sql ='''SELECT c.descripcion FROM clases c
            JOIN cats_clase cat ON c.id_cat=cat.id
            WHERE cat.descripcion='Usuario';'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql).fetchall()]
            clases = ParamEdit(sugerencias, rowData[2])
            clases.textChanged.connect(
                lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(
                rowNum, 2, clases)
            item3 = QtWidgets.QTableWidgetItem(str(rowData[3]))
            # Los centramos.
            item3.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 3, item3)
            item4 = QtWidgets.QTableWidgetItem(str(rowData[4]))
            item4.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 4, item4)
            item5 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            item5.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 5, item5)

            core.generarBotones(
                lambda: self.saveOne(tabla, dal.saveUsuarios, datos),
                lambda: self.deleteUsuarios(datos), tabla, rowNum)

            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(8)

    def deleteUsuarios(self, datos: list | None = None):
        """Este método elimina una fila de la tabla de la gestión
        usuarios.

        Parámetros
        ----------
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        tabla = self.pantallaUsuarios.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()

        idd = tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd = int(idd)

        hayRelacion = dal.verifElimUsuario(idd)
        desc = tabla.item(row, 1).text()
        if hayRelacion:
            mensaje = f"El usuario {desc} tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este usuario."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = f"Esta acción no se puede deshacer. ¿Desea eliminar el usuario {desc}?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                datosEliminados = [fila for fila in datos
                                   if fila[0] == idd][0]
            except TypeError:
                datosEliminados = []
                for numCol in range(tabla.columnCount() - 2):
                    if core.camposUsuarios[1][numCol] < 2:
                        datosEliminados.append(tabla.item(row, numCol).text())
                    else:
                        datosEliminados.append(tabla.cellWidget(row, numCol).text())
            dal.insertarHistorial(self.usuario, 'Eliminación', 'Usuarios',
                                  datosEliminados[1], datosEliminados[2:])
            dal.eliminarDatos('personal', idd)
            tabla.removeRow(row)

    def fetchClases(self):
        """Este método refresca la gestión clases."""
        tabla = self.pantallaClases.tableWidget
        barraBusqueda = self.pantallaClases.lineEdit

        try:
            tabla.disconnect()
        except:
            pass
        tabla.setSortingEnabled(False)
        tabla.setRowCount(0)

        datos = dal.obtenerDatos("clases", barraBusqueda.text())
        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            item0 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            sugerencias =[i[0] for i in
                         bdd.cur.execute('SELECT descripcion FROM cats_clase').fetchall()]
            cats = ParamEdit(sugerencias, rowData[1])
            cats.textChanged.connect(
                lambda: self.habilitarSaves(None, None, tabla))
            if rowData[2] in {"Egresado", "Destituído"}:
                cats.setEnabled(False)
            tabla.setCellWidget(rowNum, 1, cats)

            
            core.generarBotones(
                lambda: self.saveOne(tabla, dal.saveClases, datos),
                lambda: self.deleteClases(datos), tabla, rowNum)
            
            item2 = QtWidgets.QTableWidgetItem(str(rowData[2]))
            item2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            if rowData[2] in {"Egresado", "Destituído"}:
                item2.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                tabla.cellWidget(
                    rowNum, tabla.columnCount()-1).setEnabled(False)
            tabla.setItem(rowNum, 2, item2)


            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader(
        ).setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(10)

    def fetchUbis(self):
        """Este método refresca la gestión ubicaciones."""
        tabla = self.pantallaUbis.tableWidget
        barraBusqueda = self.pantallaUbis.lineEdit

        tabla.setSortingEnabled(False)

        try:
            tabla.disconnect()
        except:
            pass

        datos = dal.obtenerDatos("ubicaciones", barraBusqueda.text())

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            item0 = QtWidgets.QTableWidgetItem(str(rowData[0]))
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            item1 = QtWidgets.QTableWidgetItem(str(rowData[1]))
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 1, item1)

            core.generarBotones(
                lambda: self.saveOne(tabla, dal.saveUbis, datos),
                lambda: self.deleteUbis(datos), tabla, rowNum)

            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(12)

    def deleteUbis(self, datos: list | None = None):
        """Este método elimina una fila de la tabla de la gestión
        ubicaciones.

        Parámetros
        ----------
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        tabla = self.pantallaUbis.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()

        idd = tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd = int(idd)

        hayRelacion = dal.verifElimUbi(idd)
        desc = tabla.item(row, 1).text()
        if hayRelacion:
            mensaje = f"La ubicacion {desc} está relacionada con registros en otras gestiones. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar esta ubicacion."
            return PopUp('Advertencia', mensaje).exec()
        mensaje = f"Esta acción no se puede deshacer. ¿Desea eliminar la ubicacion {desc}?"
        popup = PopUp("Pregunta", mensaje).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                datosEliminados = [fila for fila in datos
                                   if fila[0] == idd][0]
            except TypeError:
                datosEliminados = []
                for numCol in range(tabla.columnCount() - 2):
                    if core.camposUbis[1][numCol] < 2:
                        datosEliminados.append(tabla.item(row, numCol).text())
                    else:
                        datosEliminados.append(tabla.cellWidget(row, numCol).text())
            dal.insertarHistorial(self.usuario, 'Eliminación', 'Ubicaciones',
                                  datosEliminados[1], None)
            dal.eliminarDatos('ubicaciones', idd)
            tabla.removeRow(row)

    def fetchReps(self):
        """Este método refresca el listado de reparaciones."""
        tabla = self.pantallaReps.tableWidget
        barraBusqueda = self.pantallaReps.lineEdit

        desdeFecha = self.pantallaReps.desdeFecha
        hastaFecha = self.pantallaReps.hastaFecha
        try:
            tabla.disconnect()
        except:
            pass
        try:
            desdeFecha.disconnect()
            hastaFecha.disconnect()
        except:
            pass

        desdeFecha.setMaximumDate(QtCore.QDate.currentDate())
        hastaFecha.setMinimumDate(QtCore.QDate.currentDate())

        datosCrudos = dal.obtenerDatos("reparaciones", barraBusqueda.text())
        datos = []
        for rowData in datosCrudos:
            fechaEnvio = QtCore.QDate.fromString(rowData[5], 'yyyy/MM/dd')
            fechaRegreso = QtCore.QDate.fromString(rowData[6], 'yyyy/MM/dd')
            if (
                fechaEnvio >= desdeFecha.date()
                and fechaEnvio <= hastaFecha.date()
            ) or (
                fechaRegreso >= desdeFecha.date()
                and fechaRegreso <= hastaFecha.date()
            ):
                datos.append(rowData)
        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            for cellNum, cellData in enumerate(rowData):
                if core.camposReps[1][cellNum]:
                    item = QtWidgets.QTableWidgetItem(str(cellData))
                else:
                    item = QtWidgets.QTableWidgetItem()
                    item.setData(0, cellData)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum, cellNum, item)
            tabla.setRowHeight(rowNum, 35)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.horizontalHeader(
        ).setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader(
        ).setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader(
        ).setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)

        desdeFecha.dateChanged.connect(self.fetchReps)
        hastaFecha.dateChanged.connect(self.fetchReps)

        self.stackedWidget.setCurrentIndex(11)

    def deleteClases(self, datos: list | None = None):
        """Este método elimina una fila de la tabla de la gestión
        clases.

        Parámetros
        ----------
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        """
        tabla = self.pantallaClases.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()

        idd = tabla.item(row, 0).text()

        if not idd:
            return tabla.removeRow(row)
        idd = int(idd)

        hayRelacion = dal.verifElimClases(idd)
        desc = tabla.item(row, 2).text()
        if hayRelacion:
            mensaje = f"La clase {desc} tiene relaciones. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar esta clase."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = f"Esta acción no se puede deshacer. ¿Desea eliminar la clase {desc}?"
        popup = PopUp("Pregunta", mensaje).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                datosEliminados = [fila for fila in datos
                                   if fila[0] == idd][0]
            except TypeError:
                datosEliminados = []
                for numCol in range(tabla.columnCount() - 2):
                    if core.camposClases[1][numCol] < 2:
                        datosEliminados.append(tabla.item(row, numCol).text())
                    else:
                        datosEliminados.append(tabla.cellWidget(row, numCol).text())
            dal.insertarHistorial(
                self.usuario, "Eliminación", "Clases", datosEliminados[1], datosEliminados[2:])
            dal.eliminarDatos('clases', idd)
            tabla.removeRow(row)
            
    def fetchHistorial(self):
        """Este método refresca el historial."""
        tabla = self.pantallaHistorial.tableWidget
        barraBusqueda = self.pantallaHistorial.lineEdit

        desdeFecha = self.pantallaHistorial.desdeFecha
        hastaFecha = self.pantallaHistorial.hastaFecha
        listaGestion = self.pantallaHistorial.listaGestion
        try:
            tabla.disconnect()
        except:
            pass
        try:
            listaGestion.disconnect()
            desdeFecha.disconnect()
            hastaFecha.disconnect()
        except:
            pass

        desdeFecha.setMaximumDateTime(QtCore.QDateTime.currentDateTime())
        hastaFecha.setMinimumDateTime(QtCore.QDateTime.currentDateTime())

        gestionSeleccionada = listaGestion.currentText()
        gestiones = bdd.cur.execute("""SELECT DISTINCT g.descripcion
                                FROM historial h
                                JOIN gestiones g
                                ON g.id=h.id_gest""").fetchall()
        listaGestion.clear()
        listaGestion.addItem("Todas")
        for gestion in gestiones:
            listaGestion.addItem(gestion[0])
        listaGestion.setCurrentIndex(
            listaGestion.findText(gestionSeleccionada))

        if gestionSeleccionada == "Todas":
            filtroGestion = (None,)
        else:
            filtroGestion = (gestionSeleccionada,)

        tabla.setRowCount(0)
        rawData = dal.obtenerDatos("historial", None, filtroGestion)
        datos = []
        for rawRow in rawData:
            fecha = QtCore.QDateTime.fromString(
                rawRow[1], 'yyyy/MM/dd HH:mm:ss')
            if fecha >= desdeFecha.dateTime() and fecha <= hastaFecha.dateTime():
                if rawRow[2] == 'Stock':
                    if rawRow[3] == 'Inserción':
                        datosInsertados = rawRow[6].split(';')
                        desc = f"""                Se insertó la herramienta {rawRow[4]}, con los siguientes datos:
                        - Cantidad en condiciones: {datosInsertados[0]}
                        - Cantidad de baja: {datosInsertados[1]}
                        - Grupo: {datosInsertados[2]}
                        - Subgrupo: {datosInsertados[3]}
                        - Ubicación: {datosInsertados[4]}"""
                    elif rawRow[3] == 'Edición':
                        datosViejos = rawRow[5].split(';')
                        datosNuevos = rawRow[6].split(';')
                        desc = f"""                Se editó la herramienta {rawRow[4]}, y se reemplazaron los siguientes datos:
                        - Descripción: {rawRow[4]}, por {datosNuevos[0]}
                        - Cantidad en condiciones: {datosViejos[0]}, por {datosNuevos[1]}
                        - Cantidad de baja: {datosViejos[1]}, por {datosNuevos[2]}
                        - Grupo: {datosViejos[2]}, por {datosNuevos[3]}
                        - Subgrupo: {datosViejos[3]}, por {datosNuevos[4]}
                        - Ubicación: {datosViejos[4]}, por {datosNuevos[5]}"""
                    elif rawRow[3] == 'Eliminación':
                        datosEliminados = rawRow[5].split(';')
                        desc = f"""                Se eliminó la herramienta {rawRow[4]}, que tenía los siguientes datos:
                        - Cantidad en condiciones: {datosEliminados[0]}
                        - Cantidad en reparacion: {datosEliminados[1]}
                        - Cantidad de baja: {datosEliminados[2]}
                        - Cantidad prestadas: {datosEliminados[3]}
                        - Grupo: {datosEliminados[4]}
                        - Subgrupo: {datosEliminados[5]}
                        - Ubicación: {datosEliminados[6]}"""
                elif rawRow[2] == 'Subgrupos':
                    if rawRow[3] == 'Inserción':
                        datosInsertados = rawRow[6].split(';')
                        desc = f"Se insertó el subgrupo {rawRow[4]}, perteneciendo al grupo {datosInsertados[0]}."
                    elif rawRow[3] == 'Edición':
                        datosViejos = rawRow[5].split(';')
                        datosNuevos = rawRow[6].split(';')
                        desc = f"""                Se editó el subgrupo {rawRow[4]}, y se reemplazaron los siguientes datos:
                        - Subgrupo: {rawRow[4]}, por {datosNuevos[0]}
                        - Grupo: {datosViejos[0]}, por {datosNuevos[1]}"""
                    elif rawRow[3] == 'Eliminación':
                        datosEliminados = rawRow[5].split(';')
                        desc = f"Se eliminó el subgrupo {rawRow[4]}, que pertenecía al grupo {datosEliminados[0]}."
                elif rawRow[2] == 'Grupos':
                    if rawRow[3] == 'Inserción':
                        datosInsertados = rawRow[6].split(';')
                        desc = f"Se insertó el grupo {rawRow[4]}."
                    elif rawRow[3] == 'Edición':
                        datosViejos = rawRow[5].split(';')
                        datosNuevos = rawRow[6].split(';')
                        desc = f"Se editó el grupo {rawRow[4]}, y se reemplazó por el grupo {datosNuevos[0]}."
                    elif rawRow[3] == 'Eliminación':
                        datosEliminados = rawRow[5].split(';')
                        desc = f"Se eliminó el grupo {rawRow[4]}."
                elif rawRow[2] == 'Alumnos':
                    if rawRow[3] == 'Inserción':
                        datosInsertados = rawRow[6].split(';')
                        desc = f"""                Se insertó el alumno {rawRow[4]}, con los siguientes datos:
                        - Curso: {datosInsertados[0]}
                        - DNI: {datosInsertados[1]}"""
                    elif rawRow[3] == 'Edición':
                        datosViejos = rawRow[5].split(';')
                        datosNuevos = rawRow[6].split(';')
                        desc = f"""                Se editó el alumno {rawRow[4]}, y se reemplazaron los siguientes datos:
                        - Nombre y apellido: {rawRow[4]}, por {datosNuevos[0]}
                        - Curso: {datosViejos[0]}, por {datosNuevos[1]}
                        - DNI: {datosViejos[1]}, por {datosNuevos[2]}"""
                    elif rawRow[3] == 'Eliminación':
                        datosEliminados = rawRow[5].split(';')
                        desc = f"Se eliminó el alumno {rawRow[4]}, que pertenecía al curso {datosEliminados[0]} y tenía el dni {datosEliminados[1]}."
                elif rawRow[2] == 'Personal':
                    if rawRow[3] == 'Inserción':
                        datosInsertados = rawRow[6].split(';')
                        desc = f"""                Se insertó el personal {rawRow[4]}, con los siguientes datos:
                        - Clase: {datosInsertados[0]}
                        - DNI: {datosInsertados[1]}"""
                    elif rawRow[3] == 'Edición':
                        datosViejos = rawRow[5].split(';')
                        datosNuevos = rawRow[6].split(';')
                        desc = f"""                Se editó el personal {rawRow[4]}, y se reemplazaron los siguientes datos:
                        - Nombre y apellido: {rawRow[4]}, por {datosNuevos[0]}
                        - Clase: {datosViejos[0]}, por {datosNuevos[1]}
                        - DNI: {datosViejos[1]}, por {datosNuevos[2]}"""
                    elif rawRow[3] == 'Eliminación':
                        datosEliminados = rawRow[5].split(';')
                        desc = f"Se eliminó el personal {rawRow[4]}, cuya clase era {datosEliminados[0]} y tenía el dni {datosEliminados[1]}."
                elif rawRow[2] == 'Clases':
                    if rawRow[3] == 'Inserción':
                        datosInsertados = rawRow[6].split(';')
                        desc = f"Se insertó la clase {rawRow[4]}, perteneciendo a la categoría {datosInsertados[0]}."
                    elif rawRow[3] == 'Edición':
                        datosViejos = rawRow[5].split(';')
                        datosNuevos = rawRow[6].split(';')
                        desc = f"""                Se editó la clase {rawRow[4]}, y se reemplazaron los siguientes datos:
                        - Clase: {rawRow[4]}, por {datosNuevos[0]}
                        - Categoría: {datosViejos[0]}, por {datosNuevos[1]}"""
                    elif rawRow[3] == 'Eliminación':
                        datosEliminados = rawRow[5].split(';')
                        desc = f"Se eliminó la clase {rawRow[4]}, que pertenecía a la categoría {datosEliminados[0]}."
                elif rawRow[2] == 'Ubicaciones':
                    if rawRow[3] == 'Inserción':
                        datosInsertados = rawRow[6].split(';')
                        desc = f"Se insertó la ubicación {rawRow[4]}."
                    elif rawRow[3] == 'Edición':
                        datosViejos = rawRow[5].split(';')
                        datosNuevos = rawRow[6].split(';')
                        desc = f"Se editó la ubicación {rawRow[4]}, y se reemplazó por la ubicación {datosNuevos[0]}."
                    elif rawRow[3] == 'Eliminación':
                        datosEliminados = rawRow[5].split(';')
                        desc = f"Se eliminó la ubicación {rawRow[4]}."

                row = [rawRow[0], rawRow[1], rawRow[2],
                       rawRow[3], rawRow[4], dedent(desc)]
                for cellData in row:
                    if barraBusqueda.text() in cellData:
                        datos.append(row)
                        break

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            for cellNum, cellData in enumerate(rowData):
                if core.camposHistorial[1][cellNum]:
                    item = QtWidgets.QTableWidgetItem(str(cellData))
                else:
                    item = QtWidgets.QTableWidgetItem()
                    item.setData(0, cellData)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum, cellNum, item)

            tabla.setRowHeight(rowNum, 35)
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        listaGestion.setMinimumWidth(
            listaGestion.minimumSizeHint().width() + 100
        )
        listaGestion.currentIndexChanged.connect(self.fetchHistorial)
        desdeFecha.dateTimeChanged.connect(self.fetchHistorial)
        hastaFecha.dateTimeChanged.connect(self.fetchHistorial)

        self.stackedWidget.setCurrentIndex(9)

    def fetchDeudas(self):
        """Este método refresca el listado de deudas."""
        radioHerramienta = self.pantallaDeudas.radioHerramienta
        listaTablas = self.pantallaDeudas.stackedWidget

        if radioHerramienta.isChecked():
            listaTablas.setCurrentIndex(0)
            tabla = listaTablas.findChild(
                QtWidgets.QTableWidget, "tablaHerramienta")
        else:
            listaTablas.setCurrentIndex(1)
            tabla = listaTablas.findChild(
                QtWidgets.QTableWidget, "tablaPersona")
        barraBusqueda = self.pantallaDeudas.lineEdit

        nMov = self.pantallaDeudas.nMov
        nTurno = self.pantallaDeudas.nTurno
        listaPanolero = self.pantallaDeudas.listaPanolero

        try:
            listaPanolero.disconnect()
        except:
            pass

        panoleroSeleccionado = listaPanolero.currentText()
        panoleros = bdd.cur.execute("""SELECT DISTINCT p.nombre_apellido || ' ' || c.descripcion
                                FROM movimientos m
                                JOIN turnos t
                                ON m.id_turno = t.id
                                JOIN personal p
                                ON p.id=t.id_panolero
                                JOIN clases c
                                ON p.id_clase = c.id""").fetchall()

        listaPanolero.clear()
        listaPanolero.addItem("Todos")
        for panolero in panoleros:
            listaPanolero.addItem(panolero[0])
        listaPanolero.setCurrentIndex(
            listaPanolero.findText(panoleroSeleccionado))

        filtros = []
        for i in (nMov, nTurno):
            if i.value():
                filtros.append(i.value())
            else:
                filtros.append(None)

        if panoleroSeleccionado == "Todos":
            filtros.append(None)
        else:
            filtros.append(panoleroSeleccionado)

        tabla.setSortingEnabled(False)
        tabla.setRowCount(0)
        tabla.horizontalHeader().setVisible(True)

        # Este fetch es especial porque trabaja con dos tablas.
        # La idea es que van ordenadas de forma especial.
        # Primero, inicializamos los contadores.
        contGrupo = 0
        cant = 0

        # Dependiendo de qué forma de ordenar esté activada, mostramos
        # una u otra tabla y inicializará la variable coldata de forma
        # diferente, lo que indica si la columna herramientas va antes
        # o despues.
        if radioHerramienta.isChecked():
            colData = 0
        else:
            colData = 2
        
        datos = dal.obtenerDatos("deudas", barraBusqueda.text(), filtros)
        datos = sorted(datos, key=lambda i:i[colData])
        try:
            grupo = datos[0][colData]
        except:
            pass
        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            # Sumamos la cantidad, para que muestre la cantidad total
            # de deudas de la herramienta/alumno y no una cantidad por
            # entrada.
            ultimaFila=0
            # Si el elemento coincide con el grupo de deudas que
            # iniciamos...
            if rowData[colData] == grupo and rowNum<len(datos)-1:
                #...sumamos 1 al contador de grupo
                contGrupo += 1
                cant += rowData[1]
            # Si no...
            else:
                # Hay que comprobar que el elemento no sea el último, porque,
                # como está programado, recorre todos los elementos y finaliza
                # el grupo al encontrar un elemento distinto, por lo que si el
                # elemento es el último hay que cerrar el grupo por la fuerza.
                if rowNum==len(datos)-1:
                    # Si el último elemento pertenece al grupo anteriormente
                    # declarado...
                    if rowData[colData] == grupo:
                        # Sumamos la cantidad y añadimos 1 al contador
                        # de grupo y ultima fila. 
                        cant += rowData[1]
                        contGrupo += 1
                        # Ultima fila es importante para cerrar el
                        # grupo.
                        ultimaFila=1
                    # Si el último elemento no coincide con el grupo
                    # anterior, establecemos los items del nuevo y
                    # último grupo.
                    else:
                        itemo=QtWidgets.QTableWidgetItem(str(datos[rowNum][colData]))
                        itemo.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                                    QtCore.Qt.ItemFlag.ItemIsEnabled)
                        itemo.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        tabla.setItem(rowNum, 0, itemo)
                        itemCantt=QtWidgets.QTableWidgetItem()
                        itemCantt.setData(0, cant)
                        itemCantt.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                                    QtCore.Qt.ItemFlag.ItemIsEnabled)
                        itemCantt.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        tabla.setItem(rowNum, 1, itemCantt)
                #Si no es el último y entró a este bloque, entonces 
                # es de otro grupo y se rompió el grupo anterior.
                # establecemos el nombre del grupo de filas y la
                # cantidad total adeudada del elemento/pérsona
                # Está bien que printee lo de QTableView, no es un error
                tabla.setSpan(rowNum - contGrupo + ultimaFila, 0, contGrupo, 1)
                tabla.setSpan(rowNum - contGrupo + ultimaFila, 1, contGrupo, 1)
                # Usamos el rowNum -1 porque, al romper el grupo con un
                # nuevo dato, queremos usar el dato anterior.
                itemP=QtWidgets.QTableWidgetItem(str(datos[rowNum-1][colData]))
                # Lo hacemos no editable
                itemP.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                itemP.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum - contGrupo + ultimaFila, 0, itemP)
                itemCant=QtWidgets.QTableWidgetItem()
                itemCant.setData(0, cant)
                itemCant.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                itemCant.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum - contGrupo + ultimaFila, 1, itemCant)
                contGrupo = 1
                cant = rowData[1]
                grupo = datos[rowNum][colData]

            # Buscamos cual dato es mediante el cual no agrupamos y lo
            # insertamos en la fila de forma normal, sin span.
            if not colData:
                itemOtro=QtWidgets.QTableWidgetItem(rowData[2])
            else:
                itemOtro=QtWidgets.QTableWidgetItem(rowData[0])
            itemOtro.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 2, itemOtro)

            # Añadimos el resto de la fila normal mediante un bucle
            for i in range(3, 8):
                # Si i es 3, necesitamos el dato de la cantidad, que es
                # el 1.
                if i == 3:
                    item=QtWidgets.QTableWidgetItem(str(rowData[1]))
                # Si no, usamos el dato anterior a i
                else:
                    item=QtWidgets.QTableWidgetItem(str(rowData[i-1]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                tabla.setItem(rowNum, i, item)
        tabla.resizeRowsToContents()
        tabla.resizeColumnsToContents()
        tabla.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded);
        tabla.resizeRowsToContents()
        tabla.horizontalHeader(
        ).setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        listaPanolero.setMinimumWidth(
            listaPanolero.minimumSizeHint().width() + 100
        )
        listaPanolero.currentIndexChanged.connect(self.fetchDeudas)

        self.stackedWidget.setCurrentIndex(14)

    def fetchResumen(self):
        """Este método refresca el resumen de deudas."""
        hastaFecha = self.pantallaResumen.hastaFecha
        tablaDeudas = self.pantallaResumen.tablaDeudas
        tablaBaja = self.pantallaResumen.tablaBaja
        labelDeudas = self.pantallaResumen.labelDeudas
        labelBaja = self.pantallaResumen.labelBaja
        tablaDeudas.setSortingEnabled(False)
        tablaBaja.setSortingEnabled(False)

        try:
            hastaFecha.disconnect()
        except:
            pass

        # Este fetch tiene dos tablas, asi que hacemos dos veces
        rawData = dal.obtenerDatos(f"resumen{os.sep}deudas")
        datos = []
        # Filtramos por fecha
        for rawRow in rawData:
            fecha = QtCore.QDate.fromString(rawRow[7][:10], 'yyyy/MM/dd')
            if fecha == hastaFecha.date():
                datos.append(rawRow[:7])

        # Si se encontraron datos de la primera tabla
        if datos:
            # Se muestra la tabla
            labelDeudas.setText('Han quedado herramientas adeudadas:')
            tablaDeudas.setRowCount(0)

            for rowNum, rowData in enumerate(datos):
                tablaDeudas.insertRow(rowNum)
                for cellNum, cellData in enumerate(rowData):
                    if core.camposDeudas[1][cellNum]:
                        item = QtWidgets.QTableWidgetItem(str(cellData))
                    else:
                        item = QtWidgets.QTableWidgetItem()
                        item.setData(0, cellData)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                                  QtCore.Qt.ItemFlag.ItemIsEnabled)
                    tablaDeudas.setItem(rowNum, cellNum, item)
                tablaDeudas.setRowHeight(rowNum, 35)
            tablaDeudas.resizeRowsToContents()
            tablaDeudas.resizeColumnsToContents()
            tablaDeudas.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            tablaDeudas.horizontalHeader(
            ).setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader(
            ).setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader(
            ).setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader(
            ).setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.setSortingEnabled(True)
            tablaDeudas.show()
        # Si no
        else:
            # no se muestra.
            labelDeudas.setText('No han quedado herramientas adeudadas.')
            tablaDeudas.hide()

        # Hacemos lo mismo con la segunda tabla
        rawData = dal.obtenerDatos(f"resumen{os.sep}baja")
        datos = []
        for rawRow in rawData:
            fecha = QtCore.QDate.fromString(rawRow[8], 'yyyy/MM/dd')
            if fecha == hastaFecha.date():
                datos.append(rawRow[:8])

        if datos:
            for rowNum, rowData in enumerate(datos):
                tablaBaja.insertRow(rowNum)
                for cellNum, cellData in enumerate(rowData):
                    if core.camposBaja[1][cellNum]:
                        item = QtWidgets.QTableWidgetItem(str(cellData))
                    else:
                        item = QtWidgets.QTableWidgetItem()
                        item.setData(0, cellData)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                                  QtCore.Qt.ItemFlag.ItemIsEnabled)
                    tablaBaja.setItem(rowNum, cellNum, item)

                tablaBaja.setRowHeight(rowNum, 35)
            tablaBaja.resizeRowsToContents()
            tablaBaja.resizeColumnsToContents()
            tablaBaja.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            tablaBaja.horizontalHeader(
            ).setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaBaja.horizontalHeader(
            ).setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaBaja.horizontalHeader(
            ).setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaBaja.horizontalHeader(
            ).setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaBaja.setSortingEnabled(True)

            tablaBaja.show()
        else:
            labelBaja.setText(
                'No se han devuelto herramientas en estado de baja.')
            tablaBaja.hide()

        hastaFecha.dateChanged.connect(self.fetchResumen)
        self.stackedWidget.setCurrentIndex(15)


# Creamos la app
app = QtWidgets.QApplication(sys.argv)
# Le cargamos la stylesheet
app.setStyleSheet(open(os.path.join(os.path.abspath(
    os.getcwd()), f'ui{os.sep}styles.qss'), 'r').read())

# Cargamos las fuentes que usamos en la app
core.cargarFuentes()

# Hacemos el objeto de la clase de la ventana principal
window = MainWindow()
# Ejecutamos la app
app.exec()
