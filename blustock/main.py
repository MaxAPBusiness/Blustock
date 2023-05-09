from PyQt6 import QtWidgets, uic, QtCore,QtGui
import sys
from penegordo_ui import Ui_Inicio

class Penegordo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("penegordo.ui",self)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("teodio.ui",self)
        with open('sopas (1).qss', 'r') as file:
            self.setStyleSheet(file.read())
        self.inicio = Ui_Inicio()
        self.penegordo = Penegordo()
        self.stackedWidget.addWidget(self.penegordo)
        self.stackedWidget.setCurrentIndex(0)
        self.show()

app=QtWidgets.QApplication(sys.argv)
window=Ui()
app.exec()
print("God")