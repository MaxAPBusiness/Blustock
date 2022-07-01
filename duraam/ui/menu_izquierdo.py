import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import os

os.chdir(f"{os.path.abspath(__file__)}/../../..")

class MenuIzquierdo(qtw.QToolBar):
    def __init__(self):
        super().__init__()

        self.setOrientation(qtc.Qt.Orientation.Vertical)
        self.setFloatable(False)
        self.setMovable(False)

        titulo=qtw.QLabel("Gestiones: ")
        titulo.setObjectName("gestiones-titulo")
        self.gestion1=qtw.QRadioButton('GESTIÓN DE HERRAMIENTAS')
        self.gestion2=qtw.QRadioButton('Gestión de Herramientas viejo')
        self.gestion3=qtw.QRadioButton('GESTIÓN DE TURNOS')
        self.gestion4=qtw.QRadioButton('GESTIÓN DE ALUMNOS')
        self.gestion5=qtw.QRadioButton('GESTIÓN DE PROFESORES')
        self.gestion1.setObjectName("gestion")
        self.gestion2.setObjectName("gestion")
        self.gestion3.setObjectName("gestion")
        self.gestion4.setObjectName("gestion")
        self.gestion5.setObjectName("gestion")

        self.addWidget(titulo)
        self.addWidget(self.gestion1)
        self.addWidget(self.gestion2)
        self.addWidget(self.gestion3)
        self.addWidget(self.gestion4)
        self.addWidget(self.gestion5)
        self.gestion1.toggle()
        
        with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/menu_izquierdo.qss", "r") as qss:
            self.setStyleSheet(qss.read())