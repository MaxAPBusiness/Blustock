# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpinBox, QStackedWidget, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import logo_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(801, 522)
        MainWindow.setStyleSheet(u"")
        self.actionGesti_n_de_subgrupos = QAction(MainWindow)
        self.actionGesti_n_de_subgrupos.setObjectName(u"actionGesti_n_de_subgrupos")
        self.actionGesti_n_de_grupos = QAction(MainWindow)
        self.actionGesti_n_de_grupos.setObjectName(u"actionGesti_n_de_grupos")
        self.actionListado = QAction(MainWindow)
        self.actionListado.setObjectName(u"actionListado")
        self.actionConsultas = QAction(MainWindow)
        self.actionConsultas.setObjectName(u"actionConsultas")
        self.actionGestion_de_movimientos = QAction(MainWindow)
        self.actionGestion_de_movimientos.setObjectName(u"actionGestion_de_movimientos")
        self.actionAlumnos = QAction(MainWindow)
        self.actionAlumnos.setObjectName(u"actionAlumnos")
        self.actionProfesores = QAction(MainWindow)
        self.actionProfesores.setObjectName(u"actionProfesores")
        self.actionlogo = QAction(MainWindow)
        self.actionlogo.setObjectName(u"actionlogo")
        self.actionaa = QAction(MainWindow)
        self.actionaa.setObjectName(u"actionaa")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayoutWidget = QWidget(self.page)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 771, 41))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.gridLayoutWidget_2 = QWidget(self.page)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(30, 110, 721, 291))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.gridLayoutWidget_2)
        if (self.tableWidget.columnCount() < 10):
            self.tableWidget.setColumnCount(10)
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
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        if (self.tableWidget.rowCount() < 11):
            self.tableWidget.setRowCount(11)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget.setItem(2, 0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget.setItem(3, 0, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget.setItem(4, 0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget.setItem(5, 0, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget.setItem(6, 0, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget.setItem(7, 0, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget.setItem(8, 0, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget.setItem(9, 0, __qtablewidgetitem29)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.page)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(30, 60, 291, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_5 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        icon = QIcon()
        icon.addFile(u"../blustock/lupa.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon)

        self.horizontalLayout.addWidget(self.pushButton_5)

        self.lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEchoMode(QLineEdit.Normal)
        self.lineEdit.setCursorPosition(0)
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setPlaceholderText(u"")
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalLayoutWidget_2 = QWidget(self.page)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(350, 60, 401, 23))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.spinBox = QSpinBox(self.horizontalLayoutWidget_2)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_2.addWidget(self.spinBox)

        self.dateTimeEdit = QDateTimeEdit(self.horizontalLayoutWidget_2)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")

        self.horizontalLayout_2.addWidget(self.dateTimeEdit)

        self.radioButton = QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_2.addWidget(self.radioButton)

        self.pushButton = QPushButton(self.page)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(610, 410, 131, 51))
        self.horizontalLayoutWidget_3 = QWidget(self.page)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(40, 410, 281, 61))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_4 = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout_3.addWidget(self.stackedWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 801, 22))
        self.menuHerramientas = QMenu(self.menubar)
        self.menuHerramientas.setObjectName(u"menuHerramientas")
        self.menuPersonal = QMenu(self.menubar)
        self.menuPersonal.setObjectName(u"menuPersonal")
        self.menuMovimientos = QMenu(self.menubar)
        self.menuMovimientos.setObjectName(u"menuMovimientos")
        self.menuProfesor = QMenu(self.menubar)
        self.menuProfesor.setObjectName(u"menuProfesor")
        self.menuProfesor.setLayoutDirection(Qt.RightToLeft)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHerramientas.menuAction())
        self.menubar.addAction(self.menuPersonal.menuAction())
        self.menubar.addAction(self.menuMovimientos.menuAction())
        self.menubar.addAction(self.menuProfesor.menuAction())
        self.menuHerramientas.addAction(self.actionGesti_n_de_subgrupos)
        self.menuHerramientas.addAction(self.actionGesti_n_de_grupos)
        self.menuHerramientas.addAction(self.actionListado)
        self.menuHerramientas.addAction(self.actionConsultas)
        self.menuPersonal.addAction(self.actionAlumnos)
        self.menuPersonal.addAction(self.actionProfesores)
        self.menuMovimientos.addAction(self.actionGestion_de_movimientos)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionGesti_n_de_subgrupos.setText(QCoreApplication.translate("MainWindow", u"Gesti\u00f3n de subgrupos", None))
        self.actionGesti_n_de_grupos.setText(QCoreApplication.translate("MainWindow", u"Gesti\u00f3n de grupos", None))
        self.actionListado.setText(QCoreApplication.translate("MainWindow", u"Listado", None))
        self.actionConsultas.setText(QCoreApplication.translate("MainWindow", u"Consultas", None))
        self.actionGestion_de_movimientos.setText(QCoreApplication.translate("MainWindow", u"Gestion de movimientos", None))
        self.actionAlumnos.setText(QCoreApplication.translate("MainWindow", u"Alumnos", None))
        self.actionProfesores.setText(QCoreApplication.translate("MainWindow", u"Profesores", None))
        self.actionlogo.setText(QCoreApplication.translate("MainWindow", u"logo", None))
        self.actionaa.setText(QCoreApplication.translate("MainWindow", u"aa", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"PROFESORES", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"New Column", None));
        ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem12 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem13 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem14 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem15 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem16 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem17 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem18 = self.tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem19 = self.tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem20 = self.tableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"New Row", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem21 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"aaaaa", None));
        ___qtablewidgetitem22 = self.tableWidget.item(2, 0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"aaaa", None));
        ___qtablewidgetitem23 = self.tableWidget.item(3, 0)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"aaaaa", None));
        ___qtablewidgetitem24 = self.tableWidget.item(4, 0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"aaaa", None));
        ___qtablewidgetitem25 = self.tableWidget.item(5, 0)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"aaaaa", None));
        ___qtablewidgetitem26 = self.tableWidget.item(6, 0)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"aaaaaa", None));
        ___qtablewidgetitem27 = self.tableWidget.item(7, 0)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"aaaaaa", None));
        ___qtablewidgetitem28 = self.tableWidget.item(8, 0)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"aaaaaa", None));
        ___qtablewidgetitem29 = self.tableWidget.item(9, 0)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"aaaaa", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.pushButton_5.setText("")
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"CONFIRMAR", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Borrar", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Crear", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Editar", None))
        self.menuHerramientas.setTitle(QCoreApplication.translate("MainWindow", u"HERRAMIENTAS", None))
        self.menuPersonal.setTitle(QCoreApplication.translate("MainWindow", u"PERSONAL", None))
        self.menuMovimientos.setTitle(QCoreApplication.translate("MainWindow", u"MOVIMIENTOS", None))
        self.menuProfesor.setTitle(QCoreApplication.translate("MainWindow", u"PROFESOR", None))
    # retranslateUi

