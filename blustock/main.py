from PyQt6 import QtWidgets, QtCore, QtGui, uic
import sys
import os
os.chdir(f"{os.path.abspath(__file__)}{os.sep}..")
from db.bbdd import BBDD
from boton import BotonFila


bbdd=BBDD()
bbdd.refrescarBBDD()

class MainWindow(QtWidgets.QMainWindow):
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
        pantallaLogin.Ingresar.clicked.connect(lambda: self.login())

        pantallas=[pantallaLogin, pantallaAlumnos, pantallaGrupos, pantallaHerramientas,
                   pantallaMovimientos, pantallaOtroPersonal, pantallaSubgrupos, pantallaTurnos,
                   pantallaUsuarios]

        for pantalla in pantallas:

            self.stackedWidget.addWidget(pantalla)
            try:
                
                pantalla.tableWidget.horizontalHeader().setFont(QtGui.QFont("Oswald", 11))
                
            except:
                pass #¿Qué esperabas, un print, boludito?
        
        self.opcionStock.triggered.connect(self.fetchstock)
        self.opcionSubgrupos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.opcionGrupos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.opcionAlumnos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.opcionOtroPersonal.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.opcionTurnos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.opcionMovimientos.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.opcionUsuariosG.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(8))
        self.opcionHistorial.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(9))
        self.stackedWidget.addWidget(pantallaHistorial)

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
                self.stackedWidget.setCurrentIndex(1)
                self.menubar.show()

            else:
                self.findChild(QtWidgets.QLabel,"passwordState").setText("Contraseña incorrecta")
        else:
            self.findChild(QtWidgets.QLabel,"usuarioState").setText("Usuario incorrecto")

    def fetchstock(self):
        bbdd.cur.execute("SELECT * FROM stock")
        datos = bbdd.cur.fetchall()

        for row_num, row in enumerate(datos):
            self.findChild(QtWidgets.QTableWidget,"stock").insertRow(row_num)
            self.findChild(QtWidgets.QTableWidget,"stock").setItem(row_num, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.findChild(QtWidgets.QTableWidget,"stock").setItem(row_num, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.findChild(QtWidgets.QTableWidget,"stock").setItem(row_num, 2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.findChild(QtWidgets.QTableWidget,"stock").setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.findChild(QtWidgets.QTableWidget,"stock").setItem(row_num, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.findChild(QtWidgets.QTableWidget,"stock").setItem(row_num, 5,QtWidgets.QTableWidgetItem(str(row[2]+row[3]+row[4])))
            bbdd.cur.execute("select descripcion from subgrupos where id = ?",(row[5],))
            a = bbdd.cur.fetchone()
            bbdd.cur.execute("select descripcion from grupos where (select id_grupo from subgrupos where id = ?)",(row[5],))
            b = bbdd.cur.fetchone()
            self.findChild(QtWidgets.QTableWidget,"stock").setItem(row_num, 6,QtWidgets.QTableWidgetItem(str(b[0])))
            self.findChild(QtWidgets.QTableWidget,"stock").setItem(row_num, 7,QtWidgets.QTableWidgetItem(str(a[0])))
            edit = BotonFila("editar.png")
            borrar = BotonFila("eliminar.png")
            self.findChild(QtWidgets.QTableWidget,"stock").setCellWidget(row_num, 8, edit)
            self.findChild(QtWidgets.QTableWidget,"stock").setCellWidget(row_num, 9, borrar)
            self.findChild(QtWidgets.QTableWidget,"stock").setRowHeight(0, 35)
            self.findChild(QtWidgets.QTableWidget,"stock").resizeColumnsToContents()


        self.stackedWidget.setCurrentIndex(3)

    

app=QtWidgets.QApplication(sys.argv)

for fuente in os.listdir(os.path.join(os.path.abspath(os.getcwd()), f'rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
            f'rsc{os.sep}fonts{os.sep}{fuente}')
        )
    
window=MainWindow()
app.exec()
