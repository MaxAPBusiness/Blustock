from PyQt6 import QtWidgets, QtCore, QtGui, uic
import sys
import os

os.chdir(f"{os.path.abspath(__file__)}{os.sep}..")

class PantallaAlumnos(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}login.ui'), self)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}main.ui'), self)
        pantallaAlumnos=PantallaAlumnos()
        self.stackedWidget.addWidget(pantallaAlumnos)

        with open(os.path.join(os.path.abspath(os.getcwd()), 'styles.qss'), 'r') as file:
            self.setStyleSheet(file.read())
        self.stackedWidget.setCurrentIndex(2)
        self.show()

app=QtWidgets.QApplication(sys.argv)
QtGui.QFontDatabase.addApplicationFont("rsc/fonts/Oswald-VariableFont_wght.ttf")
window=MainWindow()
app.exec()
print("God")