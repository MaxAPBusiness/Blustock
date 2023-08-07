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
import sys
import sqlite3
import pandas as pd
import core
import types
from unidecode import unidecode
from textwrap import dedent
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from db.bdd import bdd
from dal.dal import dal
from ui.presets.popup import PopUp
from ui.presets.param_edit import ParamEdit
from ui.presets.Toolbotoon import toolboton
from PyQt6 import QtWidgets, QtCore, QtGui, uic

bdd.refrescarBDD()

class MainWindow(QtWidgets.QMainWindow):
    """Esta clase crea la ventana principal.

    Hereda: PyQt6.QtWidgets.QMainWindow

    Métodos
    -------
        __init__(self):
            El constructor de la clase MainWindow.

            Crea la ventana principal con un menú inicialmente
            escondido y una colección de pantallas.

        actualizarHastaFechas(self):
            Actualiza los filtros de fecha y hora con la fecha y hora
            actuales.
        
        habilitarSaves(self, row: int | None = None,
                       col: int | None = None,
                       tabla: QtWidgets.QTableWidget | None = None):
            Habilita el botón de guardar de una fila de una tabla de
            una gestión.
        
        actualizarTotal(self, row: int, col: int,
                        tabla: QtWidgets.QTableWidget | None = None):
            Actualiza el campo total de la tabla stock cuando se
            modifican las cantidades.
        
        fetchStock(self):
            Actualiza las sugerencias de los campos de subgrupos al
            editar lo ingresado en un campo de grupos relacionado, ya
            que las sugerencias de subgrupos deben estar relacionadas
            al grupo ingresado.
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
        pathAlumnos=os.path.join(os.path.abspath(os.getcwd()),
                                 f'ui{os.sep}screens_uis{os.sep}alumnos.ui')
        # # Cargamos el ui al widget vacío
        uic.loadUi(pathAlumnos, self.pantallaAlumnos)
        
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
        self.opcionStock.triggered.connect(self.fetchStock)
        self.opcionSubgrupos.triggered.connect(self.fetchSubgrupos)
        self.opcionGrupos.triggered.connect(self.fetchGrupos)
        self.opcionAlumnos.triggered.connect(self.fetchAlumnos)
        self.opcionOtroPersonal.triggered.connect(self.fetchOtroPersonal)
        self.opcionTurnos.triggered.connect(self.fetchTurnos)
        self.opcionMovimientos.triggered.connect(self.fetchMovimientos)
        self.opcionUsuarios.triggered.connect(self.fetchUsuarios)
        self.GestionUbicaciones.triggered.connect(self.fetchUbicaciones)
        self.GestionClases.triggered.connect(self.fetchClases)
        self.realizarMovimientos.triggered.connect(self.realizarMovimiento)
        self.GestionReparacion.triggered.connect(self.fetchReparaciones)
        self.opcionHistorial.triggered.connect(self.fetchHistorial)
        self.opcionDeudas.triggered.connect(self.fetchDeudas)
        self.opcionResumen.triggered.connect(self.fetchResumen)

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
                
        self.pantallaLogin.Ingresar.clicked.connect(self.login)

        # Empezamos a conectar los botones de agregar de todas las
        # gestiones.
        # Primero obtenemos sugerencias para los campos con cuadro de 
        # sugerencia de las tablas.
        sugerenciasGrupos=[i[0] for i in bdd.cur.execute(
            'SELECT descripcion FROM grupos').fetchall()]
        sugerenciasUbis=[i[0] for i in bdd.cur.execute(
            'SELECT descripcion FROM ubicaciones').fetchall()]
        # Conectamos el botón.
        self.pantallaStock.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaStock.tableWidget, 
                lambda: self.saveOne(self.pantallaStock.tableWidget,
                                     self.saveStock, self.fetchStock),
                self.deleteStock, self.actualizarTotal, core.camposStock[0],
                (sugerenciasGrupos, [], sugerenciasUbis,),
                self.actualizarSugerenciasSubgrupos))
        # Además, escondemos la primera columna. Esto es porque es la
        # columna id es necesaria para tener el número de fila pero no
        # queremos que la vean los usuarios porque no es info necesaria
        self.pantallaStock.botonGuardar.clicked.connect(
            lambda: core.saveAll(
                self.pantallaStock.tableWidget, self.saveStock,
                dal.obtenerDatos("stock", self.pantallaStock.lineEdit.text()),
                self.fetchStock))
        self.pantallaStock.tableWidget.setColumnHidden(0, True)

        sql='''SELECT c.descripcion FROM clases c
               JOIN cats_clase cat ON c.id_cat=cat.id
               WHERE cat.descripcion='Personal';'''
        sugerenciasClasesP=[i[0] for i in bdd.cur.execute(sql).fetchall()]
        self.pantallaOtroPersonal.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaOtroPersonal.tableWidget, self.saveOtroPersonal,
                self.deleteOtroPersonal, self.habilitarSaves,
                core.camposOtroPersonal[0], [sugerenciasClasesP]))
        self.pantallaOtroPersonal.tableWidget.setColumnHidden(0, True)

        sugerenciasGruposS=[i[0] for i in bdd.cur.execute(
            'SELECT descripcion FROM grupos').fetchall()]
        self.pantallaSubgrupos.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaSubgrupos.tableWidget,
                lambda: self.saveOne(self.pantallaSubgrupos.tableWidget,
                        self.saveSubgrupos, self.fetchSubgrupos),                
                self.deleteSubgrupos, self.habilitarSaves,
                core.camposSubgrupos[0], [sugerenciasGruposS]))
        # Además, escondemos la primera columna. Esto es porque es la
        # columna id es necesaria para tener el número de fila pero no
        # queremos que la vean los usuarios porque no es info necesaria
        self.pantallaSubgrupos.botonGuardar.clicked.connect(
            lambda: core.saveAll(
                self.pantallaSubgrupos.tableWidget, self.saveSubgrupos,
                dal.obtenerDatos(
                    "subgrupos", self.pantallaSubgrupos.lineEdit.text()),
                self.fetchSubgrupos))
        self.pantallaSubgrupos.tableWidget.setColumnHidden(0, True)

        self.pantallaGrupos.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaGrupos.tableWidget, self.saveGrupos,
                self.deleteGrupos, self.habilitarSaves, core.camposGrupos[0]))
        self.pantallaGrupos.tableWidget.setColumnHidden(0, True)

        sql='''SELECT c.descripcion FROM clases c
               JOIN cats_clase cat ON c.id_cat=cat.id
               WHERE cat.descripcion='Alumno';'''
        sugerenciasClasesA=[i[0] for i in bdd.cur.execute(sql).fetchall()]
        self.pantallaAlumnos.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaAlumnos.tableWidget,
                self.saveAlumnos, self.deleteAlumnos,  self.habilitarSaves,
                core.camposAlumnos[0], [sugerenciasClasesA]))
        self.pantallaAlumnos.botonCargar.clicked.connect(
            self.cargarPlanilla)
        self.pantallaAlumnos.tableWidget.setColumnHidden(0, True)

        self.pantallaUbis.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaUbis.tableWidget, self.saveUbicaciones,
                self.deleteUbicaciones, self.habilitarSaves,
                core.camposUbis[0]))
        self.pantallaUbis.tableWidget.setColumnHidden(0, True)

        sugerenciasCat=[i[0] for i in bdd.cur.execute(
            'SELECT descripcion FROM cats_clase').fetchall()]
        self.pantallaClases.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
            self.pantallaClases.tableWidget, self.saveClases,
            self.deleteClases, self.habilitarSaves, core.camposClases[0],
            [sugerenciasCat]))
        self.pantallaClases.tableWidget.setColumnHidden(0, True)

        sql='''SELECT c.descripcion FROM clases c
               JOIN cats_clase cat ON c.id_cat=cat.id
               WHERE cat.descripcion='Usuario';'''
        sugerenciasClasesU=[i[0] for i in bdd.cur.execute(sql).fetchall()]
        self.pantallaUsuarios.pushButton_2.clicked.connect(
            lambda: core.insertarFilas(
                self.pantallaUsuarios.tableWidget, self.saveUsuarios,
                self.deleteUsuarios, self.habilitarSaves,
                core.camposUsuarios[0], [sugerenciasClasesU]))
        self.pantallaUsuarios.tableWidget.setColumnHidden(0, True)

        # Conectamos los parámetros de las gestiones y listados para
        # que se refresquen las tablas cada vez que el usuario cambie
        # un parámetro.
        self.pantallaStock.tableWidget.cellChanged.connect(
            self.actualizarTotal)
        self.pantallaStock.lineEdit.editingFinished.connect(self.fetchStock)
        self.pantallaStock.botonImprimir.clicked.connect(self.printStock)

        self.pantallaAlumnos.lineEdit.editingFinished.connect(
            self.fetchAlumnos)
        self.pantallaClases.lineEdit.editingFinished.connect(self.fetchClases)
        self.pantallaGrupos.lineEdit.editingFinished.connect(self.fetchGrupos)

        self.pantallaMovs.lineEdit.editingFinished.connect(
            self.fetchMovimientos)
        self.pantallaMovs.nId.valueChanged.connect(
            self.fetchMovimientos)
        self.pantallaMovs.nTurno.valueChanged.connect(
            self.fetchMovimientos)

        self.pantallaOtroPersonal.lineEdit.editingFinished.connect(
            self.fetchOtroPersonal)
        self.pantallaReps.lineEdit.editingFinished.connect(
            self.fetchReparaciones)

        self.pantallaTurnos.lineEdit.editingFinished.connect(self.fetchTurnos)
        self.pantallaTurnos.nId.valueChanged.connect(self.fetchTurnos)

        self.pantallaSubgrupos.lineEdit.editingFinished.connect(
            self.fetchSubgrupos)
        self.pantallaUbis.lineEdit.editingFinished.connect(
            self.fetchUbicaciones)
        self.pantallaClases.lineEdit.editingFinished.connect(self.fetchClases)
        self.pantallaHistorial.lineEdit.editingFinished.connect(
            self.fetchHistorial)
        self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentTextChanged.connect(self.check)
        self.pantallaDeudas.lineEdit.editingFinished.connect(self.fetchDeudas)
        self.pantallaDeudas.radioHerramienta.toggled.connect(self.fetchDeudas)
        self.pantallaDeudas.radioPersona.toggled.connect(self.fetchDeudas)
        self.pantallaDeudas.nMov.valueChanged.connect(self.fetchDeudas)
        self.pantallaDeudas.nTurno.valueChanged.connect(self.fetchDeudas)
        self.pantallaTurnos.desdeFecha.dateChanged.connect(self.fetchTurnos)
        self.pantallaTurnos.hastaFecha.dateChanged.connect(self.fetchTurnos)
        self.pantallaRealizarMov.cursoComboBox.currentTextChanged.connect(self.alumnos)
        self.pantallaRealizarMov.pushButton.clicked.connect(self.saveMovimiento)

        self.boton = toolboton("usuario", self)
        self.boton.setIconSize(QtCore.QSize(60, 40))
        self.label = QtWidgets.QLabel(str("El pañolero en turno es: "))
        self.label.setObjectName("sopas")
        widget_with_layout = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget_with_layout)
        layout.addWidget(self.label)
        layout.addWidget(self.boton)
        self.menubar.setCornerWidget(widget_with_layout,QtCore.Qt.Corner.TopRightCorner)

        # Actualizamos las fechas a los valores actuales.
        self.actualizarHastaFechas()

        # Hacemos un timer que actualice las fechas máximas cada 5 minutos
        timer=QtCore.QTimer()
        timer.timeout.connect(self.actualizarHastaFechas)
        timer.start(300000)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        # Establecemos la pantalla del login como pantalla por defecto.
        self.stackedWidget.setCurrentIndex(0)
        # Cambiamos el titulo de la ventana y la hacemos pantalla completa.
        self.move(0,0)
        self.setFixedSize(QtGui.QGuiApplication.primaryScreen().size())
        boton = QtWidgets.QPushButton()
        boton.setObjectName("prueba")
        boton.setText("X")
        boton.setFixedSize(40, 40)
        boton.setVisible(True)
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}cerrar.png'
        pixmap = QtGui.QPixmap(path)
        boton.clicked.connect(lambda:self.close())
        self.pantallaLogin.gridLayout.addWidget(boton, 0, 1, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.show()  
      
    def closeEvent(self, event: QtGui.QCloseEvent):
        if self.sender() != None:
            event.accept()
        else:
            event.ignore()

    def actualizarHastaFechas(self):
        """Este método actualiza los filtros de fecha y hora con la
        fecha y hora actuales.
        """
        self.pantallaReps.hastaFecha.setDate(
            QtCore.QDate.fromString(
                date.today().strftime("%Y/%m/%d"), "yyyy/MM/dd"))
        self.pantallaTurnos.hastaFecha.setDate(QtCore.QDate.fromString(
            date.today().strftime("%Y/%m/%d"), "yyyy/MM/dd"))
        self.pantallaMovs.hastaFecha.setDateTime(QtCore.QDateTime.fromString(
            datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "yyyy/MM/dd HH:mm:ss"))
        self.pantallaHistorial.hastaFecha.setDateTime(QtCore.QDateTime.fromString(
            datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "yyyy/MM/dd HH:mm:ss"))
        self.pantallaResumen.hastaFecha.setDate(QtCore.QDate.fromString(
            date.today().strftime("%Y/%m/%d"), "yyyy/MM/dd"))

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
                self.fetchStock()
                if bdd.cur.execute("SELECT c.descripcion FROM clases c join personal p on p.id_clase = c.id WHERE dni = ?",(self.usuario,)).fetchone()[0] != "Director de Taller":
                    self.menubar.actions()[4].setVisible(False)
                pañolero = bdd.cur.execute("select nombre_apellido from turnos join personal p on p.id = id_panolero WHERE fecha_egr is null").fetchone()
                if pañolero != None:
                    mensaje = "Hay un turno sin finalizar, desea continuarlo o finalizarlo?"
                    popup = PopUp("Turno",mensaje)

                    class sopas(QtCore.QObject):
                        def eventFilter(self, obj, event):
                            # Ignore all key events
                            if event.type() in [QtCore.QEvent.Type.KeyPress, QtCore.QEvent.Type.KeyRelease]:
                                return True  # Return True to indicate the event has been handled and should be ignored
                            return super().eventFilter(obj, event)
                        
                    filtro = sopas(popup)
                    popup.installEventFilter(filtro)
                    popup.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint)
                    popup.setWindowFlag(QtCore.Qt.WindowType.WindowTitleHint)
                    popup.button(QtWidgets.QMessageBox.StandardButton.Cancel).hide()
                    popup = PopUp("Turno",mensaje).exec()
                    if popup == QtWidgets.QMessageBox.StandardButton.Yes:
                        self.label.setText("El pañolero en turno es: " + pañolero[0])
                        self.label.setObjectName("sopas")
                        self.boton.menu().actions()[4].setVisible(False)
                        self.boton.menu().actions()[0].setVisible(False)
                        for i in range(7):
                            if i != 1:
                                self.menubar.actions()[i].setVisible(False)
                                
                    if popup == QtWidgets.QMessageBox.StandardButton.No:
                        profe = dal.obtenerDatos("usuarios", self.usuario,)
                        hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        bdd.cur.execute("""UPDATE turnos SET fecha_egr = ?, id_prof_egr = ? WHERE fecha_egr is null""", (hora, profe[0][0],))
                        bdd.con.commit()
                        self.label.setText("Usuario: " + bdd.cur.execute("SELECT nombre_apellido FROM personal WHERE dni = ?",(self.usuario,)).fetchone()[0])
                        for i in range(7):
                            if i != 1:
                                self.menubar.actions()[i].setVisible(True)
                                
                        if bdd.cur.execute("SELECT c.descripcion FROM clases c join personal p on p.id_clase = c.id WHERE dni = ?",(self.usuario,)).fetchone()[0] != "Director de Taller":
                            self.menubar.actions()[4].setVisible(False)
                        self.boton.menu().actions()[0].setVisible(True)
                        self.boton.menu().actions()[4].setVisible(True)

                else:
                    self.label.setText("Usuario: " + bdd.cur.execute("SELECT nombre_apellido FROM personal WHERE dni = ?",(self.usuario,)).fetchone()[0])

                self.menubar.show()
                self.pantallaLogin.usuarioState.setText("")
                self.pantallaLogin.passwordState.setText("")

            else:
                self.pantallaLogin.passwordState.setText("contraseña incorrecta")
                self.pantallaLogin.usuarioState.setText("")

        else:
            self.pantallaLogin.usuarioState.setText("usuario incorrecto")
            self.pantallaLogin.passwordState.setText("")

    def alumnos(self):
        self.pantallaRealizarMov.alumnoComboBox.clear()
        for i in dal.obtenerDatos("alumnos", self.pantallaRealizarMov.cursoComboBox.currentText(),):
            self.pantallaRealizarMov.alumnoComboBox.addItem(i[1])

    def check(self):
        if self.pantallaRealizarMov.tipoDeMovimientoComboBox.currentText() == "Envío a Reparación":
            self.pantallaRealizarMov.estadoComboBox.itemText
            self.pantallaRealizarMov.estadoComboBox.removeItem(self.pantallaRealizarMov.estadoComboBox.findText("En Reparación"))
        else:
            for i in dal.obtenerDatos("estados", ""):
                if 2 == self.pantallaRealizarMov.estadoComboBox.count():
                    self.pantallaRealizarMov.estadoComboBox.addItem(i[1])

    def realizarMovimiento(self):
        self.pantallaRealizarMov.tipoDeMovimientoComboBox.clear()
        self.pantallaRealizarMov.herramientaComboBox.clear()
        self.pantallaRealizarMov.estadoComboBox.clear()
        self.pantallaRealizarMov.cursoComboBox.clear()
        self.pantallaRealizarMov.ubicacionComboBox.clear()
        
        for i in dal.obtenerDatos("tipos_mov", ""):
            self.pantallaRealizarMov.tipoDeMovimientoComboBox.addItem(i[1])

        for i in dal.obtenerDatos("stock", ""):
            self.pantallaRealizarMov.herramientaComboBox.addItem(i[1])

        for i in dal.obtenerDatos("estados", ""):
            self.pantallaRealizarMov.estadoComboBox.addItem(i[1])

        for i in dal.obtenerDatos("clases", ""):
            self.pantallaRealizarMov.cursoComboBox.addItem(i[1])
        
        for i in dal.obtenerDatos("ubicaciones", ""):
            self.pantallaRealizarMov.ubicacionComboBox.addItem(i[1])

        self.pantallaRealizarMov.cursoComboBox.currentTextChanged.connect(
            self.alumnos)
        self.pantallaRealizarMov.pushButton.clicked.connect(
            self.saveMovimiento)

        self.stackedWidget.setCurrentIndex(13)
    
    def sumar(self,cant,herramienta,estado):
            try:
                estado = estado[estado.index(" "):]
                estado = estado[1:]
            except:
                pass
            estado = unidecode(estado)
            estado = "cant_" + estado.lower()
            query = f"select {estado} from stock WHERE id = ?"
            params = (herramienta,)
            if bdd.cur.execute(query,params)==None:
                query = f"UPDATE stock SET {estado} = 0 + ? WHERE id = ?"
            else:
                query = f"UPDATE stock SET {estado} = {estado} + ? WHERE id = ?"
                params = (cant, herramienta)
            self.sopas=True
            bdd.cur.execute(query,params)

    def restar(self,cant,herramienta,estado):
        if bdd.cur.execute("select cant_condiciones from stock").fetchall()[0][0]-cant>=0:
            try:
                estado = estado[estado.index(" "):]
                estado = estado[1:]
            except:
                pass
            estado = unidecode(estado)
            estado = "cant_" + estado.lower()
            query = f"select {estado} from stock WHERE id = ?"
            params = (herramienta,)
            if bdd.cur.execute(query,params)==None:
                query = f"UPDATE stock SET {estado} = 0 - ? WHERE id = ?"
            else:
                query = f"UPDATE stock SET {estado} = {estado} - ? WHERE id = ?"
                params = (cant, herramienta)
            bdd.cur.execute(query, params)
            self.sopas=True
        else:
            self.sopas=False

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
            where s.descripcion LIKE ? and s.id_ubi  LIKE ?""" ,(self.pantallaRealizarMov.herramientaComboBox.currentText(), ubicacion[0][0])).fetchone()

        descripcion = self.pantallaRealizarMov.descripcionLineEdit.text()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if cant == 0:
            mensaje = """Por favor ingrese un valor mayor a 0."""
            return PopUp("Error", mensaje).exec()
        else:
            if persona != "" and persona != None:
                if turno == " " or turno == None or turno == []:
                    turno = bdd.cur.execute("SELECT nombre_apellido FROM personal WHERE dni = ?",(self.usuario,)).fetchone()
                bdd.cur.execute("INSERT INTO movimientos(id_turno,id_elem,id_estado,cant,id_persona,fecha_hora,id_tipo,descripcion) VALUES(?, ?, ?, ?, ?, ?, ?,?)",
                                (turno[0][0], herramienta[0], estado[0][0], cant, persona[0], fecha, tipo[0][0], descripcion))
                if tipo[0][0] == 1:
                    self.sumar(cant,herramienta[0],estado[0][1])
                if tipo[0][0] == 2:
                    self.restar(cant,herramienta[0],estado[0][1])
                    self.sumar(cant,herramienta[0],"En reparacion")
                if tipo[0][0] == 3:
                    self.restar(cant,herramienta[0],estado[0][1])
                    self.sumar(cant,herramienta[0],"prest")
                if tipo[0][0] == 4:
                    self.sumar(cant,herramienta[0],estado[0][1])
                    self.restar(cant,herramienta[0],"prest")
                if tipo[0][0] == 5:
                    self.restar(cant,herramienta[0],estado[0][1])
                    self.sumar(cant,herramienta[0],"De baja")
                
                bdd.con.commit()
                if self.sopas == True:
                    self.pantallaRealizarMov.tipoDeMovimientoComboBox.clear()
                    self.pantallaRealizarMov.herramientaComboBox.clear()
                    self.pantallaRealizarMov.estadoComboBox.clear()
                    self.pantallaRealizarMov.cursoComboBox.clear()
                    self.pantallaRealizarMov.ubicacionComboBox.clear()
                    mensaje = """Movimiento cargado con exito."""
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
            tabla=self.sender()
        if row is None:
            row=tabla.indexAt(self.sender().pos()).row()
        tabla.cellWidget(row, tabla.columnCount()-2).setEnabled(True)
    def insertarFilas(self, tabla: QtWidgets.QTableWidget,
                      funcGuardar: types.FunctionType,
                      funcEliminar: types.FunctionType,
                      camposObligatorios: tuple | None = None,
                      camposNoEditables: tuple | None = None,
                      camposSugeridos: tuple | None = None,
                      sugerencias: tuple | list | None= None,
                      campoEspecial: int | None = None):
        """Este método inserta una nueva fila en la tabla stock.

        Si la fila anterior fue recientemente ingresada y los datos no
        fueron modificados, en vez de añadir una nueva fila se le
        muestra un mensaje al usuario pidiéndole que ingrese los datos
        primero.

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
        # Si no se pasa la tabla por parámetro, se asume que la tabla
        # modificada es quien llamó a este método. Esto es porque
        # cuando se llama a este método desde una tabla modificada, hay
        # ocasiones en las que la tabla
        if tabla is None:
            tabla=self.sender()
        
        # Si la fila no se pasa, se asume que fue un widget quien llamó
        # a este método.
        if row is None:
            # Se obtiene la posicion de la fila a través del widget.
            row=tabla.indexAt(self.sender().pos()).row()
        # Habilitamos el botón de saves para que el usuario pueda hacer
        # cambios.
        tabla.cellWidget(row, tabla.columnCount()-2).setEnabled(True)

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
            #... se usa la tabla de la pantalla stock.
            tabla = self.pantallaStock.tableWidget
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
        if col in (2, 3, 4):
            # ...obtenemos los valores de las cantidades
            cantCond = int(tabla.item(row, 2).text())
            cantRep = tabla.item(row, 3).text()
            cantBaja = tabla.item(row, 4).text()
            cantPrest = tabla.item(row, 5).text()
            # Las cantidades en reparación y de baja pueden no ser
            # numéricas ("-", significa dato nulo), por lo que hay que
            # checkear si el usuario las ingresó como numéricas o no
            # antes de hacer cuentas.
            # Si las cantidades en reparación y de baja son numéricas..
            if (cantRep.isnumeric() and cantBaja.isnumeric()):
                #... se calcula el total sumando todas las cantidades
                total = QtWidgets.QTableWidgetItem(
                            str(cantCond + int(cantRep)
                            + int(cantBaja) + int(cantPrest)))
            # Si no...
            else:
                #... se calcula el total sumando solamente las
                # cantidades en condiciones y adeudadas.
                total = QtWidgets.QTableWidgetItem(
                            str(cantCond) + int(cantRep))
            # El campo se hace no editable y se guarda en la tabla
            total.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                           QtCore.Qt.ItemFlag.ItemIsEnabled)
            tabla.setItem(row, 6, total)

    def actualizarSugerenciasSubgrupos(self):
        """Este método actualiza las sugerencias de los campos de
        subgrupos al editar lo ingresado en un campo de grupos
        relacionado, ya que las sugerencias de subgrupos deben estar
        relacionadas al grupo ingresado.
        """
        # Usamos la tabla de stock.
        tabla=self.pantallaStock.tableWidget
        # Obtenemos la fila del campo de grupos modificado.
        row = tabla.indexAt(self.sender().pos()).row()
        # Obtenemos los nuevos datos.
        grupo=tabla.cellWidget(row, 7).text()
        # Obtenemos el cuadro de sugerencias del campo subgrupos.
        completer=tabla.cellWidget(row, 8).completer()
        # Obtenemos sugerencias actualizadas.
        sugerencias=[i[0] for i in 
                     bdd.cur.execute('''SELECT s.descripcion FROM subgrupos s
                     JOIN grupos g ON s.id_grupo = g.id
                     WHERE g.descripcion LIKE ?''', (grupo,)).fetchall()]
        # Añadimos las sugerencias actualizadas al campo de subgrupos.
        completer.setModel(QtCore.QStringListModel(sugerencias))
        # Habilitamos el boton de guardar para que el usuario pueda
        # guardar los cambios.
        tabla.cellWidget(row, tabla.columnCount()-2).setEnabled(True)
    
    def fetchStock(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        # La mayoría de métodos de stock son parecidos a este, por lo
        # que solo voy a documentar esta función.
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
        
        # Guardamos los filtros.
        barraBusqueda = self.pantallaStock.lineEdit
        listaUbi = self.pantallaStock.listaUbi

        # Desconectamos el filtro por la misma razón que la tabla.
        listaUbi.disconnect()
        # Obtenemos el texto seleccionado.
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

        if ubiSeleccionada == "Todas":
            filtroUbi = (None,)
        else:
            filtroUbi = (ubiSeleccionada,)

        # Se obtienen los datos de la base de datos.
        datos = dal.obtenerDatos("stock", barraBusqueda.text(), filtroUbi)

        # Se refresca la tabla, eliminando todas las filas anteriores.
        tabla.setRowCount(0)

        # Por cada número de fila y los contenidos de ésta en los datos
        # obtenidos...
        for rowNum, rowData in enumerate(datos):
            # ...se añade una fila a la tabla.
            tabla.insertRow(rowNum)

            # Empezamos a añadir los items.
            item0=QtWidgets.QTableWidgetItem(str(rowData[0]))
            # Los centramos.
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 0, item0)
            item1=QtWidgets.QTableWidgetItem(str(rowData[1]))
            item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 1, item1)
            item2=QtWidgets.QTableWidgetItem()
            item2.setData(0, rowData[2])
            item2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 2, item2)
            item3=QtWidgets.QTableWidgetItem()
            item3.setData(0, rowData[3])
            item3.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(rowNum, 3, item3)
            item4=QtWidgets.QTableWidgetItem()
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
                           bdd.cur.execute('SELECT descripcion FROM grupos').fetchall()]
            # Creamos el campo con sugerencia.
            paramGrupos=ParamEdit(sugerencias, rowData[7])
            # Cuando termina de editarse, hacemos que actualice el
            # cuadro de sugerencias del campo grupos.
            paramGrupos.editingFinished.connect(self.actualizarSugerenciasSubgrupos)
            tabla.setCellWidget(rowNum, 7, paramGrupos)
            sql = '''SELECT s.descripcion FROM subgrupos s
                   JOIN grupos g ON s.id_grupo = g.id
                   WHERE g.descripcion LIKE ?'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql, (rowData[7],)).fetchall()]
            subgrupos=ParamEdit(sugerencias, rowData[8])
            subgrupos.textChanged.connect(lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(rowNum, 8, subgrupos)
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute('SELECT descripcion FROM ubicaciones').fetchall()]
            ubicaciones=ParamEdit(sugerencias, rowData[9])
            ubicaciones.textChanged.connect(lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(rowNum, 9, ubicaciones)

            # Generamos los botones para la fila de la tabla
            core.generarBotones(
                lambda: self.saveOne(
                    tabla, self.saveStock, self.fetchStock, datos),
                lambda: self.deleteStock(datos), tabla, rowNum)

        # Cambiamos la altura de la fila.
        tabla.setRowHeight(0, 35)
        # Hacemos que las columnas no puedan ser menos anchas que sus
        # contenidos.
        tabla.resizeColumnsToContents()

        # Hacemos que las columnas se expandan al ampliar la pantalla.
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            7, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            8, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            9, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        # Hacemos que cada vez que se edite una celda de una tabla, se
        # ejecuta la función.
        tabla.cellChanged.connect(self.actualizarTotal)
        tabla.setSortingEnabled(True)
        listaUbi.currentIndexChanged.connect(self.fetchStock)
        self.stackedWidget.setCurrentIndex(3)

    def saveOne(self, tabla, funcSave, funcFetch, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla stock de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla stock, que se usarán para obtener
                el id de la fila en la tabla.
        """
        # Se pregunta al usuario si desea guardar los cambios en la
        # tabla. NOTA: Esos tabs en el string son para mantener la
        # misma identación en todas las líneas así dedent funciona,
        # sino le da ansiedad.
        # Obtenemos los ids de los campos que no podemos dejar vacíos.
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()
        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            exito=funcSave(tabla, row, datos)
            if exito == True:    
                info = "Los datos se han guardado con éxito."
                PopUp("Aviso", info).exec()
            posicion = barra.value()
            funcFetch()
            barra.setValue(posicion)
    
    def saveStock(self, tabla, row, datos):
        iCampos = (1, 2, 7, 8, 9)
        # Por cada campo que no debe ser nulo...
        for iCampo in iCampos:
            # Si el campo está vacio...
            if tabla.item(row, iCampo) is not None:
                texto = tabla.item(row, iCampo).text()
            else:
                texto = tabla.cellWidget(row, iCampo).text()
            if texto == "":
                # Le pide al usuario que termine de llenar los campos
                # y corta la función.
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            cond = int(tabla.item(row, 2).text())
            rep = tabla.item(row, 3).text()
            baja = tabla.item(row, 4).text()
            prest = int(tabla.item(row, 5).text())
            if rep not in ("-", "") or baja not in ("-", ""):
                rep = int(rep)
                baja = int(baja)

            else:
                rep = None
                baja = None
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingrese los datos correctamente."
            return PopUp("Error", mensaje).exec()

        # Se obtiene el texto de todas las celdas.
        desc = tabla.item(row, 1).text()
        grupo = tabla.cellWidget(row, 7).text()
        subgrupo = tabla.cellWidget(row, 8).text()
        ubi = tabla.cellWidget(row, 9).text()

        # Verificamos que el grupo esté registrado.
        idGrupo = bdd.cur.execute(
            "SELECT id FROM grupos WHERE descripcion LIKE ?", (grupo,)
        ).fetchone()
        # Si no lo está...
        if not idGrupo:
            # Muestra un mensaje de error al usuario y termina la
            # función.
            info = "El grupo ingresado no está registrado. Regístrelo e ingrese nuevamente"
            return PopUp("Error", info).exec()

        # Verificamos que el subgrupo esté registrado y que
        # coincida con el grupo ingresado.
        idSubgrupo = bdd.cur.execute(
            "SELECT id FROM subgrupos WHERE descripcion LIKE ? AND id_grupo = ?",
            (subgrupo, idGrupo[0],)
        ).fetchone()
        if not idSubgrupo:
            info = "El subgrupo ingresado no está registrado o no pertenece al grupo ingresado. Regístrelo o asegúrese que esté relacionado al grupo e ingrese nuevamente."
            return PopUp("Error", info).exec()

        idUbi = bdd.cur.execute("SELECT id FROM ubicaciones WHERE descripcion LIKE ?",
                                (ubi,)).fetchone()
        if not idUbi:
            info = "La ubicación ingresada no está registrada. Regístrela e intente nuevamente."
            return PopUp("Error", info).exec()

        datosNuevos = ["" if cell in ("-", None) else cell for cell in [desc, cond, rep, baja, prest, grupo, subgrupo, ubi]]
        try:
            idd = tabla.item(row, 0).text()
            if not idd:
                bdd.cur.execute(
                    "INSERT INTO stock VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)",
                    (desc, cond, rep, baja, prest,
                        idSubgrupo[0], idUbi[0],)
                )
                dal.insertarHistorial(
                    self.usuario, 'Inserción', 'Stock', desc, None, datosNuevos)
            else:
                idd=int(idd)
                # Guardamos los datos de la fila en
                bdd.cur.execute(
                    """UPDATE stock
                    SET descripcion = ?, cant_condiciones = ?, cant_reparacion=?,
                    cant_baja = ?, cant_prest=?, id_subgrupo = ?, id_ubi=?
                    WHERE id = ?""",
                    (desc, cond, rep, baja, prest,
                        idSubgrupo[0], idUbi[0], idd,)
                )
                datosViejos = [["" if cellData in ("-", None) else cellData for cellData in fila] for fila in datos if fila[0] == idd][0]
                dal.insertarHistorial(
                    self.usuario, 'Edición', 'Stock', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "La herramienta que desea ingresar ya está ingresada. Ingrese otra información o revise la información ya ingresada"
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True

    def deleteStock(self, datos: list | None = None) -> None:
        """Este método elimina una fila de una tabla de la base de
        datos

        Parámetros
        ----------
        idd: int | None = None
            El número que relaciona la fila de la tabla de la UI con la
            fila de la tabla de la base de datos.
            Default: None
        """
        # Obtenemos la tabla a la que vamos a realizarle la eliminación
        tabla = self.pantallaStock.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        barra = tabla.verticalScrollBar()
        idd=tabla.item(row, 0).text()
        # Si no se pasó el argumento idd, significa que la fila no está
        # relacionada con la base de datos. Eso significa que la fila
        # se insertó en la tabla de la UI, pero aún no se guardaron los
        # cambios en la base de datos. En ese caso...
        if not idd:
            # ...solo debemos sacarla de la UI.
            return tabla.removeRow(row)
        idd=int(idd)
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
        if hayRelacion:
            mensaje = "La herramienta/insumo tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar esta herramienta/insumo."
            return PopUp('Advertencia', mensaje).exec()

        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar la herramienta/insumo?"
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Obtenemos los datos para guardarlos en el historial.
            datosEliminados = [fila for fila in datos if fila[0] == idd][0]

            # Insertamos los datos en el historial para que quede registro.
            dal.insertarHistorial(
                self.usuario, "Eliminación", "Stock", datosEliminados[1], datosEliminados[1:])
            # Eliminamos los datos
            dal.eliminarDatos('stock', idd)
            posicion = barra.value()
            self.fetchStock()
            barra.setValue(posicion)

    def printStock(self):
        """Este método genera un spreadsheet a partir de la tabla de la
        pantalla stock.
        """
        info = "Los datos que se imprimirán serán los datos guardados en la base de datos. Guarde todos los cambios antes de imprimir."
        boton = PopUp('Advertencia', info).exec()
        if boton == QtWidgets.QMessageBox.StandardButton.Ok:
            dialog = QtWidgets.QFileDialog(self)
            dialog.setDirectory(os.path.expanduser('~documents'))
            dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
            dialog.setOption(QtWidgets.QFileDialog.Option.ShowDirsOnly)
            dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
            dialog.setDefaultSuffix('xlsx')
            dialog.setWindowTitle('Guardar archivo')
            filename = dialog.getSaveFileName()[0]
            if not filename:
                return
            barraBusqueda = self.pantallaStock.lineEdit
            listaUbi = self.pantallaStock.listaUbi
            if listaUbi.currentText() == "Todas":
                filtroUbi = (None,)
            else:
                filtroUbi = (listaUbi.currentText(),)

            rawData = dal.obtenerDatos(
                "stock", barraBusqueda.text(), filtroUbi)
            datos = []
            for rowNum, rawRow in enumerate(rawData):
                datos.append([rawRow[1], rawRow[2], rawRow[3], rawRow[4],
                              rawRow[5], rawRow[6], rawRow[7], rawRow[8]])
                if rawRow[3] == "-":
                    datos[rowNum].insert(5, rawRow[2])
                else:
                    total = rawRow[2] + rawRow[3] + rawRow[4] + rawRow[5]
                    datos[rowNum].insert(5, total)
            columnas = ["Elemento", "Cant. en Condiciones",
                        "Cant. en Reparación", "Cant. de Baja",
                        "Cant. Prestadas", "Total", "Grupo", "Subgrupo",
                        "Ubicación"]
            df = pd.DataFrame(datos, columns=columnas)
            df.to_excel(filename)
            info = "Los datos se imprimieron exitosamente."
            PopUp('Aviso', info).exec()

    def cargarPlanilla(self):
        info = '¿La planilla está en el formato de tutorvip?'
        formato = PopUp('Pregunta-Info', info).exec()
        if formato == QtWidgets.QMessageBox.StandardButton.Yes:
            info = '¿Desea usar el formato de cursos del tutorvip o el formato de cursos simplificado?'
            actualizarCursos = PopUp('Pregunta', info).exec()
            if actualizarCursos in (QtWidgets.QMessageBox.StandardButton.Yes,
                                    QtWidgets.QMessageBox.StandardButton.No):
                actualizarCursos = (QtWidgets.QMessageBox.StandardButton.Yes
                                    == actualizarCursos)
            else:
                return
        elif formato == QtWidgets.QMessageBox.StandardButton.No:
            info = 'Esta acción no se puede deshacer. Los datos de la gestión se actualizarán en base al dni y se actualizarán los nombres y los cursos en base a los datos de la planilla. Asegúrese que los dni de la planilla y de la gestión alumnos sean correctos, de lo contrario se pueden originar alumnos duplicados. Además, asegúrese de que los datos (columnas) de la planilla esten en el siguiente orden: nombre, curso y dni.'
            if PopUp('Advertencia', info).exec() != QtWidgets.QMessageBox.StandardButton.Ok:
                return
            actualizarCursos=True
        else:
            return
        formato = formato == QtWidgets.QMessageBox.StandardButton.Yes

        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(os.path.expanduser('~documents'))
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        dialog.setNameFilter("Hoja de cálculo (*.xlsx *.xls *.xlsm *.xlsb *.xltx *.xltm *.xlt *.xlam *.xla *.xlw *.xlr)")
        dialog.setWindowTitle('Abrir archivo')
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
        else:
            return
        try:
            df=pd.read_excel(filename)
        except:
            info='El archivo proporcionado no es válido como planilla. Proporcione un archivo válido.'
            return PopUp('Error', info).exec()
        cols = list(df.columns.values)
                
        if len(cols) != 3:
            info='La plantilla proporcionada tiene una cantidad de columnas distinta al formato requerido. Proporcione la cantidad justa de columnas.'
            return PopUp('Error', info).exec()
        
        if formato:
            df=df[[cols[2], cols[0], cols[1]]]
            cols = list(df.columns.values)
 
        if ("dni" in cols[0].lower() or "curso" in cols[0].lower()
            or "dni" in cols[1].lower() or "curso" in cols[2].lower()
            or "nombre" in cols[2].lower()):
            info='Los datos proporcionados no están ordenados correctamente. Ordene los datos de la planilla correctamente e intente nuevamente.'
            return PopUp('Error', info).exec()
        dal.cargarPlanilla(df.values.tolist(), actualizarCursos)
        self.fetchAlumnos()
        PopUp('Aviso', 'La planilla se ha cargado con éxito.').exec()

    def fetchAlumnos(self):
        """Este método obtiene los datos de la tabla personal y los
        inserta en la tabla de la interfaz de usuario.
        """
        tabla = self.pantallaAlumnos.tableWidget
        barraBusqueda = self.pantallaAlumnos.lineEdit
        try:
            tabla.disconnect()
        except:
            pass


        tabla.setSortingEnabled(False)

        datos = dal.obtenerDatos("alumnos", barraBusqueda.text())

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
            sql='''SELECT c.descripcion FROM clases c
            JOIN cats_clase cat ON c.id_cat=cat.id
            WHERE cat.descripcion='Alumno';'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql).fetchall()]
            cursos = ParamEdit(sugerencias, rowData[2])
            cursos.textChanged.connect(lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(
                rowNum, 2, cursos)
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[3])))

            core.generarBotones(
                lambda: self.saveAlumnos(datos), lambda: self.deleteAlumnos(datos), tabla, rowNum)

            self.pantallaAlumnos.tableWidget.setRowHeight(0, 35)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(1)

    def saveAlumnos(self, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla alumnos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla alumnos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        tabla = self.pantallaAlumnos.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()
        iCampos = (1, 2, 3)

        for iCampo in iCampos:
            if iCampo == 2:
                texto=tabla.cellWidget(row, iCampo).text()
            else:
                texto=tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            nombre = tabla.item(row, 1).text()
            clase = tabla.cellWidget(row, 2).text()

            idClase = bdd.cur.execute(
                "SELECT id FROM clases WHERE descripcion LIKE ? AND id_cat=1", (
                    clase,)
            ).fetchone()
            if not idClase:
                info = "El curso ingresado no está registrado o no está vinculado correctamente a la categoría alumno. Regístrelo o revise los datos ya ingresados."
                return PopUp("Error", info).exec()
            datosNuevos = [nombre, clase, dni]
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                        (nombre, dni, idClase[0],)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Alumnos', nombre, None, datosNuevos[1:])
                else:
                    idd = int(tabla.item(row, 0).text())
                    bdd.cur.execute(
                        """UPDATE personal
                        SET nombre_apellido=?, id_clase=?, dni=?
                        WHERE id = ?""",
                        (nombre, idClase[0], dni, idd,)
                    )
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    dal.insertarHistorial(
                        self.usuario, 'Edición', 'Alumnos', datosViejos[1], datosViejos[2:], datosNuevos)
            except sqlite3.IntegrityError:
                info = "El dni ingresado ya está registrado. Regístre uno nuevo o revise la información ya ingresada."
                return PopUp("Error", info).exec()

            bdd.con.commit()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchAlumnos()
            barra.setValue(posicion)

    def deleteAlumnos(self, datos: list | None = None) -> None:
        """Este método elimina una fila de una tabla de la base de
        datos

        Parámetros
        ----------
        idd: int | None = None
            El número que relaciona la fila de la tabla de la UI con la
            fila de la tabla de la base de datos.
            Default: None
        """
        tabla = self.pantallaAlumnos.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()
        barra = tabla.verticalScrollBar()
        
        idd=tabla.item(row, 0).text()

        if not idd:
            return tabla.removeRow(row)
        
        idd=int(idd)

        hayRelacion = dal.verifElimAlumnos(idd)
        if hayRelacion:
            mensaje = "El alumno tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este alumno."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el alumno/a?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            datosEliminados = [fila for fila in datos if fila[0] == idd][0]
            dal.insertarHistorial(
                self.usuario, "Eliminación", "Alumnos", datosEliminados[1], datosEliminados[2:])

            dal.eliminarDatos('personal', idd)
            posicion = barra.value()
            self.fetchAlumnos()
            barra.setValue(posicion)

    def fetchMovimientos(self):
        """Este método obtiene los datos de la tabla movimientos y los
        inserta en la tabla de la interfaz de usuario.
        """
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

        desdeFecha.setMaximumDateTime(
            QtCore.QDateTime.fromString(
                datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "yyyy/MM/dd HH:mm:ss"))
        hastaFecha.setMaximumDateTime(
            QtCore.QDateTime.fromString(
                (datetime.now()+relativedelta(years=100)).strftime("%Y/%m/%d %H/%M/%S"), "yyyy/MM/dd HH:mm:ss"))

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
                rowData[7], 'yyyy/MM/dd HH:mm:ss')
            if fecha >= desdeFecha.dateTime() and fecha <= hastaFecha.dateTime():
                datos.append(rowData)

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            for cellNum, cellData in enumerate(rowData):
                item = QtWidgets.QTableWidgetItem(str(cellData))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum, cellNum, item)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeMode.Stretch)

        listaElem.currentIndexChanged.connect(self.fetchMovimientos)
        listaPersona.currentIndexChanged.connect(self.fetchMovimientos)
        listaPanolero.currentIndexChanged.connect(self.fetchMovimientos)
        desdeFecha.dateTimeChanged.connect(self.fetchMovimientos)
        hastaFecha.dateTimeChanged.connect(self.fetchMovimientos)

        self.stackedWidget.setCurrentIndex(4)

    def fetchGrupos(self):
        """Este método obtiene los datos de la tabla grupos y los
        inserta en la tabla de la interfaz de usuario.
        """

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

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))

            core.generarBotones(
                lambda: self.saveGrupos(datos), lambda: self.deleteGrupos(datos), tabla, rowNum)
            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(2)

    def saveGrupos(self, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla grupos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla grupos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        tabla = self.pantallaGrupos.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()

        if tabla.item(row, 1).text() == "":
            mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            grupo = tabla.item(row, 1).text()
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO grupos VALUES(NULL, ?)", (grupo,))
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Grupos', grupo, None, None)
                else:
                    idd = int(tabla.item(row, 0).text())
                    bdd.cur.execute(
                        "UPDATE grupos SET descripcion = ? WHERE id = ?",
                        (grupo, idd,)
                    )
                    datosNuevos = [grupo]
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    dal.insertarHistorial(
                        self.usuario, 'Edición', 'Grupos', datosViejos[1], None, datosNuevos)
            except sqlite3.IntegrityError:
                mensaje = "El grupo que desea ingresar ya está ingresado. Ingrese otro grupo o revise los datos ya ingresados."
                return PopUp("Error", mensaje).exec()

            bdd.con.commit()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchGrupos()
            barra.setValue(posicion)

    def deleteGrupos(self, datos: list | None = None) -> None:
        """Este método elimina una fila de una tabla de la base de
        datos

        Parámetros
        ----------
        idd: int | None = None
            El número que relaciona la fila de la tabla de la UI con la
            fila de la tabla de la base de datos.
            Default: None
        """
        tabla = self.pantallaGrupos.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()
        barra = tabla.verticalScrollBar()

        idd=tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd=int(idd)

        hayRelacion = dal.verifElimGrupos(idd)
        if hayRelacion:
            mensaje = "El grupo tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este grupo."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el grupo?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            datosEliminados = [fila for fila in datos if fila[0] == idd][0]
            dal.insertarHistorial(
                self.usuario, 'Eliminación', 'Grupos', datosEliminados[1], None)
            dal.eliminarDatos('grupos', idd)
            posicion = barra.value()
            self.fetchGrupos()
            barra.setValue(posicion)

    def fetchOtroPersonal(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        tabla = self.pantallaOtroPersonal.tableWidget
        barraBusqueda = self.pantallaOtroPersonal.lineEdit
        try:
            tabla.disconnect()
        except:
            pass


        tabla.setSortingEnabled(False)

        datos = dal.obtenerDatos("otro_personal", barraBusqueda.text())

        tabla.setRowCount(0)
        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
            sql='''SELECT c.descripcion FROM clases c
            JOIN cats_clase cat ON c.id_cat=cat.id
            WHERE cat.descripcion='Personal';'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql).fetchall()]
            clases = ParamEdit(sugerencias, rowData[2])
            clases.textChanged.connect(lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(
                rowNum, 2, clases)
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[3])))

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            core.generarBotones(
                lambda: self.saveOtroPersonal(datos), lambda: self.deleteOtroPersonal(datos), tabla, rowNum)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(5)

    def saveOtroPersonal(self, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla personal de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla personal, que se usarán para
                obtener el id de la fila en la tabla.
        """
        tabla = self.pantallaOtroPersonal.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()
        iCampos = (1, 2, 3)
        for iCampo in iCampos:
            if iCampo==2:
                texto=tabla.cellWidget(row, iCampo).text()
            else:
                texto=tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            nombre = tabla.item(row, 1).text()
            clase = tabla.cellWidget(row, 2).text()

            idClase = bdd.cur.execute(
                "SELECT id FROM clases WHERE descripcion = ? AND id_cat=2", (
                    clase,)
            ).fetchone()
            if not idClase:
                info = 'La clase ingresada no está registrada o no está vinculada a la categoría "Personal". Regístrela o revise los datos ya ingresados.'
                return PopUp("Error", info).exec()
            
            datosNuevos = [nombre, clase, dni,]
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                        (nombre, dni, idClase[0],)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Personal', nombre, None, datosNuevos[1:])
                else:
                    idd = int(tabla.item(row, 0).text())
                    bdd.cur.execute(
                        """UPDATE personal
                        SET nombre_apellido=?, dni=?, id_clase=?
                        WHERE id = ?""",
                        (nombre, dni, idClase[0], idd,)
                    )
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    dal.insertarHistorial(
                        self.usuario, 'Edición', 'Personal', datosViejos[1], datosViejos[2:], datosNuevos)
            except sqlite3.IntegrityError:
                info = "El dni ingresado ya está registrado. Ingrese uno nuevo o revise la información ya ingresada."
                return PopUp("Error", info).exec()
            bdd.con.commit()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchOtroPersonal()
            barra.setValue(posicion)

    def saveSubgrupos(self, tabla, row, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla subgrupos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla subgrupos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        iCampos = (1, 2)
        for iCampo in iCampos:
            if iCampo == 2:
                texto=tabla.cellWidget(row, iCampo).text()
            else:
                texto=tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        subgrupo = tabla.item(row, 1).text()
        grupo = tabla.cellWidget(row, 2).text()

        idGrupo = bdd.cur.execute(
            "SELECT id FROM grupos WHERE descripcion LIKE ?", (grupo,)
        ).fetchone()
        if not idGrupo:
            info = "El grupo ingresado no está registrado. Regístrelo e ingrese nuevamente"
            return PopUp("Error", info).exec()

        datosNuevos = [subgrupo, grupo]

        try:
            if not datos:
                bdd.cur.execute(
                    "INSERT INTO subgrupos VALUES(NULL, ?, ?)",
                    (subgrupo, idGrupo[0])
                )
                dal.insertarHistorial(
                    self.usuario, 'Inserción', 'Subgrupos', subgrupo, None, datosNuevos[1:])
            else:
                idd = int(tabla.item(row, 0).text())
                # Guardamos los datos de la fila en
                bdd.cur.execute(
                    """UPDATE subgrupos
                    SET descripcion=?, id_grupo=?
                    WHERE id = ?""",
                    (subgrupo, idGrupo[0], idd)
                )
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                dal.insertarHistorial(
                    self.usuario, 'Edición', 'Subgrupos', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El subgrupo ingresado ya está registrado en el grupo. Ingrese un subgrupo distinto, ingreselo en un grupo distinto o revise los datos ya ingresados."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True

    def deleteOtroPersonal(self, datos: list | None = None) -> None:
        """Este método elimina una fila de una tabla de la base de
        datos 

        Parámetros
        ----------
        idd: int | None = None
            El número que relaciona la fila de la tabla de la UI con la
            fila de la tabla de la base de datos.
            Default: None
        """
        tabla = self.pantallaOtroPersonal.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()
        barra = tabla.verticalScrollBar()

        idd=tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd=int(idd)

        hayRelacion = dal.verifElimOtroPersonal(idd)
        if hayRelacion:
            mensaje = "El personal tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar el personal."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el personal?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            datosViejos = [fila for fila in datos if fila[0] == idd][0]
            dal.insertarHistorial(
                self.usuario, 'Eliminación', 'Personal', datosViejos[1], datosViejos[2:])
            dal.eliminarDatos('personal', idd)
            posicion = barra.value()
            self.fetchOtroPersonal()
            barra.setValue(posicion)

    def fetchSubgrupos(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
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
            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
            sugerencias=[i[0] for i in
                bdd.cur.execute('SELECT descripcion FROM grupos').fetchall()]
            grupos=ParamEdit(sugerencias, rowData[2])
            grupos.textChanged.connect(lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(rowNum, 2, grupos)

            core.generarBotones(
                lambda: self.saveOne(
                    tabla, self.saveSubgrupos, self.fetchSubgrupos, datos),
                lambda: self.deleteSubgrupos(datos), tabla, rowNum)

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(6)


    def deleteSubgrupos(self, datos: list | None = None) -> None:
        """Este método elimina una fila de una tabla de la base de
        datos

        Parámetros
        ----------
        idd: int | None = None
            El número que relaciona la fila de la tabla de la UI con la
            fila de la tabla de la base de datos.
            Default: None
        """
        tabla = self.pantallaSubgrupos.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()

        idd=tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd=int(idd)
        hayRelacion = dal.verifElimSubgrupos(idd)
        if hayRelacion:
            mensaje = "El subgrupo tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este subgrupo."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el subgrupo?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            datosViejos = [fila for fila in datos if fila[0] == idd][0]
            dal.insertarHistorial(
                self.usuario, 'Eliminación', 'Subgrupos', datosViejos[1], datosViejos[2:])
            dal.eliminarDatos('subgrupos', idd)
            posicion = barra.value()
            self.fetchSubgrupos()
            barra.setValue(posicion)

    def fetchTurnos(self):
        """Este método obtiene los datos de la tabla turnos y los
        inserta en la tabla de la interfaz de usuario.
        """
        tabla = self.pantallaTurnos.tableWidget
        barraBusqueda = self.pantallaTurnos.lineEdit
        nId = self.pantallaTurnos.nId
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

        desdeFecha.setMaximumDate(QtCore.QDate.fromString(
            date.today().strftime("%Y/%m/%d"), "yyyy/MM/dd"))
        hastaFecha.setMaximumDate(QtCore.QDate.fromString(
            (date.today()+relativedelta(years=100)).strftime("%Y/%m/%d"), "yyyy/MM/dd"))

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
                item = QtWidgets.QTableWidgetItem(str(cellData))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum, cellNum, item)

        # Método setRowHeight: cambia la altura de una fila.
        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            6, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(7)

    def fetchUsuarios(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
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

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
            sql='''SELECT c.descripcion FROM clases c
            JOIN cats_clase cat ON c.id_cat=cat.id
            WHERE cat.descripcion='Usuario';'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql).fetchall()]
            clases = ParamEdit(sugerencias, rowData[2])
            clases.textChanged.connect(lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(
                rowNum, 2, clases)
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[3])))
            tabla.setItem(
                rowNum, 4, QtWidgets.QTableWidgetItem(str(rowData[4])))
            tabla.setItem(
                rowNum, 5, QtWidgets.QTableWidgetItem(str(rowData[5])))
            core.generarBotones(
                lambda: self.saveUsuarios(datos),
                lambda: self.deleteUsuarios(datos), tabla, rowNum)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(8)

    def saveUsuarios(self, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla alumnos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla alumnos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        tabla = self.pantallaUsuarios.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()
        iCampos = (1, 2, 3, 4, 5)

        for iCampo in iCampos:
            if iCampo == 2:
                texto=tabla.cellWidget(row, iCampo).text()
            else:
                texto=tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            nombre = tabla.item(row, 1).text()
            clase = tabla.cellWidget(row, 2).text()
            usuario = tabla.item(row, 4).text()
            contrasena = tabla.item(row, 5).text()

            idClase = bdd.cur.execute(
                "SELECT id FROM clases WHERE descripcion LIKE ? AND id_cat=3", (
                    clase,)
            ).fetchone()
            if not idClase:
                info = "La clase ingresada no está registrada o no está vinculada correctamente a la categoría usuario. Regístrela o revise los datos ya ingresados."
                return PopUp("Error", info).exec()
            # datosNuevos = [nombre, dni, clase, usuario]
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO personal VALUES(NULL, ?, ?, ?, ?, ?)",
                        (nombre, dni, idClase[0], usuario, contrasena)
                    )
                    # dal.insertarHistorial(
                        # self.usuario, 'Inserción', 'Alumnos', nombre, None, datosNuevos)
                else:
                    idd = int(tabla.item(row, 0).text())
                    bdd.cur.execute(
                        """UPDATE personal
                        SET nombre_apellido=?, id_clase=?, dni=?
                        WHERE id = ?""",
                        (nombre, idClase[0], dni, idd,)
                    )
                    # datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    # dal.insertarHistorial(
                    #     self.usuario, 'Edición', 'Alumnos', datosViejos[1], datosViejos[2:], datosNuevos)
            except sqlite3.IntegrityError:
                info = "El dni ingresado ya está registrado. Regístre uno nuevo o revise la información ya ingresada."
                return PopUp("Error", info).exec()

            bdd.con.commit()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchUsuarios()
            barra.setValue(posicion)

    def deleteUsuarios(self, datos: list | None = None) -> None:
        """Este método elimina una fila de una tabla de la base de
        datos

        Parámetros
        ----------
        idd: int | None = None
            El número que relaciona la fila de la tabla de la UI con la
            fila de la tabla de la base de datos.
            Default: None
        """
        tabla = self.pantallaUsuarios.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()
        barra = tabla.verticalScrollBar()

        idd = tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd = int(idd)

        hayRelacion = dal.verifElimUsuario(idd)
        if hayRelacion:
            mensaje = "El usuario tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este usuario."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el usuario?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # dal.insertarHistorial(self.usuario, "eliminación", "stock", row, datosEliminados)
            # # Eliminamos los datos
            dal.eliminarDatos('personal', idd)

        posicion = barra.value()
        self.fetchUsuarios()
        barra.setValue(posicion)

    def fetchClases(self):
        tabla = self.pantallaClases.tableWidget
        barraBusqueda = self.pantallaClases.lineEdit
        try:
            tabla.disconnect()
        except:
            pass


        tabla.setSortingEnabled(False)

        datos = dal.obtenerDatos("clases", barraBusqueda.text())

        tabla.setRowCount(0)
        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
            sugerencias=[i[0] for i in
                bdd.cur.execute('SELECT descripcion FROM cats_clase').fetchall()]
            cats = ParamEdit(sugerencias, rowData[2])
            cats.textChanged.connect(lambda: self.habilitarSaves(None, None, tabla))
            tabla.setCellWidget(rowNum, 2, cats)

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            core.generarBotones(
                lambda: self.saveClases(datos), lambda: self.deleteClases(datos), tabla, rowNum)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(10)

    def fetchUbicaciones(self):
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

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            core.generarBotones(
                lambda: self.saveUbicaciones(datos), lambda: self.deleteUbicaciones(datos), tabla, rowNum)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.setSortingEnabled(True)
        tabla.cellChanged.connect(self.habilitarSaves)

        self.stackedWidget.setCurrentIndex(12)

    def saveUbicaciones(self, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla subgrupos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla subgrupos, que se usarán para
                obtener el id de la fila en la tabla.
        """

        # Se pregunta al usuario si desea guardar los cambios en la
        # tabla. NOTA: Esos tabs en el string son para mantener la
        # misma identación en todas las líneas así dedent funciona,
        # sino le da ansiedad.
        # Obtenemos los ids de los campos que no podemos dejar vacíos.
        tabla = self.pantallaUbis.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()

        iCampos = (1,)
        # Por cada campo que no debe ser nulo...
        for iCampo in iCampos:
            # Si el campo está vacio...
            if tabla.item(row, iCampo).text() == "":
                # Le pide al usuario que termine de llenar los campos
                # y corta la función.
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            ubicacion = tabla.item(row, 1).text()
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO ubicaciones VALUES(NULL, ?)",
                        (ubicacion,)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Ubicaciones', ubicacion, None, None)
                else:
                    idd = int(tabla.item(row, 0).text())
                    bdd.cur.execute(
                        """UPDATE ubicaciones
                        SET descripcion=?
                        WHERE id = ?""",
                        (ubicacion, idd)
                    )
                    datosNuevos = [ubicacion,]
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    dal.insertarHistorial(
                        self.usuario, 'Edición', 'Ubicaciones', datosViejos[1], None, datosNuevos)
            except sqlite3.IntegrityError:
                info = "El subgrupo ingresado ya está registrado en ese grupo. Ingrese otro subgrupo, ingreselo en otro grupo o revise los datos ya ingresados."
                return PopUp("Error", info).exec()

            bdd.con.commit()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchUbicaciones()
            barra.setValue(posicion)

    def deleteUbicaciones(self, datos: list | None = None) -> None:
        tabla = self.pantallaUbis.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()
        barra = tabla.verticalScrollBar()

        idd=tabla.item(row, 0).text()
        if not idd:
            return tabla.removeRow(row)
        idd=int(idd)

        hayRelacion = dal.verifElimUbi(idd)
        if hayRelacion:
            mensaje = "La ubicacion está relacionada con registros en otras gestiones. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar esta ubicacion."
            return PopUp('Advertencia', mensaje).exec()
        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar la ubicacion?"
        popup = PopUp("Pregunta", mensaje).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            des = tabla.item(row, 1).text()
            dal.insertarHistorial(
                self.usuario, "Eliminación", "Ubicaciones", des, None)
            dal.eliminarDatos('ubicaciones', idd)
            posicion = barra.value()
            self.fetchUbicaciones()
            barra.setValue(posicion)

    def fetchReparaciones(self):
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

        desdeFecha.setMaximumDate(QtCore.QDate.fromString(
            date.today().strftime("%Y/%m/%d"), "yyyy/MM/dd"))
        hastaFecha.setMaximumDate(QtCore.QDate.fromString(
            (date.today()+relativedelta(years=1)).strftime("%Y/%m/%d"), "yyyy/MM/dd"))

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
                item = QtWidgets.QTableWidgetItem(str(cellData))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum, cellNum, item)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeMode.Stretch)

        desdeFecha.dateChanged.connect(self.fetchReparaciones)
        hastaFecha.dateChanged.connect(self.fetchReparaciones)

        self.stackedWidget.setCurrentIndex(11)

    def saveClases(self, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla subgrupos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla subgrupos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        tabla = self.pantallaClases.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()

        iCampos = (1, 2,)
        for iCampo in iCampos:
            if tabla.item(row, iCampo) is not None:
                texto=tabla.item(row, iCampo).text()
            else:
                texto=tabla.cellWidget(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()
        cat = tabla.cellWidget(row, 2).text()
        idCat = bdd.cur.execute(
            'SELECT id FROM cats_clase WHERE descripcion LIKE ?', (cat,)).fetchone()
        if not idCat:
            mensaje = "La categoría ingresada no está registrada. Ingresela e intente nuevamente."
            return PopUp("Error", mensaje).exec()
        
        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            clase = tabla.item(row, 1).text()
            datosNuevos = [clase, cat,]
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO clases VALUES(NULL, ?, ?)",
                        (clase, idCat[0],)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Clases', clase, None, datosNuevos[1:])
                else:
                    idd = int(tabla.item(row, 0).text())
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    if cat != datosViejos[2] and dal.verifElimClases(idd):
                        mensaje = "La clase que desea cambiar de categoría tiene personal relacionado. Por motivos de seguridad, debe eliminar primero el personal relacionado antes de modificar la categoría de la clase."
                        return PopUp("Advertencia", mensaje).exec()
                    bdd.cur.execute(
                        """UPDATE clases
                        SET descripcion=?,
                        id_cat=?
                        WHERE id = ?""",
                        (clase, idCat[0], idd)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Edición', 'Clases', datosViejos[1], datosViejos[2:], datosNuevos)
            except sqlite3.IntegrityError:
                info = "La clase ingresada ya está registrada. Ingrese otra o revise los datos ya ingresados."
                return PopUp("Error", info).exec()

            bdd.con.commit()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchClases()
            barra.setValue(posicion)

    def deleteClases(self, datos: list | None = None):
        tabla = self.pantallaClases.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()
        barra = tabla.verticalScrollBar()

        idd=tabla.item(row, 0).text()

        if not idd:
            return tabla.removeRow(row)
        idd=int(idd)

        hayRelacion = dal.verifElimClases(idd)
        if hayRelacion:
            mensaje = "La clase tiene relaciones. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar esta clase."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar la clase?"
        popup = PopUp("Pregunta", mensaje).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            datosEliminados = [fila for fila in datos if fila[0] == idd][0]
            dal.insertarHistorial(
                self.usuario, "Eliminación", "Clases", datosEliminados[1], datosEliminados[2:])
            dal.eliminarDatos('clases', idd)
            posicion = barra.value()
            self.fetchClases()
            barra.setValue(posicion)

    def fetchHistorial(self):
        """Este método obtiene los datos de la tabla historial y los
        inserta en la tabla de la interfaz de usuario.
        """
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

        desdeFecha.setMaximumDateTime(
            QtCore.QDateTime.fromString(
                datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "yyyy/MM/dd HH:mm:ss"))
        hastaFecha.setMaximumDateTime(
            QtCore.QDateTime.fromString(
                (datetime.now()+relativedelta(years=100)).strftime("%Y/%m/%d %H/%M/%S"), "yyyy/MM/dd HH:mm:ss"))

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
                        - Cantidad en reparacion: {datosInsertados[1]}
                        - Cantidad de baja: {datosInsertados[2]}
                        - Cantidad prestadas: {datosInsertados[3]}
                        - Grupo: {datosInsertados[4]}
                        - Subgrupo: {datosInsertados[5]}
                        - Ubicación: {datosInsertados[6]}"""
                    elif rawRow[3] == 'Edición':
                        datosViejos = rawRow[5].split(';')
                        datosNuevos = rawRow[6].split(';')
                        desc = f"""                Se editó la herramienta {rawRow[4]}, y se reemplazaron los siguientes datos:
                        - Descripción: {rawRow[4]}, por {datosNuevos[0]}
                        - Cantidad en condiciones: {datosViejos[0]}, por {datosNuevos[1]}
                        - Cantidad en reparacion: {datosViejos[1]}, por {datosNuevos[2]}
                        - Cantidad de baja: {datosViejos[2]}, por {datosNuevos[3]}
                        - Cantidad prestadas: {datosViejos[3]}, por {datosNuevos[4]}
                        - Grupo: {datosViejos[4]}, por {datosNuevos[5]}
                        - Subgrupo: {datosViejos[5]}, por {datosNuevos[6]}
                        - Ubicación: {datosViejos[6]}, por {datosNuevos[7]}"""
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
                item = QtWidgets.QTableWidgetItem(str(cellData))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(rowNum, cellNum, item)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.resizeRowsToContents()

        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeMode.Stretch)

        listaGestion.currentIndexChanged.connect(self.fetchHistorial)
        desdeFecha.dateTimeChanged.connect(self.fetchHistorial)
        hastaFecha.dateTimeChanged.connect(self.fetchHistorial)

        self.stackedWidget.setCurrentIndex(9)

    def fetchDeudas(self):
        """Este método obtiene los datos de la tabla deudas y los
        inserta en la tabla de la interfaz de usuario.
        """
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

        datos = dal.obtenerDatos("deudas", barraBusqueda.text(), filtros)

        tabla.setRowCount(0)
        grupo = ''
        contGrupo = 1
        cant = 0
        if radioHerramienta.isChecked():
            colData = 0
        else:
            colData = 2
        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            cant += rowData[1]

            if rowData[colData] == grupo:
                contGrupo += 1
            else:
                # Está bien que printee lo de QTableView, no es un error
                tabla.setSpan(rowNum+1-contGrupo, 0, contGrupo, 1)
                tabla.setSpan(rowNum+1-contGrupo, 1, contGrupo, 1)
                tabla.setItem(rowNum+1-contGrupo, 0,
                              QtWidgets.QTableWidgetItem(rowData[colData]))
                tabla.setItem(rowNum+1-contGrupo, 1,
                              QtWidgets.QTableWidgetItem(str(cant)))
                contGrupo = 0
                cant = 0

            if not colData:
                tabla.setItem(
                    rowNum, 2, QtWidgets.QTableWidgetItem(rowData[2]))
            else:
                tabla.setItem(
                    rowNum, 2, QtWidgets.QTableWidgetItem(rowData[0]))

            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 4, QtWidgets.QTableWidgetItem(str(rowData[3])))
            tabla.setItem(
                rowNum, 5, QtWidgets.QTableWidgetItem(str(rowData[4])))
            tabla.setItem(
                rowNum, 6, QtWidgets.QTableWidgetItem(str(rowData[5])))
            tabla.setItem(
                rowNum, 7, QtWidgets.QTableWidgetItem(str(rowData[6])))

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        for i in range(tabla.rowCount()):
            for j in range(tabla.columnCount()):
                item = QtWidgets.QTableWidgetItem(tabla.item(i, j).text())
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
                tabla.setItem(i, j, item)

        listaPanolero.currentIndexChanged.connect(self.fetchDeudas)

        self.stackedWidget.setCurrentIndex(14)

    def fetchResumen(self):
        """Este método obtiene datos para insertar en la tabla de la
        interfaz de usuario.
        """
        hastaFecha = self.pantallaResumen.hastaFecha
        tablaDeudas = self.pantallaResumen.tablaDeudas
        tablaBaja = self.pantallaResumen.tablaBaja
        labelDeudas = self.pantallaResumen.labelDeudas
        labelBaja = self.pantallaResumen.labelBaja

        try:
            hastaFecha.disconnect()
        except:
            pass

        hastaFecha.setMaximumDate(QtCore.QDate.fromString(
            (date.today()+relativedelta(years=1)).strftime("%Y/%m/%d"), "yyyy/MM/dd"))

        rawData = dal.obtenerDatos("resumen_deudas")
        datos = []
        for rawRow in rawData:
            fecha = QtCore.QDate.fromString(rawRow[7][:10], 'yyyy/MM/dd')
            if fecha == hastaFecha.date():
                datos.append(rawRow)

        if datos:
            labelDeudas.setText('Han quedado herramientas adeudadas:')
            tablaDeudas.setRowCount(0)

            for rowNum, rowData in enumerate(datos):
                tablaDeudas.insertRow(rowNum)
                for cellNum, cellData in enumerate(rowData):
                    item = QtWidgets.QTableWidgetItem(str(cellData))
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                                  QtCore.Qt.ItemFlag.ItemIsEnabled)
                    tablaDeudas.setItem(
                        rowNum, cellNum, QtWidgets.QTableWidgetItem(str(cellData)))

            tablaDeudas.setRowHeight(0, 35)
            tablaDeudas.resizeColumnsToContents()
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                0, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                4, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                5, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.show()
        else:
            labelDeudas.setText('No han quedado herramientas adeudadas.')
            tablaDeudas.hide()

        rawData = dal.obtenerDatos("resumen_baja")
        datos = []
        for rawRow in rawData:
            fecha = QtCore.QDate.fromString(rawRow[8], 'yyyy/MM/dd')
            if fecha == hastaFecha.date():
                datos.append(rawRow)

        if datos:
            for rowNum, rowData in enumerate(datos):
                tablaBaja.insertRow(rowNum)
                for cellNum, cellData in enumerate(rowData):
                    item = QtWidgets.QTableWidgetItem(str(cellData))
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                                  QtCore.Qt.ItemFlag.ItemIsEnabled)
                    tablaBaja.setItem(
                        rowNum, cellNum, QtWidgets.QTableWidgetItem(str(cellData)))

            tablaBaja.setRowHeight(0, 35)
            tablaBaja.resizeColumnsToContents()
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                0, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                2, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                5, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaDeudas.horizontalHeader().setSectionResizeMode(
                6, QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablaBaja.show()
        else:
            labelBaja.setText(
                'No se han devuelto herramientas en estado de baja.')
            tablaBaja.hide()

        hastaFecha.dateChanged.connect(self.fetchResumen)
        self.stackedWidget.setCurrentIndex(15)

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(open(os.path.join(os.path.abspath(os.getcwd()), f'ui{os.sep}styles.qss'), 'r').read())
for fuente in os.listdir(os.path.join(os.path.abspath(os.getcwd()), f'ui{os.sep}rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
                     f'ui{os.sep}rsc{os.sep}fonts{os.sep}{fuente}')
    )

window = MainWindow()
app.exec()