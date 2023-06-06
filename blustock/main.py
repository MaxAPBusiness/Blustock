"""El archivo principal. Genera la ventana principal y ejecuta la 
aplicación.

Clases:
    MainWindow(qtw.QMainWindow): crea la ventana principal.

Objetos:
    app: La aplicación principal.
"""
from ui.presets.boton import BotonFila
from ui.presets.popup import PopUp
from db.bbdd import BBDD
from PyQt6 import QtWidgets, QtCore, QtGui, uic
import sys
import os
import types

os.chdir(f"{os.path.abspath(__file__)}{os.sep}..")


bbdd = BBDD()
bbdd.refrescarBBDD()


class MainWindow(QtWidgets.QMainWindow):
    """Esta clase crea la ventana principal.

    Hereda: PyQt6.QtWidgets.QMainWindow

    Atributos
    ---------

    Métodos
    -------
        __init__(self):
            El constructor de la clase MainWindow.

            Crea la ventana principal con una cabecera, un menú
            izquierdo (inicialmente escondido) y una colección de
            pantallas."""

    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}main.ui'), self)
        self.menubar.hide()

        self.filaEditada = 0

        self.pantallaAlumnos = QtWidgets.QWidget()
        uic.loadUi(
            os.path.join(
                os.path.abspath(os.getcwd()),
                f'ui{os.sep}screens_uis{os.sep}alumnos.ui'
            ), self.pantallaAlumnos)
        self.pantallaGrupos = QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}grupos.ui'), self.pantallaGrupos)
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
        self.pantallaLogin.Ingresar.clicked.connect(self.login)

        pantallas = (self.pantallaLogin, self.pantallaAlumnos, 
                    self.pantallaGrupos, self.pantallaStock,
                    self.pantallaMovimientos,
                    self.pantallaOtroPersonal, self.pantallaSubgrupos, 
                    self.pantallaTurnos, self.pantallaUsuarios,
                    self.pantallaHistorial)

        for pantalla in pantallas:
            self.stackedWidget.addWidget(pantalla)
            try:
                pantalla.tableWidget.horizontalHeader().setFont(QtGui.QFont("Oswald", 11))
                path = f'ui{os.sep}rsc{os.sep}icons{os.sep}buscar.png'
                pixmap=QtGui.QPixmap(path)
                pantalla.label_2.setPixmap(pixmap)
            except Exception as e:
                print(e)  # Si, puse el print al final

        self.opcionStock.triggered.connect(self.fetchstock)
        self.opcionSubgrupos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(6))
        self.opcionGrupos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))
        self.opcionAlumnos.triggered.connect(self.fetchalumnos)
        self.opcionOtroPersonal.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(5))
        self.opcionTurnos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(7))
        self.opcionMovimientos.triggered.connect(self.fetchmovimientos)
        self.opcionUsuariosG.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(8))
        self.opcionHistorial.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(9))

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

        self.pantallaStock.pushButton_2.clicked.connect(self.insertStock)
        self.stackedWidget.setCurrentIndex(0)
        self.show()

    def login(self):
        bbdd.cur.execute("SELECT count(*) FROM personal WHERE usuario = ?",
                         (self.findChild(QtWidgets.QLineEdit, "usuariosLineEdit").text(),))
        check = bbdd.cur.fetchone()
        if check[0] >= 1:
            bbdd.cur.execute("SELECT count(*) FROM personal WHERE usuario = ? and contrasena = ?", (self.findChild(
                QtWidgets.QLineEdit, "usuariosLineEdit").text(), self.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text(),))
            check = bbdd.cur.fetchone()
            if check[0] == 1:
                self.fetchstock()
                self.menubar.show()

            else:
                self.findChild(QtWidgets.QLabel, "passwordState").show()
                self.findChild(QtWidgets.QLabel, "usuarioState").hide()
        else:
            self.findChild(QtWidgets.QLabel, "usuarioState").show()
            self.findChild(QtWidgets.QLabel, "passwordState").hide()

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
    
    def generarBotones(self, save: types.FunctionType, delete: types.FunctionType,
                    table: QtWidgets.QTableWidget, row: types.FunctionType):
        # Se crean dos botones: uno de editar y uno de eliminar
        # Para saber que hacen BotonFila, vayan al código de la
        # clase.
        guardar = BotonFila("guardar")
        guardar.clicked.connect(save)
        borrar = BotonFila("eliminar")
        borrar.clicked.connect(delete)

        # Se añaden los botones a cada fila.
        # Método setCellWidget(row, column, widget): añade un
        # widget a la celda de una tabla.
        table.setCellWidget(row, 7, guardar)
        table.setCellWidget(row, 8, borrar)
    
    def insertStock(self):
        """Esta función inserta una nueva fila en la tabla stock"""
        tabla=self.pantallaStock.tableWidget
        row=tabla.rowCount()
        tabla.insertRow(row)
        self.generarBotones(self.saveStock, self.deletestock, tabla, row)

        

    # Estas funciones pueden funcionar sin estar en la clase. Si el
    # archivo main se hace muy largo, podemos moverlos a módulos.
    def fetchstock(self):
        """Esta función obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario."""
        tabla = self.pantallaStock.tableWidget

        # Se seleccionan los datos de la tabla de la base de datos
        # Método execute(): ejecuta código SQL
        bbdd.cur.execute("SELECT * FROM stock")

        # Método fetchall: obtiene los datos seleccionados y los
        # transforma en una lista.
        datos = bbdd.cur.fetchall()

        # Se busca la tabla de la pantalla stock para insertarle los
        # datos.
        tabla.setRowCount(0)

        # Bucle: por cada fila de la tabla, se obtiene el número de
        # fila y los contenidos de la fila.
        # Método enumerate: devuelve una lista con el número y el
        # elemento.
        for row_num, row in enumerate(datos):
            # Se añade la fila a la tabla.
            # Método insertRow(int): inserta una fila en una QTable.
            tabla.insertRow(row_num)

            # Inserta el texto en cada celda. Las celdas por defecto no
            # tienen nada, por lo que hay que añadir primero un item
            # que contenga el texto. No se puede establecer texto asi
            # nomás.
            # Método setItem(row, column, item): establece el item de
            # una celda de una tabla.
            # QTableWidgetItem: un item de pantalla.tableWidget. Se puede crear con
            # texto por defecto.
            tabla.setItem(
                row_num, 0, QtWidgets.QTableWidgetItem(str(row[1])))
            tabla.setItem(
                row_num, 1, QtWidgets.QTableWidgetItem(str(row[2])))
            tabla.setItem(
                row_num, 2, QtWidgets.QTableWidgetItem(str(row[3])))
            tabla.setItem(
                row_num, 3, QtWidgets.QTableWidgetItem(str(row[4])))
            tabla.setItem(
                row_num, 4, QtWidgets.QTableWidgetItem(str(row[2]+row[3]+row[4])))

            # Para lo que está aca abajo propongo hacer un join para
            # ahorrar tiempo de proceso del programa. Si no quieren
            # hacerlo los chicos no pasa nada, lo hago yo. - Maxi
            bbdd.cur.execute(
                "select descripcion from subgrupos where id = ?", (row[5],))
            a = bbdd.cur.fetchone()
            bbdd.cur.execute(
                "select descripcion from grupos where id=(select id_grupo from subgrupos where id = ?)", (row[5],))
            b = bbdd.cur.fetchone()
            tabla.setItem(
                row_num, 5, QtWidgets.QTableWidgetItem(str(b[0])))
            tabla.setItem(
                row_num, 6, QtWidgets.QTableWidgetItem(str(a[0])))

            self.generarBotones(self.saveStock, self.deletestock, tabla, row_num)

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

        self.stackedWidget.setCurrentIndex(3)
        tabla.cellClicked.connect(
            lambda row: self.obtenerFilaEditada(tabla, row))

    def obtenerFilaEditada(self, tabla, row):
        """Esta función imprime la fila clickeada.
        Hay que verla después"""
        self.filaEditada = self.pantallaStock.tableWidget.item(row, 0).text()
        print(self.filaEditada)

    def saveStock(self):
        """Esta función guarda los cambios hechos en la tabla de la ui
        en la tabla de la base de datos"""
        # Esta función todavía no esta terminada, cuando esté la voy a
        # comentar. :) Chicos: no usen esta función de ejemplo aún.
        index = self.pantallaStock.tableWidget.indexAt(self.sender().pos())
        row = index.row()
        desc = self.pantallaStock.tableWidget.item(row, 0).text()
        cond = self.pantallaStock.tableWidget.item(row, 1).text()
        rep = self.pantallaStock.tableWidget.item(row, 2).text()
        baja = self.pantallaStock.tableWidget.item(row, 3).text()
        subgrupo = self.pantallaStock.tableWidget.item(row, 6).text()
        idd= bbdd.cur.execute(
            "select id from subgrupos where descripcion = ?", (subgrupo,)).fetchone()
        if not idd:
            popup=PopUp("Error", "Error", 
                        "El subgrupo ingresado no está registrado. Regístrelo")
        bbdd.cur.execute("Update stock set descripcion = ?,cant_condiciones = ?,cant_reparacion=?,cant_baja = ?,id_subgrupo = ? where descripcion = ?",
                         (desc, cond, rep, baja, id[0], self.filaEditada))
        bbdd.con.commit()
        self.fetchstock()

    def deletestock(self):
        """Esta función elimina la fila de la tabla"""
        # Nota: la función aún no está terminada.
        # Para saber que hace la clase, entrar al archivo
        # mensaje_emergente.py
        mensaje = PopUp("Pregunta", "Atención",
                        "¿Desea eliminar la herramienta/insumo?")

        # Con esta variable guardamos el botón que presionó el usuario.
        botonPresionado = mensaje.exec()

        # Si el usuario presionó el boton si
        if botonPresionado == QtWidgets.QMessageBox.StandardButton.Yes:
            self.pantallaStock.tableWidget = self.findChild(
                QtWidgets.QTableWidget, "stock")
            # Busca la fila en la que está el botón
            row = (self.pantallaStock.tableWidget.indexAt(self.sender().pos())).row()
            desc = self.pantallaStock.tableWidget.item(row, 0).text()
            bbdd.cur.execute(
                "DELETE FROM stock WHERE descripcion = ?", (desc,))
            bbdd.con.commit()
            self.fetchstock()
        # TODO: eliminar las relaciones de clave foránea correctamente.
        # TODO: guardar los cambios en el historial.

    def fetchalumnos(self):
        bbdd.cur.execute("SELECT * FROM personal where tipo!='profesor'")
        datos = bbdd.cur.fetchall()
        self.pantallaAlumnos.tableWidget.setRowCount(0)

        for row_num, row in enumerate(datos):
            self.pantallaAlumnos.tableWidget.insertRow(row_num)
            self.pantallaAlumnos.tableWidget.setItem(
                row_num, 0, QtWidgets.QTableWidgetItem(str(row_num+1)))
            self.pantallaAlumnos.tableWidget.setItem(
                row_num, 1, QtWidgets.QTableWidgetItem(str(row[0])))
            self.pantallaAlumnos.tableWidget.setItem(
                row_num, 2, QtWidgets.QTableWidgetItem(str(row[1])))
            self.pantallaAlumnos.tableWidget.setItem(
                row_num, 3, QtWidgets.QTableWidgetItem(str(row[2])))
            edit = BotonFila("editar.png")
            borrar = BotonFila("eliminar.png")
            self.pantallaAlumnos.tableWidget.setCellWidget(row_num, 4, edit)
            self.pantallaAlumnos.tableWidget.setCellWidget(row_num, 5, borrar)
            self.pantallaAlumnos.tableWidget.setRowHeight(0, 35)

        self.pantallaAlumnos.tableWidget.resizeColumnsToContents()
        self.pantallaAlumnos.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaAlumnos.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(1)

    def fetchmovimientos(self):
        bbdd.cur.execute("SELECT * FROM movimientos")
        datos = bbdd.cur.fetchall()
        self.pantallaMovimientos.tableWidget.setRowCount(0)

        for row_num, row in enumerate(datos):
            if row[3] == 0:
                estado = "Baja"
            if row[3] == 1:
                estado = "Condiciones"
            if row[3] == 2:
                estado = "Reparacion"
            if row[7] == 0:
                tipo = "Devolucion"
            if row[7] == 1:
                tipo = "Retiro"
            if row[7] == 2:
                tipo = "Ingreso de materiales"

            self.pantallaMovimientos.tableWidget.insertRow(row_num)
            self.pantallaMovimientos.tableWidget.setItem(row_num, 0, QtWidgets.QTableWidgetItem(str(
                bbdd.cur.execute("select descripcion from stock where id=?", (row[2],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(
                row_num, 1, QtWidgets.QTableWidgetItem(str(estado)))
            self.pantallaMovimientos.tableWidget.setItem(row_num, 2, QtWidgets.QTableWidgetItem(str(bbdd.cur.execute(
                "select nombre_apellido from personal where dni=?", (row[5],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(
                bbdd.cur.execute("select tipo from personal where dni=?", (row[5],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(
                row_num, 4, QtWidgets.QTableWidgetItem(str(row[6])))
            self.pantallaMovimientos.tableWidget.setItem(
                row_num, 5, QtWidgets.QTableWidgetItem(str(row[4])))
            self.pantallaMovimientos.tableWidget.setItem(
                row_num, 6, QtWidgets.QTableWidgetItem(str(tipo)))
            self.pantallaMovimientos.tableWidget.setItem(row_num, 7, QtWidgets.QTableWidgetItem(str(bbdd.cur.execute(
                "select nombre_apellido from personal where dni=(select id_panolero from turnos where id =?)", (row[1],)).fetchone()[0])))

            edit = BotonFila("editar.png")
            borrar = BotonFila("eliminar.png")
            self.pantallaMovimientos.tableWidget.setCellWidget(row_num, 8, edit)
            self.pantallaMovimientos.tableWidget.setCellWidget(row_num, 9, borrar)
            self.pantallaMovimientos.tableWidget.setRowHeight(0, 35)

        self.pantallaMovimientos.tableWidget.resizeColumnsToContents()
        self.pantallaMovimientos.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaMovimientos.tableWidget.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(4)


app = QtWidgets.QApplication(sys.argv)

for fuente in os.listdir(os.path.join(os.path.abspath(os.getcwd()), f'ui{os.sep}rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
                     f'ui{os.sep}rsc{os.sep}fonts{os.sep}{fuente}')
    )

window = MainWindow()
app.exec()
