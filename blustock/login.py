from PyQt5 import QtWidgets, uic, QtCore,QtGui
import sys


class sopas(QtWidgets.QWidget):    
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.abspath(os.getcwd()), f'uis{os.sep}login.ui'), self)
        self.login.triggered.connect(self.login)

    def login(self):
        db.cur.execute("SELECT count(*) FROM personal WHERE usuario = ?",(self.usuariosLineEdit.text(),))
        check = db.cur.fetchall()
        if check == 1:
            db.cur.execute("SELECT count(*) FROM personal WHERE usuario = ? and contrasena = ?",(self.usuariosLineEdit.text(),self.passwordLineEdit.text(),))
            check = db.cur.fetchall()




        