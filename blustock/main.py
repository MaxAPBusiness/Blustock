"""El archivo principal. Genera la ventana principal y ejecuta la 
aplicación.

Clases:
    MainWindow(qtw.QMainWindow): crea la ventana principal.

Objetos:
    app: La aplicación principal.
"""
from PyQt6 import QtWidgets, QtCore, QtGui, uic
import sys
import os
os.chdir(f"{os.path.abspath(__file__)}{os.sep}..")
from db.bbdd import BBDD
from uis.mostrar_mensaje import MensajeEmergente
from boton import BotonFila


bbdd=BBDD()
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
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}main.ui'), self)
        self.menubar.hide()

        pantallaAlumnos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}alumnos.ui'), pantallaAlumnos)
        pantallaGrupos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}grupos.ui'), pantallaGrupos)
        pantallaHerramientas=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}herramientas.ui'), pantallaHerramientas)
        pantallaHistorial=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}historial.ui'), pantallaHistorial)
        pantallaMovimientos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}movimientos.ui'), pantallaMovimientos)
        pantallaOtroPersonal=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}otro_personal.ui'), pantallaOtroPersonal)
        pantallaSubgrupos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}subgrupos.ui'), pantallaSubgrupos)
        pantallaTurnos=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}turnos.ui'), pantallaTurnos)
        pantallaUsuarios=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}usuarios.ui'), pantallaUsuarios)
        pantallaLogin=QtWidgets.QWidget()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}login.ui'), pantallaLogin)
        pantallaLogin.Ingresar.clicked.connect(self.login)

        pantallas=(pantallaLogin, pantallaAlumnos, pantallaGrupos, pantallaHerramientas,
                   pantallaMovimientos, pantallaOtroPersonal, pantallaSubgrupos, pantallaTurnos,
                   pantallaUsuarios)

        for pantalla in pantallas:
            self.stackedWidget.addWidget(pantalla)
            try:
                pantalla.tableWidget.horizontalHeader().setFont(QtGui.QFont("Oswald", 11))
                
            except:
                pass #¿Qué esperabas, un print, boludito?
        
        self.stackedWidget.addWidget(pantallaHistorial)
        self.opcionStock.triggered.connect(self.fetchstock)
        self.opcionSubgrupos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.opcionGrupos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.opcionAlumnos.triggered.connect(self.fetchalumnos)
        self.opcionOtroPersonal.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.opcionTurnos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.opcionMovimientos.triggered.connect(self.fetchmovimientos)
        self.opcionUsuariosG.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(8))
        self.opcionHistorial.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(9))

        with open(os.path.join(os.path.abspath(os.getcwd()), 'styles.qss'), 'r') as file:
            self.setStyleSheet(file.read())
        self.stackedWidget.setCurrentIndex(0)
        self.show()

    def login(self):
        bbdd.cur.execute("SELECT count(*) FROM personal WHERE usuario = ?",(self.findChild(QtWidgets.QLineEdit,"usuariosLineEdit").text(),))
        check = bbdd.cur.fetchone()
        if check[0] >= 1:
            bbdd.cur.execute("SELECT count(*) FROM personal WHERE usuario = ? and contrasena = ?",(self.findChild(QtWidgets.QLineEdit,"usuariosLineEdit").text(),self.findChild(QtWidgets.QLineEdit,"passwordLineEdit").text(),))
            check = bbdd.cur.fetchone()
            if check[0] == 1:
                self.fetchstock()
                self.menubar.show()

            else:
                self.findChild(QtWidgets.QLabel,"passwordState").setText("Contraseña incorrecta")
        else:
            self.findChild(QtWidgets.QLabel,"usuarioState").setText("Usuario incorrecto")

    def fetchstock(self):
        """Esta función obtiene los datos de la tabla stock y los
        inserta en la tabla de la interfaz de usuario."""

        # Se seleccionan los datos de la tabla de la base de datos
        # Método execute(): ejecuta código SQL
        bbdd.cur.execute("SELECT * FROM stock")

        # Método fetchall: obtiene los datos seleccionados y los
        # transforma en una lista.
        datos = bbdd.cur.fetchall()

        # Se busca la tabla de la pantalla stock para insertarle los
        # datos.
        tabla = self.findChild(QtWidgets.QTableWidget,"stock")
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
            # QTableWidgetItem: un item de tabla. Se puede crear con
            # texto por defecto.
            tabla.setItem(row_num, 0, QtWidgets.QTableWidgetItem(str(row[1])))
            tabla.setItem(row_num, 1,QtWidgets.QTableWidgetItem(str(row[2])))
            tabla.setItem(row_num, 2, QtWidgets.QTableWidgetItem(str(row[3])))
            tabla.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row[4])))
            tabla.setItem(row_num, 4,QtWidgets.QTableWidgetItem(str(row[2]+row[3]+row[4])))

            # Para lo que está aca abajo propongo hacer un join para 
            # ahorrar tiempo de proceso del programa. Si no quieren
            # hacerlo los chicos no pasa nada, lo hago yo. - Maxi
            bbdd.cur.execute("select descripcion from subgrupos where id = ?",(row[5],))
            a = bbdd.cur.fetchone()
            bbdd.cur.execute("select descripcion from grupos where id=(select id_grupo from subgrupos where id = ?)",(row[5],))
            b = bbdd.cur.fetchone()
            tabla.setItem(row_num, 5,QtWidgets.QTableWidgetItem(str(b[0])))
            tabla.setItem(row_num, 6,QtWidgets.QTableWidgetItem(str(a[0])))

            # Se crean dos botones: uno de editar y uno de eliminar
            # Para saber que hacen BotonFila, vayan al código de la
            # clase.
            edit = BotonFila("editar.png")
            edit.clicked.connect(self.updatestock)
            borrar = BotonFila("eliminar.png")
            borrar.clicked.connect(self.deletestock)

            # Se añaden los botones a cada fila.
            # Método setCellWidget(row, column, widget): añade un
            # widget a la celda de una tabla.
            tabla.setCellWidget(row_num, 7, edit)
            tabla.setCellWidget(row_num, 8, borrar)

        # Método setRowHeight: cambia la altura de una fila.
        tabla.setRowHeight(0, 35)
        tabla.resizeColumnsToContents()

        # Método setSectionResizeMode(column, ResizeMode): hace que una
        # columna de una tabla se expanda o no automáticamente conforme
        # se extiende la tabla.
        tabla.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(5,QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(6,QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(3)
        tabla.cellClicked.connect(lambda row: self.obtenerFilaEditada(tabla, row))


    def obtenerFilaEditada(self,tabla,row):
        """Esta función imprime la fila clickeada.
        Hay que verla después"""
        tabla = self.findChild(QtWidgets.QTableWidget,"stock")
        global filaEditada
        filaEditada = tabla.item(row, 0).text()
        print(filaEditada)

    def updatestock(self):
        """Esta función permite actualizar los datos modificados en la
        tabla"""
        # Esta función todavía no esta terminada, cuando esté la voy a
        # comentar. :)
        global filaEditada
        tabla = self.findChild(QtWidgets.QTableWidget,"stock")
        index = tabla.indexAt(self.sender().pos())
        row = index.row()
        desc = tabla.item(row, 0).text()    
        cond = tabla.item(row, 1).text()
        rep = tabla.item(row, 2).text()
        baja = tabla.item(row, 3).text()
        subgrupo = tabla.item(row, 6).text()
        id = bbdd.cur.execute("select id from subgrupos where descripcion = ?",(subgrupo,)).fetchone()
        print(id[0])
        bbdd.cur.execute("Update stock set descripcion = ?,cant_condiciones = ?,cant_reparacion=?,cant_baja = ?,id_subgrupo = ? where descripcion = ?",(desc,cond,rep,baja,id[0],filaEditada))
        bbdd.con.commit()
        self.fetchstock()

    def deletestock(self):
        """Esta función elimina la fila de la tabla"""   
        # Para saber que hace la clase, entrar al archivo
        # mensaje_emergente.py
        mensaje=MensajeEmergente("Pregunta", "Atención", "¿Desea eliminar la herramienta/insumo?")

        # Con esta variable guardamos el botón que presionó el usuario.
        botonPresionado=mensaje.exec()

        # Si el usuario presionó el boton si
        if botonPresionado == QtWidgets.QMessageBox.StandardButton.Yes:
            tabla = self.findChild(QtWidgets.QTableWidget,"stock")
            # Busca la fila en la que está el botón
            row = (tabla.indexAt(self.sender().pos())).row()
            desc = tabla.item(row, 0).text()
            bbdd.cur.execute("DELETE FROM stock WHERE descripcion = ?", (desc,))
            bbdd.con.commit()
            self.fetchstock()
        # TODO: guardar los cambios en el historial/implementar los 
        # usuarios correctamente. 


    def fetchalumnos(self):
        bbdd.cur.execute("SELECT * FROM personal where tipo!='profesor'")
        datos = bbdd.cur.fetchall()
        tabla = self.findChild(QtWidgets.QTableWidget,"alumnos")
        tabla.setRowCount(0)

        for row_num, row in enumerate(datos):
            tabla.insertRow(row_num)
            tabla.setItem(row_num, 0, QtWidgets.QTableWidgetItem(str(row_num+1)))
            tabla.setItem(row_num, 1, QtWidgets.QTableWidgetItem(str(row[0])))
            tabla.setItem(row_num, 2,QtWidgets.QTableWidgetItem(str(row[1])))
            tabla.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row[2])))
            edit = BotonFila("editar.png")
            borrar = BotonFila("eliminar.png")
            tabla.setCellWidget(row_num, 4, edit)
            tabla.setCellWidget(row_num, 5, borrar)
            tabla.setRowHeight(0, 35)

        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(1)

    def fetchmovimientos(self):
        bbdd.cur.execute("SELECT * FROM movimientos")
        datos = bbdd.cur.fetchall()
        tabla = self.findChild(QtWidgets.QTableWidget,"movimientos")
        tabla.setRowCount(0)

        for row_num, row in enumerate(datos):
            if row[3]==0:
                estado="Baja" 
            if row[3]==1:
                estado="Condiciones"
            if row[3]==2:
                estado="Reparacion"
            if row[7]==0:
                tipo="Devolucion" 
            if row[7]==1:
                tipo="Retiro"
            if row[7]==2:
                tipo="Ingreso de materiales"
            
            tabla.insertRow(row_num)
            tabla.setItem(row_num, 0, QtWidgets.QTableWidgetItem(str(bbdd.cur.execute("select descripcion from stock where id=?",(row[2],)).fetchone()[0])))
            tabla.setItem(row_num, 1, QtWidgets.QTableWidgetItem(str(estado)))
            tabla.setItem(row_num, 2,QtWidgets.QTableWidgetItem(str(bbdd.cur.execute("select nombre_apellido from personal where dni=?",(row[5],)).fetchone()[0])))
            tabla.setItem(row_num, 3,QtWidgets.QTableWidgetItem(str(bbdd.cur.execute("select tipo from personal where dni=?",(row[5],)).fetchone()[0])))            
            tabla.setItem(row_num, 4,QtWidgets.QTableWidgetItem(str(row[6])))  
            tabla.setItem(row_num, 5,QtWidgets.QTableWidgetItem(str(row[4])))  
            tabla.setItem(row_num, 6,QtWidgets.QTableWidgetItem(str(tipo)))
            tabla.setItem(row_num, 7,QtWidgets.QTableWidgetItem(str(bbdd.cur.execute("select nombre_apellido from personal where dni=(select id_panolero from turnos where id =?)",(row[1],)).fetchone()[0])))

            edit = BotonFila("editar.png")
            borrar = BotonFila("eliminar.png")
            tabla.setCellWidget(row_num, 8, edit)
            tabla.setCellWidget(row_num, 9, borrar)
            tabla.setRowHeight(0, 35)

        tabla.resizeColumnsToContents()
        tabla.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.stackedWidget.setCurrentIndex(4)

app=QtWidgets.QApplication(sys.argv)

for fuente in os.listdir(os.path.join(os.path.abspath(os.getcwd()), f'rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
            f'rsc{os.sep}fonts{os.sep}{fuente}')
        )
    
window=MainWindow()
app.exec()
