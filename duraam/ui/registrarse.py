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
        titulo.setObjectName("titulo") 
        subtitulo=qtw.QLabel("Recuerda que, para acceder a las bases de datos de gestión, tu registro debe ser autorizado por el administrador.")
        subtitulo.setObjectName("subtitulo") 

        label1=qtw.QLabel("Nombre y Apellido: ")
        label2=qtw.QLabel("Usuario: ")
        label3=qtw.QLabel("Contraseña: ")
        label4=qtw.QLabel("Confirmar contraseña: ")

        self.entry1=qtw.QLineEdit()
        self.entry2=qtw.QLineEdit()
        self.entry3=qtw.QLineEdit()
        self.entry4=qtw.QLineEdit()

        self.entry1.setObjectName("entry")
        self.entry2.setObjectName("entry")
        self.entry3.setObjectName("entry")
        self.entry4.setObjectName("entry")
    
        self.show1=qtw.QCheckBox()
        self.show2=qtw.QCheckBox()
        self.show1.stateChanged.connect(lambda:self.showPassword(self.show.isChecked()))
        self.show2.stateChanged.connect(lambda:self.showPassword(self.show.isChecked()))
        self.showPassword(False)

        self.confirmar=qtw.QPushButton("confirmar")
        self.confirmar.setObjectName("confirmar")
        self.ingresar=qtw.QPushButton("¿Ya estás registrado? Inicia sesión.")
        self.ingresar.sesetObjectName("boton-texto")

        layout=qtw.QGridLayout()
        layout.addWidget(titulo, 0, 0, 1, 3)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(label3, 3, 0)
        layout.addWidget(label4, 4, 0)
        layout.addWidget(self.entry1, 1, 1)
        layout.addWidget(self.entry2, 2, 1)
        layout.addWidget(self.entry3, 3, 1)
        layout.addWidget(self.entry4, 4, 1)
        layout.addWidget(self.show1, 3, 2)
        layout.addWidget(self.show2, 4, 2)
        layout.addWidget(self.confirmar, 3, 1, 1, 3)
        self.setLayout(layout)
    
    def showPassword(self, checked):
        if checked:
            self.entry3.setEchoMode(qtw.QLineEdit.EchoMode.Normal)
            self.entry4.setEchoMode(qtw.QLineEdit.EchoMode.Normal)
            self.show1.setIcon(qtg.QIcon("../images/hide.png"))
            self.show2.setIcon(qtg.QIcon("../images/hide.png"))
        else:
            self.entry3.setEchoMode(qtw.QLineEdit.EchoMode.Password)
            self.entry4.setEchoMode(qtw.QLineEdit.EchoMode.Password)
            self.show1.setIcon(qtg.QIcon("../images/mostrar.png"))
            self.show2.setIcon(qtg.QIcon("../images/mostrar.png"))