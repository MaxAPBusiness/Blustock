"""Este módulo crea una pantalla para gestionar la tabla solicitudes.

Clases
------
    Solicitudes(qtw.QWidget):
        Crea una pantalla para gestionar la tabla 
        solicitudes.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import db.inicializar_bbdd as db
import os

from . import mostrar_mensaje as m
from .botones import BotonFila

class Solicitudes(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla 
    solicitudes.

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
            El constructor de la clase Solicitudes.

            Crea la pantalla, un QWidget, que contiene un título
            descrptivo, un QLabel y una tabla, un QTableWidget, que
            muestra los datos de la tabla usuarios y que
            contiene botones para editarlos.

        mostrarDatos(self):
            Obtiene los datos de la tabla usuarios y los
            introduce en la tabla de la pantalla.

        aceptar(self):
            Aprueba la solicitud de usuario.
        
        rechazar(self):
            Rechaza la solicitud de usuario.
    """
    def __init__(self):
        super().__init__()

        self.titulo=qtw.QLabel("Solicitudes de usuario")
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
        """Este método obtiene los datos de la tabla solicitudes y los
        introduce en la tabla de la pantalla.

        Solo muestra las solicitudes pendientes, no las rechazadas.
        """
        db.cur.execute("SELECT usuario, nombre_apellido FROM solicitudes WHERE ESTADO='Pendiente'")
        consulta = db.cur.fetchall()

        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):

            for j in range(len(consulta[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(consulta[i][j])))

            self.tabla.setRowHeight(i, 35)

            botonAceptar = BotonFila("aceptar")
            botonAceptar.clicked.connect(lambda: self.aceptar(consulta[i][0]))
            self.tabla.setCellWidget(i, len(self.campos)-2, botonAceptar)

            botonRechazar = BotonFila("rechazar")
            botonRechazar.clicked.connect(lambda: self.rechazar(consulta[i][0]))
            self.tabla.setCellWidget(i, len(self.campos)-1, botonRechazar)

    def aceptar(self):
        """Este método aprueba la solicitud de usuario.
        
        Inserta los datos de la solicitud en la tabla usuarios y
        elimina la solicitud.
        """
        
        botonClickeado = qtw.QApplication.focusWidget()
        posicion = self.tabla.indexAt(botonClickeado.pos())
        idd=posicion.sibling(posicion.row(), 0).data()
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
        "¿Está seguro que desea aceptar la solicitud? El usuario podrá acceder a todas las bases de datos.")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            db.cur.execute("SELECT usuario, contrasena, nombre_apellido FROM solicitudes WHERE usuario = ?", (idd,)) 
            datos=db.cur.fetchall()
            db.cur.execute("INSERT INTO usuarios VALUES (NULL, ?, ?, ?)", datos[0])
            db.cur.execute("DELETE FROM solicitudes WHERE usuario = ?", (datos[0][0],))
            db.con.commit()
            self.mostrarDatos()

    def rechazar(self):
        """Este método rechaza la solicitud de usuario.
        
        Cambia el estado a rechazado, para que, cuando la persona
        quiera ver si su solicitud fue aprobada, se le notifique que
        fue rechazada.
        """
        
        botonClickeado = qtw.QApplication.focusWidget()
        posicion = self.tabla.indexAt(botonClickeado.pos())
        idd=posicion.sibling(posicion.row(), 0).data()
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                              "¿Está seguro que desea rechazar la solicitud?")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            db.cur.execute("UPDATE solicitudes SET ESTADO='Rechazado' WHERE usuario = ?", (idd,))
            db.con.commit()
            self.mostrarDatos()
