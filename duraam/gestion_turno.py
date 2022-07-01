import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import sqlite3 as db
import os

con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur = con.cursor()


def mostrarMensaje(title, msg, info):
    window = qtw.QMessageBox()
    if title == "Error":
        window.setIcon(qtw.QMessageBox.Icon.Critical)
    elif title == "Advertencia" or title == "Warning":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
    elif title == "Aviso" or title == "Information":
        window.setIcon(qtw.QMessageBox.Icon.Information)
    else:
        print("Error de titulo")
        return
    window.setText(msg)
    window.setInformativeText(info)
    window.setWindowTitle(title)
    window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    window.exec()


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        pixmap = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png")
        label1 = qtw.QLabel("")
        label1.setPixmap(pixmap)
        self.setMaximumSize(1140, 600)
        self.setMinimumSize(1140, 400)
        self.widgetCentral = qtw.QWidget()
        self.fondo = qtw.QWidget()
        self.fondo.setObjectName("fondo")
        self.titulo = qtw.QLabel("DURAAM")
        self.titulo.setObjectName("titulo")
        self.Actualizar = qtw.QPushButton("Actualizar")
        self.Actualizar.setObjectName("actualizar")
        self.agregar = qtw.QPushButton("Agregar")
        self.agregar.setObjectName("agregar")
        self.checkbox1 = qtw.QRadioButton("Nombre")
        self.checkbox2 = qtw.QRadioButton("Grupo")
        self.checkbox3 = qtw.QRadioButton("Subgrupo")
        self.label2 = qtw.QLabel("Ordenar por:")
        self.entry = qtw.QLineEdit()
        self.entry.setObjectName("entry")
        tabla = qtw.QTableWidget(self)
        tabla.setObjectName("tabla")
        tabla.setColumnCount(8)
        campos = ["#", "Descripción", "En condiciones",
                  "En reparación", "De baja", "Grupo", "SubGrupo",""]
        cur.execute('SELECT * FROM HERRAMIENTAS')
        query = cur.fetchall()
        tabla.setRowCount(len(query))
        self.mostrarDatos(tabla, campos)
        self.agregar.clicked.connect(lambda: self.editar(campos, []))
        self.Actualizar.clicked.connect(
            lambda: self.mostrarDatos(tabla, campos))
        layout = qtw.QGridLayout()
        layout.addWidget(self.fondo, 1, 1, 1, 9)
        layout.addWidget(label1, 1, 1)
        layout.addWidget(self.titulo, 1, 2)
        layout.addWidget(self.label2, 3, 2)
        layout.addWidget(self.checkbox1, 3, 3)
        layout.addWidget(self.checkbox2, 3, 4)
        layout.addWidget(self.checkbox3, 3, 5)
        layout.addWidget(self.entry, 3, 1)
        layout.addWidget(self.Actualizar, 2, 1)
        layout.addWidget(self.agregar, 5, 1)
        layout.addWidget(tabla, 4, 1, 1, 9)

        self.widgetCentral.setLayout(layout)
        self.setCentralWidget(self.widgetCentral)

    def editar(self, campos, datos):
        editar = Editar(campos, datos)
        editar.show()

    def mostrarDatos(self, tabla, campos):
        cur.execute('SELECT * FROM HERRAMIENTAS')
        query = cur.fetchall()
        tabla.setRowCount(len(query))
        for i in range(len(query)):
            for j in range(len(query[i])):
                tabla.setItem(i, j, qtw.QTableWidgetItem(str(query[i][j])))
            botonUwU = qtw.QPushButton("Editar")
            botonUwU.clicked.connect(lambda: self.editar(campos, query[i]))
            tabla.setCellWidget(i, 7, botonUwU)


class Editar(qtw.QWidget):
    def __init__(self, campos, datos):
        super().__init__()
        layout = qtw.QGridLayout()
        if datos:
            label = qtw.QLabel(campos[0])
            label2 = qtw.QLabel(str(datos[0]))
            layout.addWidget(label, 0, 0)
            layout.addWidget(label2, 0, 1)
            self.entry1 = qtw.QLineEdit(datos[1])
            self.entry2 = qtw.QSpinBox()
            self.entry3 = qtw.QSpinBox()
            self.entry4 = qtw.QSpinBox()
            self.entry2.setValue(datos[2])
            self.entry3.setValue(datos[2])
            self.entry4.setValue(datos[2])
            self.entry5 = qtw.QLineEdit(datos[5])
            self.entry6 = qtw.QLineEdit(datos[6])
        else:
            self.entry1 = qtw.QLineEdit()
            self.entry2 = qtw.QSpinBox()
            self.entry3 = qtw.QSpinBox()
            self.entry4 = qtw.QSpinBox()
            self.entry5 = qtw.QLineEdit()
            self.entry6 = qtw.QLineEdit()
        layout.addWidget(self.entry1, 1, 1)
        layout.addWidget(self.entry2, 2, 1)
        layout.addWidget(self.entry3, 3, 1)
        layout.addWidget(self.entry4, 4, 1)
        layout.addWidget(self.entry5, 5, 1)
        layout.addWidget(self.entry6, 6, 1)
        for i in range(1, len(campos)):
            label = qtw.QLabel(campos[i])
            layout.addWidget(label, i, 0)

        confirmar = qtw.QPushButton("Confirmar")
        confirmar.clicked.connect(lambda: self.confirmarr(datos))
        layout.addWidget(confirmar, 7, 0, 1, 2)
        self.setLayout(layout)

    def confirmarr(self, datos):
        global mostrarMensaje
        if datos:
            cur.execute("""
            UPDATE HERRAMIENTAS 
            SET DESC_LARGA=?, CANT_CONDICIONES=?, CANT_REPARACION=?, CANT_BAJA=?,ID_GRUPO=?,ID_SUBGRUPO=? WHERE ID=?""", (
                self.entry1.text(), self.entry2.value(), self.entry3.value(
                ), self.entry4.value(), self.entry5.text(), self.entry1.text(), datos[0],
            ))
            con.commit()
            mostrarMensaje("Information", "Aviso",
                           "Se han modificado los datos.")
            
        else:
            cur.execute("INSERT INTO HERRAMIENTAS VALUES(NULL, ?, ?, ?, ?, ?, ?) ", (
                self.entry1.text(), self.entry2.value(), self.entry3.value(
                ), self.entry4.value(), self.entry5.text(), self.entry6.text(),
            ))
            con.commit()
            mostrarMensaje("Information", "Aviso",
                           "Se ha ingresado una herramienta.")


app = qtw.QApplication(sys.argv)
window = MainWindow()
with open(f"{os.path.abspath(os.getcwd())}/duraam/gestion.qss", 'r') as css:
    window.setStyleSheet(css.read())
window.show()
app.exec()
