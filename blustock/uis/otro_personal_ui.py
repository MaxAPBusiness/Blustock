# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'otro_personal.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200;400;700&display=swap');\n"
"\n"
"*{\n"
"    font-family: 'Raleway-blod';\n"
"    font-weight: 400;\n"
"}\n"
"\n"
"QMenuBar{\n"
"\n"
"    background-color: #293045;\n"
"    padding: 0;    \n"
"    text-transform: capitalize;\n"
"    font-size: 14px;\n"
"    color:white;\n"
"    display: flex;\n"
"    flex-direction: column;\n"
"\n"
"}\n"
"\n"
"QMenuBar:item{\n"
"    padding: 17px;\n"
"    border-radius: 10px;\n"
"\n"
"}\n"
"\n"
"QMenuBar:item:selected{\n"
"    background-color: #768AC5;\n"
"    color:black;\n"
"    border-radius: 5px;\n"
"    margin: 10px;\n"
"    \n"
"    \n"
"\n"
"}\n"
"\n"
"QMenu{\n"
"    background-color: #293045;\n"
"\n"
"    color: white;\n"
"}\n"
"\n"
"QMenu:item{\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QMenu:item:selected{\n"
"    background-color: #768AC5;\n"
"    color:white;\n"
"\n"
"}\n"
"Qmenu#icon{\n"
"   icon:size 40px; \n"
"    \n"
"}\n"
"\n"
"\n"
"QRadioButton:indicator{\n"
"    borde"
                        "r-style: solid;\n"
"    border-color:  #293045;\n"
"    border-radius: 6%;\n"
"    border-width:  2px;\n"
"    background-color: #BABFCE;\n"
"}\n"
"QRadioButton::indicator:checked{\n"
"    background-color: #768AC5;\n"
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
"\n"
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
"#pushButton,#pushButton_2,#pushButton_3{\n"
"    width: 85px;\n"
"    height: 30px;\n"
"}"
                        "\n"
"\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 70))
        font = QFont()
        font.setFamilies([u"Raleway-blod"])
        font.setBold(False)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setPixmap(QPixmap(u"lupa.png"))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)
        self.lineEdit.setMinimumSize(QSize(340, 0))
        font1 = QFont()
        font1.setFamilies([u"Raleway-blod"])
        font1.setPointSize(10)
        font1.setBold(False)
        self.lineEdit.setFont(font1)
        self.lineEdit.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.tableWidget.rowCount() < 1):
            self.tableWidget.setRowCount(1)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setItem(0, 4, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setItem(0, 5, __qtablewidgetitem12)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QFrame.Plain)
        self.tableWidget.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(60, -1, 60, -1)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        font2 = QFont()
        font2.setFamilies([u"Raleway-blod"])
        font2.setPointSize(12)
        font2.setBold(False)
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font2)
        self.pushButton.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Gesti\u00f3n de alumnos", None))
        self.label_2.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Buscar...", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"DNI", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Nombre y Apellido", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Curso", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem4 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem5 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"43290132", None));
        ___qtablewidgetitem6 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Juan ", None));
        ___qtablewidgetitem7 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"6\u00b0C", None));
        ___qtablewidgetitem8 = self.tableWidget.item(0, 4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Editar", None));
        ___qtablewidgetitem9 = self.tableWidget.item(0, 5)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Borrar", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Agregar", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Pase anual", None))
    # retranslateUi
