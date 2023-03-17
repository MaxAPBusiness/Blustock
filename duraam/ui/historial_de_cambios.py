"""Este módulo crea una pantalla para mostrar los datos de la tabla
historial_de_cambios. 

Clases
------
    HistorialDeCambios(qtw.QWidget):
        Crea una pantalla para mostrar los datos de la tabla
        historial_de_cambios.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os
import datetime as dt

import db.inicializar_bbdd as db
from .botones import BotonOrdenar

# Método dedent: elimina la identación de un texto.
# Lo usamos para que los textos multilinea (los que tienen """) se
# muestren sin la sangría del código de la izquierda.
from textwrap import dedent

class HistorialDeCambios(qtw.QWidget):
    """Esta clase crea una pantalla mostrar los datos de la tabla
    historial_de_cambios. 

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            La tabla de la pantalla.
        campos : tuple
            Los títulos de las columnas de la tabla.
        barraBusqueda : QLineEdit
            La barra de búsqueda.
        radioHerramienta : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            herramienta.
        radioAlumno : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            alumno.
        radioFecha : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            fecha.
        entryFechaDesde : QDateTimeEdit
            El entry de fecha para marcar desde que fecha se pueden
            mostrar los datos.
        entryFechaHasta : QDateTimeEdit
            El entry de fecha para marcar hasta que fecha se pueden
            mostrar los datos.
        listaHerramientas : QComboBox
            Una lista para elegir una herramienta para que se muestren
            solo sus datos
        listaEstado : QComboBox
            Una lista para elegir que se muestren solo los datos con un
            dato específico

    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionAdministradores.

            Crea la pantalla, un QWidget, que contiene un título
            descrptivo, un QLabel y una tabla, un QTableWidget, que
            muestra los datos de la tabla administradores y que
            contiene botones para degradar su rol.

        mostrarDatos(self):
            Obtiene los datos de la tabla administradores y los
            introduce en la tabla de la pantalla.

        degradar(self):
            Degrada el rol del administrador a usuario.
    """

    def __init__(self):
        super().__init__()

        titulo = qtw.QLabel("Historial de cambios")
        titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("Nombre y apellido", "Usuario",
                       "Fecha y hora", "Descripción del cambio")
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(0, 125)
        self.tabla.setColumnWidth(3, 400)

        self.barraBusqueda = qtw.QLineEdit()
        self.barraBusqueda.setObjectName("buscar")
        self.barraBusqueda.setClearButtonEnabled(True)
        self.barraBusqueda.setPlaceholderText("Buscar...")
        iconoLupa = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        contenedorIconoLupa = qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        self.barraBusqueda.textEdited.connect(lambda: self.mostrarDatos())
        labelOrdenar = qtw.QLabel("Ordenar por: ")
        self.radioUsuario = qtw.QRadioButton("Usuario")
        self.radioFecha = qtw.QRadioButton("Fecha")
        self.radioTipo = qtw.QRadioButton("Tipo")
        self.radioTabla = qtw.QRadioButton("Tabla")
        self.radioUsuario.setObjectName("Radio1")
        self.radioFecha.setObjectName("Radio2")
        self.radioTipo.setObjectName("Radio3")
        self.radioTabla.setObjectName("Radio3")
        self.radioUsuario.toggled.connect(lambda: self.mostrarDatos())
        self.radioFecha.toggled.connect(lambda: self.mostrarDatos())
        self.radioTipo.toggled.connect(lambda: self.mostrarDatos())
        self.radioTabla.toggled.connect(lambda: self.mostrarDatos())

        self.botonOrdenar = BotonOrdenar()
        self.botonOrdenar.stateChanged.connect(lambda: self.ordenar())

        labelUsuario = qtw.QLabel("Usuario: ")
        self.usuario = qtw.QComboBox()
        self.usuario.addItem("Todos")
        db.cur.execute("SELECT usuario FROM administradores WHERE id IN (SELECT DISTINCT id_usuario FROM historial_de_cambios)")
        for i in db.cur.fetchall():
            self.usuario.addItem(i[0])
        db.cur.execute("SELECT usuario FROM usuarios WHERE id IN (SELECT DISTINCT id_usuario FROM historial_de_cambios)")
        for i in db.cur.fetchall():
            self.usuario.addItem(i[0])
        self.usuario.currentIndexChanged.connect(lambda: self.mostrarDatos())

        labelFechaDesde = qtw.QLabel("Desde: ")
        self.entryFechaDesde = qtw.QDateEdit()
        self.entryFechaDesde.setDate(
            qtc.QDate.fromString(
                "12/12/2012", "dd/MM/yyyy")
        )
        self.entryFechaDesde.editingFinished.connect(
            lambda: self.mostrarDatos())

        labelFechaHasta = qtw.QLabel("Hasta: ")
        self.entryFechaHasta = qtw.QDateEdit()
        self.entryFechaHasta.setDate(
            qtc.QDate.fromString(
                dt.date.today().strftime("%d/%m/%Y"),
                "dd/MM/yyyy"
            )
        )
        self.entryFechaHasta.editingFinished.connect(
            lambda: self.mostrarDatos())

        labelTipo = qtw.QLabel("Tipo: ")
        self.tipo = qtw.QComboBox()
        self.tipo.addItem("Todos")
        self.tipo.addItem("Insercion")
        self.tipo.addItem("Edicion")
        self.tipo.addItem("Eliminación")
        self.tipo.addItem("Pase anual")
        self.tipo.addItem("Pase histórico individual")
        self.tipo.addItem("Pase histórico grupal")
        self.tipo.addItem("Verificacion de solicitud")
        self.tipo.addItem("Rechazo de solicitud")
        self.tipo.addItem("Ascenso")
        self.tipo.addItem("Descenso")
        self.tipo.currentIndexChanged.connect(lambda: self.mostrarDatos())

        labelTabla = qtw.QLabel("Tabla: ")
        self.seleccionarTabla = qtw.QComboBox()
        self.seleccionarTabla.addItem("Todas")
        self.seleccionarTabla.addItem("Herramientas")
        self.seleccionarTabla.addItem("Movimientos de herramientas")
        self.seleccionarTabla.addItem("Turnos del pañol")
        self.seleccionarTabla.addItem("Alumnos")
        self.seleccionarTabla.addItem("Profesores")
        self.seleccionarTabla.addItem("Grupos")
        self.seleccionarTabla.addItem("Subgrupos")
        self.seleccionarTabla.addItem("Alumnos históricos")
        self.seleccionarTabla.addItem("Profesores históricos")
        self.seleccionarTabla.addItem("Usuarios")
        self.seleccionarTabla.addItem("Administradores")
        self.seleccionarTabla.currentIndexChanged.connect(
            lambda: self.mostrarDatos())

        layout = qtw.QVBoxLayout()
        layout.addWidget(titulo)
        contenedor1 = qtw.QWidget()
        contenedor1Layout = qtw.QGridLayout()
        contenedor1Layout.addWidget(self.barraBusqueda, 0, 0)
        contenedor1Layout.addWidget(contenedorIconoLupa, 0, 0)
        contenedor1Layout.addWidget(labelOrdenar, 0, 1)
        contenedor1Layout.addWidget(self.radioUsuario, 0, 2)
        contenedor1Layout.addWidget(self.radioFecha, 0, 3)
        contenedor1Layout.addWidget(self.radioTipo, 0, 4)
        contenedor1Layout.addWidget(self.radioTabla, 0, 5)
        contenedor1Layout.addWidget(self.botonOrdenar, 0, 6)
        contenedor1.setLayout(contenedor1Layout)
        layout.addWidget(contenedor1)
        contenedor2 = qtw.QWidget()
        contenedor2Layout = qtw.QHBoxLayout()
        contenedor2Layout.addWidget(labelUsuario)
        contenedor2Layout.addWidget(self.usuario)
        contenedor2Layout.addWidget(labelFechaDesde)
        contenedor2Layout.addWidget(self.entryFechaDesde)
        contenedor2Layout.addWidget(labelFechaHasta)
        contenedor2Layout.addWidget(self.entryFechaHasta)
        contenedor2Layout.addWidget(labelTipo)
        contenedor2Layout.addWidget(self.tipo)
        contenedor2Layout.addWidget(labelTabla)
        contenedor2Layout.addWidget(self.seleccionarTabla)
        contenedor2.setLayout(contenedor2Layout)
        layout.addWidget(contenedor2)
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla administradores y
        los introduce en la tabla de la pantalla.

        Los datos se muestran acorde a los filtros seleccionados de la
        pantalla. La descripción se muestra acorde al tipo de cambio
        registrado.
        """
        if self.usuario.currentText() == "Todos":
            usuario = ""
        else:
            usuario = self.usuario.currentText()

        if self.tipo.currentText() == "Todos":
            tipo = ""
        else:
            tipo = self.tipo.currentText()

        if self.seleccionarTabla.currentText() == "Todas":
            tabla = ""
        else:
            tabla = self.seleccionarTabla.currentText()

        if self.radioUsuario.isChecked():
            orden = "ORDER BY nombre, h.fecha_hora"
        elif self.radioFecha.isChecked():
            orden = "ORDER BY h.fecha_hora"
        elif self.radioTipo.isChecked():
            orden = "ORDER BY h.tipo, h.fecha_hora"
        elif self.radioTabla.isChecked():
            orden = "ORDER BY h.tabla, h.fecha_hora"
        else:
            orden = ""
        
        if orden and self.botonOrdenar.isChecked():
            orden += " DESC"
        elif self.botonOrdenar.isChecked():
            orden="ORDER BY nombre DESC"

        # Explico esta monstruosidad. Primero, si el rol es 0, es
        # decir, si el rol es usuario, entonces selecciona el nombre
        # de la tabla usuarios. Sino, selecciona el nombre de la tabla
        # administradores. Lo guarda bajo el alias "nombre". Luego,
        # hace lo mismo para el usuario y lo guarda bajo el alias
        # "usuario". Luego selecciona la fecha y hora, tipo, tabla,
        # id de fila, datos viejos y datos nuevos de la tabla historial
        # de cambios. Luego hace los joins. Después, hace la
        # comparación con la búsqueda (ya explicado en otros módulos).
        # Finalmente, verifica que los datos coincidan con lo
        # seleccionado en las listas. Para una explicación más
        # detallada sobre los campos y como se registran los datos en
        # el historial, lean el código sql de la app y el módulo
        # registrar_cambios.py
        db.cur.execute(f"""
        SELECT (CASE WHEN h.rol = 0 THEN u.nombre_apellido ELSE a.nombre_apellido END) AS nombre,
        (CASE WHEN h.rol = 0 THEN u.usuario ELSE a.usuario END) AS nombre_usuario,
        h.fecha_hora, h.tipo, h.tabla, h.id_fila, h.datos_viejos, h.datos_nuevos
        FROM historial_de_cambios h
        LEFT JOIN usuarios u
        ON u.id = h.id_usuario
        LEFT JOIN administradores a
        ON a.id = h.id_usuario
        WHERE (nombre LIKE ? 
        OR nombre_usuario LIKE ? 
        OR h.fecha_hora LIKE ?
        OR h.tipo LIKE ? 
        OR h.tabla LIKE ? 
        OR h.id_fila LIKE ? 
        OR h.datos_viejos LIKE ?
        OR h.datos_nuevos LIKE ?)
        AND nombre_usuario LIKE ?
        AND h.tipo LIKE ?
        AND h.tabla LIKE ?
        {orden}
        """, (f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
              f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
              f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
              f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
              f"%{usuario}%", f"%{tipo}%", f"%{tabla}%",))
        fetch = db.cur.fetchall()
        consulta = []
        for i in fetch:
            fecha = qtc.QDateTime.fromString(i[2], "dd/MM/yyyy hh:mm:ss")
            if (fecha >= qtc.QDateTime.fromString(f"{self.entryFechaDesde.date().toString('dd/MM/yyyy')} 00:00:00", "dd/MM/yyyy hh:mm:ss")
                and fecha <= qtc.QDateTime.fromString(f"{self.entryFechaHasta.date().toString('dd/MM/yyyy')} 23:59:59", "dd/MM/yyyy hh:mm:ss")):
                consulta.append(i)

        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            self.tabla.setItem(i, 0, qtw.QTableWidgetItem(str(consulta[i][0])))
            self.tabla.setItem(i, 1, qtw.QTableWidgetItem(str(consulta[i][1])))
            self.tabla.setItem(i, 2, qtw.QTableWidgetItem(str(consulta[i][2])))

            # Dependiendo del tipo de consulta, muestra algo distinto
            # en el campo descripción.
            # Los datos viejos del historial son los datos antes de un
            # cambio, los datos nuevos son los datos que aparecen
            # despues del cambio. Al insertar datos, por ejemplo, no
            # se guarda nada en los datos viejos porque no hay.
            # De la misma forma, al eliminar datos, no se guarda nada
            # en el campo datos nuevos.
            if consulta[i][3] == "Insercion":
                if consulta[i][5]:
                    textoId = f" de id {consulta[i][5]}"
                else:
                    textoId = ""
                descripcion = f"Agregó a la tabla {consulta[i][4]} la fila{textoId} con los datos {consulta[i][7]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Edicion":
                if consulta[i][5]:
                    textoId = f" de id {consulta[i][5]}"
                else:
                    textoId = ""
                descripcion = f"Editó la fila{textoId} de la tabla {consulta[i][4]}, reemplazando los datos{consulta[i][6]} con los datos {consulta[i][7]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Eliminacion simple":
                if consulta[i][5]:
                    textoId = f" de id {consulta[i][5]}"
                else:
                    textoId = ""
                descripcion = f"Eliminó de la tabla {consulta[i][4]} la fila{textoId} que tenía los datos {consulta[i][6]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Eliminacion compleja":
                if consulta[i][5]:
                    textoId = f" de id {consulta[i][5]}"
                else:
                    textoId = ""
                descripcion = dedent(f"""Eliminó de las tablas {consulta[i][4]} la fila{textoId}
                            que tenía los datos {consulta[i][6]},
                            lo que eliminó también todas las filas relacionadas en otras tablas.""")
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Pase Anual":
                descripcion = f"Realizó el pase anual de los alumnos de id: {consulta[i][6]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Pase historico individual":
                descripcion = f"Realizó el pase histórico individual de {consulta[i][4]} de la persona de id: {consulta[i][5]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Pase historico grupal":
                descripcion = f"Realizó el pase histórico grupal de {consulta[i][4]} de las personas de id: {consulta[i][6]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Verificacion de solicitud":
                descripcion = f"Aceptó la solicitud del usuario cuyos datos son: {consulta[i][7]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Rechazo de solicitud":
                descripcion = f"Rechazó la solicitud del usuario cuyos datos eran: {consulta[i][6]}"
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Ascenso":
                descripcion = f"Ascendió al usuario con los datos: {consulta[i][7]} a administrador."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            elif consulta[i][3] == "Descenso":
                descripcion = f"Descendió al administrador con los datos: {consulta[i][7]} a usuario."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))

            self.tabla.setRowHeight(i, 35)
    
    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()
