# gestion_herramientas.py: la gestión de herramientas. Contiene una tabla, que muestra 
#                          la tabla de la base de datos; una barra de buscador; botones para 
#                          ordenar alfabéticamente la tabla por nombre, grupo y subgrupo de 
#                          herramientas; botones para editar y eliminar los datos; un botón
#                          para agregar herramientas. 
#                          Para editar y agregar, aparece un submenú con los datos a introducir.

# Se importan las librerías.
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import sqlite3 as db
import os

from show_password import showPassword

# Se hace una conexión a la base de datos
os.chdir(f"{os.path.abspath(__file__)}/../../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()


# clase GestiónHerramientas: ya explicada. Es un widget que después se ensambla en un stackwidget en main.py.
class IniciarSesion(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        titulo=qtw.QLabel("""
  Bienvenido al sistema de gestión de bases de datos del pañol!
  Inicia sesión
        """)
        titulo.setObjectName("titulo") 
        titulo.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        label1=qtw.QLabel("Usuario: ")
        label2=qtw.QLabel("Contraseña: ")

        label1.setObjectName("ingresar-label")
        label2.setObjectName("ingresar-label")

        self.entry1=qtw.QLineEdit()
        self.entry2=qtw.QLineEdit()

        self.entry1.setObjectName("modificar-entry")
        self.entry2.setObjectName("modificar-entry")

        self.entry1.setMaxLength(20)
        self.entry2.setMaxLength(20)

        self.show=qtw.QCheckBox()
        self.show.stateChanged.connect(lambda:showPassword(self.entry2, self.show, self.show.isChecked()))
        showPassword(self.entry2, self.show, False)
        self.show.setObjectName("show")
        self.show.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        self.confirmar=qtw.QPushButton("confirmar")
        self.confirmar.setObjectName("confirmar-grande")
        self.confirmar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        self.registrarse=qtw.QPushButton("¿No tienes una cuenta? Regístrate")
        self.registrarse.setObjectName("boton-texto")
        self.registrarse.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        layout=qtw.QGridLayout()
        layout.addWidget(titulo, 0, 0, 1, 3, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label1, 1, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(label2, 2, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.entry1, 1, 1)
        layout.addWidget(self.entry2, 2, 1)
        layout.addWidget(self.show, 2, 2)
        layout.addWidget(self.confirmar, 3, 0, 1, 3, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.registrarse, 4, 0, 1, 3, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
    