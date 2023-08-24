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
from datetime import datetime
from ui.presets.popup import PopUp

class NuevoTurno(QDialog):
    def __init__(self,usuario):
        self.turnFinalized = None
        self.usuario = usuario
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.pardir),os.getcwd(),"ui", 'screens_uis', 'cargar_turno.ui'), self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Cargar turno")
        sugerencias=[]
        self.setFixedSize(600, 400)
        for i in dal.obtenerDatos("clases",""):
            self.cursoComboBox.addItem(i[2])
            sugerencias.append(i[2])

        for i in dal.obtenerDatos("ubicaciones",""):
            self.comboBox.addItem(i[1])

        cuadroSugerencias = QtWidgets.QCompleter(sugerencias, self)
        cuadroSugerencias.setCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive)
        cuadroSugerencias.setCompletionMode(
            QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        cuadroSugerencias.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        
        self.cursoComboBox.setCurrentIndex(-1)
        self.cursoComboBox.setCompleter(cuadroSugerencias)
        self.cursoComboBox.textActivated.connect(self.curso)
        self.buttonBox.accepted.connect(self.turno)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Save).setText("Crear turno")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        self.show()
    
    def curso(self):
        self.alumnoComboBox.clear()

        for i in dal.obtenerDatos("alumnos",self.cursoComboBox.currentText(),):
            self.alumnoComboBox.addItem(i[1])

    def turno(self):
        if bdd.cur.execute("select count(*) from turnos WHERE fecha_egr is null").fetchall()[0][0] == 0:
            if self.alumnoComboBox.currentText() != "":
                profe = dal.obtenerDatos("usuarios",self.usuario,)
                alumno = dal.obtenerDatos("alumnos",self.alumnoComboBox.currentText(),)
                panol = dal.obtenerDatos("ubicaciones",self.comboBox.currentText(),)
                fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                bdd.cur.execute("INSERT INTO turnos(id_panolero, fecha_ing, id_prof_ing, id_ubi) VALUES (?, ?, ?, ?)", (alumno[0][0], fecha, profe[0][0], panol[0][0]))
                bdd.con.commit()
                mensaje = """El turno se cargo con exito."""
                self.turnFinalized = True
                PopUp("Aviso", mensaje).exec()

            else:
                mensaje = """Por favor ingrese un alumno."""
                PopUp("Error", mensaje).exec()


        else:
            mensaje = """Ya hay un turno activo en este momento."""
            PopUp("Error", mensaje).exec()
            

class TerminarTurno(QDialog):
    def __init__(self,usuario):
        self.turnFinalized = None
        self.usuario = usuario
        super().__init__()
        self.setFixedSize(600, 400)
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}finalizar_turno.ui'), self)
        self.setWindowTitle("Finalizar turno")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
        pixmap = QtGui.QPixmap(path)
        self.showPass.setIcon(QtGui.QIcon(QtGui.QIcon(pixmap)))
        self.showPass.setIconSize(QtCore.QSize(25, 25))
        self.showPass.clicked.connect(lambda: self.mostrarContrasena(self.showPass, self.contrasenaLineEdit))
        self.buttonBox.accepted.connect(self.cerrar)
        print(self.buttonBox.standardButtons())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText("Terminar turno")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")

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
        if bdd.cur.execute("select count(*) from turnos WHERE fecha_egr is null").fetchall()[0][0] != 0:
            if self.contrasenaLineEdit.text() == dal.obtenerDatos("usuarios", self.usuario)[0][5]:
                self.turnFinalized = True
                profe = dal.obtenerDatos("usuarios", self.usuario,)
                hora = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                bdd.cur.execute("""UPDATE turnos SET fecha_egr = ?, id_prof_egr = ? WHERE fecha_egr is null""", (hora, profe[0][0],))
                bdd.con.commit()
                mensaje = """El turno se ha finalizado correctamente"""
                PopUp("Aviso", mensaje).exec()
            else:
                mensaje = """Contraseña incorrecta. El turno no se ha finalizado"""
                PopUp("Error", mensaje).exec()
        else:
            mensaje = """No hay ningún turno activo en este momento."""
            PopUp("Error", mensaje).exec()



class cerrarSesion(QDialog):
    def __init__(self,usuario):
        self.turnFinalized = None
        self.usuario = usuario
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()),
                   f'ui{os.sep}screens_uis{os.sep}finalizar_turno.ui'), self)
        self.setWindowTitle("Cerrar la aplicacion")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.Contrasena.setText("Para cerrar la aplicacion, por favor ingrese su contraseña")
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
        pixmap = QtGui.QPixmap(path)
        self.showPass.setIcon(QtGui.QIcon(QtGui.QIcon(pixmap)))
        self.showPass.setIconSize(QtCore.QSize(25, 25))
        self.showPass.clicked.connect(lambda: self.mostrarContrasena(self.showPass, self.contrasenaLineEdit))
        self.buttonBox.accepted.connect(self.cerrar)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText("Cerrar la aplicacion")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
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
        try:
            if self.contrasenaLineEdit.text() == dal.obtenerDatos("usuarios", self.usuario)[0][5]:
                mensaje = """¿Está seguro de que desea cerrar la aplicacion?"""
                popup = PopUp("Pregunta", mensaje).exec()
                if popup == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.turnFinalized = True
            else:
                mensaje = """Contraseña incorrecta. No es posible cerrar la aplicacion"""
                PopUp("Error", mensaje).exec()
        except IndexError:
            mensaje = """Contraseña incorrecta. No es posible cerrar la aplicacion"""
            PopUp("Error", mensaje).exec()
