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
class Registrarse(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        titulo=qtw.QLabel("Regístrate")
        titulo.setObjectName("titulo-grande") 

        subtitulo=qtw.QLabel("Recuerda que, para acceder a las bases de datos de gestión,\ntu registro debe ser autorizado por el administrador.")
        subtitulo.setObjectName("subtitulo") 
        subtitulo.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        label1=qtw.QLabel("Nombre y Apellido: ")
        label2=qtw.QLabel("Usuario: ")
        label3=qtw.QLabel("Contraseña: ")
        label4=qtw.QLabel("Confirmar contraseña: ")

        label1.setObjectName("ingresar-label")
        label2.setObjectName("ingresar-label")
        label3.setObjectName("ingresar-label")
        label4.setObjectName("ingresar-label")

        self.entry1=qtw.QLineEdit()
        self.entry2=qtw.QLineEdit()
        self.entry3=qtw.QLineEdit()
        self.entry4=qtw.QLineEdit()

        self.entry1.setObjectName("modificar-entry")
        self.entry2.setObjectName("modificar-entry")
        self.entry3.setObjectName("modificar-entry")
        self.entry4.setObjectName("modificar-entry")

        self.entry2.setMaxLength(20)
        self.entry3.setMaxLength(20)
        self.entry4.setMaxLength(20)
    
        self.show1=qtw.QCheckBox()
        self.show2=qtw.QCheckBox()

        self.show1.stateChanged.connect(lambda:showPassword(self.entry3, self.show1, self.show1.isChecked()))
        self.show2.stateChanged.connect(lambda:showPassword(self.entry4, self.show2, self.show2.isChecked()))
        self.show1.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
        self.show2.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
        showPassword(self.entry3, self.show1, False)
        showPassword(self.entry4, self.show2, False)

        self.show1.setObjectName("show")
        self.show2.setObjectName("show")

        self.confirmar=qtw.QPushButton("confirmar")
        self.confirmar.setObjectName("confirmar-grande")
        self.confirmar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        self.ingresar=qtw.QPushButton("¿Ya estás registrado? Inicia sesión.")
        self.ingresar.setObjectName("boton-texto")
        self.ingresar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        layout=qtw.QGridLayout()
        layout.addWidget(titulo, 0, 0, 1, 3, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitulo, 1, 0, 1, 3, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label1, 2, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(label2, 3, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(label3, 4, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(label4, 5, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.entry1, 2, 1)
        layout.addWidget(self.entry2, 3, 1)
        layout.addWidget(self.entry3, 4, 1)
        layout.addWidget(self.entry4, 5, 1)
        layout.addWidget(self.show1, 4, 2)
        layout.addWidget(self.show2, 5, 2)
        layout.addWidget(self.confirmar, 6, 0, 1, 3, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.ingresar, 7, 0, 1, 3, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
    