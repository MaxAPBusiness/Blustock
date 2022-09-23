"""Este módulo crea un menú izquierdo.

Clases
------
    MenuIzquierdo(qtw.QToolBar): crea un menú izquierdo.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import os

os.chdir(f"{os.path.abspath(__file__)}/../../..")


class MenuIzquierdo(qtw.QToolBar):
    """Esta clase crea un menú izquierdo.

    Este menú izquierdo permite navegar por las gestiones. Está 
    integrado por un título descriptivo y botones de radio,
    QRadioButton.

    Hereda: PyQt6.QtWidgets.QToolBar

    Atributos
    ---------
        gestion1 : QRadioButton
            El botón de radio para ir a la gestión de herramientas.
        gestion2 : QRadioButton
            El botón de radio para ir a la gestión de movimientos.
        gestion3 : QRadioButton
            El botón de radio para ir a la gestión de turnos.
        gestion4 : QRadioButton
            El botón de radio para ir a la gestión de alumnos.
        gestion5 : QRadioButton
            El botón de radio para ir a la gestión de profesores.
        gestion6 : QRadioButton
            El botón de radio para ir a la gestión de grupos.
        gestion7 : QRadioButton
            El botón de radio para ir a la gestión de subgrupos.
        gestion8 : QRadioButton
            El botón de radio para ir a la gestión de alumnos
            históricos.
        gestion9 : QRadioButton
            El botón de radio para ir a la gestión de profesores
            históricos.
        gestion10 : QRadioButton
            El botón de radio para ir a la gestión de solicitudes.
        gestion11 : QRadioButton
            El botón de radio para ir a la gestión de usuarios.
        gestion12 : QRadioButton
            El botón de radio para ir a la gestión de administradores.
        gestion13 : QRadioButton
            El botón de radio para ir al historial de cambios.
    """

    def __init__(self):
        super().__init__()

        # Método setOrientation: cambia la orientación del menú / barra
        # de herramientas. Por defecto es horizontal. Nosotros la
        # hacemos vertical. El método toma como parámetro una variable
        # de la clase Orientation, que es subclase de Qt.
        self.setOrientation(qtc.Qt.Orientation.Vertical)
        self.setFloatable(False)
        self.setMovable(False)

        titulo = qtw.QLabel("Gestiones: ")
        titulo.setObjectName("gestiones-titulo")

        self.gestion1 = qtw.QRadioButton("GESTIÓN DE HERRAMIENTAS")
        self.gestion2 = qtw.QRadioButton("GESTIÓN DE MOVIMIENTOS")
        self.gestion3 = qtw.QRadioButton("GESTIÓN DE TURNOS")
        self.gestion4 = qtw.QRadioButton("GESTIÓN DE ALUMNOS")
        self.gestion5 = qtw.QRadioButton("GESTIÓN DE PROFESORES")
        self.gestion6 = qtw.QRadioButton("GESTIÓN DE GRUPOS")
        self.gestion7 = qtw.QRadioButton("GESTIÓN DE SUBGRUPOS")
        self.gestion8 = qtw.QRadioButton("GESTIÓN DE ALUMNOS\nHISTÓRICOS")
        self.gestion9 = qtw.QRadioButton("GESTIÓN DE PROFESORES\nHISTÓRICOS")
        self.gestion10 = qtw.QRadioButton("GESTIÓN DE SOLICITUDES")
        self.gestion11 = qtw.QRadioButton("GESTIÓN DE USUARIOS")
        self.gestion12 = qtw.QRadioButton("GESTIÓN DE ADMINISTRADORES")
        self.gestion13 = qtw.QRadioButton("HISTORIAL DE CAMBIOS")
        self.gestion1.toggle()

        container = qtw.QWidget()
        # setSizePolicy: regula si queremos que el widget se agrande al
        # agrandar la ventana o no. Tiene dos parámetros, la expansión
        # en ancho y en alto. Nosotros ponemos que sí a ambas para que
        # se expanda conforme agrandamos la pantalla.
        container.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)

        # Esto establece la altura y el ancho mínimos que puede tener el
        # menú.
        container.setMinimumHeight(800)
        container.setMinimumWidth(300)

        self.contenedorLayout = qtw.QGridLayout()
        self.contenedorLayout.addWidget(titulo, 0, 0, 1, 2)
        gestiones = (
            self.gestion1, self.gestion2, self.gestion3, self.gestion4,
            self.gestion5, self.gestion6, self.gestion7, self.gestion8,
            self.gestion9, self.gestion13
        )
        for i in range(len(gestiones)):
            gestiones[i].setObjectName("gestion")
            self.contenedorLayout.addWidget(gestiones[i], i+1, 0)
        self.contador = i
        self.gestion10.setObjectName("gestion")
        self.gestion11.setObjectName("gestion")
        self.gestion12.setObjectName("gestion")

        container.setLayout(self.contenedorLayout)

        # QScrollArea: es un área que, si se le da a un widget, le da
        # una barra para desplazarse (barra lateral)
        scroll = qtw.QScrollArea()
        scroll.setWidget(container)
        self.addWidget(scroll)

        with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/menu_izquierdo.qss", "r") as qss:
            self.setStyleSheet(qss.read())
