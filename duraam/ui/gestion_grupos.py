"""Este módulo crea una pantalla para gestionar la tabla grupos. 

Clases
------
    GestionGrupos(qtw.QWidget):
        Crea una pantalla para gestionar la tabla grupos.
"""
import sqlite3
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

import db.inicializar_bbdd as db
from .botones import BotonOrdenar, BotonFila
from . import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionGrupos(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla grupos.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            La tabla de la pantalla.
        campos : tuple
            Los títulos de las columnas de la tabla.
        barraBusqueda : QLineEdit
            La barra de búsqueda.
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
            buscar los datos; un botón, QCheckBox, para ordenar los
            datos mostrados de manera ascendente o descendente; un 
            botón, un QPushButton, para insertar datos a la tabla.

        mostrarDatos(self):
            Obtiene los datos de la tabla grupos y los introduce en 
            la tabla de la pantalla.

        ordenar(self):
            Cambia el ícono del botonOrdenar y actualiza los datos de
            la tabla de la pantalla.

        modificarLinea(self, tipo):
            Crea un formulario para insertar o editar datos en la tabla
            grupos.

        confirmarModificacion(self, tipo, datosPorDefecto=None):
            Modifica los datos de la tabla grupos.

        eliminar(self):
            Elimina la fila de la tabla grupos.
    """

    def __init__(self):
        super().__init__()

        self.titulo = qtw.QLabel("GESTIÓN DE grupos")
        self.titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("Grupo", "", "")
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(1, 35)
        self.tabla.setColumnWidth(2, 35)

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

        self.botonOrdenar = BotonOrdenar()
        self.botonOrdenar.stateChanged.connect(lambda: self.ordenar())

        botonAgregar = qtw.QPushButton("Agregar")
        botonAgregar.setObjectName("agregar")
        botonAgregar.clicked.connect(
            lambda: self.modificarLinea("agregar"))
        botonAgregar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.titulo)
        contenedor1 = qtw.QWidget()
        contenedor1Layout = qtw.QGridLayout()
        contenedor1Layout.addWidget(self.barraBusqueda, 1, 0)
        contenedor1Layout.addWidget(contenedorIconoLupa, 1, 0)
        contenedor1Layout.addWidget(self.botonOrdenar, 1, 1)
        contenedor1.setLayout(contenedor1Layout)
        layout.addWidget(contenedor1)
        layout.addWidget(self.tabla)
        layout.addWidget(botonAgregar)
        self.setLayout(layout)
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla grupos y los
        introduce en la tabla de la pantalla.
        """
        if self.botonOrdenar.isChecked():
            orden = 'ORDER BY id ASC'
        else:
            orden = 'ORDER BY id DESC'

        db.cur.execute(f"SELECT * FROM grupos WHERE id LIKE ? {orden}",
                       (f"%{self.barraBusqueda.text()}%",))
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
        en la tabla grupos.

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
        confirmarModificacion: modifica los datos de la tabla grupos.
        """
        self.ventanaEditar = qtw.QWidget()
        self.ventanaEditar.setWindowTitle("Agregar Grupo")
        self.ventanaEditar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        layoutVentanaModificar = qtw.QGridLayout()

        for i in range(len(self.campos)-2):
            label = qtw.QLabel(f"{self.campos[i]}: ")
            label.setObjectName("modificar-label")
            layoutVentanaModificar.addWidget(
                label, i, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)

        self.entry1 = qtw.QLineEdit()
        self.entry1.setMaxLength(40)

        datos = []
        if tipo == "editar":
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            for cell in range(0, len(self.campos)-2):
                datos.append(posicion.sibling(posicion.row(), cell).data())

            self.entry1.setText(datos[0])

            self.ventanaEditar.setWindowTitle("Editar")

        self.entry1.setObjectName("modificar-entry")
        layoutVentanaModificar.addWidget(self.entry1, 0, 1)

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")

        botonConfirmar.clicked.connect(
            lambda: self.confirmarModificacion(tipo, datos))
        layoutVentanaModificar.addWidget(
            botonConfirmar, i+1, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        self.ventanaEditar.setLayout(layoutVentanaModificar)
        self.ventanaEditar.show()

    def confirmarModificacion(self, tipo: str, datosPorDefecto: list | None = None):
        """Este método modifica los datos de la tabla grupos.

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
                        en la tabla grupos.
        """
        if tipo == "editar":
            try:
                db.cur.execute(
                    "UPDATE grupos SET ID = ? WHERE ID = ?",
                    (self.entry1.text().upper(), datosPorDefecto,)
                )
                db.cur.execute(
                    "UPDATE herramientas SET grupo = ? WHERE grupo = ?",
                    (self.entry1.text().upper(), datosPorDefecto,)
                )
                db.cur.execute(
                    "UPDATE subgrupos SET grupo = ? WHERE grupo = ?",
                    (self.entry1.text().upper(), datosPorDefecto,)
                )

                registrarCambios("Edicion", "Grupos", datosPorDefecto[0],
                                 datosPorDefecto[0], self.entry1.text().upper())
                db.con.commit()
                m.mostrarMensaje("Information", "Aviso",
                                 "Se ha actualizado el grupo.")
            except sqlite3.IntegrityError:
                return m.mostrarMensaje("Error", "Error",
                                        "El ID ingresado ya está registrado. Por favor, ingrese otro.")
        else:
            try:
                db.cur.execute(
                    "INSERT INTO grupos VALUES(?) ",
                    (self.entry1.text().upper(),)
                )
                registrarCambios(
                    "Insercion", "Grupos", self.entry1.text().upper(), None,
                    self.entry1.text().upper()
                )
                db.con.commit()
                m.mostrarMensaje(
                    "Information", "Aviso",
                    "Se ha ingresado un grupo."
                )
            except sqlite3.IntegrityError:
                return m.mostrarMensaje(
                    "Error", "Error",
                    "El grupo ingresado ya está registrado. Por favor, ingrese otro."
                )

        self.mostrarDatos()
        self.ventanaEditar.close()

    def eliminar(self):
        """Este método elimina la fila de la tabla grupos.

        Antes de eliminar, confirma la decisión del usuario.
        Si los datos están relacionados con otras tablas, vuelve a
        confirmar la decisión del usuario. Luego, elimina la fila de la
        tabla grupos y las filas en donde los datos estaban
        relacionados. Por último, registra los cambios y actualiza la
        tabla.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                     "¿Está seguro que desea eliminar estos datos?")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd = posicion.sibling(posicion.row(), 0).data()
            db.cur.execute(
                "SELECT grupo FROM herramientas WHERE grupo = ?", (idd,))
            herramientas = db.cur.fetchall()
            db.cur.execute(
                "SELECT grupo FROM subgrupos WHERE grupo = ?", (idd,))
            subgrupo = db.cur.fetchall()
            tipo = "Eliminacion simple"
            tablas = "Alumnos"
            if herramientas or subgrupo:
                tipo = "Eliminacion compleja"
                tablas = "Alumnos Movimientos de herramientas"
                respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                             """
                Todavía hay herramientas y/o subgrupos cargados. 
                Eliminar el grupo eliminará también TODOS los datos en los que está ingresado.
                ¿Desea eliminarlo de todas formas?
                """)
            if respuesta == qtw.QMessageBox.StandardButton.Yes:
                db.cur.execute("SELECT * FROM grupos WHERE ID = ?", (idd,))
                datosEliminados = db.cur.fetchall()[0]
                db.cur.execute("DELETE FROM grupos WHERE ID = ?", (idd,))

                db.cur.execute(
                    "SELECT ID FROM herramientas WHERE grupo = ?", (idd,))
                herramientas = db.cur.fetchall()
                if herramientas:
                    db.cur.execute(
                        "DELETE FROM herramientas WHERE grupo = ?", (idd,))
                    db.cur.execute(
                        """
                        DELETE FROM movimientos_herramientas
                        WHERE id_herramienta = ?""",
                        (idd,)
                    )
                db.cur.execute("DELETE FROM subgrupos WHERE grupo = ?", (idd,))
                registrarCambios(tipo, tablas, idd, f"{datosEliminados}", None)
                db.con.commit()
                self.mostrarDatos()
