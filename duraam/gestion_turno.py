import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        pixmap = qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png")
        label1=qtw.QLabel("")
        label1.setPixmap(pixmap)
        self.setMaximumSize(1140,600)
        self.setMinimumSize(1140,400)
        self.widgetCentral=qtw.QWidget()
        self.fondo=qtw.QWidget()
        self.fondo.setObjectName("fondo")
        self.titulo=qtw.QLabel("DURAAM")
        self.titulo.setObjectName("titulo")
        self.Actualizar=qtw.QPushButton("Actualizar")
        self.Actualizar.setObjectName("actualizar")
        self.agregar=qtw.QPushButton("Agregar")
        self.agregar.setObjectName("agregar")
        self.checkbox1=qtw.QRadioButton("Nombre")
        self.checkbox2=qtw.QRadioButton("Grupo")
        self.checkbox3=qtw.QRadioButton("Fecha")
        self.label2=qtw.QLabel("Ordenar por:")
        self.entry=qtw.QLineEdit()
        self.entry.setObjectName("entry")
        tabla=qtw.QTableWidget(self)
        tabla.setObjectName("tabla")
        tabla.setColumnCount(11)
        tabla.setRowCount(5)
        tabla.setHorizontalHeaderLabels(["#", "Nombre", "Descripcion", "C","R","B","Grupo","SubGrupo","Acciones","Fecha","  "])
        for i in range(5):
            botonUwU=qtw.QPushButton("Editar")
            tabla.setCellWidget(i, 10, botonUwU);
        layout=qtw.QGridLayout()
        layout.addWidget(self.fondo,1,1,1,9)
        layout.addWidget(label1, 1,1)
        layout.addWidget(self.titulo,1,2)
        layout.addWidget(self.label2,3,2)
        layout.addWidget(self.checkbox1,3,3)
        layout.addWidget(self.checkbox2,3,4)
        layout.addWidget(self.checkbox3,3,5)
        layout.addWidget(self.entry,3,1)
        layout.addWidget(self.Actualizar,2,1)
        layout.addWidget(self.agregar,5,1)
        layout.addWidget(tabla,4,1,1,9)

        self.widgetCentral.setLayout(layout)
        self.setCentralWidget(self.widgetCentral)
        
        
      


app = qtw.QApplication(sys.argv)
window = MainWindow()
with open(f"{os.path.abspath(os.getcwd())}/duraam/gestion.qss", 'r') as css:
    window.setStyleSheet(css.read())
window.show()
app.exec()