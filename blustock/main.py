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
import datetime as time
import sys
import os



os.chdir( f"{os.path.dirname(__file__)}{os.sep}.." )

from db.bbdd import BBDD
from ui.presets.popup import PopUp
from ui.presets.botones import BotonFila
import types
from textwrap import dedent

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
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}main.ui'), self)
        self.menubar.hide()

        self.filaEditada=0

        pantallaAlumnos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}alumnos.ui'), pantallaAlumnos)
        pantallaGrupos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}grupos.ui'), pantallaGrupos)
        pantallaHerramientas=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}herramientas.ui'), pantallaHerramientas)
        pantallaHistorial=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}historial.ui'), pantallaHistorial)
        pantallaMovimientos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}movimientos.ui'), pantallaMovimientos)
        pantallaOtroPersonal=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}otro_personal.ui'), pantallaOtroPersonal)
        pantallaSubgrupos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}subgrupos.ui'), pantallaSubgrupos)
        pantallaTurnos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}turnos.ui'), pantallaTurnos)
        pantallaUsuarios=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}usuarios.ui'), pantallaUsuarios)
        pantallaLogin=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}screens_uis{os.sep}login.ui'), pantallaLogin)
        pantallaLogin.Ingresar.clicked.connect(self.login)

        pantallas=(pantallaLogin, pantallaAlumnos, pantallaGrupos, pantallaHerramientas,
                   pantallaMovimientos, pantallaOtroPersonal, pantallaSubgrupos, pantallaTurnos,
                   pantallaUsuarios)

        for pantalla in pantallas:
            self.stackedWidget.addWidget(pantalla)
            try:
                pantalla.tableWidget.horizontalHeader().setFont(QtGui.QFont("Oswald", 11))
                path = f'ui{os.sep}rsc{os.sep}icons{os.sep}buscar.png'
                pixmap=QtGui.QPixmap(path)
                pantalla.label_2.setPixmap(pixmap)
            except Exception as e:
                pass  # Si, puse el print al final #No,no pusiste el print al final

        self.opcionStock.triggered.connect(self.fetchstock)
        self.opcionSubgrupos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.opcionGrupos.triggered.connect(self.fetchGrupos)
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

        with open(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}styles.qss'), 'r') as file:
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
                self.usuario = bbdd.cur.execute("SELECT dni FROM personal WHERE usuario = ? and contrasena = ?",(self.findChild(QtWidgets.QLineEdit,"usuariosLineEdit").text(),self.findChild(QtWidgets.QLineEdit,"passwordLineEdit").text(),)).fetchall()[0][0]
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
                    table: QtWidgets.QTableWidget, row: int):
        """Este método genera botones para guardar cambios y eliminar
        filas y los inserta en una fila de una tabla de la UI
        """
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
        """Este método inserta una nueva fila en la tabla stock.
        
        Si la fila anterior fue recientemente ingresada y los datos no
        fueron modificados, en vez de añadir una nueva fila se le
        muestra un mensaje al usuario pidiéndole que ingrese los datos
        primero.
        """
        # Guardamos la tabla que vamos a modificar en una variable para
        # simplificar el código (en vez de escribir toooodo el nombre 
        # de la tabla, al guardarla en una variable podemos
        # directamente escribir solamente el nombre de la variable y
        # no escribir todo el nombre de la tabla).
        tabla=self.pantallaStock.tableWidget

        # Las filas en la tabla se ingresan escribiendo el índice en
        # el que queremos que se ingresen. Para ingresar la fila al
        # final, tenemos que saber el índice del final. Para obtenerlo,
        # contamos la cantidad de filas: por ejemplo, si queremos
        # agregar una fila al final y la tabla tiene 5 filas, si las
        # contamos vamos a obtener el número 5; si usamos ese número 
        # como índice para agregar la fila, la fila se va a agregar al
        # final.
        indiceFinal=tabla.rowCount()

        # Antes de agregar la fila, queremos comprobar que la última
        # fila de la tabla no tenga campos vacíos. Esto lo hacemos
        # para que el usuario no pueda ingresar múltiples filas vacías
        # haciendo que el sistema detecte si la fila anterior está
        # vacía.
        ultimaFila = tabla.indexAt(indiceFinal - 1).row()

        # Obtenemos los datos de los cuatro campos que no deben estar
        # vacíos y los insertamos a todos en una lista.
        desc = tabla.item(ultimaFila, 0).text()
        cond = tabla.item(ultimaFila, 1).text()
        grupo = tabla.item(ultimaFila, 5).text()
        subgrupo = tabla.item(ultimaFila, 6).text()
        datosRequeridos=(desc, cond, grupo, subgrupo)

        # Si alguno de los datos esta vacío...
        if "" in datosRequeridos:
            # Se informa al usuario y termina la función antes de
            # ingresar la fila.
            mensaje="""   Ha agregado una fila y todavía no ha ingresado los
            datos. Ingreselos, guarde los cambios e intente nuevamente."""
            return PopUp("Error", mensaje)

        # Se añade la fila al final.
        tabla.insertRow(indiceFinal)
        # Se añaden campos de texto en todas las celdas ya que por
        # defecto no vienen.
        for numCol in tabla.columnCount() - 2:
            tabla.setItem(ultimaFila, numCol, QtWidgets.QTableWidgetItem()) 
        self.generarBotones(self.saveStock, self.deletestock, tabla, ultimaFila)


        

    # Estas funciones pueden funcionar sin estar en la clase. Si el
    # archivo main se hace muy largo, podemos moverlos a módulos.
    def fetchstock(self, busqueda):
        """Este método obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario.
        """
        tabla = self.pantallaStock.tableWidget

        # Se seleccionan los datos de la tabla de la base de datos
        # Método execute(): ejecuta código SQL
        sql="""SELECT s.descripcion, s.cant_condiciones, s.cant_reparacion,
               s.cant_baja, sub.descripcion, u.descripcion
               FROM stock s
               JOIN subgrupos sub
               ON s.id_subgrupo = sub.id
               JOIN ubicaciones u
               ON s.id_ubi=u.id_ubi
               """
        bbdd.cur.execute("SELECT * FROM stock""")

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
        for rowNum, rowData in enumerate(datos):
            # Se añade la fila a la tabla.
            # Método insertRow(int): inserta una fila en una QTable.
            tabla.insertRow(rowNum)

            # Inserta el texto en cada celda. Las celdas por defecto no
            # tienen nada, por lo que hay que añadir primero un item
            # que contenga el texto. No se puede establecer texto asi
            # nomás.
            # Método setIt
            # em(row, column, item): establece el item de
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
            total=rowData[2]+rowData[3]+rowData[4]
            tabla.setItem(rowNum, 4, QtWidgets.QTableWidgetItem(str(total)))

            # Para lo que está aca abajo propongo hacer un join para
            # ahorrar tiempo de proceso del programa. Además,
            # capacitaríamos a los chicos en algo fundamental de base
            # de datos. - Maxi
            bbdd.cur.execute(
                "select descripcion from subgrupos where id = ?", (rowData[5],))
            subgrupo = bbdd.cur.fetchone()[0]
            bbdd.cur.execute(
                "select descripcion from grupos where id=(select id_grupo from subgrupos where id = ?)", (rowData[5],))
            grupo = bbdd.cur.fetchone()[0]
            tabla.setItem(rowNum, 5, QtWidgets.QTableWidgetItem(str(grupo)))
            tabla.setItem(
                rowNum, 6, QtWidgets.QTableWidgetItem(str(subgrupo)))

            self.generarBotones(self.saveStock, self.deletestock, tabla, rowNum)

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
            lambda: self.obtenerFilaEditada(tabla, rowNum))

    def obtenerFilaEditada(self, tabla, row):
        """Esta método imprime la fila clickeada.
        Hay que verla después"""
        self.filaEditada = tabla.item(row, 0).text()
        print(self.filaEditada)

    def saveStock(self):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla de la base de datos"""
        # Se pregunta al usuario si desea guardar los cambios en la
        # tabla. NOTA: Esos tabs en el string son para mantener la
        # misma identación en todas las líneas así dedent funciona,
        # sino le da ansiedad.
        info = """        Esta acción no se puede deshacer.
        ¿Desea guardar los cambios hechos en la fila en la base de datos?"""
        popup=PopUp("Pregunta", info)
        if popup==QtWidgets.QMessageBox.StandardButton.Yes:
            # Se obtiene la fila en la que está el boton.
            index = self.pantallaStock.tableWidget.indexAt(self.sender().pos())
            row = index.row()

        print(self.filaEditada)

        id = bbdd.cur.execute("select id from subgrupos where descripcion = ?",(subgrupo,)).fetchone()
        print(id[0])
        bbdd.cur.execute("Update stock set descripcion = ?,cant_condiciones = ?,cant_reparacion=?,cant_baja = ?,id_subgrupo = ? where id = ?",(desc,cond,rep,baja,id[0],self.sender().id))
        bbdd.con.commit()
        self.fetchstock()

    def deletestock(self):
        """Este método elimina una fila de una tabla de la base de
        datos."""
        # Con esta variable guardamos el botón que presionó el usuario
        # a la vez que ejecutamos la ventana emergente.
        mensaje="""    Eliminar la herramienta/insumo eliminará también todos
        los registros relacionados (movimientos y reparaciones).
        ¿Desea eliminar la herramienta/insumo?"""
        popup=PopUp("Aviso", mensaje)

        # Si el usuario presionó el boton sí
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            # Busca la fila en la que está el botón
            row = (self.pantallaStock.tableWidget.indexAt(self.sender().pos())).row()
            desc = self.pantallaStock.tableWidget.item(row, 0).text()
            cond = self.pantallaStock.tableWidget.item(row, 1).text()
            rep = self.pantallaStock.tableWidget.item(row, 2).text()
            baja = self.pantallaStock.tableWidget.item(row, 3).text()
            grupo = self.pantallaStock.tableWidget.item(row, 5).text()
            subgrupo= self.pantallaStock.tableWidget.item(row, 6).text()
            todo = f"desc: {desc}, cant cond: {cond}, cant rep: {rep}, cant baja: {baja}, grupo: {grupo}, subgrupo: {subgrupo}"
            bbdd.cur.execute("INSERT INTO historial_de_cambios(id_usuario,fecha_hora,tipo,tabla,id_fila,datos_viejos) values(?,?,?,?,?,?) ", (self.usuario,time.datetime.now(),"eliminación","stock de herramientas",row,todo))            
            idStock=bbdd.cur.execute("SELECT id FROM stock WHERE descripcion = ?", (desc,))
            bbdd.cur.execute("DELETE FROM movimientos WHERE id_elem = ?", (idStock,))
            bbdd.cur.execute("DELETE FROM reparaciones WHERE id_herramienta = ?", (idStock,))
            bbdd.cur.execute("DELETE FROM stock WHERE descripcion = ?", (desc,))
            bbdd.con.commit()
            self.fetchstock()
        # TODO: guardar los cambios en el historial.

    def fetchalumnos(self):
        bbdd.cur.execute("SELECT * FROM personal where tipo!='profesor'")
        datos = bbdd.cur.fetchall()
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

    def fetchmovimientos(self):
        bbdd.cur.execute("SELECT * FROM movimientos")
        datos = bbdd.cur.fetchall()
        self.pantallaMovimientos.tableWidget.setRowCount(0)

        for rowNum, row in enumerate(datos):
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

            self.pantallaMovimientos.tableWidget.insertRow(rowNum)
            self.pantallaMovimientos.tableWidget.setItem(rowNum, 0, QtWidgets.QTableWidgetItem(str(
                bbdd.cur.execute("select descripcion from stock where id=?", (row[2],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(
                rowNum, 1, QtWidgets.QTableWidgetItem(str(estado)))
            self.pantallaMovimientos.tableWidget.setItem(rowNum, 2, QtWidgets.QTableWidgetItem(str(bbdd.cur.execute(
                "select nombre_apellido from personal where dni=?", (row[5],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(rowNum, 3, QtWidgets.QTableWidgetItem(str(
                bbdd.cur.execute("select tipo from personal where dni=?", (row[5],)).fetchone()[0])))
            self.pantallaMovimientos.tableWidget.setItem(
                rowNum, 4, QtWidgets.QTableWidgetItem(str(row[6])))
            self.pantallaMovimientos.tableWidget.setItem(
                rowNum, 5, QtWidgets.QTableWidgetItem(str(row[4])))
            self.pantallaMovimientos.tableWidget.setItem(
                rowNum, 6, QtWidgets.QTableWidgetItem(str(tipo)))
            self.pantallaMovimientos.tableWidget.setItem(rowNum, 7, QtWidgets.QTableWidgetItem(str(bbdd.cur.execute(
                "select nombre_apellido from personal where dni=(select id_panolero from turnos where id =?)", (row[1],)).fetchone()[0])))

            edit = BotonFila("editar.png", row[0])
            borrar = BotonFila("eliminar.png", row[0])
            tabla.setCellWidget(row_num, 8, edit)
            tabla.setCellWidget(row_num, 9, borrar)
            tabla.setRowHeight(0, 35)

        self.pantallaMovimientos.tableWidget.resizeColumnsToContents()
        self.pantallaMovimientos.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.pantallaMovimientos.tableWidget.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(4)


for fuente in os.listdir(os.path.join(os.path.abspath(os.getcwd()), f'blustock{os.sep}ui{os.sep}rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
                     f'ui{os.sep}rsc{os.sep}fonts{os.sep}{fuente}')
    )

window = MainWindow()
app.exec()
