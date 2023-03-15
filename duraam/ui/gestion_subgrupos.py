"""Este módulo crea una pantalla para gestionar la tabla subgrupos. 

Clases
------
    GestionSubgrupos(qtw.QWidget):
        Crea una pantalla para gestionar la tabla subgrupos.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os
import sqlite3

import db.inicializar_bbdd as db
from .botones import BotonOrdenar, BotonFila
from . import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionSubgrupos(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla subgrupos.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            La tabla de la pantalla.
        campos : tuple
            Los títulos de las columnas de la tabla.
        barraBusqueda : QLineEdit
            La barra de búsqueda.
        radioSubrupo : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            subgrupo.
        radioGrupo : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            grupo.
        botonOrdenar : QPushButton
            Un botón para ordenar los datos de manera ascendente o
            descendente.

    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionGrupos.

            Crea la pantalla, un QWidget, que contiene: un título
            descriptivo, un QLabel; una tabla, un QTableWidget, que
            muestra los datos de la tabla grupos y contiene botones
            para editarlos; una barra de buscador, un QLineEdit, para
            buscar los datos; botones de radio, QRadioButton, para 
            ordenar los datos en base a una columna seleccionada, un
            botón, QCheckBox, para ordenar los datos mostrados de
            manera ascendente o descendente; un botón, un QPushButton,
            para insertar datos a la tabla.

        mostrarDatos(self):
            Obtiene los datos de la tabla grupos y los introduce en 
            la tabla de la pantalla.

        modificarLinea(self, tipo):
            Crea un formulario para insertar o editar datos en la tabla
            subgrupos.

        confirmarModificacion(self, tipo, datosPorDefecto=None):
            Modifica los datos de la tabla subgrupos.

        eliminar(self):
            Elimina la fila de la tabla subgrupos.
    """

    def __init__(self):
        super().__init__()

        self.titulo = qtw.QLabel("GESTIÓN DE SUBGRUPOS")
        self.titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("Subgrupo", "Grupo", "", "")
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(2, 35)
        self.tabla.setColumnWidth(3, 35)

        self.barraBusqueda = qtw.QLineEdit()
        self.barraBusqueda.setObjectName("buscar")
        self.barraBusqueda.setClearButtonEnabled(True)
        self.barraBusqueda.setPlaceholderText("Buscar...")
        self.barraBusqueda.textEdited.connect(lambda: self.mostrarDatos())

        iconoLupa = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        contenedorIconoLupa = qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        labelOrdenar = qtw.QLabel("Ordenar: ")
        self.radioSubgrupo = qtw.QRadioButton("Subgrupo")
        self.radioGrupo = qtw.QRadioButton("Grupo")
        self.radioSubgrupo.setObjectName("Radio1")
        self.radioGrupo.setObjectName("Radio2")
        self.radioSubgrupo.toggled.connect(lambda: self.mostrarDatos())
        self.radioGrupo.toggled.connect(lambda: self.mostrarDatos())

        self.botonOrdenar = BotonOrdenar()
        self.botonOrdenar.stateChanged.connect(lambda: self.ordenar())

        self.agregar = qtw.QPushButton("Agregar")
        self.agregar.setObjectName("agregar")
        self.agregar.clicked.connect(
            lambda: self.modificarLinea("agregar"))
        self.agregar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.titulo)
        contenedor1 = qtw.QWidget()
        contenedor1Layout = qtw.QGridLayout()
        contenedor1Layout.addWidget(self.barraBusqueda, 0, 0)
        contenedor1Layout.addWidget(contenedorIconoLupa, 0, 0)
        contenedor1Layout.addWidget(labelOrdenar, 0, 1)
        contenedor1Layout.addWidget(self.radioSubgrupo, 0, 2)
        contenedor1Layout.addWidget(self.radioGrupo, 0, 3)
        contenedor1Layout.addWidget(self.botonOrdenar, 0, 4)
        contenedor1.setLayout(contenedor1Layout)
        layout.addWidget(contenedor1)
        layout.addWidget(self.tabla)
        layout.addWidget(self.agregar)
        self.setLayout(layout)
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla subgrupos y los
        introduce en la tabla de la pantalla.
        """
        if self.radioSubgrupo.isChecked():
            orden = "ORDER BY id"
        elif self.radioGrupo.isChecked():
            orden = "ORDER BY grupo"
        else:
            orden = ""
        
        if orden and self.botonOrdenar.isChecked():
            orden += " ASC"

        db.cur.execute(
            f"SELECT * FROM SUBGRUPOS WHERE ID LIKE ? AND GRUPO LIKE ? {orden}",
            (
                f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
            )
        )
        consulta = db.cur.fetchall()
        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(
                    i, j, qtw.QTableWidgetItem(str(consulta[i][j])))
            self.tabla.setRowHeight(i, 35)

            botonEditar = BotonFila("editar")
            botonEditar.clicked.connect(lambda: self.modificarLinea("editar"))
            self.tabla.setCellWidget(i, len(self.campos)-2, botonEditar)

            botonEliminar = BotonFila("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar())
            self.tabla.setCellWidget(i, len(self.campos)-1, botonEliminar)

    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()

    def modificarLinea(self, tipo: str):
        """Este método crea un formulario para insertar o editar datos
        en la tabla subgrupos.

        El formulario es un QWidget que funciona como ventana. Por cada
        campo de la fila, agrega un entry (QLineEdit o QSpinbox) y un
        label descriptivo. Al confirmar los datos, ejecuta el método 
        confirmarModificacion.

        Parámetros
        ----------
            tipo : str
                el tipo de formulario.

        Ver también
        -----------
        confirmarModificacion: modifica los datos de la tabla subgrupos.
        """
        self.ventanaEditar = qtw.QWidget()
        self.ventanaEditar.setWindowTitle("Agregar Subgrupo")
        self.ventanaEditar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        layoutVentanaModificar = qtw.QGridLayout()

        for i in range(len(self.campos)-2):
            label = qtw.QLabel(f"{self.campos[i]}: ")
            label.setObjectName("modificar-label")
            layoutVentanaModificar.addWidget(
                label, i, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)

        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QLineEdit()
        db.cur.execute("SELECT ID FROM GRUPOS")
        sugerenciasGrupos = []
        for i in db.cur.fetchall():
            sugerenciasGrupos.append(i[0])
        cuadroSugerenciasGrupos = qtw.QCompleter(sugerenciasGrupos, self)
        cuadroSugerenciasGrupos.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry2.setCompleter(cuadroSugerenciasGrupos)

        datos = []
        if tipo == "editar":
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            for cell in range(0, len(self.campos)-2):
                datos.append(posicion.sibling(posicion.row(), cell).data())

            self.entry1.setText(datos[0])
            self.entry2.setText(datos[1])

            self.ventanaEditar.setWindowTitle("Editar")

        entries = [self.entry1, self.entry2]
        for i in range(len(entries)):
            entries[i].setObjectName("modificar-entry")
            layoutVentanaModificar.addWidget(entries[i], i, 1)

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))
        botonConfirmar.clicked.connect(
            lambda: self.confirmarModificacion(tipo, datos))
        layoutVentanaModificar.addWidget(
            botonConfirmar, i+1, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        self.ventanaEditar.setLayout(layoutVentanaModificar)
        self.ventanaEditar.show()

    def confirmarModificacion(self, tipo: str, datosPorDefecto: list | None = None):
        """Este método modifica los datos de la tabla subgrupos.

        Intenta realizar los cambios, registrarlos en el historial,
        notificar al usuario el éxito de la operacion, actualizar la
        tabla de la pantalla y cerrar el formulario. Si la base de
        datos arroja un sqlite3.IntegrityError durante el intento, le
        notifica al usuario que se ha repetido un valor único y termina
        la ejecución de la función, sin modificar la tabla.

        Parámetros
        ----------
            tipo : str
                El tipo de modificación.
            datosPorDefecto : list, default = None
                Los datos de la fila previos a la modificación. 

        Ver también
        -----------
        modificarLinea: crea un formulario para insertar o editar datos
                        en la tabla subgrupos.
        """
        db.cur.execute("SELECT ID FROM GRUPOS WHERE ID = ?",
                       (self.entry2.text(),))
        grupo = db.cur.fetchall()
        if not grupo:
            return m.mostrarMensaje(
                "Error", "Error", "El grupo no está ingresado. Asegúrese de ingresar el grupo primero")

        if tipo == "editar":
            try:
                db.cur.execute(
                    "SELECT * FROM SUBGRUPOS WHERE ID = ?", (datosPorDefecto[0],))
                datosViejos = db.cur.fetchall()[0]
                db.cur.execute("UPDATE SUBGRUPOS SET ID = ?, GRUPO = ? WHERE ID = ?", (
                    self.entry1.text().upper(
                    ), grupo[0][0], datosPorDefecto[0],
                ))
                db.cur.execute("UPDATE HERRAMIENTAS SET SUBGRUPO = ? WHERE SUBGRUPO = ? AND GRUPO = ?", (
                    self.entry1.text().upper(), datosPorDefecto[0], grupo[0][0]
                ))

                registrarCambios(
                    "Edicion", "Subgrupos", datosPorDefecto[0][0], f"{datosViejos}",
                    f"{(self.entry1.text().upper(), grupo[0][0])}"
                )

                db.con.commit()
                m.mostrarMensaje("Information", "Aviso",
                                 "Se ha actualizado el subgrupo.")
            except sqlite3.IntegrityError:
                return m.mostrarMensaje("Error", "Error", "El ID ingresado ya está registrado. Por favor, ingrese otro.")
        else:
            try:
                db.cur.execute("INSERT INTO SUBGRUPOS VALUES(?, ?) ", (
                    self.entry1.text().upper(), grupo[0][0],
                ))
                registrarCambios(
                    "Insercion", "Subgrupos", self.entry1.text().upper(), None,
                    f"{(self.entry1.text().upper(), grupo[0][0])}"
                )
                db.con.commit()
                m.mostrarMensaje("Information", "Aviso",
                                 "Se ha ingresado un subgrupo.")
            except sqlite3.IntegrityError:
                return m.mostrarMensaje("Error", "Error", "El subgrupo ingresado ya está registrado. Por favor, ingrese otro.")

        self.mostrarDatos()
        self.ventanaEditar.close()

    def eliminar(self):
        """Este método elimina la fila de la tabla subgrupos."""
        resp = m.mostrarMensaje("Pregunta", "Advertencia",
                                "¿Está seguro que desea eliminar estos datos?")
        if resp == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd = posicion.sibling(posicion.row(), 0).data()
            db.cur.execute("SELECT * FROM SUBGRUPOS WHERE ID = ?", (idd,))
            datosEliminados = db.cur.fetchall()[0]
            db.cur.execute("DELETE FROM SUBGRUPOS WHERE ID = ?", (idd,))
            db.cur.execute(
                "UPDATE HERRAMIENTAS SET SUBGRUPO=NULL WHERE SUBGRUPO = ?", (idd,))
            registrarCambios("Eliminacion simple", "Subgrupos",
                             idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()
