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
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Advertencia" or title == "Warning":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Aviso" or title == "Information":
        window.setIcon(qtw.QMessageBox.Icon.Information)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Pregunta" or title == "Question":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
        window.setStandardButtons(
            qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No)
    else:
        print("Error de titulo")
        return
    window.setText(msg)
    window.setInformativeText(info)
    window.setWindowTitle(title)
    return window.exec()


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.widgetCentral = qtw.QWidget()

        pixmap = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png")
        label1 = qtw.QLabel("")
        label1.setPixmap(pixmap)

        self.fondo = qtw.QWidget()
        self.fondo.setObjectName("fondo")

        self.titulo = qtw.QLabel("DURAAM")
        self.titulo.setObjectName("titulo")

        self.actualizar = qtw.QPushButton("actualizar")
        self.actualizar.setObjectName("actualizar")

        self.agregar = qtw.QPushButton("Agregar")
        self.agregar.setObjectName("agregar")

        self.label2 = qtw.QLabel("Ordenar por:")
        self.checkbox1 = qtw.QRadioButton("Nombre")
        self.checkbox2 = qtw.QRadioButton("Grupo")
        self.checkbox3 = qtw.QRadioButton("Subgrupo")

        self.checkbox1.toggle.connect(self.ordenar(self.checkbox1))
        self.checkbox2.toggle.connect(self.ordenar(self.checkbox2))
        self.checkbox3.toggle.connect(self.ordenar(self.checkbox3))

        self.entry = qtw.QLineEdit()
        self.entry.setObjectName("entry")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(9)
        self.campos = ["ID", "Descripción", "En condiciones",
                       "En reparación", "De baja", "Grupo", "SubGrupo", "", ""]
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        cur.execute('SELECT * FROM HERRAMIENTAS')
        query = cur.fetchall()
        self.tabla.setRowCount(len(query))
        self.mostrarDatos()

        self.agregar.clicked.connect(
            lambda: self.editar(self.campos, 'agregar'))
        self.actualizar.clicked.connect(
            lambda: self.mostrarDatos(self.tabla, self.campos))
        layout = qtw.QGridLayout()
        layout.addWidget(self.fondo, 1, 1, 1, 9)
        layout.addWidget(label1, 1, 1)
        layout.addWidget(self.titulo, 1, 2)
        layout.addWidget(self.label2, 3, 2)
        layout.addWidget(self.checkbox1, 3, 3)
        layout.addWidget(self.checkbox2, 3, 4)
        layout.addWidget(self.checkbox3, 3, 5)
        layout.addWidget(self.entry, 3, 1)
        layout.addWidget(self.actualizar, 2, 1)
        layout.addWidget(self.agregar, 5, 1)
        layout.addWidget(self.tabla, 4, 1, 1, 9)

        self.widgetCentral.setLayout(layout)
        self.widgetCentral.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)
        self.setCentralWidget(self.widgetCentral)

        self.edita = None

    
    def editar(self, tipo):
        global Editar
        boton = qtw.QApplication.focusWidget()
        i = self.tabla.indexAt(boton.pos())
        datos = []
        if tipo == 'editar':
            for cell in range(0, 9):
                datos.append(i.sibling(i.row(), cell).data())
            self.edita = Editar(self.campos, datos)
        else:
            self.edita = Editar(self.campos, None)
        self.edita.show()
        self.mostrarDatos(self.tabla, self.campos)

    def mostrarDatos(self, campos):
        cur.execute('SELECT * FROM HERRAMIENTAS')
        query = cur.fetchall()
        self.tabla.setRowCount(len(query))
        for i in range(len(query)):
            idd = query[i][0]
            for j in range(len(query[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(query[i][j])))
            botonUwU = qtw.QPushButton("Editar")
            boton2 = qtw.QPushButton("Eliminar")
            botonUwU.clicked.connect(lambda: self.editar(campos, 'editar'))
            boton2.clicked.connect(lambda: self.eliminar(self.tabla, idd))
            self.tabla.setCellWidget(i, 7, botonUwU)
            self.tabla.setCellWidget(i, 8, boton2)

    def eliminar(self, idd):
        global mostrarMensaje
        resp = mostrarMensaje('Pregunta', 'Advertencia',
                              '¿Está seguro que desea eliminar estos datos?')
        if resp == qtw.QMessageBox.StandardButton.Yes:
            cur.execute('DELETE FROM HERRAMIENTAS WHERE ID=?', (idd,))
            con.commit()
            boton = qtw.QApplication.focusWidget()
            i = self.tabla.indexAt(boton.pos())
            self.tabla.removeRow(i.row())

    def closeEvent(self, event):
        if self.edita:
            self.edita.close()


class Editar(qtw.QWidget):
    def __init__(self, campos, datos):
        super().__init__()
        layout = qtw.QGridLayout()
        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QSpinBox()
        self.entry3 = qtw.QSpinBox()
        self.entry4 = qtw.QSpinBox()
        self.entry5 = qtw.QLineEdit()
        self.entry6 = qtw.QLineEdit()

        if datos:
            label = qtw.QLabel(campos[0])
            label2 = qtw.QLabel(str(datos[0]))
            layout.addWidget(label, 0, 0)
            layout.addWidget(label2, 0, 1)

            self.entry1.setText(datos[1])
            self.entry2.setValue(int(datos[2]))
            self.entry3.setValue(int(datos[3]))
            self.entry4.setValue(int(datos[4]))
            self.entry5.setText(datos[5])
            self.entry6.setText(datos[6])

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
        global window
        if datos:
            cur.execute("""
            UPDATE HERRAMIENTAS 
            SET DESC_LARGA=?, CANT_CONDICIONES=?, CANT_REPARACION=?, CANT_BAJA=?,ID_GRUPO=?,ID_SUBGRUPO=? WHERE ID=?""", (
                self.entry1.text(), self.entry2.value(), self.entry3.value(
                ), self.entry4.value(), self.entry5.text(), self.entry6.text(), datos[0],
            ))
            con.commit()
            mostrarMensaje("Information", "Aviso",
                           "Se ha actualizado la herramienta.")
        else:
            cur.execute("INSERT INTO HERRAMIENTAS VALUES(NULL, ?, ?, ?, ?, ?, ?) ", (
                self.entry1.text(), self.entry2.value(), self.entry3.value(
                ), self.entry4.value(), self.entry5.text(), self.entry6.text(),
            ))
            con.commit()
            mostrarMensaje("Information", "Aviso",
                           "Se ha ingresado una herramienta.")
        window.mostrarDatos(window.tabla, window.campos)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainWindow()

    with open(f"{os.path.abspath(os.getcwd())}/duraam/gestion.qss", 'r') as css:
        window.setStyleSheet(css.read())

    window.show()
    app.exec()
