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
        self.gestion2=qtw.QRadioButton('GESTIÓN DE MOVIMIENTOS')
        self.gestion3=qtw.QRadioButton('GESTIÓN DE TURNOS')
        self.gestion4=qtw.QRadioButton('GESTIÓN DE ALUMNOS')
        self.gestion5=qtw.QRadioButton('GESTIÓN DE PROFESORES')
        self.gestion6=qtw.QRadioButton('GESTIÓN DE GRUPOS')
        self.gestion7=qtw.QRadioButton('GESTIÓN DE SUBGRUPOS')
        self.gestion8=qtw.QRadioButton('GESTIÓN DE ALUMNOS\nHISTÓRICOS')
        self.gestion9=qtw.QRadioButton('GESTIÓN DE PROFESORES\nHISTÓRICOS')
        self.gestion10=qtw.QRadioButton('SOLICITUDES')

        container=qtw.QWidget()
        container.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)
        container.setMinimumHeight(700)
        container.setMinimumWidth(300)
        containerLayout=qtw.QGridLayout()

        containerLayout.addWidget(titulo, 0, 0, 1, 2)

        self.gestiones=[self.gestion1, self.gestion2, self.gestion3, self.gestion4, 
                        self.gestion5, self.gestion6, self.gestion7, self.gestion8,
                        self.gestion9, self.gestion10]
        
        for i in range(len(self.gestiones)):
            self.gestiones[i].setObjectName("gestion")
            containerLayout.addWidget(self.gestiones[i], i+1, 0)

        self.gestion1.toggle()
        container.setLayout(containerLayout)

        scroll=qtw.QScrollArea()
        scroll.setWidget(container)

        self.addWidget(scroll)
        
        with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/menu_izquierdo.qss", "r") as qss:
            self.setStyleSheet(qss.read())