"""Este módulo crea una pantalla para gestionar la tabla usuarios. 

Clases
------
    GestionUsuarios(qtw.QWidget):
        Crea una pantalla para gestionar la tabla usuarios.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

import db.inicializar_bbdd as db
from botones import BotonEliminar
import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionUsuarios(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla usuarios.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            La tabla de la pantalla.
        campos : tuple
            Los títulos de las columnas de la tabla.
        
    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionUsuarios.

            Crea la pantalla, un QWidget, que contiene un título
            descrptivo, un QLabel y una tabla, un QTableWidget, que
            muestra los datos de la tabla usuarios y que
            contiene botones para editarlos.

        mostrarDatos(self):
            Obtiene los datos de la tabla usuarios y los
            introduce en la tabla de la pantalla.

        hacerAdmin(self):
            Asciende el rol del usuario a administrador.
        
        eliminar(self):
            Elimina la fila de la tabla usuarios.
    """
    def __init__(self):
        super().__init__()

        self.titulo=qtw.QLabel("Gestión de usuarios")
        self.titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("Usuario", "Nombre y Apellido", "", "")                   
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(1, 125)
        self.tabla.setColumnWidth(2, 35)
        self.tabla.setColumnWidth(3, 35)
        self.mostrarDatos()

        layout = qtw.QGridLayout()
        layout.addWidget(self.titulo, 0, 0)
        layout.addWidget(self.tabla, 1, 0, 1, 9)
        self.setLayout(layout)


    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla usuarios y
        los introduce en la tabla de la pantalla.
        """
        db.cur.execute("SELECT usuario, nombre_apellido FROM usuarios")
        consulta = db.cur.fetchall()

        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(consulta[i][j])))
            self.tabla.setRowHeight(i, 35)

            botonHacerAdmin = qtw.QPushButton()
            botonHacerAdmin.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/ascender.png")))
            botonHacerAdmin.setIconSize(qtc.QSize(25, 25))
            botonHacerAdmin.setObjectName("aceptar")
            botonHacerAdmin.clicked.connect(lambda: self.hacerAdmin())
            botonHacerAdmin.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, len(self.campos)-2, botonHacerAdmin)

            botonEliminar = BotonEliminar()
            botonEliminar.clicked.connect(lambda: self.eliminar())
            self.tabla.setCellWidget(i, len(self.campos)-1, botonEliminar)

    def hacerAdmin(self):
        """Este método asciende el rol del usuario a administrador."""
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                              "¿Está seguro que desea eliminar estos datos?")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd=posicion.sibling(posicion.row(), 0).data()
            db.cur.execute("SELECT * FROM usuarios WHERE usuario = ?", (idd,)) 
            datos=db.cur.fetchall()[0]
            db.cur.execute("INSERT INTO administradores VALUES (?, ?, ?, ?)", datos)
            db.cur.execute("DELETE FROM usuarios WHERE usuario = ?", (datos[1],))
            registrarCambios("Ascenso", "Usuarios Usuarios", datos[0], f"{datos}", f"{datos}")
            db.con.commit()
            self.mostrarDatos()

    def eliminar(self):
        """Este método elimina la fila de la tabla usuarios."""
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                "¿Está seguro que desea eliminar el usuario? No podrá volver a acceder al sistema.")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd=posicion.sibling(posicion.row(), 0).data()
            db.cur.execute("SELECT * FROM usuarios WHERE ID = ?", (idd,))
            datosEliminados=db.cur.fetchall()[0]
            db.cur.execute("DELETE FROM usuarios WHERE usuario = ?", (idd,))
            registrarCambios("Eliminacion simple", "Usuarios", idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()