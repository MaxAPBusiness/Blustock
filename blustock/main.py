from PyQt6 import QtWidgets, QtCore, QtGui, uic
import sys
import os
os.chdir(f"{os.path.abspath(__file__)}{os.sep}..")
from db.bbdd import BBDD

bbdd=BBDD()
bbdd.refrescarBBDD()

"""class PantallaAlumnos(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}penegordo.ui'), self)"""

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}main.ui'), self)
        """pantallaAlumnos=PantallaAlumnos()
        self.stackedWidget.addWidget(pantallaAlumnos)"""

        with open(os.path.join(os.path.abspath(os.getcwd()), 'styles.qss'), 'r') as file:
            self.setStyleSheet(file.read())
        self.stackedWidget.setCurrentIndex(0)
        self.show()

    """def login(self):
        db.cur.execute("SELECT count(*) FROM personal WHERE usuario = ?",(self.usuariosLineEdit.text(),))
        check = db.cur.fetchall()
        if check == 1:
            db.cur.execute("SELECT count(*) FROM personal WHERE usuario = ? and contrasena = ?",(self.usuariosLineEdit.text(),self.passwordLineEdit.text(),))
            check = db.cur.fetchall()
            if check == 1:
                self.stackedWidget.setCurrentIndex(1)
        self.show()"""

app=QtWidgets.QApplication(sys.argv)

for fuente in os.listdir(
    os.path.join(os.path.abspath(os.getcwd()), f'rsc{os.sep}fonts')):
    QtGui.QFontDatabase.addApplicationFont(
        os.path.join(os.path.abspath(os.getcwd()),
            f'rsc{os.sep}fonts{os.sep}{fuente}')
        )
    
window=MainWindow()
app.exec()
print("God")