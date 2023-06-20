"""Este módulo crea una función para mostrar un mensaje en la pantalla.

Clases
---------
    PopUp(QMessageBox()):
        Genera un mensaje emergente.
"""
import os
from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from dal.dal import dal
from db.bdd import bdd
import sys
import datetime as time
import sqlite3 as sq

class nuu(QDialog):
    def __init__(self,usuario):
        self.usuario = usuario
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.pardir),"blustock","ui", 'screens_uis', 'cargar_turno.ui'), self)

        for i in dal.obtenerDatos("clases",""):
            self.cursoComboBox.addItem(i[1])
        
        for i in dal.obtenerDatos("ubicaciones",""):
            self.comboBox.addItem(i[1])

        self.cursoComboBox.currentTextChanged.connect(self.curso)
        self.buttonBox.accepted.connect(self.turno)

        self.show()
    
    def curso(self):
        self.alumnoComboBox.clear()

        for i in dal.obtenerDatos("alumnos",self.cursoComboBox.currentText(),):

            self.alumnoComboBox.addItem(i[1])


    def turno(self):
        profe = dal.obtenerDatos("usuarios",self.usuario,)
        alumno = dal.obtenerDatos("alumnos",self.alumnoComboBox.currentText(),)
        panol = dal.obtenerDatos("ubicaciones",self.comboBox.currentText(),)
        fecha = time.datetime.now().strftime("%d/%m/%Y")
        hora = time.datetime.now().strftime("%H:%M:%S")
        bdd.cur.execute("INSERT INTO turnos(id_panolero, fecha, hora_ing, id_prof_ing, id_ubi) VALUES (?, ?, ?, ?, ?)", (alumno[0][0], fecha, hora, profe[0][0], panol[0][0]))
        bdd.con.commit()