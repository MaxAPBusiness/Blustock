from PyQt6 import QtWidgets as qtw
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
        self.pushButton_5.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_2.clicked.connect(lambda: self.registro())
        self.pushButton_8.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_6.clicked.connect(lambda: self.ingreso())
        self.pushButton_9.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButton_7.clicked.connect(lambda: self.ingreso())
        self.pushButton_10.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_4.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))

        self.comboBox.currentTextChanged.connect(
            lambda: self.cambiarIdioma(self.comboBox, 2))
        self.comboBox_2.currentTextChanged.connect(
            lambda: self.cambiarIdioma(self.comboBox_2, 3))
        self.comboBox_3.currentTextChanged.connect(
            lambda: self.cambiarIdioma(self.comboBox_3, 1))
        self.comboBox_4.currentTextChanged.connect(
            lambda: self.cambiarIdioma(self.comboBox_4, 0))

        self.lineEdit_14.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.lineEdit_15.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.lineEdit_10.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.lineEdit_7.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.lineEdit_33.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.lineEdit_34.setEchoMode(qtw.QLineEdit.EchoMode.Password)

        self.spinbox.setMaximum(99999999)
        self.spinbox.setButtonSymbols(
            qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinbox2.setMaximum(99999999)
        self.spinbox2.setButtonSymbols(
            qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinbox3.setMaximum(99999999)
        self.spinbox3.setButtonSymbols(
            qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinbox4.setMaximum(99999999)
        self.spinbox4.setButtonSymbols(
            qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)

    def mostrarMensaje(self, title, msg, info):
        window = qtw.QMessageBox()
        if title=="Error":
            window.setIcon(qtw.QMessageBox.Icon.Critical)
        elif title=="Advertencia" or title=="Warning":
            window.setIcon(qtw.QMessageBox.Icon.Warning)
        elif title=="Aviso" or title=="Information":
            window.setIcon(qtw.QMessageBox.Icon.Information)
        else:
            print("Error de titulo")
            return
        window.setText(msg)
        window.setInformativeText(info)
        window.setWindowTitle(title)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
        window.exec()

    def cambiarIdioma(self, combobox, i):
        combobox.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(i)

    def ingreso(self):
        if self.stackedWidget.currentIndex() == 0:
            cur.execute("SELECT NOMBRE_APE_ALUM, DNI, EMAIL, CONTRASENA FROM USUARIOS WHERE NOMBRE_APE_ALUM=? AND DNI=? AND CONTRASENA=?", (f"{self.lineEdit_31.text().upper()}", f"{self.spinbox.value()}",
                                                                                                                                 f"{self.lineEdit_33.text()}"))
            data=cur.fetchall()
            if len(data) > 0:
                print("a")
                self.stackedWidget.setCurrentIndex(4)
                self.label_25.setText(data[0][0])
                self.label_27.setText(data[0][2])

            else:
                self.mostrarMensaje("Advertencia","Error al intentar ingresar",
                                  "Los datos ingresados no coinciden. Por favor, asegúrese de estar registrado y de que el usuario y la contraseña son correctos.")
        else:
            cur.execute("SELECT NOMBRE_APE_ALUM, DNI, CONTRASENA FROM USUARIOS WHERE NOMBRE_APE_ALUM=? AND DNI=? AND CONTRASENA=?", (f"{self.lineEdit_32.text().upper()}", f"{self.spinbox2.value()}",
                                                                                                                                 f"{self.lineEdit_34.text()}"))
            if len(cur.fetchall()) > 0:
                print("a")
                self.stackedWidget.setCurrentIndex(4)

            else:
                self.mostrarMensaje("Warning","Log in failed:",
                                  "Data doesn't match. Please, ensure you are registered and the username and password are correct.")

    def registro(self):
        if self.stackedWidget.currentIndex() == 3:
            if not (self.lineEdit_13.text() and self.lineEdit_14.text() and self.lineEdit_16.text() and self.lineEdit_17.text() and self.spinbox4.value() > 0):
                self.mostrarMensaje("Error","Error: información faltante",
                                  "Falta información obligatoria. Por favor, rellene todos los campos obligatorios e ingrese nuevamente")
                return
            elif len(self.lineEdit_14.text()) < 8:
                self.mostrarMensaje("Error","Error: contraseña inválida",
                                  "La contraseña es demasiado corta. Por favor, ingrese una contraseña entre 8 y 20 caracteres.")
                return
            elif len(self.lineEdit_14.text()) > 20:
                self.mostrarMensaje("Error","Error: contraseña inválida",
                                  "La contraseña es demasiado larga. Por favor, ingrese una contraseña entre 8 y 20 caracteres.")
            elif self.lineEdit_14.text() != self.lineEdit_15.text():
                self.mostrarMensaje("Error","Error: contraseña inválida",
                                  "Las contraseñas no coinciden. Por favor, ingrese nuevamente.")
            else:
                try:
                    cur.execute("INSERT INTO USUARIOS VALUES(NULL,?,?,?,?)", (f"{self.lineEdit_13.text().upper()} {self.lineEdit_17.text().upper()}", 
                    self.spinbox.value(), self.lineEdit_16.text(), self.lineEdit_14.text()))
                    con.commit()
                    self.mostrarMensaje("Aviso", "Aviso",
                                  "Los datos se han ingresado correctamente")
                except:
                    self.mostrarMensaje("Error","Error: ingreso fallido",
                                      "El DNI ya está ingresado. Por favor, ingrese otro.")

        else:
            if not (self.lineEdit_9.text() and self.lineEdit_12.text() and self.spinbox3.value() > 0 and self.lineEdit_10.text() and self.lineEdit_7.text()):
                self.mostrarMensaje("Error","Error: missing information",
                                  "Required information is missing. Please fill all required fields.")
                return
            elif len(self.lineEdit_10.text()) < 8:
                self.mostrarMensaje("Error","Error: invalid password",
                                  "Password is too short. Please enter a password between 8 and 20 characters.")
                return
            elif len(self.lineEdit_10.text()) > 20:
                self.mostrarMensaje("Error","Error: invalid password",
                                  "Password is too long. Please enter a password between 8 and 20 characters.")
                return
            elif self.lineEdit_10.text() != self.lineEdit_7.text():
                self.mostrarMensaje("Error","Error: invalid password",
                                  "Passwords don't match. Please enter both passwords correctly.")
                return
            else:
                try:
                    cur.execute("INSERT INTO USUARIOS VALUES(NULL,?,?,?,?)", (f"{self.lineEdit_9.text().upper()} {self.lineEdit_12.text().upper()}"
                    , self.spinbox2.value(), self.lineEdit_11.text(), self.lineEdit_10.text()))
                    con.commit()
                    self.mostrarMensaje("Aviso", "Aviso",
                                  "Los datos se han ingresado correctamente")
                except:
                    self.mostrarMensaje("Error",
                        "Error: register failed",
                        "The ID is already registered. Please, sign up with another ID."
                    )


if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    window = qtw.QMainWindow()
    ui = MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
