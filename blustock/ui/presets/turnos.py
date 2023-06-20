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
import sys

class nuu(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.pardir),"blustock","ui", 'screens_uis', 'Turno.ui'), self)

        for i in dal.obtenerDatos("clases",""):
            self.cursoComboBox.addItem(i[1])
        
        for i in dal.obtenerDatos("ubicaciones",""):
            self.comboBox.addItem(i[1])

        self.cursoComboBox.currentTextChanged.connect(self.curso)
        self.show()
    
    def curso(self):
        self.alumnoComboBox.clear()

        for i in dal.obtenerDatos("alumnos",self.cursoComboBox.currentText(),):

            self.alumnoComboBox.addItem(i[1])


