# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'submenu_subgrupo.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(317, 174)
        MainWindow.setStyleSheet(u"@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200;400;700&display=swap');\n"
"\n"
"*{\n"
"    font-family: 'Raleway-blod';\n"
"    font-weight: 400;\n"
"}\n"
"\n"
"#label{\n"
"    font-size: 20px;\n"
"}\n"
"\n"
"QLineEdit{\n"
"    border-radius: 5px;\n"
"    background-color: #BABFCE;\n"
"    \n"
"}\n"
"\n"
"#title{\n"
"    width: 100px;\n"
"    height: 200px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    border-color:#293045;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    background-color: #BABFCE;\n"
"    color:#293045;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:#768AC5;\n"
"    color:aliceblue;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #293045;\n"
"\n"
"}\n"
"\n"
"#pushButton_5{\n"
"    padding: 10px;\n"
"    background-color: #768AC5;\n"
"    border-radius: 15%;\n"
"}\n"
"\n"
"#pushButton_2,#pushButton_3,#pushButton_4{\n"
"    width: 20px;\n"
"    height: 30px;\n"
"}\n"
"\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 16777215))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_7.setMargin(0)

        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_2.addWidget(self.pushButton, 2, 1, 1, 1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_2.addWidget(self.lineEdit, 1, 1, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_2.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Grupo:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Confirmar", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Subgrupo:", None))
    # retranslateUi

