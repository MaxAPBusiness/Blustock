from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from ui import Ui_MainWindow
import sqlite3 as db
import os

con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur = con.cursor()


class MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.pushButton_3.clicked.connect(lambda: self.registro())
        self.pushButton_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_2.clicked.connect(lambda: self.registro())
        self.pushButton_8.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_6.clicked.connect(lambda: self.ingreso())
        self.pushButton_9.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_7.clicked.connect(lambda: self.ingreso())
        self.pushButton_10.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.comboBox.currentTextChanged.connect(lambda: self.cambiarIdioma(self.comboBox, 2))
        self.comboBox_2.currentTextChanged.connect(lambda: self.cambiarIdioma(self.comboBox_2, 3))
        self.comboBox_3.currentTextChanged.connect(lambda: self.cambiarIdioma(self.comboBox_3, 1))
        self.comboBox_4.currentTextChanged.connect(lambda: self.cambiarIdioma(self.comboBox_4, 0))

        self.lineEdit_14.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.lineEdit_15.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.lineEdit_10.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.lineEdit_7.setEchoMode(qtw.QLineEdit.EchoMode.Password)


    def mostrarError(self, error, info):
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Icon.Critical)
        msg.setText(error)
        msg.setInformativeText(info)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
        msg.exec()

    def cambiarIdioma(self,combobox, i):
        combobox.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(i)
    
    def ingreso(self):
        cur.execute("SELECT NOMBRE_APE_ALUM, DNI, CONTRASENA FROM USUARIOS WHERE NOMBRE_APE_ALUM=? AND DNI=? AND CONTRASEÑA=?", (f"{self.lineEdit_31.text().upper()}",f"{self.lineEdit_33.text().upper()}",
                f"{self.lineEdit_36.text()}"))
        data=cur.fetchall()
        
        if len(data)>0:
            self.stackedWidget.setCurrentIndex(4)

        else:
            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Icon.Warning)
            msg.setText("Aviso")
            msg.setInformativeText("Los datos ingresados no coinciden. Porfavor, asegúrese de estar registrado y haber ingresado los datos correctamente.")
            msg.setWindowTitle("Aviso")
            msg.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
            msg.exec()

    def registro(self):
        if self.stackedWidget.currentIndex() == 3:
            if not (self.lineEdit_13.text() and self.lineEdit_14.text() and self.lineEdit_15.text() and self.lineEdit_17.text() and self.lineEdit_18.text()):
                self.mostrarError("Error: información faltante",
                                "Falta información obligatoria. Por favor, rellene todos los campos obligatorios e ingrese nuevamente")
                return
            elif len(self.lineEdit_14.text()) < 8:
                self.mostrarError("Error: contraseña inválida",
                                "La contraseña es demasiado corta. Por favor, ingrese una contraseña entre 8 y 20 caracteres.")
                return
            elif len(self.lineEdit_14.text()) > 20:
                self.mostrarError("Error: contraseña inválida",
                                "La contraseña es demasiado larga. Por favor, ingrese una contraseña entre 8 y 20 caracteres.")
                return
            elif self.lineEdit_14.text() != self.lineEdit_15.text():
                self.mostrarError("Error: contraseña inválida",
                                "Las contraseñas no coinciden. Por favor, ingrese nuevamente.")
                return
        else:
            if not (self.lineEdit_9.text() and self.lineEdit_12.text() and self.lineEdit_8.text() and self.lineEdit_10.text() and self.lineEdit_7.text()):
                self.mostrarError("Error: missing information",
                                "Required information is missing. Please fill all required fields.")
                return
            elif len(self.lineEdit_10.text()) < 8:
                self.mostrarError("Error: invalid password",
                                "Password is too short. Please enter a password between 8 and 20 characters.")
                return
            elif len(self.lineEdit_10.text()) > 20:
                self.mostrarError("Error: invalid password",
                                "Password is too long. Please enter a password between 8 and 20 characters.")
                return
            elif self.lineEdit_10.text() != self.lineEdit_7.text():
                self.mostrarError("Error: invalid password",
                                "Passwords don't match. Please enter both passwords correctly.")
                return
        try:
            cur.execute("INSERT INTO USUARIOS VALUES (NULL, ?, ?, ?, ?)", (f"{self.lineEdit_17.text().upper()} {self.lineEdit_13.text().upper()}",
                f"{self.lineEdit_18.text().upper()}", f"{self.lineEdit_16.text().upper()}", f"{self.lineEdit_14.text()}"))
            con.commit()
            msg = qtw.QMessageBox()
            if self.stackedWidget.currentIndex() == 3:
                msg.setIcon(qtw.QMessageBox.Icon.Information)
                msg.setText("Aviso")
                msg.setInformativeText("Se han ingresado los datos con éxito.")
                msg.setWindowTitle("Aviso")
                msg.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
                msg.exec()      
            else:
                msg.setIcon(qtw.QMessageBox.Icon.Information)
                msg.setText("Information")
                msg.setInformativeText("Data has been succesfully saved.")
                msg.setWindowTitle("Information")
                msg.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
                msg.exec()
        except:
            self.mostrarError(
                    "Error: datos repetidos",
                    "El DNI ya está ingresado en el sistema. Por favor, ingrese otro."
               )


if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    window = qtw.QMainWindow()
    ui = MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
