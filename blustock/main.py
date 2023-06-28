"""El archivo principal. Genera la ventana principal y ejecuta la 
aplicación.

Clases:
    MainWindow(qtw.QMainWindow): crea la ventana principal.

Objetos:
    app: La aplicación principal.
"""
import os
os.chdir(f"{os.path.abspath(__file__)}{os.sep}..")
import sys
import types
import sqlite3
import pandas as pd
import datetime as time
from textwrap import dedent
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from db.bdd import bdd
from dal.dal import dal
from ui.presets.popup import PopUp
from ui.presets.boton import BotonFila
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

            Crea la ventana principal con una cabecera, un menú
            izquierdo (inicialmente escondido) y una colección de
            pantallas.
    """

    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}main.ui'), self)
        boton = toolboton("usuario", self)
        boton.setIconSize(QtCore.QSize(60, 40))
        self.menubar.setCornerWidget(boton)
        self.menubar.hide()

        self.pantallaAlumnos = QtWidgets.QWidget()
        uic.loadUi(
            os.path.join(
                os.path.abspath(os.getcwd()),
                f'ui{os.sep}screens_uis{os.sep}alumnos.ui'
            ), self.pantallaAlumnos)

        self.pantallaGrupos = QtWidgets.QWidget()

        pathGrupos = os.path.join(os.path.abspath(os.getcwd()),
                                  f'ui{os.sep}screens_uis{os.sep}grupos.ui')

        uic.loadUi(pathGrupos, self.pantallaGrupos)

        self.pantallaStock = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd(
        )), f'ui{os.sep}screens_uis{os.sep}stock.ui'), self.pantallaStock)
        self.pantallaHistorial = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd(
        )), f'ui{os.sep}screens_uis{os.sep}historial.ui'), self.pantallaHistorial)
        self.pantallaMovimientos = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd(
        )), f'ui{os.sep}screens_uis{os.sep}movimientos.ui'), self.pantallaMovimientos)
        self.pantallaOtroPersonal = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd(
        )), f'ui{os.sep}screens_uis{os.sep}otro_personal.ui'), self.pantallaOtroPersonal)
        self.pantallaSubgrupos = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd(
        )), f'ui{os.sep}screens_uis{os.sep}subgrupos.ui'), self.pantallaSubgrupos)
        self.pantallaTurnos = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}turnos.ui'), self.pantallaTurnos)
        self.pantallaUsuarios = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(
            os.getcwd()), f'ui{os.sep}screens_uis{os.sep}usuarios.ui'), self.pantallaUsuarios)
        self.pantallaLogin = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}login.ui'), self.pantallaLogin)
        self.pantallaClases = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}clases.ui'), self.pantallaClases)
        self.pantallaReparaciones = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}reparaciones.ui'), self.pantallaReparaciones)
        self.pantallaUbicaciones = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}ubicaciones.ui'), self.pantallaUbicaciones)
        self.pantallaNmovimiento = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}n-movimiento.ui'), self.pantallaNmovimiento)
        self.pantallaDeudas = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}deudas.ui'), self.pantallaDeudas)
        self.pantallaResumen = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}resumen.ui'), self.pantallaResumen)

        self.pantallaLogin.Ingresar.clicked.connect(self.login)

        pantallas = (self.pantallaLogin, self.pantallaAlumnos,
                     self.pantallaGrupos, self.pantallaStock,
                     self.pantallaMovimientos, self.pantallaOtroPersonal,
                     self.pantallaSubgrupos, self.pantallaTurnos,
                     self.pantallaUsuarios, self.pantallaHistorial,
                     self.pantallaClases, self.pantallaReparaciones,
                     self.pantallaUbicaciones, self.pantallaNmovimiento,
                     self.pantallaDeudas, self.pantallaResumen)

        for pantalla in pantallas:
            self.stackedWidget.addWidget(pantalla)
            try:
                path = f'ui{os.sep}rsc{os.sep}icons{os.sep}buscar.png'
                pixmap = QtGui.QPixmap(path)
                pantalla.label_2.setPixmap(pixmap)
                pantalla.tableWidget.horizontalHeader().setFont(QtGui.QFont("Oswald", 11))
            except:
                pass

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

        with open(os.path.join(os.path.abspath(os.getcwd()), f'ui{os.sep}styles.qss'), 'r') as file:
            self.setStyleSheet(file.read())

        self.pantallaLogin.passwordState.hide()
        self.pantallaLogin.usuarioState.hide()

        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
        pixmap = QtGui.QPixmap(path)
        self.pantallaLogin.showPass.setIcon(QtGui.QIcon(QtGui.QIcon(pixmap)))
        self.pantallaLogin.showPass.setIconSize(QtCore.QSize(25, 25))
        self.pantallaLogin.showPass.clicked.connect(
            lambda: self.mostrarContrasena(
                self.pantallaLogin.showPass, self.pantallaLogin.passwordLineEdit
            )
        )

        self.pantallaStock.pushButton_2.clicked.connect(
            lambda: self.insertarFilas(self.pantallaStock.tableWidget,
                                       self.saveStock, self.deleteStock,
                                       (0, 1, 6, 7, 8), (4, 5,)))
        self.pantallaOtroPersonal.pushButton_2.clicked.connect(
            lambda: self.insertarFilas(
                self.pantallaOtroPersonal.tableWidget, self.saveOtroPersonal,
                self.deleteOtroPersonal, (0, 1, 2)
            )
        )
        self.pantallaSubgrupos.pushButton_2.clicked.connect(
            lambda: self.insertarFilas(self.pantallaSubgrupos.tableWidget,
                                       self.saveSubgrupos,
                                       self.deleteSubgrupos, (0, 1)))
        self.pantallaGrupos.pushButton_2.clicked.connect(
            lambda: self.insertarFilas(self.pantallaGrupos.tableWidget,
                                       self.saveGrupos,
                                       self.deleteGrupos, (0,)))
        self.pantallaAlumnos.pushButton_2.clicked.connect(
            lambda: self.insertarFilas(self.pantallaAlumnos.tableWidget,
                                       self.saveAlumnos,
                                       self.deleteAlumnos, (0, 1, 2)))
        self.pantallaUbicaciones.pushButton_2.clicked.connect(
            lambda: self.insertarFilas(self.pantallaUbicaciones.tableWidget,
                                       self.saveUbicaciones,
                                       self.deleteUbicaciones, (0,)))
        self.pantallaClases.pushButton_2.clicked.connect(
            lambda: self.insertarFilas(self.pantallaClases.tableWidget,
                                       self.saveClases,
                                       self.deleteClases, (0, 1,)))

        self.pantallaStock.tableWidget.cellChanged.connect(
            self.actualizarTotal)
        self.pantallaStock.lineEdit.editingFinished.connect(self.fetchStock)
        self.pantallaStock.botonImprimir.clicked.connect(self.printStock)

        self.pantallaAlumnos.lineEdit.editingFinished.connect(
            self.fetchAlumnos)
        self.pantallaClases.lineEdit.editingFinished.connect(self.fetchClases)
        self.pantallaGrupos.lineEdit.editingFinished.connect(self.fetchGrupos)

        self.pantallaMovimientos.lineEdit.editingFinished.connect(
            self.fetchMovimientos)
        self.pantallaMovimientos.nId.valueChanged.connect(
            self.fetchMovimientos)
        self.pantallaMovimientos.nTurno.valueChanged.connect(
            self.fetchMovimientos)

        self.pantallaOtroPersonal.lineEdit.editingFinished.connect(
            self.fetchOtroPersonal)

        self.pantallaReparaciones.lineEdit.editingFinished.connect(
            self.fetchReparaciones)

        self.pantallaTurnos.lineEdit.editingFinished.connect(self.fetchTurnos)
        self.pantallaTurnos.nId.valueChanged.connect(self.fetchTurnos)

        self.pantallaSubgrupos.lineEdit.editingFinished.connect(
            self.fetchSubgrupos)
        self.pantallaUbicaciones.lineEdit.editingFinished.connect(
            self.fetchUbicaciones)
        self.pantallaClases.lineEdit.editingFinished.connect(self.fetchClases)

        self.pantallaHistorial.lineEdit.editingFinished.connect(
            self.fetchHistorial)

        self.pantallaDeudas.lineEdit.editingFinished.connect(self.fetchDeudas)
        self.pantallaDeudas.radioHerramienta.toggled.connect(self.fetchDeudas)
        self.pantallaDeudas.radioPersona.toggled.connect(self.fetchDeudas)
        self.pantallaDeudas.nMov.valueChanged.connect(self.fetchDeudas)
        self.pantallaDeudas.nTurno.valueChanged.connect(self.fetchDeudas)

        self.pantallaReparaciones.hastaFecha.setDate(
            # Esta función también recibe dos parametros asi que estén
            # atentos, solo que el primero es un string que viene de
            # la librería dt, esta explicado mas adelante, pero el
            # segundo string es igual al segundo que usamos en el
            # primer entry de fecha.
            QtCore.QDate.fromString(
                # Clase datetime: construye un objeto datetime de
                # python, que no es un QDateTime de qt.
                # Método now: obtiene la fecha y hora actuales.
                # Método strftime: transforma una fecha de python en un
                # string. Cada porcentaje y letra simboliza un tipo de
                # dato. A diferencia del segundo string, este no
                # necesita una letra por cada dígito sino que entiende
                # que cada conjunto de digitos es un tipo de dato.
                # %d son los dos digitos de dia, %m son los dos de mes,
                # %Y son los cuatro de año, %H son los dos de hora, %M
                # son los dos de minuto y %S los dos de segundo.
                # Fijense que, fuera de las letras, las barras y los :
                # estan en los mismos lugares que en el segundo string.
                date.today().strftime("%Y/%m/%d"), "yyyy/MM/dd"))
        self.pantallaTurnos.hastaFecha.setDate(QtCore.QDate.fromString(
            date.today().strftime("%Y/%m/%d"), "yyyy/MM/dd"))
        self.pantallaMovimientos.hastaFecha.setDateTime(QtCore.QDateTime.fromString(
            datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "yyyy/MM/dd HH:mm:ss"))
        self.pantallaResumen.hastaFecha.setDate(QtCore.QDate.fromString(
            date.today().strftime("%Y/%m/%d"), "yyyy/MM/dd"))

        self.stackedWidget.setCurrentIndex(0)
        self.show()

    def login(self):
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
                self.menubar.show()

            else:
                self.pantallaLogin.passwordState.show()
                self.pantallaLogin.usuarioState.hide()
        else:
            self.pantallaLogin.usuarioState.show()
            self.pantallaLogin.passwordState.hide()

    def mostrarContrasena(self, boton, entry: QtWidgets.QLineEdit):
        """Este método muestra o esconde lo ingresado en el campo de
        contraseña vinculado dependiendo del estado de activación del 
        botón.

        Parámetros
        ----------
            entry : QtWidgets.QLineEdit
                El entry de contraseña vinculado al botón.
        """
        # Si el botón está presionado
        if boton.isChecked():
            # Muestra lo ingresado en el campo.
            entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            # Cambia el ícono.
            path = f'ui{os.sep}rsc{os.sep}icons{os.sep}esconder.png'
            pixmap = QtGui.QPixmap(path)
        else:
            # Cifra lo ingresado en el campo.
            entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            path = f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
            pixmap = QtGui.QPixmap(path)
        boton.setIcon(QtGui.QIcon(pixmap))
        boton.setIconSize(QtCore.QSize(25, 25))

    def generarBotones(self, funcGuardar: types.FunctionType, funcEliminar: types.FunctionType,
                       tabla: QtWidgets.QTableWidget, numFila: int):
        """Este método genera botones para guardar cambios y eliminar
        filas y los inserta en una fila de una tabla de la UI

        Parámetros
        ----------
            funcGuardar: types.FunctionType
                La función que estará vinculada al botón guardar.
            funcEliminar: types.FunctionType
                La función que estará vinculada al botón eliminar.
            tabla: QtWidgets.QTableWidget
                La tabla a la que se le añadirán los botones.
            numFila: int
                La fila en la que se insertarán los botones.
        """
        # Se crean dos botones: uno de editar y uno de eliminar
        # Para saber que hacen BotonFila, vayan al código de la
        # clase.
        guardar = BotonFila("guardar")
        # Conectamos el botón a su función guardar correspondiente.
        guardar.clicked.connect(funcGuardar)
        borrar = BotonFila("eliminar")
        borrar.clicked.connect(funcEliminar)

        # Se añaden los botones a cada fila.
        # Método setCellWidget(row, column, widget): añade un
        # widget a la celda de una tabla.

        tabla.setCellWidget(numFila, tabla.columnCount() - 2, guardar)
        tabla.setCellWidget(numFila, tabla.columnCount() - 1, borrar)

    def sopas(self):
        self.pantallaNmovimiento.alumnoComboBox.clear()
        for i in dal.obtenerDatos("alumnos", self.pantallaNmovimiento.cursoComboBox.currentText(),):
            print(i)
            self.pantallaNmovimiento.alumnoComboBox.addItem(i[1])

    def realizarMovimiento(self):
        for i in dal.obtenerDatos("tipos_mov", ""):
            self.pantallaNmovimiento.tipoDeMovimientoComboBox.addItem(i[1])

        for i in dal.obtenerDatos("stock", ""):
            self.pantallaNmovimiento.herramientaComboBox.addItem(i[1])

        for i in dal.obtenerDatos("estados", ""):
            self.pantallaNmovimiento.estadoComboBox.addItem(i[1])

        for i in dal.obtenerDatos("clases", ""):
            self.pantallaNmovimiento.cursoComboBox.addItem(i[1])

        self.pantallaNmovimiento.cursoComboBox.currentTextChanged.connect(
            self.sopas)
        self.pantallaNmovimiento.pushButton.clicked.connect(
            self.saveMovimiento)

        self.stackedWidget.setCurrentIndex(13)

    def saveMovimiento(self):
        turno = bdd.cur.execute(
            "select id from turnos where fecha_egr IS NULL").fetchall()
        tipo = dal.obtenerDatos(
            "tipos_mov", self.pantallaNmovimiento.tipoDeMovimientoComboBox.currentText())
        herramienta = dal.obtenerDatos(
            "stock", self.pantallaNmovimiento.herramientaComboBox.currentText())
        cant = self.pantallaNmovimiento.cantidadSpinBox.value()
        estado = dal.obtenerDatos(
            "estados", self.pantallaNmovimiento.estadoComboBox.currentText())
        persona = dal.obtenerDatos(
            "personas", self.pantallaNmovimiento.alumnoComboBox.currentText())
        descripcion = self.pantallaNmovimiento.descripcionLineEdit.text()
        fecha = time.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if cant == 0:
            mensaje = """       Por favor ingrese un valor 
            mayor a 0."""
            return PopUp("Error", mensaje).exec()
        else:
            bdd.cur.execute("INSERT INTO movimientos(id_turno,id_elem,id_estado,cant,id_persona,fecha_hora,id_tipo,descripcion) VALUES(?, ?, ?, ?, ?, ?, ?,?)",
                            (turno[0][0], herramienta[0][0], estado[0][0], cant, persona[0][0], fecha, tipo[0][0], descripcion))
            bdd.con.commit()
            mensaje = """       Movimiento cargado con exito."""
            return PopUp("Aviso", mensaje).exec()

    def insertarFilas(self, tabla: QtWidgets.QTableWidget,
                      funcGuardar: types.FunctionType,
                      funcEliminar: types.FunctionType,
                      camposObligatorios: tuple | None = None,
                      camposNoEditables: tuple | None = None):
        """Este método inserta una nueva fila en la tabla stock.

        Si la fila anterior fue recientemente ingresada y los datos no
        fueron modificados, en vez de añadir una nueva fila se le
        muestra un mensaje al usuario pidiéndole que ingrese los datos
        primero.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla a la que se le van a insertar los elementos.
            camposObligatorios: tuple
                Los campos de la fil anterior que se van a verificar
                para que no estén en blanco, evitando así que se puedan
                insertar múltiples filas en blanco.
            funcGuardar: types.FunctionType
                La función guardar que el botón guardar de la fila
                ejecutará.
            funcEliminar: types.FunctionType
                La función eliminar que el botón eliminar de la fila
                ejecutará.
        """
        try:
            tabla.disconnect()
        except:
            pass
        # Las filas en la tabla se ingresan escribiendo el índice en
        # el que queremos que se ingresen. Para ingresar la fila al
        # final, tenemos que saber el índice del final. Para obtenerlo,
        # contamos la cantidad de filas: por ejemplo, si queremos
        # agregar una fila al final y la tabla tiene 5 filas, si las
        # contamos vamos a obtener el número 5; si usamos ese número
        # como índice para agregar la fila, la fila se va a agregar al
        # final.
        indiceFinal = tabla.rowCount()

        # Antes de agregar la fila, queremos comprobar que la última
        # fila de la tabla no tenga campos vacíos. Esto lo hacemos
        # para que el usuario no pueda ingresar múltiples filas vacías
        # haciendo que el sistema detecte si la fila anterior está
        # vacía.
        ultimaFila = indiceFinal-1
        if ultimaFila >= 0:
            # Por cada campo que no debe ser nulo...
            for iCampo in camposObligatorios:
                # Si el campo está vacio...
                if tabla.item(ultimaFila, iCampo) is not None:
                    texto=tabla.item(ultimaFila, iCampo).text()
                else:
                    texto=tabla.cellWidget(ultimaFila, iCampo).text()
                if texto == "":
                    # Le pide al usuario que termine de llenar los campos
                    # y corta la función.
                    mensaje = "Ha agregado una fila y todavía no ha ingresado los datos de la fila anterior. Ingreselos, guardelos cambios e intente nuevamente."
                    return PopUp("Error", mensaje).exec()

        # Se añade la fila al final.
        tabla.insertRow(indiceFinal)
        tabla.scrollToItem(tabla.item(indiceFinal-1, 0),
                           QtWidgets.QAbstractItemView.ScrollHint.PositionAtBottom)
        # Se añaden campos de texto en todas las celdas ya que por
        # defecto no vienen.
        for numCol in range(tabla.columnCount() - 2):
            if camposNoEditables:
                if numCol not in camposNoEditables:
                    tabla.setItem(indiceFinal, numCol,
                                  QtWidgets.QTableWidgetItem(""))
                else:
                    campoNoEditable = QtWidgets.QTableWidgetItem("")
                    campoNoEditable.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                    tabla.setItem(indiceFinal, numCol, campoNoEditable)
            else:
                tabla.setItem(indiceFinal, numCol,
                              QtWidgets.QTableWidgetItem(""))
        self.generarBotones(
            funcGuardar, funcEliminar, tabla, indiceFinal)

    def actualizarTotal(self, row, col):
        tabla = self.pantallaStock.tableWidget
        if col in (1, 2, 3):
            tabla = self.pantallaStock.tableWidget
            cantCond = int(tabla.item(row, 1).text())
            cantRep = tabla.item(row, 2).text()
            cantBaja = tabla.item(row, 3).text()
            cantPrest = tabla.item(row, 4).text()
            if cantRep.isnumeric() and cantBaja.isnumeric() and cantPrest.isnumeric():
                total = QtWidgets.QTableWidgetItem(
                    str(cantCond + int(cantRep) + int(cantBaja) + int(cantPrest)))
            else:
                total = QtWidgets.QTableWidgetItem(str(cantCond))
            total.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            tabla.setItem(row, 5, total)

    def actualizarSugerenciasSubgrupos(self):
        tabla=self.pantallaStock.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        grupo=tabla.cellWidget(row, 6).text()
        completer=tabla.cellWidget(row, 7).completer()
        sugerencias=[i[0] for i in 
                     bdd.cur.execute('''SELECT s.descripcion FROM subgrupos s
                     JOIN grupos g ON s.id_grupo = g.id
                     WHERE g.descripcion LIKE ?''', (grupo,)).fetchall()]
        completer.setModel(QtCore.QStringListModel(sugerencias))
    
    def fetchStock(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        # Se guardan la tabla y la barra de búsqueda de la pantalla
        # stock en variables para que el código se simplifique y se
        # haga más legible.
        tabla = self.pantallaStock.tableWidget
        try:
            tabla.disconnect()
        except:
            pass
        barraBusqueda = self.pantallaStock.lineEdit
        listaUbi = self.pantallaStock.listaUbi
        listaUbi.disconnect()
        ubiSeleccionada = listaUbi.currentText()
        ubis = bdd.cur.execute("""SELECT DISTINCT u.descripcion
                                FROM stock s
                                JOIN ubicaciones u
                                ON u.id=s.id_ubi""").fetchall()
        listaUbi.clear()
        listaUbi.addItem("Todas")
        for ubi in ubis:
            listaUbi.addItem(ubi[0])
        listaUbi.setCurrentIndex(listaUbi.findText(ubiSeleccionada))

        if ubiSeleccionada == "Todas":
            filtroUbi = (None,)
        else:
            filtroUbi = (ubiSeleccionada,)

        # Se obtienen los datos de la base de datos pasando como
        # parámetro la tabla de la que queremos obtener los daots y
        # el texto de la barra de búsqueda mediante el cual queremos
        # filtrarlos.
        datos = dal.obtenerDatos("stock", barraBusqueda.text(), filtroUbi)

        # Se refresca la tabla, eliminando todas las filas anteriores.
        tabla.setRowCount(0)

        # Bucle: por cada fila de los datos obtenidos de la tabla de la
        # base de datos, se obtiene el número de fila y los contenidos
        # de ésta.
        # Método enumerate: devuelve una lista con el número y el
        # elemento.
        for rowNum, rowData in enumerate(datos):
            # Se añade una fila a la tabla.
            # Método insertRow(int): inserta una fila en una QTable.
            tabla.insertRow(rowNum)

            # Inserta el texto en cada celda. Las celdas por defecto no
            # tienen nada, por lo que hay que añadir primero un item
            # que contenga el texto. No se puede establecer texto asi
            # nomás, tira error.
            # Método setItem(row, column, item): establece el item de
            # una celda de una tabla.
            # QTableWidgetItem: un item de pantalla.tableWidget. Se puede crear con
            # texto por defecto.
            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[2])))
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[3])))
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[4])))
            cantPrest = QtWidgets.QTableWidgetItem(str(rowData[5]))
            cantPrest.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                               QtCore.Qt.ItemFlag.ItemIsEnabled)
            tabla.setItem(
                rowNum, 4, cantPrest)

            if rowData[3] not in ("-", ""):
                total = QtWidgets.QTableWidgetItem(
                    str(rowData[2] + rowData[3] + rowData[4] + rowData[5]))
            else:
                total = QtWidgets.QTableWidgetItem(str(rowData[2]))
            total.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                           QtCore.Qt.ItemFlag.ItemIsEnabled)

            tabla.setItem(rowNum, 5, total)

            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute('SELECT descripcion FROM grupos').fetchall()]
            paramGrupos=ParamEdit(sugerencias, rowData[6])
            paramGrupos.editingFinished.connect(self.actualizarSugerenciasSubgrupos)
            tabla.setCellWidget(rowNum, 6, paramGrupos)
            sql = '''SELECT s.descripcion FROM subgrupos s
                   JOIN grupos g ON s.id_grupo = g.id
                   WHERE g.descripcion LIKE ?'''
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute(sql, (rowData[6],)).fetchall()]
            tabla.setCellWidget(rowNum, 7, ParamEdit(sugerencias, rowData[7]))
            sugerencias = [sugerencia[0] for sugerencia in
                           bdd.cur.execute('SELECT descripcion FROM ubicaciones').fetchall()]
            tabla.setCellWidget(rowNum, 8, ParamEdit(sugerencias, rowData[8]))

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Se generan e insertan los botones en la fila, pasando
            # como parámetros las funciones que queremos que los
            # botones tengan y la tabla y la fila de la tabla en la que
            # queremos que se inserten.
            self.generarBotones(
                lambda: self.saveStock(datos), lambda: self.deleteStock(datos), tabla, rowNum)

        # Método setRowHeight: cambia la altura de una fila.
        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        # Método setSectionResizeMode(column, ResizeMode): hace que una
        # columna de una tabla se expanda o no automáticamente conforme
        # se extiende la tabla.
        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            6, QtWidgets.QHeaderView.ResizeMode.Stretch)

        tabla.cellChanged.connect(self.actualizarTotal)
        listaUbi.currentIndexChanged.connect(self.fetchStock)
        self.stackedWidget.setCurrentIndex(3)

    def saveStock(self, datos: list | None = None):
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
        tabla = self.pantallaStock.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()
        iCampos = (0, 1, 6, 7, 8)
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
            cond = int(tabla.item(row, 1).text())
            rep = tabla.item(row, 2).text()
            baja = tabla.item(row, 3).text()
            prest = tabla.item(row, 4).text()
            if rep not in ("-", "") or baja not in ("-", ""):
                rep = int(rep)
                baja = int(baja)
                try:
                    prest = int(prest)
                except:
                    prest = 0
            else:
                rep = None
                baja = None
                prest = None
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingrese los datos correctamente."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:

            # Se obtiene el texto de todas las celdas.
            desc = tabla.item(row, 0).text()
            grupo = tabla.cellWidget(row, 6).text()
            subgrupo = tabla.cellWidget(row, 7).text()
            ubi = tabla.cellWidget(row, 8).text()

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

            datosNuevos = [cond, rep, baja, prest, grupo, subgrupo, ubi]
            try:
                if not datos:
                    idd = None
                    bdd.cur.execute(
                        "INSERT INTO stock VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)",
                        (desc, cond, rep, baja, prest,
                         idSubgrupo[0], idUbi[0],)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Stock', desc, None, datosNuevos)
                else:
                    idd = datos[row][0]
                    # Guardamos los datos de la fila en
                    bdd.cur.execute(
                        """UPDATE stock
                        SET descripcion = ?, cant_condiciones = ?, cant_reparacion=?,
                        cant_baja = ?, cant_prest=?, id_subgrupo = ?, id_ubi=?
                        WHERE id = ?""",
                        (desc, cond, rep, baja, prest,
                         idSubgrupo[0], idUbi[0], idd,)
                    )
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    dal.insertarHistorial(
                        self.usuario, 'Edición', 'Stock', datosViejos[1], datosViejos[2:], datosNuevos)
            except sqlite3.IntegrityError:
                info = "La herramienta que desea ingresar ya está ingresada. Ingrese otra información o revise la información ya ingresada"
                return PopUp("Error", info).exec()

            bdd.con.commit()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchStock()
            barra.setValue(posicion)

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

        if not datos:
            idd = None
        else:
            if row == len(datos):
                idd = None
            else:
                idd = datos[row][0]
        # Si no se pasó el argumento idd, significa que la fila no está
        # relacionada con la base de datos. Eso significa que la fila
        # se insertó en la tabla de la UI, pero aún no se guardaron los
        # cambios en la base de datos. En ese caso...
        if not idd:
            # ...solo debemos sacarla de la UI.
            return tabla.removeRow(row)
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

    def fetchAlumnos(self):
        """Este método obtiene los datos de la tabla personal y los
        inserta en la tabla de la interfaz de usuario.
        """

        tabla = self.pantallaAlumnos.tableWidget
        barraBusqueda = self.pantallaAlumnos.lineEdit

        datos = dal.obtenerDatos("alumnos", barraBusqueda.text())

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[2])))
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[3])))

            self.generarBotones(
                lambda: self.saveAlumnos(datos), lambda: self.deleteAlumnos(datos), tabla, rowNum)

            self.pantallaAlumnos.tableWidget.setRowHeight(0, 35)

        # Método setRowHeight: cambia la altura de una fila.
        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        # Esto lo hacían ustedes creo
        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)

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
        iCampos = (0, 1, 2)

        for iCampo in iCampos:
            if tabla.item(row, iCampo).text() == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 2).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**10:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            nombre = tabla.item(row, 0).text()
            clase = tabla.item(row, 1).text().capitalize()

            idClase = bdd.cur.execute(
                "SELECT id FROM clases WHERE descripcion = ? AND id_cat=1", (
                    clase,)
            ).fetchone()
            if not idClase:
                info = "El curso ingresado no está registrado o no está vinculado correctamente a la categoría alumno. Regístrelo o revise los datos ya ingresados."
                return PopUp("Error", info).exec()
            datosNuevos = [nombre, dni, clase]
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                        (nombre, dni, idClase[0],)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Alumnos', nombre, None, datosNuevos)
                else:
                    idd = datos[row][0]
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

        if not datos:
            idd = None
        else:
            if row == len(datos):
                idd = None
            else:
                idd = datos[row][0]

        if not idd:
            return tabla.removeRow(row)

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
        tabla = self.pantallaMovimientos.tableWidget
        barraBusqueda = self.pantallaMovimientos.lineEdit
        nId = self.pantallaMovimientos.nId
        listaElem = self.pantallaMovimientos.listaElem
        listaPersona = self.pantallaMovimientos.listaPersona
        desdeFecha = self.pantallaMovimientos.desdeFecha
        hastaFecha = self.pantallaMovimientos.hastaFecha
        nTurno = self.pantallaMovimientos.nTurno
        listaPanolero = self.pantallaMovimientos.listaPanolero

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

        datos = dal.obtenerDatos("grupos", barraBusqueda.text())
        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):

            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))

            self.generarBotones(
                lambda: self.saveGrupos(datos), lambda: self.deleteGrupos(datos), tabla, rowNum)
            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)

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

        if tabla.item(row, 0).text() == "":
            mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            grupo = tabla.item(row, 0).text()
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO grupos VALUES(NULL, ?)", (grupo,))
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Grupos', grupo, None, None)
                else:
                    idd = datos[row][0]
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

        if not datos:
            idd = None
        else:
            if row == len(datos):
                idd = None
            else:
                idd = datos[row][0]

        if not idd:
            return tabla.removeRow(row)

        hayRelacion = dal.verifElimGrupos(idd)
        if hayRelacion:
            mensaje = "El grupo tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este grupo."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el grupo?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            grupo = tabla.item(row, 0).text()
            dal.insertarHistorial(
                self.usuario, 'Eliminación', 'Grupos', grupo, None)
            dal.eliminarDatos('grupos', idd)
            posicion = barra.value()
            self.fetchGrupos()
            barra.setValue(posicion)

# --------------- lo que modifique está abajo --------------------------#
    def fetchOtroPersonal(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        # Se guardan la tabla y la barra de búsqueda de la pantalla
        # OtroPersonal en variables para que el código se simplifique y se
        # haga más legible.
        tabla = self.pantallaOtroPersonal.tableWidget
        barraBusqueda = self.pantallaOtroPersonal.lineEdit

        # Se obtienen los datos de la base de datos pasando como
        # parámetro la tabla de la que queremos obtener los datos y
        # el texto de la barra de búsqueda mediante el cual queremos
        # filtrarlos.
        datos = dal.obtenerDatos("otro_personal", barraBusqueda.text())
        # Se refresca la tabla, eliminando todas las filas anteriores.
        tabla.setRowCount(0)

        # Bucle: por cada fila de la tabla, se obtiene el número de
        # fila y los contenidos de ésta.
        # Método enumerate: devuelve una lista con el número y el
        # elemento.
        for rowNum, rowData in enumerate(datos):
            # Se añade una fila a la tabla.
            # Método insertRow(int): inserta una fila en una QTable.
            tabla.insertRow(rowNum)

            # Inserta el texto en cada celda. Las celdas por defecto no
            # tienen nada, por lo que hay que añadir primero un item
            # que contenga el texto. No se puede establecer texto asi
            # nomás, tira error.
            # Método setItem(row, column, item): establece el item de
            # una celda de una tabla.
            # QTableWidgetItem: un item de pantalla.tableWidget. Se puede crear con
            # texto por defecto.

            # DNI
            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))
            # Nombre y Apellido
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[2])))
            # Descripción
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[3])))

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Se generan e insertan los botones en la fila, pasando
            # como parámetros las funciones que queremos que los
            # botones tengan y la tabla y la fila de la tabla en la que
            # queremos que se inserten.

            self.generarBotones(
                lambda: self.saveOtroPersonal(datos), lambda: self.deleteOtroPersonal(datos), tabla, rowNum)

        # Método setRowHeight: cambia la altura de una fila.
        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)

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

        # Se pregunta al usuario si desea guardar los cambios en la
        # tabla. NOTA: Esos tabs en el string son para mantener la
        # misma identación en todas las líneas así dedent funciona,
        # sino le da ansiedad.
        # Obtenemos los ids de los campos que no podemos dejar vacíos.
        tabla = self.pantallaOtroPersonal.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()
        iCampos = (0, 1, 2)
        # Por cada campo que no debe ser nulo...
        for iCampo in iCampos:
            # Si el campo está vacio...
            if tabla.item(row, iCampo).text() == "":
                # Le pide al usuario que termine de llenar los campos
                # y corta la función.
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 2).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**10:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios hechos en la fila en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            nombre = tabla.item(row, 0).text()
            clase = tabla.item(row, 1).text().capitalize()

            # Verificamos que el grupo esté registrado.
            idClase = bdd.cur.execute(
                "SELECT id FROM clases WHERE descripcion = ? AND id_cat=2", (
                    clase,)
            ).fetchone()
            # Si no lo está...
            if not idClase:
                # Muestra un mensaje de error al usuario y termina la
                # función.
                info = 'La clase ingresada no está registrada o no está vinculada a la categoría "Personal". Regístrela o revise los datos ya ingresados.'
                return PopUp("Error", info).exec()
            datosNuevos = [nombre, dni, clase]
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                        (nombre, dni, idClase[0],)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Personal', nombre, None, datosNuevos)
                else:
                    idd = datos[row][0]
                    # Guardamos los datos de la fila en
                    bdd.cur.execute(
                        """UPDATE personal
                        SET nombre_apellido=?, dni=?, id_clase=?
                        WHERE id = ?""",
                        (nombre, dni, idClase[0], idd,)
                    )
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    dal.insertarHistorial(
                        self.usuario, 'Edición', 'Personal', datosViejos[1], datosViejos[1:], datosNuevos)
            except sqlite3.IntegrityError:
                info = "El dni ingresado ya está registrado. Ingrese uno nuevo o revise la información ya ingresada."
                return PopUp("Error", info).exec()
            bdd.con.commit()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchOtroPersonal()
            barra.setValue(posicion)

    def saveSubgrupos(self, datos: list | None = None):
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
        tabla = self.pantallaSubgrupos.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()
        iCampos = (0, 1)
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
            # Se obtiene el texto de todas las celdas.
            subgrupo = tabla.item(row, 0).text()
            grupo = tabla.item(row, 1).text().capitalize()

            # Verificamos que el grupo esté registrado.
            idGrupo = bdd.cur.execute(
                "SELECT id FROM grupos WHERE descripcion = ?", (grupo,)
            ).fetchone()
            # Si no lo está...
            if not idGrupo:
                # Muestra un mensaje de error al usuario y termina la
                # función.
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
                        self.usuario, 'Inserción', 'Subgrupos', subgrupo, None, datosNuevos)
                else:
                    idd = datos[row][0]
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
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
            posicion = barra.value()
            self.fetchSubgrupos()
            barra.setValue(posicion)

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

        if not datos:
            idd = None
        else:
            if row == len(datos):
                idd = None
            else:
                idd = datos[row][0]

        if not idd:
            return tabla.removeRow(row)

        hayRelacion = dal.verifElimOtroPersonal(idd)
        if hayRelacion:
            mensaje = "El personal tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar el personal."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el personal?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            datosViejos = [fila for fila in datos if fila[0] == idd][0]
            dal.insertarHistorial(
                self.usuario, 'Eliminación', 'Personal', datosViejos[3], datosViejos[1:])
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
        datos = dal.obtenerDatos("subgrupos", barraBusqueda.text())
        tabla.setRowCount(0)
        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)
            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[2])))

            self.generarBotones(
                lambda: self.saveSubgrupos(datos), lambda: self.deleteSubgrupos(datos), tabla, rowNum)

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(6)

        lambda: self.stackedWidget.setCurrentIndex(6)

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

        if not datos:
            idd = None
        else:
            if row == len(datos):
                idd = None
            else:
                idd = datos[row][0]

        if not idd:
            return tabla.removeRow(row)
        hayRelacion = dal.verifElimSubgrupos(idd)
        if hayRelacion:
            mensaje = "El subgrupo tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este subgrupo."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el subgrupo?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            datosViejos = [fila for fila in datos if fila[0] == idd][0]
            dal.insertarHistorial(
                self.usuario, 'Eliminación', 'Subgrupos', datosViejos[1], datosViejos[1:])
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
        desdeFecha = self.pantallaReparaciones.desdeFecha
        hastaFecha = self.pantallaReparaciones.hastaFecha
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

        # Esto lo hacían ustedes creo
        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pantallaTurnos.desdeFecha.dateChanged.connect(self.fetchTurnos)
        self.pantallaTurnos.hastaFecha.dateChanged.connect(self.fetchTurnos)

        self.stackedWidget.setCurrentIndex(7)

    # y que onda con el save

    def fetchUsuarios(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        # Se guardan la tabla y la barra de búsqueda de la pantalla
        # stock en variables para que el código se simplifique y se
        # haga más legible.
        tabla = self.pantallaUsuarios.tableWidget
        barraBusqueda = self.pantallaUsuarios.lineEdit

        datos = dal.obtenerDatos("usuarios", barraBusqueda.text())

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):

            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[2])))
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[3])))
            tabla.setItem(
                rowNum, 4, QtWidgets.QTableWidgetItem(str(rowData[4])))

            self.generarBotones(
                self.saveUsuarios, self.deleteUsuarios, tabla, rowNum)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        # Esto lo hacían ustedes creo
        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(8)

    def saveUsuarios(self):
        print("No implementado")

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

        if not datos:
            idd = None
        else:
            if row == len(datos):
                idd = None
            else:
                idd = datos[row][0]

        if not idd:
            return tabla.removeRow(row)

        hayRelacion = dal.verifElimUsuario(idd)
        if hayRelacion:
            mensaje = "El usuario tiene movimientos o un seguimiento de reparación relacionados. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar este usuario."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar el usuario?"
        popup = PopUp("Pregunta", mensaje).exec()

        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # # Obtenemos los datos para guardarlos en el historial.
            # desc = tabla.item(row, 0).text()
            # cond = tabla.item(row, 1).text()"stock"datos
            # rep = tabla.item(row, 2).text()
            # baja = tabla.item(row, 3).text()
            # grupo = tabla.item(row, 5).text()
            # subgrupo = tabla.item(row, 6).text()
            # ubi = tabla.item(row, 7).text()

            # datosEliminados = f"desc: {desc}, ubi: {ubi},\n cant cond: {cond}, cant rep: {rep}, cant baja: {baja},\n grupo: {grupo}, subgrupo: {subgrupo}"

            # # Insertamos los datos en el historial para que quede registro.
            # dal.insertarHistorial(self.usuario, "eliminación", "stock", row, datosEliminados)
            # # Eliminamos los datos
            # dal.eliminarDatos(idd)
            print("ME DIJERON QUE NO LO HAGA")
        self.fetchUsuarios()

    def fetchClases(self):
        tabla = self.pantallaClases.tableWidget
        barraBusqueda = self.pantallaClases.lineEdit

        datos = dal.obtenerDatos("clases", barraBusqueda.text())
        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))
            sugerencias=[i[0] for i in
                bdd.cur.execute('SELECT descripcion FROM cats_clase').fetchall()]
            tabla.setCellWidget(rowNum, 1, ParamEdit(sugerencias, rowData[2]))

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            self.generarBotones(
                lambda: self.saveClases(datos), lambda: self.deleteClases(datos), tabla, rowNum)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(10)

    def fetchUbicaciones(self):
        tabla = self.pantallaUbicaciones.tableWidget
        barraBusqueda = self.pantallaUbicaciones.lineEdit

        datos = dal.obtenerDatos("ubicaciones", barraBusqueda.text())

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))

            for col in range(tabla.columnCount()):
                item = tabla.item(rowNum, col)
                if item is not None:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            self.generarBotones(
                lambda: self.saveUbicaciones(datos), lambda: self.deleteUbicaciones(datos), tabla, rowNum)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)

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
        tabla = self.pantallaUbicaciones.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        barra = tabla.verticalScrollBar()

        iCampos = (0,)
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
            ubicacion = tabla.item(row, 0).text()
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO ubicaciones VALUES(NULL, ?)",
                        (ubicacion,)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Ubicaciones', ubicacion, None, None)
                else:
                    idd = datos[row][0]
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
        tabla = self.pantallaUbicaciones.tableWidget
        row = (tabla.indexAt(self.sender().pos())).row()
        barra = tabla.verticalScrollBar()

        if not datos:
            idd = None
        else:
            if row == len(datos):
                idd = None
            else:
                idd = datos[row][0]

        if not idd:
            return tabla.removeRow(row)

        hayRelacion = dal.verifElimUbi(idd)
        if hayRelacion:
            mensaje = "La ubicacion está relacionada con registros en otras gestiones. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar esta ubicacion."
            return PopUp('Advertencia', mensaje).exec()
        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar la ubicacion?"
        popup = PopUp("Pregunta", mensaje).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            des = tabla.item(row, 0).text()
            datosEliminados = [des,]
            dal.insertarHistorial(
                self.usuario, "Eliminación", "Ubicaciones", row, datosEliminados)
            dal.eliminarDatos('ubicaciones', idd)
            posicion = barra.value()
            self.fetchUbicaciones()
            barra.setValue(posicion)

    def fetchReparaciones(self):
        tabla = self.pantallaReparaciones.tableWidget
        barraBusqueda = self.pantallaReparaciones.lineEdit
        desdeFecha = self.pantallaReparaciones.desdeFecha
        hastaFecha = self.pantallaReparaciones.hastaFecha
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
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeMode.Stretch)

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

        iCampos = (0,1,)
        for iCampo in iCampos:
            if tabla.item(row, iCampo) is not None:
                texto=tabla.item(row, iCampo).text()
            else:
                texto=tabla.cellWidget(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()
        cat = tabla.cellWidget(row, 1).text()
        idCat = bdd.cur.execute(
            'SELECT id FROM cats_clase WHERE descripcion LIKE ?', (cat,)).fetchone()
        if not idCat:
            mensaje = "La categoría ingresada no está registrada. Ingresela e intente nuevamente."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            clase = tabla.item(row, 0).text()
            datosNuevos = [clase, cat,]
            try:
                if not datos:
                    bdd.cur.execute(
                        "INSERT INTO clases VALUES(NULL, ?, ?)",
                        (clase, idCat[0],)
                    )
                    dal.insertarHistorial(
                        self.usuario, 'Inserción', 'Clases', clase, None, datosNuevos)
                else:
                    idd = datos[row][0]
                    bdd.cur.execute(
                        """UPDATE clases
                        SET descripcion=?,
                        id_cat=?
                        WHERE id = ?""",
                        (clase, idCat[0], idd)
                    )
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
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

        if not datos:
            idd = None
        else:
            if row == len(datos):
                idd = None
            else:
                idd = datos[row][0]

        if not idd:
            return tabla.removeRow(row)

        hayRelacion = dal.verifElimClases(idd)
        if hayRelacion:
            mensaje = "La clase tiene relaciones. Por motivos de seguridad, debe eliminar primero los registros relacionados antes de eliminar esta clase."
            return PopUp('Advertencia', mensaje).exec()

        mensaje = "Esta acción no se puede deshacer. ¿Desea eliminar la clase?"
        popup = PopUp("Pregunta", mensaje).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            des = tabla.item(row, 0).text()
            cat = tabla.item(row, 1).text()
            datosEliminados = [cat,]
            dal.insertarHistorial(
                self.usuario, "Eliminación", "Clases", des, datosEliminados)
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

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[2])))
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[3])))
            tabla.setItem(
                rowNum, 4, QtWidgets.QTableWidgetItem(str(rowData[4])))
            tabla.setItem(
                rowNum, 5, QtWidgets.QTableWidgetItem(str(rowData[5])))

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
            tablaBaja.show()
        else:
            labelBaja.setText(
                'No se han devuelto herramientas en estado de baja.')
            tablaBaja.hide()

        hastaFecha.dateChanged.connect(self.fetchResumen)
        self.stackedWidget.setCurrentIndex(15)


app = QtWidgets.QApplication(sys.argv)

for fuente in os.listdir(os.path.join(os.path.abspath(os.getcwd()), f'ui{os.sep}rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
                     f'ui{os.sep}rsc{os.sep}fonts{os.sep}{fuente}')
    )

window = MainWindow()
app.exec()
