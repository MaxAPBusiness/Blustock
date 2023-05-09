# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'historial.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

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
"#pushButton_2,#pushButton_3,#pushButton_4{\n"
"    width: 65px;\n"
"    height: 30px;\n"
""
                        "}\n"
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
        self.label_2.setPixmap(QPixmap(u"Nueva carpeta/lupa.png"))

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

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_2.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.horizontalLayout_2.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.horizontalLayout_2.addWidget(self.checkBox_4)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_6)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_4.addWidget(self.comboBox)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")

        self.horizontalLayout_4.addWidget(self.dateEdit)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.dateEdit_2 = QDateEdit(self.centralwidget)
        self.dateEdit_2.setObjectName(u"dateEdit_2")

        self.horizontalLayout_4.addWidget(self.dateEdit_2)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.comboBox_3 = QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.horizontalLayout_4.addWidget(self.comboBox_3)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_4.addWidget(self.comboBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget.rowCount() < 2):
            self.tableWidget.setRowCount(2)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setItem(1, 1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setItem(1, 2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setItem(1, 3, __qtablewidgetitem13)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QFrame.Plain)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(110)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tableWidget)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Historial de cambios", None))
        self.label_2.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Buscar...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Ordenar por:", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Usuario", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Fecha", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"Tabla", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"^", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Usuario:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Desde:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Hasta:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Tipo:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Tabla:", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Nombre y apellido", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Usuario", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Fecha y hora", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Descripcion", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem4 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"AAAAA", None));
        ___qtablewidgetitem5 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"admin12345", None));
        ___qtablewidgetitem6 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"17/04/2023", None));
        ___qtablewidgetitem7 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Agreg\u00f3 a la tabla Grupos la fila de id A con los datos A.", None));
        ___qtablewidgetitem8 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"AAAAA", None));
        ___qtablewidgetitem9 = self.tableWidget.item(1, 1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"admin12345", None));
        ___qtablewidgetitem10 = self.tableWidget.item(1, 2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"17/04/2023", None));
        ___qtablewidgetitem11 = self.tableWidget.item(1, 3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Edit\u00f3 la fila de id J de la tabla Subgrupos, reemplazando los datos('JJ', 'A') con los datos ('JJ', 'A').", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

