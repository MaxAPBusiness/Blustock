"""El archivo principal. Genera la ventana principal y ejecuta la 
aplicación.

Clases:
    MainWindow(qtw.QMainWindow): crea la ventana principal.

Objetos:
    app: La aplicación principal.
"""
import os
os.chdir(f"{os.path.abspath(__file__)}{os.sep}..")

from PyQt6 import QtWidgets, QtCore, QtGui, uic
from ui.presets.boton import BotonFila
from ui.presets.popup import PopUp
from db.bdd import bdd
from dal.dal import dal
import datetime as time
import types
import sys

bdd.refrescarBDD()


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
                pixmap = QtGui.QPixmap(path)
                pantalla.label_2.setPixmap(pixmap)
            except Exception as e:
                pass  # Si, puse el print al final #No,no pusiste el print al final

        self.opcionStock.triggered.connect(self.fetchStock)
        self.opcionSubgrupos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(6))
        self.opcionGrupos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))
        self.opcionAlumnos.triggered.connect(self.fetchalumnos)
        self.opcionOtroPersonal.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(5))
        self.opcionTurnos.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(7))
        self.opcionMovimientos.triggered.connect(lambda:self.stackedWidget.setCurrentIndex(4))
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

        self.pantallaStock.pushButton_2.clicked.connect(
            lambda: self.insertarFilas(self.pantallaStock.tableWidget, 
                                      self.saveStock, self.deleteStock, 
                                      (0, 1, 5, 6, 7)))
        self.pantallaStock.lineEdit.editingFinished.connect(self.fetchStock)
        self.stackedWidget.setCurrentIndex(0)
        self.show()

    def login(self):
        bdd.cur.execute("SELECT count(*) FROM personal WHERE usuario = ?",
                         (self.findChild(QtWidgets.QLineEdit, "usuariosLineEdit").text(),))
        check = bdd.cur.fetchone()
        if check[0] >= 1:
            bdd.cur.execute("SELECT count(*) FROM personal WHERE usuario = ? and contrasena = ?", (self.findChild(
                QtWidgets.QLineEdit, "usuariosLineEdit").text(), self.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text(),))
            check = bdd.cur.fetchone()
            if check[0] == 1:
                self.usuario = bdd.cur.execute("SELECT dni FROM personal WHERE usuario = ? and contrasena = ?", (self.findChild(
                    QtWidgets.QLineEdit, "usuariosLineEdit").text(), self.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text(),)).fetchall()[0][0]
                self.fetchStock()
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

    def generarBotones(self, funcGuardar: types.FunctionType, funcEliminar: types.FunctionType,
                       tabla: QtWidgets.QTableWidget, numFila: int):
        """Este método genera botones para guardar cambios y eliminar
        filas y los inserta en una fila de una tabla de la UI

        Parámetros
        ----------
            funcGuardar : types.FunctionType
                La función que estará vinculada al botón guardar.
            funcEliminar : types.FunctionType
                La función que estará vinculada al botón eliminar.
            tabla : QtWidgets.QTableWidget
                La tabla a la que se le añadirán los botones.
            numFila : int
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


    def insertarFilas(self, tabla: QtWidgets.QTableWidget,
                      funcGuardar: types.FunctionType,
                      funcEliminar: types.FunctionType,
                      camposObligatorios: tuple | None = None):
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

        # Por cada campo que no debe ser nulo...
        for iCampo in camposObligatorios:
            # Si el campo está vacio...
            if tabla.item(ultimaFila, iCampo).text() == "":
                # Le pide al usuario que termine de llenar los campos
                # y corta la función.
                mensaje = """       Ha agregado una fila y todavía no ha ingresado los
                datos. Ingreselos, guarde los cambios e intente nuevamente."""
                return PopUp("Error", mensaje).exec()

        # Se añade la fila al final.
        tabla.insertRow(indiceFinal)
        # Se añaden campos de texto en todas las celdas ya que por
        # defecto no vienen.
        for numCol in range(tabla.columnCount() - 2):
            tabla.setItem(indiceFinal, numCol, QtWidgets.QTableWidgetItem(""))
        self.generarBotones(
            funcGuardar, funcEliminar, tabla, indiceFinal)

    # Estas funciones pueden funcionar sin estar en la clase. Si el
    # archivo main se hace muy largo, podemos crear la API del programa

    def fetchStock(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        # Se guardan la tabla y la barra de búsqueda de la pantalla
        # stock en variables para que el código se simplifique y se
        # haga más legible.
        tabla = self.pantallaStock.tableWidget
        barraBusqueda = self.pantallaStock.lineEdit

        # Se obtienen los datos de la base de datos pasando como
        # parámetro la tabla de la que queremos obtener los daots y 
        # el texto de la barra de búsqueda mediante el cual queremos
        # filtrarlos.
        datos=dal.obtenerDatos("stock", barraBusqueda.text())

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
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[2])))
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[3])))
            # Se calcula el total de stock, sumando las herramientas o
            # insumos en condiciones, reparación y de baja.
            total = rowData[1]+rowData[2]+rowData[3]
            tabla.setItem(rowNum, 4, QtWidgets.QTableWidgetItem(str(total)))

            tabla.setItem(
                rowNum, 5, QtWidgets.QTableWidgetItem(str(rowData[4])))
            tabla.setItem(
                rowNum, 6, QtWidgets.QTableWidgetItem(str(rowData[5])))
            tabla.setItem(
                rowNum, 7, QtWidgets.QTableWidgetItem(str(rowData[6])))

            # Se generan e insertan los botones en la fila, pasando
            # como parámetros las funciones que queremos que los
            # botones tengan y la tabla y la fila de la tabla en la que
            # queremos que se inserten.
            self.generarBotones(
                self.saveStock, self.deleteStock, tabla, rowNum)

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
        """Esta método imprime la fila clickeada.
        Hay que verla después"""
        print(row)
        self.filaEditada = tabla.item(row, 0).text()
        print(self.filaEditada)

    def saveStock(self):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla de la base de datos"""
        # Se pregunta al usuario si desea guardar los cambios en la
        # tabla. NOTA: Esos tabs en el string son para mantener la
        # misma identación en todas las líneas así dedent funciona,
        # sino le da ansiedad.
        # Obtenemos los ids de los campos que no podemos dejar vacíos.
        tabla=self.pantallaStock.tableWidget
        index = tabla.indexAt(self.sender().pos())
        row = index.row()
        iCampos=(0, 1, 5, 6, 7)
        # Por cada campo que no debe ser nulo...
        for iCampo in iCampos:
            # Si el campo está vacio...
            if tabla.item(row, iCampo).text() == "":
                # Le pide al usuario que termine de llenar los campos
                # y corta la función.
                mensaje = """       Hay campos en blanco que son obligatorios.
                Ingreselos e intente nuevamente."""
                return PopUp("Error", mensaje).exec()

        info = """        Esta acción no se puede deshacer.
        ¿Desea guardar los cambios hechos en la fila en la base de datos?"""
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:

            # Se obtiene el texto de todas las celdas.
            desc = tabla.item(row, 0).text()
            cond = tabla.item(row, 1).text()
            rep = tabla.item(row, 2).text()
            baja = tabla.item(row, 3).text()
            grupo = tabla.item(row, 5).text()
            subgrupo = tabla.item(row, 6).text()

            # Verificamos que el grupo esté registrado.
            idGrupo=bdd.cur.execute(
                "SELECT id FROM grupos WHERE descripcion = ?", (grupo,)
            ).fetchone()
            # Si no lo está...
            if not idGrupo:
                # Muestra un mensaje de error al usuario y termina la
                # función.
                info = """        El grupo ingresado no está registrado.
                Regístrelo e ingrese nuevamente"""
                return PopUp("Error", info).exec()

            # Verificamos que el subgrupo esté registrado y que
            # coincida con el grupo ingresado.
            idSubgrupo=bdd.cur.execute(
                "SELECT id FROM subgrupos WHERE descripcion = ? AND id_grupo = ?",
                (subgrupo, idGrupo[0],)
            ).fetchone()
            if not idSubgrupo:
                info = """El subgrupo ingresado no está registrado o no
                pertenece al grupo ingresado. Regístrelo o asegúrese que esté
                relacionado al grupo e ingrese nuevamente."""
                return PopUp("Error", info).exec()
            # Guardamos los datos de la fila en
            bdd.cur.execute(
                """UPDATE stock
                SET descripcion = ?, cant_condiciones = ?, cant_reparacion=?,
                cant_baja = ?, id_subgrupo = ?
                WHERE descripcion = ?""",
                (desc, cond, rep, baja, idSubgrupo[0], self.filaEditada,)
            )
            bdd.con.commit()
            self.fetchStock()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()

    def deleteStock(self):
        """Este método elimina una fila de una tabla de la base de
        datos."""
        # Obtenemos la tabla a la que vamos a realizarle la eliminación
        tabla=self.pantallaStock.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        iCampos=(0, 1, 5, 6, 7)
        # Por cada campo que no debe ser nulo...
        for iCampo in iCampos:
            # Si el campo está vacio...
            if tabla.item(row, iCampo).text() == "":
                # Le pide al usuario que termine de llenar los campos
                # y corta la función.
                return tabla.removeRow(row)
            
        desc = tabla.item(row, 0).text()
        idStock = bdd.cur.execute("SELECT id FROM stock WHERE descripcion = ?", (desc,)).fetchone()
        if not idStock:
            mensaje = """        La herramienta/insumo no está registrada.
            Por favor, regístrela primero antes de eliminarla"""
            return PopUp("Advertencia", mensaje).exec()

        movsRel=bdd.cur.execute(
            "SELECT * FROM movimientos WHERE id_elem = ?", (idStock[0],)).fetchone()
        repRel=bdd.cur.execute(
            "SELECT * FROM reparaciones WHERE id_herramienta = ?", (idStock[0],)).fetchone()
        if movsRel or repRel:
            mensaje = """        La herramienta/insumo tiene movimientos o un
            seguimiento de reparación relacionados. Por motivos de seguridad,
            debe eliminar primero los registros relacionados antes de eliminar
            esta herramienta/insumo."""
            return PopUp("Advertencia", mensaje).exec()
        
        descRepetida=tabla.findItems(tabla.item(row, 0).text(), QtCore.Qt.MatchFlag.MatchFixedString)
        if len(descRepetida) > 1:
            return tabla.removeRow(row)

        
        mensaje = """        Esta acción no se puede deshacer.
        ¿Desea eliminar la herramienta/insumo?"""
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Busca la fila en la que está el botón
            row = (tabla.indexAt(
                self.sender().pos())).row()
            desc = tabla.item(row, 0).text()
            cond = tabla.item(row, 1).text()
            rep = tabla.item(row, 2).text()
            baja = tabla.item(row, 3).text()
            grupo = tabla.item(row, 5).text()
            subgrupo = tabla.item(row, 6).text()
            todo = f"desc: {desc}, cant cond: {cond}, cant rep: {rep}, cant baja: {baja}, grupo: {grupo}, subgrupo: {subgrupo}"
            bdd.cur.execute("INSERT INTO historial_de_cambios(id_usuario,fecha_hora,tipo,tabla,id_fila,datos_viejos) values(?,?,?,?,?,?) ",
                             (self.usuario, time.datetime.now(), "eliminación", "stock de herramientas", row, todo))
            bdd.cur.execute(
                "DELETE FROM stock WHERE descripcion = ?", (desc,))
            bdd.con.commit()
            self.fetchStock()
        # TODO: guardar los cambios en el historial.

    def fetchalumnos(self):
        bdd.cur.execute("SELECT * FROM personal where tipo!='profesor'")
        datos = bdd.cur.fetchall()
        self.pantallaAlumnos.tableWidget.setRowCount(0)

        for rowNum, row in enumerate(datos):
            self.pantallaAlumnos.tableWidget.insertRow(rowNum)
            self.pantallaAlumnos.tableWidget.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowNum+1)))
            self.pantallaAlumnos.tableWidget.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(row[0])))
            self.pantallaAlumnos.tableWidget.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(row[1])))
            self.pantallaAlumnos.tableWidget.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(row[2])))
            edit = BotonFila("editar.png")
            borrar = BotonFila("eliminar.png")
            self.pantallaAlumnos.tableWidget.setCellWidget(rowNum, 4, edit)
            self.pantallaAlumnos.tableWidget.setCellWidget(rowNum, 5, borrar)
            self.pantallaAlumnos.tableWidget.setRowHeight(0, 35)

        self.pantallaAlumnos.tableWidget.resizeColumnsToContents()
        self.pantallaAlumnos.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaAlumnos.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(1)

    """def fetchmovimientos(self):
        bdd.cur.execute("SELECT * FROM movimientos")
        datos = bdd.cur.fetchall()
        self.pantallaMovimientos.tableWidget.setRowCount(0)

        for rowNum, rowData in enumerate(datos):

            self.pantallaMovimientos.tableWidget.insertRow(rowNum)
            self.pantallaMovimientos.tableWidget.setItem(rowNum, 0, QtWidgets.QTableWidgetItem(str(
                bdd.cur.execute("select descripcion from stock where id=?", (rowData[2],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(estado)))
            self.pantallaMovimientos.tableWidget.setItem(rowDataNum, 2, QtWidgets.QTableWidgetItem(str(bdd.cur.execute(
                "select nombre_apellido from personal where dni=?", (rowData[5],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(rowDataNum, 3, QtWidgets.QTableWidgetItem(str(
                bdd.cur.execute("select tipo from personal where dni=?", (rowData[5],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(
                rowNum, 4, QtWidgets.QTableWidgetItem(str(rowData[6])))
            self.pantallaMovimientos.tableWidget.setItem(
                rowNum, 5, QtWidgets.QTableWidgetItem(str(rowData[4])))
            self.pantallaMovimientos.tableWidget.setItem(
                rowNum, 6, QtWidgets.QTableWidgetItem(str(tipo)))
            self.pantallaMovimientos.tableWidget.setItem(rowNum, 7, QtWidgets.QTableWidgetItem(str(bdd.cur.execute(
                "select nombre_apellido from personal where dni=(select id_panolero from turnos where id =?)", (row[1],)).fetchone()[0])))

            self.generarBotones(self.saveStock, self.deleteStock, tabla, rowNum)
            self.pantallaMovimientos.tableWidget.setRowHeight(0, 35)

        self.pantallaMovimientos.tableWidget.resizeColumnsToContents()
        self.pantallaMovimientos.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaMovimientos.tableWidget.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(4)"""


app = QtWidgets.QApplication(sys.argv)

for fuente in os.listdir(os.path.join(os.path.abspath(os.getcwd()), f'ui{os.sep}rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
                     f'ui{os.sep}rsc{os.sep}fonts{os.sep}{fuente}')
    )

window = MainWindow()
app.exec()
