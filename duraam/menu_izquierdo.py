import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc


class MenuIzquierdo(qtw.QToolBar):
    def __init__(self):
        super().__init__()

        self.setOrientation(qtc.Qt.Orientation.Vertical)
        self.setFloatable(False)
        self.setMovable(False)

        titulo=qtw.QLabel("Gestiones: ")
        titulo.setObjectName("titulo")
        self.gestion1=qtw.QRadioButton('Gestión de herramientas')
        self.gestion2=qtw.QRadioButton('Gestión de herramientas (DUPLICADO)')
        self.gestion1.setObjectName("gestion")
        self.gestion2.setObjectName("gestion")
        self.addWidget(titulo)
        self.addWidget(self.gestion1)
        self.addWidget(self.gestion2)