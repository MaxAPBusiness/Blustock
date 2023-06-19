"""El archivo principal. Genera la ventana principal y ejecuta la 
aplicación.

Clases:
    MainWindow(qtw.QMainWindow): crea la ventana principal.

Objetos:
    app: La aplicación principal.
"""
import os
os.chdir(f"{os.path.dirname(os.path.abspath(__file__))}{os.sep}..")

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
        ui_dir = f"{os.getcwd()}{os.sep}blustock{os.sep}ui{os.sep}"

        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}main.ui'), self)
        self.menubar.hide()

        self.filaEditada = 0

        self.pantallaAlumnos = QtWidgets.QWidget()
        uic.loadUi(
            os.path.join(
                ui_dir,
                f'screens_uis{os.sep}alumnos.ui'
            ), self.pantallaAlumnos)
        
        self.pantallaGrupos = QtWidgets.QWidget()
        
        pathGrupos=os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}grupos.ui')
        
        uic.loadUi(pathGrupos, self.pantallaGrupos)
        

        self.pantallaStock = QtWidgets.QWidget()
        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}stock.ui'), self.pantallaStock)
        self.pantallaHistorial = QtWidgets.QWidget()
        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}historial.ui'), self.pantallaHistorial)
        self.pantallaMovimientos = QtWidgets.QWidget()
        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}movimientos.ui'), self.pantallaMovimientos)
        self.pantallaOtroPersonal = QtWidgets.QWidget()
        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}otro_personal.ui'), self.pantallaOtroPersonal)
        self.pantallaSubgrupos = QtWidgets.QWidget()
        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}subgrupos.ui'), self.pantallaSubgrupos)
        self.pantallaTurnos = QtWidgets.QWidget()
        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}turnos.ui'), self.pantallaTurnos)
        self.pantallaUsuarios = QtWidgets.QWidget()
        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}usuarios.ui'), self.pantallaUsuarios)
        self.pantallaLogin = QtWidgets.QWidget()
        uic.loadUi(os.path.join(ui_dir, f'screens_uis{os.sep}login.ui'), self.pantallaLogin)
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

        self.opcionSubgrupos.triggered.connect(self.fetchSubgrupos)
        self.opcionGrupos.triggered.connect(self.fetchGrupos)
        self.opcionAlumnos.triggered.connect(self.fetchAlumnos)
        self.opcionOtroPersonal.triggered.connect(self.fetchOtroPersonal)
        self.opcionTurnos.triggered.connect(self.fetchTurnos)
        self.opcionMovimientos.triggered.connect(self.fetchMovimientos)
        self.opcionUsuariosG.triggered.connect(self.fetchUsuarios)
        self.opcionHistorial.triggered.connect(
            lambda: self.stackedWidget.setCurrentIndex(9))

        with open(os.path.join(ui_dir, f'styles.qss'), 'r') as file:
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
                mensaje = """       Ha agregado una fila y todavía no ha
                ingresado los datos de la fila anterior. Ingreselos, guarde
                los cambios e intente nuevamente."""
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
    def obtenerTotal(self, tabla, row, cantCond: int, cantRep: int | None = None, cantBaja: int | None = None):
        if cantRep:
            tabla.setItem(row, 4, QtWidgets.QTableWidgetItem(str(cantCond + cantRep + cantBaja)))
        else:
            tabla.setItem(row, 4, QtWidgets.QTableWidgetItem(str(cantCond)))

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
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[2])))
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[3])))
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[4])))
            # Se calcula el total de stock, sumando las herramientas o
            # insumos en condiciones, reparación y de baja.
            self.obtenerTotal(tabla, rowNum, rowData[2], rowData[3], rowData[4])

            tabla.setItem(
                rowNum, 5, QtWidgets.QTableWidgetItem(str(rowData[5])))
            tabla.setItem(
                rowNum, 6, QtWidgets.QTableWidgetItem(str(rowData[6])))
            tabla.setItem(
                rowNum, 7, QtWidgets.QTableWidgetItem(str(rowData[7])))

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
        tabla=self.pantallaStock.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
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

        try:
            cond = int(tabla.item(row, 1).text())

            rep = tabla.item(row, 2).text()
            baja = tabla.item(row, 3).text()
            if rep != "" or baja != "":
                rep = int(rep)
                baja = int(baja)
        except:
            mensaje = """       Los datos ingresados no son válidos.
            Por favor, ingrese los datos correctamente."""
            return PopUp("Error", mensaje).exec()

        info = """        Esta acción no se puede deshacer.
        ¿Desea guardar los cambios hechos en la fila en la base de datos?"""
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            

            # Se obtiene el texto de todas las celdas.
            desc = tabla.item(row, 0).text()
            grupo = tabla.item(row, 5).text()
            subgrupo = tabla.item(row, 6).text()
            ubi = tabla.item(row, 7).text()

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
            
            idUbi=bdd.cur.execute("SELECT id FROM ubicaciones WHERE descripcion = ?",
                                  (ubi,)).fetchone()
            if not idUbi:
                info = "La ubicación ingresada no está registrada. Regístrela e intente nuevamente."
                return PopUp("Error", info).exec()
            
            if not datos:
                bdd.cur.execute(
                    "INSERT INTO stock VALUES(NULL, ?, ?, ?, ?, ?, ?)",
                    (desc, cond, rep, baja, idSubgrupo[0], idUbi[0],)
                )
            else:
                idd=datos[row][0]
                # Guardamos los datos de la fila en
                bdd.cur.execute(
                    """UPDATE stock
                    SET descripcion = ?, cant_condiciones = ?, cant_reparacion=?,
                    cant_baja = ?, id_subgrupo = ?, id_ubi=?
                    WHERE id = ?""",
                    (desc, cond, rep, baja, idSubgrupo[0], idUbi[0], idd,)
                )
            bdd.con.commit()
            self.fetchStock()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()

    def deleteStock(self, datos: list) -> None:
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
        tabla=self.pantallaStock.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        if datos:
            idd=None
        else:
            idd=datos[row][0]
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
            mensaje = """        La herramienta/insumo tiene movimientos o un
            seguimiento de reparación relacionados. Por motivos de seguridad,
            debe eliminar primero los registros relacionados antes de eliminar
            esta herramienta/insumo."""
            return PopUp('Advertencia', mensaje).exec()
        
        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = """        Esta acción no se puede deshacer.
        ¿Desea eliminar la herramienta/insumo?"""
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Obtenemos los datos para guardarlos en el historial.
            desc = tabla.item(row, 0).text()
            cond = tabla.item(row, 1).text()
            rep = tabla.item(row, 2).text()
            baja = tabla.item(row, 3).text()
            grupo = tabla.item(row, 5).text()
            subgrupo = tabla.item(row, 6).text()
            ubi = tabla.item(row, 7).text()

            datosEliminados = f"desc: {desc}, ubi: {ubi},\n cant cond: {cond}, cant rep: {rep}, cant baja: {baja},\n grupo: {grupo}, subgrupo: {subgrupo}"

            # Insertamos los datos en el historial para que quede registro.
            dal.insertarHistorial(self.usuario, "eliminación", "stock", row, datosEliminados)
            # Eliminamos los datos
            dal.eliminarDatos(idd)
            self.fetchStock()


    def fetchAlumnos(self):
        """Este método obtiene los datos de la tabla personal y los
        inserta en la tabla de la interfaz de usuario.
        """

        tabla = self.pantallaAlumnos.tableWidget
        barraBusqueda = self.pantallaAlumnos.lineEdit

    
        datos=dal.obtenerDatos("alumnos", barraBusqueda.text())

        tabla.setRowCount(0)

        for rowNum, rowData in enumerate(datos):
            tabla.insertRow(rowNum)

            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowNum)))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[1])))
            tabla.setItem(
                rowNum, 3, QtWidgets.QTableWidgetItem(str(rowData[2])))
          

            self.generarBotones(
                self.saveAlumnos, self.deleteAlumnos, tabla, rowNum)

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

        self.stackedWidget.setCurrentIndex(1)
        tabla.cellClicked.connect(
            lambda row: self.obtenerFilaEditada(tabla, row))
        

    def deleteAlumnos(self, datos: list) -> None:
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
        tabla=self.pantallaAlumnos.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        if datos:
            idd=None
        else:
            idd=datos[row][0]
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
        hayRelacion = dal.verifElimAlumnos(idd)
        if hayRelacion:
            mensaje = """        La alumno/a tiene movimientos o un
            seguimiento de reparación relacionados. Por motivos de seguridad,
            debe eliminar primero los registros relacionados antes de eliminar
            este alumno/a."""
            return PopUp('Advertencia', mensaje).exec()
        
        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = """        Esta acción no se puede deshacer.
        ¿Desea eliminar el alumno/a?"""
        popup = PopUp("Pregunta", mensaje).exec()


        # ME DIJIERON QUE ESTO NO
        # Si el usuario presionó el boton sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            print("ME DIJIERON QUE ESTO NO")
        #     # Obtenemos los datos para guardarlos en el historial.
        #     desc = tabla.item(row, 0).text()
        #     cond = tabla.item(row, 1).text()
        #     rep = tabla.item(row, 2).text()
        #     baja = tabla.item(row, 3).text()
        #     grupo = tabla.item(row, 5).text()
        #     subgrupo = tabla.item(row, 6).text()
        #     ubi = tabla.item(row, 7).text()

        #     datosEliminados = f"desc: {desc}, ubi: {ubi},\n cant cond: {cond}, cant rep: {rep}, cant baja: {baja},\n grupo: {grupo}, subgrupo: {subgrupo}"

        #     # Insertamos los datos en el historial para que quede registro.
        #     dal.insertarHistorial(self.usuario, "eliminación", "stock", row, datosEliminados)
        #     # Eliminamos los datos
        #     dal.eliminarDatos(idd)
        self.fetchAlumnos()



    def fetchMovimientos(self):

        """Este método obtiene los datos de la tabla movimientos y los
        inserta en la tabla de la interfaz de usuario.
        """

        tabla = self.pantallaMovimientos.tableWidget
        barraBusqueda = self.pantallaMovimientos.lineEdit

        datos=dal.obtenerDatos("movimientos", barraBusqueda.text())

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
            tabla.setItem(
                rowNum, 6, QtWidgets.QTableWidgetItem(str(rowData[6])))
            tabla.setItem(
                rowNum, 7, QtWidgets.QTableWidgetItem(str(rowData[7])))
            tabla.setItem(
                rowNum, 8, QtWidgets.QTableWidgetItem(str(rowData[8])))


            self.generarBotones(
                self.saveMovimientos, self.deleteMovimientos, tabla, rowNum)

        
        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        # Esto lo hacían ustedes o entendí eso
        tabla.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            6, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        self.stackedWidget.setCurrentIndex(4)

        tabla.cellClicked.connect(
            lambda row: self.obtenerFilaEditada(tabla, row))

    def saveMovimientos(self):
        # No implementado, cuando esté saveStock completo lo adapto
        pass
    def deleteMovimientos(self):
        # No implementado, cuando esté deleteStock completo lo adapto
        pass

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
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
  
            # Podría mostrarse la cantidad de herramientas en el grupo o algo
            # +-------------+-----------+--------------+
            # | descripcion | subgrupos | herramientas |
            # | Martillos   |     3     |      23      |
            # +-------------+-----------+--------------+
            # pero alto viaje

            self.generarBotones(
                self.saveGrupos, self.deleteGrupos, tabla, rowNum)

        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        # tabla.horizontalHeader().setSectionResizeMode(
        #     0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # Esto lo dejo tachado que lo acomodaban ustedes

        self.stackedWidget.setCurrentIndex(2)
        tabla.cellClicked.connect(
            lambda row: self.obtenerFilaEditada(tabla, row))

    
    def saveAlumnos(self, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla alumnos de la base de datos.
        
        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla alumnos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        tabla=self.pantallaAlumnos.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        iCampos=(0, 1, 2)

        for iCampo in iCampos:
            if tabla.item(row, iCampo).text() == "":
                mensaje = """       Hay campos en blanco que son obligatorios.
                Ingreselos e intente nuevamente."""
                return PopUp("Error", mensaje).exec()
        
        try:
            dni = int(tabla.item(row, 2).text())
        except:
            mensaje = """       Los datos ingresados no son válidos.
            Por favor, ingreselos correctamente."""
            return PopUp("Error", mensaje).exec()

        info = """        Esta acción no se puede deshacer.
        ¿Desea guardar los cambios hechos en la fila en la base de datos?"""
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            nombre = tabla.item(row, 0).text()
            clase= tabla.item(row, 1).text()

            idClase=bdd.cur.execute(
                "SELECT id FROM clases WHERE descripcion = ?", (clase,)
            ).fetchone()
            if not idClase:
                info = """        El curso ingresado no está registrado.
                Regístrelo e ingrese nuevamente"""
                return PopUp("Error", info).exec()

            if datos:
                bdd.cur.execute(
                    "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                    (nombre, idClase, dni,)
                )
            else:
                idd=datos[row][0]
                bdd.cur.execute(
                    """UPDATE alumnos
                    SET nombre_apellido=?, id_clase=?, dni=?
                    WHERE id = ?""",
                    (nombre, idClase, dni, idd,)
                )
            bdd.con.commit()
            # self.fetchStock()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
    
    def saveGrupos(self, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla grupos de la base de datos.
        
        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla grupos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        tabla=self.pantallaStock.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        if tabla.item(row, 0).text() == "":
            mensaje = """       Hay campos en blanco que son obligatorios.
            Ingreselos e intente nuevamente."""
            return PopUp("Error", mensaje).exec()

        info = """        Esta acción no se puede deshacer.
        ¿Desea guardar los cambios hechos en la fila en la base de datos?"""
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            grupo = tabla.item(row, 0).text()
            
            if datos:
                bdd.cur.execute("INSERT INTO grupos VALUES(NULL, ?)",(grupo))
            else:
                idd=datos[row][0]
                bdd.cur.execute(
                    """UPDATE grupos SET descripcion = ? WHERE id = ?""",
                    (grupo, idd,)
                )
            bdd.con.commit()
            # self.fetchStock()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
    
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
        tabla=self.pantallaAlumnos.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        iCampos=(0, 1, 2)
        # Por cada campo que no debe ser nulo...
        for iCampo in iCampos:
            # Si el campo está vacio...
            if tabla.item(row, iCampo).text() == "":
                # Le pide al usuario que termine de llenar los campos
                # y corta la función.
                mensaje = """       Hay campos en blanco que son obligatorios.
                Ingreselos e intente nuevamente."""
                return PopUp("Error", mensaje).exec()
        
        try:
            dni = int(tabla.item(row, 2).text())
        except:
            mensaje = """       Los datos ingresados no son válidos.
            Por favor, ingreselos correctamente."""
            return PopUp("Error", mensaje).exec()

        info = """        Esta acción no se puede deshacer.
        ¿Desea guardar los cambios hechos en la fila en la base de datos?"""
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Se obtiene el texto de todas las celdas.
            nombre = tabla.item(row, 0).text()
            clase= tabla.item(row, 1).text()

            # Verificamos que el grupo esté registrado.
            idClase=bdd.cur.execute(
                "SELECT id FROM clases WHERE descripcion = ?", (clase,)
            ).fetchone()
            # Si no lo está...
            if not idClase:
                # Muestra un mensaje de error al usuario y termina la
                # función.
                info = """        La clase ingresada no está registrado.
                Regístrelo e ingrese nuevamente"""
                return PopUp("Error", info).exec()

            if datos:
                bdd.cur.execute(
                    "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                    (nombre, idClase, dni,)
                )
            else:
                idd=datos[row][0]
                # Guardamos los datos de la fila en
                bdd.cur.execute(
                    """UPDATE alumnos
                    SET nombre_apellido=?, id_clase=?, dni=?
                    WHERE id = ?""",
                    (nombre, idClase, dni, idd,)
                )
            bdd.con.commit()
            # self.fetchStock()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
    
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
        tabla=self.pantallaAlumnos.tableWidget
        row = tabla.indexAt(self.sender().pos()).row()
        iCampos=(0, 1)
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
            subgrupo = tabla.item(row, 0).text()
            grupo= tabla.item(row, 1).text()

            # Verificamos que el grupo esté registrado.
            idGrupo=bdd.cur.execute(
                "SELECT id FROM clases WHERE descripcion = ?", (grupo,)
            ).fetchone()
            # Si no lo está...
            if not idGrupo:
                # Muestra un mensaje de error al usuario y termina la
                # función.
                info = """        El grupo ingresado no está registrado.
                Regístrelo e ingrese nuevamente"""
                return PopUp("Error", info).exec()

            if datos:
                bdd.cur.execute(
                    "INSERT INTO personal VALUES(NULL, ?, ?)",
                    (subgrupo, idGrupo)
                )
            else:
                idd=datos[row][0]
                # Guardamos los datos de la fila en
                bdd.cur.execute(
                    """UPDATE subgrupos
                    SET descripcion=?, id_grupo=?
                    WHERE id = ?""",
                    (subgrupo, grupo, idd)
                )
            bdd.con.commit()
            # self.fetchStock()
            info = "Los datos se han guardado con éxito."
            PopUp("Aviso", info).exec()
    
   


    
    def saveGrupos(self):
        # No implementado, cuando esté saveStock completo lo adapto
        pass
    def deleteGrupos(self, datos: list) -> None:
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
        tabla=self.pantallaGrupos.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        if datos:
            idd=None
        else:
            idd=datos[row][0]
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
        hayRelacion = dal.verifElimGrupos(idd)
        if hayRelacion:
            mensaje = """        El grupo tiene movimientos o un
            seguimiento de reparación relacionados. Por motivos de seguridad,
            debe eliminar primero los registros relacionados antes de eliminar
            este grupo."""
            return PopUp('Advertencia', mensaje).exec()
        
        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = """        Esta acción no se puede deshacer.
        ¿Desea eliminar el grupo?"""
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            print("Me dijieron que no lo hacía")
        self.fetchStock()

    

        self.stackedWidget.setCurrentIndex(4)

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
        datos=dal.obtenerDatos("otro_personal", barraBusqueda.text())
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
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[2])))
            # Nombre y Apellido
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[0])))
            # Descripción
            tabla.setItem(
                rowNum, 2, QtWidgets.QTableWidgetItem(str(rowData[1])))

            # Se generan e insertan los botones en la fila, pasando
            # como parámetros las funciones que queremos que los
            # botones tengan y la tabla y la fila de la tabla en la que
            # queremos que se inserten.

            # fijarse que no existe la función saveOtroPersonal
            self.generarBotones(
                self.saveStock, self.deleteOtroPersonal, tabla, rowNum)

        # Método setRowHeight: cambia la altura de una fila.
        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        # Método setSectionResizeMode(column, ResizeMode): hace que una
        # columna de una tabla se expanda o no automáticamente conforme
        # se extiende la tabla.

        # cuál tendria que poner que no se expanda
        # tabla.horizontalHeader().setSectionResizeMode(
        #     0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # tabla.horizontalHeader().setSectionResizeMode(
        #     3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # tabla.horizontalHeader().setSectionResizeMode(
        #     4, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(5)
        tabla.cellClicked.connect(
            lambda row: self.obtenerFilaEditada(tabla, row))

        lambda: self.stackedWidget.setCurrentIndex(5)

    def deleteOtroPersonal(self, datos: list) -> None:
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
        tabla=self.pantallaOtroPersonal.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        if row == len(datos):
            idd=None
        else:
            idd=datos[row][0]
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
        hayRelacion = dal.verifElimOtroPersonal(idd)
        if hayRelacion:
            # el personal o la persona?
            mensaje = """        El personal tiene movimientos o un
            seguimiento de reparación relacionados. Por motivos de seguridad,
            debe eliminar primero los registros relacionados antes de eliminar
            al personal."""
            return PopUp('Advertencia', mensaje).exec()
        
        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = """        Esta acción no se puede deshacer.
        ¿Desea eliminar el personal?"""
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí...

        # no lo borro pero lo comento

        # if popup == QtWidgets.QMessageBox.StandardButton.Yes:
        #     # Obtenemos los datos para guardarlos en el historial.
        #     desc = tabla.item(row, 0).text()
        #     cond = tabla.item(row, 1).text()
        #     rep = tabla.item(row, 2).text()
        #     baja = tabla.item(row, 3).text()
        #     grupo = tabla.item(row, 5).text()
        #     subgrupo = tabla.item(row, 6).text()
        #     ubi = tabla.item(row, 7).text()

        #     datosEliminados = f"desc: {desc}, ubi: {ubi},\n cant cond: {cond}, cant rep: {rep}, cant baja: {baja},\n grupo: {grupo}, subgrupo: {subgrupo}"

        #     # Insertamos los datos en el historial para que quede registro.
        #     dal.insertarHistorial(self.usuario, "eliminación", "stock", row, datosEliminados)
        #     # Eliminamos los datos
        #     dal.eliminarDatos(idd)
        #     self.fetchStock()

    # y que onda con el save
    def fetchSubgrupos(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        # Se guardan la tabla y la barra de búsqueda de la pantalla
        # stock en variables para que el código se simplifique y se
        # haga más legible.
        tabla = self.pantallaSubgrupos.tableWidget
        barraBusqueda = self.pantallaSubgrupos.lineEdit

        # Se obtienen los datos de la base de datos pasando como
        # parámetro la tabla de la que queremos obtener los datos y 
        # el texto de la barra de búsqueda mediante el cual queremos
        # filtrarlos.
        datos=dal.obtenerDatos("subgrupos", barraBusqueda.text())

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
            tabla.setItem(
                rowNum, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            tabla.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))

            # Se generan e insertan los botones en la fila, pasando
            # como parámetros las funciones que queremos que los
            # botones tengan y la tabla y la fila de la tabla en la que
            # queremos que se inserten.

            # fijarse que no existe la función saveSubgrupos
            self.generarBotones(
                self.saveStock, self.deleteSubGrupos, tabla, rowNum)

        # Método setRowHeight: cambia la altura de una fila.
        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        # Método setSectionResizeMode(column, ResizeMode): hace que una
        # columna de una tabla se expanda o no automáticamente conforme
        # se extiende la tabla.
        # tabla.horizontalHeader().setSectionResizeMode(
        # 0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(6)
        tabla.cellClicked.connect(
            lambda row: self.obtenerFilaEditada(tabla, row))
        
        lambda: self.stackedWidget.setCurrentIndex(6)

    def deleteSubGrupos(self, datos: list) -> None:
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
        tabla=self.pantallaSubgrupos.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        if row == len(datos):
            idd=None
        else:
            idd=datos[row][0]
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
        hayRelacion = dal.verifElimSubgrupos(idd)
        if hayRelacion:
            mensaje = """        El subgrupo tiene movimientos o un
            seguimiento de reparación relacionados. Por motivos de seguridad,
            debe eliminar primero los registros relacionados antes de eliminar
            este subgrupo."""
            return PopUp('Advertencia', mensaje).exec()
        
        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = """        Esta acción no se puede deshacer.
        ¿Desea eliminar el subgrupo?"""
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Obtenemos los datos para guardarlos en el historial.
            desc = tabla.item(row, 0).text()
            cond = tabla.item(row, 1).text()
            rep = tabla.item(row, 2).text()
            baja = tabla.item(row, 3).text()
            grupo = tabla.item(row, 5).text()
            subgrupo = tabla.item(row, 6).text()
            ubi = tabla.item(row, 7).text()

            datosEliminados = f"desc: {desc}, ubi: {ubi},\n cant cond: {cond}, cant rep: {rep}, cant baja: {baja},\n grupo: {grupo}, subgrupo: {subgrupo}"

            # Insertamos los datos en el historial para que quede registro.
            dal.insertarHistorial(self.usuario, "eliminación", "stock", row, datosEliminados)
            # Eliminamos los datos
            dal.eliminarDatos(idd)
            self.fetchStock()

    def fetchTurnos(self):

        """Este método obtiene los datos de la tabla turnos y los
        inserta en la tabla de la interfaz de usuario.
        """

        tabla = self.pantallaTurnos.tableWidget
        barraBusqueda = self.pantallaTurnos.lineEdit

    
        datos=dal.obtenerDatos("turnos", barraBusqueda.text())

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
            tabla.setItem(
                rowNum, 5, QtWidgets.QTableWidgetItem(str(rowData[5])))
            tabla.setItem(
                rowNum, 6, QtWidgets.QTableWidgetItem(str(rowData[6])))
            

            self.generarBotones(
                self.saveTurnos, self.deleteTurnos, tabla, rowNum) # NOne es saveTurno y deleteTurno

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

        self.stackedWidget.setCurrentIndex(7)
        tabla.cellClicked.connect(
            lambda row: self.obtenerFilaEditada(tabla, row))
        
    def saveTurnos(self):
        pass

    def deleteTurnos(self, datos: list) -> None:
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
        tabla=self.pantallaStock.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        if datos:
            idd=None
        else:
            idd=datos[row][0]
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
        hayRelacion = dal.verifElimTurnos(idd)
        if hayRelacion:
            mensaje = """        El turno tiene movimientos o un
            seguimiento de reparación relacionados. Por motivos de seguridad,
            debe eliminar primero los registros relacionados antes de eliminar
            este turno."""
            return PopUp('Advertencia', mensaje).exec()
        
        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = """        Esta acción no se puede deshacer.
        ¿Desea eliminar el turno?"""
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # # Obtenemos los datos para guardarlos en el historial.
            # desc = tabla.item(row, 0).text()
            # cond = tabla.item(row, 1).text()
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
            print("Me dijieron que no lo haga")
        self.fetchTurnos()

    def fetchUsuarios(self):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        # Se guardan la tabla y la barra de búsqueda de la pantalla
        # stock en variables para que el código se simplifique y se
        # haga más legible.
        tabla = self.pantallaUsuarios.tableWidget
        barraBusqueda = self.pantallaUsuarios.lineEdit


        datos=dal.obtenerDatos("usuarios", barraBusqueda.text())

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
            5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(
            6, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(8)

    def saveUsuarios(self):
        print("No implementado")

    def deleteUsuarios(self, datos: list) -> None:
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
        tabla=self.pantallaUsuarios.tableWidget
        # Obtenemos la fila que se va a eliminar.
        row = (tabla.indexAt(self.sender().pos())).row()
        if datos:
            idd=None
        else:
            idd=datos[row][0]
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
            mensaje = """        El usuario tiene movimientos o un
            seguimiento de reparación relacionados. Por motivos de seguridad,
            debe eliminar primero los registros relacionados antes de eliminar
            este usuario."""
            return PopUp('Advertencia', mensaje).exec()
        
        # Si no está relacionado, pregunta al usuario si confirma
        # eliminar la fila y le advierte que la acción no se puede
        # deshacer.
        mensaje = """        Esta acción no se puede deshacer.
        ¿Desea eliminar el usuario?"""
        popup = PopUp("Pregunta", mensaje).exec()

        # Si el usuario presionó el boton sí...
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # # Obtenemos los datos para guardarlos en el historial.
            # desc = tabla.item(row, 0).text()
            # cond = tabla.item(row, 1).text()
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


app = QtWidgets.QApplication(sys.argv)

for fuente in os.listdir(os.path.join(os.getcwd(), f'blustock{os.sep}ui{os.sep}rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
                     f'ui{os.sep}rsc{os.sep}fonts{os.sep}{fuente}')
    )

window = MainWindow()
app.exec()