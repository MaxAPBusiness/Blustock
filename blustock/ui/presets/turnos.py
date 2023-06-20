"""Este módulo crea una función para mostrar un mensaje en la pantalla.

Clases
---------
    PopUp(QMessageBox()):
        Genera un mensaje emergente.
"""
import os
from PyQt6.QtWidgets import QDialog
from PyQt6 import uic,QtGui,QtCore,QtWidgets
from dal.dal import dal
from db.bdd import bdd
import sys
import datetime as time
import sqlite3 as sq
from ui.presets.popup import PopUp
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
        if bdd.cur.execute("select count(*) from turnos WHERE hora_egr is null").fetchall()[0][0] != 0:
            profe = dal.obtenerDatos("usuarios",self.usuario,)
            alumno = dal.obtenerDatos("alumnos",self.alumnoComboBox.currentText(),)
            panol = dal.obtenerDatos("ubicaciones",self.comboBox.currentText(),)
            fecha = time.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            bdd.cur.execute("INSERT INTO turnos(id_panolero, fecha_ing, id_prof_ing, id_ubi) VALUES (?, ?, ?, ?)", (alumno[0][0], fecha, profe[0][0], panol[0][0]))
            bdd.con.commit()
            mensaje = """       El turno se cargo
                con exito."""
            return PopUp("aviso", mensaje).exec()

        else:
            mensaje = """       Ya hay ningun turno activo
                en este momento."""
            return PopUp("Error", mensaje).exec()


class sii(QDialog):
    def __init__(self,usuario):
        self.usuario = usuario
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.pardir),"blustock","ui", 'screens_uis', 'finalizar_turno.ui'), self)
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
        pixmap = QtGui.QPixmap(path)
        self.pushButton.setIcon(QtGui.QIcon(QtGui.QIcon(pixmap)))
        self.pushButton.setIconSize(QtCore.QSize(25, 25))
        self.pushButton.clicked.connect(lambda: self.mostrarContrasena(self.pushButton, self.contrasenaLineEdit))
        self.buttonBox.accepted.connect(self.cerrar)

        self.show()

    def mostrarContrasena(self, boton,entry: QtWidgets.QLineEdit):
        if boton.isChecked():
            entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            path = f'ui{os.sep}rsc{os.sep}icons{os.sep}esconder.png'
            pixmap = QtGui.QPixmap(path)
        else:
            entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            path = f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
            pixmap = QtGui.QPixmap(path)
        boton.setIcon(QtGui.QIcon(pixmap))
        boton.setIconSize(QtCore.QSize(25, 25))

    def cerrar(self):

        if self.contrasenaLineEdit.text()== dal.obtenerDatos("usuarios",self.usuario,)[0][5]:
            if bdd.cur.execute("select count(*) from turnos WHERE hora_egr is null").fetchall()[0][0] != 0:
                profe = dal.obtenerDatos("usuarios",self.usuario,)
                hora = time.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                bdd.cur.execute("""UPDATE turnos SET hora_egr = ?, id_prof_egr= ? WHERE hora_egr is null""",(hora,profe[0][0],))
                bdd.con.commit()
                mensaje = """El turno se ha finalizado correctamente"""
                return PopUp("Aviso", mensaje).exec()
            else:
                mensaje = """       No hay ningun turno activo
                en este momento."""
            return PopUp("Error", mensaje).exec()


        else:
            mensaje = """       Contraseña incorrecta.
       El turno no se ha finalizado"""
            return PopUp("Error", mensaje).exec()
