# gestion_herramientas.py: la gestión de herramientas. Contiene una tabla, que muestra 
#                          la tabla de la base de datos; una barra de buscador; botones para 
#                          ordenar alfabéticamente la tabla por nombre, grupo y subgrupo de 
#                          herramientas; botones para editar y eliminar los datos; un botón
#                          para agregar herramientas. 
#                          Para editar y agregar, aparece un submenú con los datos a introducir.

# Se importan las librerías.
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os
import datetime as dt

# Se importa la función m.mostrarMensaje.
import db.inicializar_bbdd as db
import mostrar_mensaje as m
from registrar_cambios import registrarCambios


# clase GestiónHerramientas: ya explicada. Es un widget que después se ensambla en un stackwidget en main.py.
class GestionRegistroAlumnosHistoricos(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        self.titulo=qtw.QLabel("GESTIÓN DEL REGISTRO DE ALUMNOS HISTÓRICOS")
        self.titulo.setObjectName("titulo")

        self.subtitulo=qtw.QLabel("Pase alumnos existentes a históricos y revise los alumnos ")
        self.subtitulo.setObjectName("subtitulo")
        # Se crea la tabla.
        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")

        # Se crean los títulos de las columnas de la tabla y se introducen en esta.
        self.campos = ["ID", "DNI", "Nombre y Apellido", "Curso",
                       "Fecha de Salida", "EMAIL", ""]      
                                
        # Se establece el número de columnas que va a tener. 
        self.tabla.setColumnCount(len(self.campos))
        # Se introducen los títulos en la tabla.
        self.tabla.setHorizontalHeaderLabels(self.campos)

        # Se esconden los números de fila de la tabla que vienen por defecto para evitar confusión con el campo ID.
        self.tabla.verticalHeader().hide()
        # Se cambia el ancho de las dos últimas columnas, porque son las que van a tener los botones de editar y eliminar.
        self.tabla.setColumnWidth(2, 120)
        self.tabla.setColumnWidth(3, 200)
        self.tabla.setColumnWidth(5, 35)
        self.tabla.setColumnWidth(6, 35)

        # Se muestran los datos.
        self.mostrarDatos()

        # Se crea una barra de búsqueda
        self.barraBusqueda = qtw.QLineEdit()
        self.barraBusqueda.setObjectName("buscar")
        # Se introduce un botón a la derecha que permite borrar la busqueda con un click.
        self.barraBusqueda.setClearButtonEnabled(True)
        # Se le pone el texto por defecto a la barra de búsqueda
        self.barraBusqueda.setPlaceholderText("Buscar...")
        # Se importa el ícono de lupa para la barra.
        iconoLupa=qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        # Se crea un label que va a contener el ícono.
        contenedorIconoLupa=qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        # Se le da la función de buscar los datos introducidos.
        self.barraBusqueda.textEdited.connect(lambda: self.mostrarDatos())
        # Se crean 3 botones de radio y un label para dar contexto.
        self.label2= qtw.QLabel("Ordenar por: ")
        self.radio1 = qtw.QRadioButton("Nombre")
        self.radio2 = qtw.QRadioButton("DNI")
        self.radio3 = qtw.QRadioButton("Fecha de salida")

        self.radio1.setObjectName("Radio1")
        self.radio2.setObjectName("Radio2")
        self.radio3.setObjectName("Radio3")

        # Se le da a los botones de radio la función de mostrar datos en un orden específico.
        self.radio1.toggled.connect(lambda: self.mostrarDatos())
        self.radio2.toggled.connect(lambda: self.mostrarDatos())
        self.radio3.toggled.connect(lambda: self.mostrarDatos())


        # Se crea el boton de agregar herramientas nuevas.
        self.botonPase = qtw.QPushButton("Pase Individual")
        self.botonPase.setObjectName("confirmar")
        # Se le da la función.
        self.botonPase.clicked.connect(
            lambda: self.paseHistoricoIndividual())
        # Cuando el cursor pasa por el botón, cambia de forma.
        self.botonPase.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        self.botonPaseEgreso = qtw.QPushButton("Pase de Egresados")
        self.botonPaseEgreso.setObjectName("confirmar")
        # Se le da la función.
        self.botonPaseEgreso.clicked.connect(
            lambda: self.paseHistoricoGrupal())
        # Cuando el cursor pasa por el botón, cambia de forma.
        self.botonPaseEgreso.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        # Se crea el layout y se le añaden todos los widgets anteriores.
        layout = qtw.QGridLayout()
        layout.addWidget(self.titulo, 0, 0)
        layout.addWidget(self.barraBusqueda, 1, 0, 1, 2)
        layout.addWidget(contenedorIconoLupa,1,0)
        layout.addWidget(self.label2, 1, 1, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.radio1, 1, 2)
        layout.addWidget(self.radio2, 1, 3, alignment=qtc.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.tabla, 2, 0, 1, 7)
        layout.addWidget(self.botonPase, 3, 0)
        layout.addWidget(self.botonPaseEgreso, 3, 1)

        # Se le da el layout al widget central
        self.setLayout(layout)

        # Se crea este atributo para que exista en la pantalla y no se generen errores al abrir la ventana de edición. Explicado más adelante.
        self.edita = None

# Función mostrar datos: busca los datos de la tabla de la base de datos y los muestra en la tabla con la que el usuario puede interactuar. Parámetro:
    # - consulta: muestra los datos de forma distinta según el tipo de consulta. Es opcional y, si no se introduce, su valor por defecto es normal. Valores:
    # - - Normal: valor por defecto. Muestra todos los datos de la tabla de la base de datos.
    # - - Buscar: Busca en la tabla de la base de datos las filas que contengan lo buscado.
    # - - Nombre: Muestra todos los datos de la tabla de la base de datos ordenados por su nombre.
    # - - Grupo: Muestra todos los datos de la tabla de la base de datos ordenados por su grupo.
    # - - Subgrupo: Muestra todos los datos de la tabla de la base de datos ordenados por su subgrupo.
    def mostrarDatos(self, consulta="Normal"):
        # Si el tipo de consulta es buscar, muestra las filas que contengan lo buscado en la tabla de la base de datos.
        if consulta=="Buscar":
            # Se crea una lista para pasar por parámetro lo buscado en la consulta de la tabla de la base de datos.
            busqueda=[]
            # Por cada campo de la tabla, se añade un valor con el que se comparará.
            for i in range(6): 
                # El valor añadido es el texto en la barra de búsqueda.
                busqueda.append(f"%{self.barraBusqueda.text()}%")
            #Se hace la consulta: selecciona cada fila que cumpla con el requisito de que al menos una celda suya contenga el valor pasado por parámetro.
            db.cur.execute("""
            SELECT * FROM ALUMNOS_HISTORICOS 
            WHERE ID LIKE ? 
            OR DNI LIKE ? 
            OR nombre_apellido LIKE ?
            OR CURSO LIKE ?
            OR FECHA_SALIDA LIKE ? 
            OR EMAIL LIKE ? 
            """, busqueda)
        # Si el tipo es nombre, se hace una consulta que selecciona todos los elementos y los ordena por su nombre.
        elif consulta=="Nombre":
            db.cur.execute("SELECT * FROM ALUMNOS_HISTORICOS ORDER BY nombre_apellido")
        # Si el tipo es grupo, se hace una consulta que selecciona todos los elementos y los ordena por su grupo.
        elif consulta=="DNI":
            db.cur.execute("SELECT * FROM ALUMNOS_HISTORICOS ORDER BY DNI")
        # Si el tipo es grupo, se hace una consulta que selecciona todos los elementos y los ordena por su grupo.
        elif consulta=="Fecha":
            db.cur.execute("SELECT * FROM ALUMNOS_HISTORICOS ORDER BY FECHA_SALIDA")
        # Si el tipo no se cambia o no se introduce, simplemente se seleccionan todos los datos como venian ordenados. 
        elif consulta=="Normal":
            db.cur.execute("SELECT * FROM ALUMNOS_HISTORICOS")
        # Si la consulta es otra, se pasa por consola que un boludo escribió la consulta mal :) y termina la ejecución de la función.
        else:
            print("Error crítico: un bobolon escribio la consulta mal.")
            return
        # Se guarda la consulta en una variable.
        consulta = db.cur.fetchall()
        # Se establece la cantidad de filas que va a tener la tabla
        self.tabla.setRowCount(len(consulta))
        # Bucle: por cada fila de la consulta obtenida, se guarda su id y se genera otro bucle que inserta todos los datos en la fila de la tabla de la ui.
        # Además, se insertan dos botones al costado de cada tabla: uno para editarla y otro para eliminarla.
        for i in range(len(consulta)):

            # Bucle: se introduce en cada celda el elemento correspondiente de la fila.
            for j in range(len(consulta[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(consulta[i][j])))

            self.tabla.setRowHeight(i, 35)
        
            botonEliminar = qtw.QPushButton()
            botonEliminar.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/eliminar.png")))
            botonEliminar.setIconSize(qtc.QSize(25, 25))
            botonEliminar.setObjectName("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar())
            botonEliminar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, len(self.campos)-1, botonEliminar)
    
    def eliminar(self):
        # se le pregunta al usuario si desea eliminar la fila.
        resp = m.mostrarMensaje("Pregunta", "Advertencia",
                              "¿Está seguro que desea eliminar estos datos?")
        # si pulsó el boton de sí:
        if resp == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            # luego se obtiene la posicion del boton.
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd=posicion.sibling(posicion.row(), 0).data()
            # elimina la fila con el id correspondiente de la tabla de la base de datos.
            db.cur.execute("SELECT * FROM MOVIMIENTOS_HERRAMIENTAS WHERE CLASE=0 AND ID_PERSONA = ?", (idd,))
            tipo="Eliminación simple"
            tablas="Alumnos históricos"
            if db.cur.fetchall():
                tipo="Eliminación compleja"
                tablas="Alumnos históricos Movimientos de herramientas"
                resp=m.mostrarMensaje("Pregunta", "Advertencia", """
El alumno tiene movimientos registrados. 
Eliminarlo eliminará tambien TODOS los movimientos en los que está registrado,
por lo que sus registros de deudas se eliminarán y podría perderse información valiosa.

¿Desea eliminarlo de todas formas?
""")
            if resp == qtw.QMessageBox.StandardButton.Yes:
                db.cur.execute("SELECT * FROM ALUMNOS_HISTORICOS WHERE ID = ?", (idd,))
                datosEliminados=db.cur.fetchall()[0]
                db.cur.execute("DELETE FROM ALUMNOS_HISTORICOS WHERE ID = ?", (idd,))
                db.cur.execute("DELETE FROM MOVIMIENTOS_HERRAMIENTAS WHERE CLASE=0 AND ID_PERSONA = ?", (idd,))
                db.cur.execute("UPDATE TURNO_PANOL SET ID_ALUMNO=NULL WHERE ID_ALUMNO = ?", (idd,))
                registrarCambios(tipo, tablas, idd, f"{datosEliminados}", None,) 
                db.con.commit()
                self.mostrarDatos()


    # Función paseHistorico: muestra un mensaje con un formulario que permite editar o ingresar los elementos a la tabla.
    # Parametros: tipo: pregunta de que tipo va a ser la edición. Valores posibles:
    # # editar: se creará una ventana con un f0rmulario y al enviar los datos se modifican los datos de la fila en la que se pulsó el boton de edición.
    # # crear / insertar / None: crea una ventana con un formulario que insertará los datos en la tabla. 
    # # Identica a la de editar pero no viene con datos por defecto.
    def paseHistoricoIndividual(self):
        # Se crea el widget que va a funcionar como ventana.
        self.menuPase = qtw.QWidget()
        # Se le da el título a la ventana, que por defecto es agregar.
        self.menuPase.setWindowTitle("Realizar Pase Histórico Individual de Alumnos")
        self.menuPase.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))

        titulo=qtw.QLabel("Ingresa al alumno que quieres pasar a histórico")
        titulo.setObjectName("subtitulo")
        label1=qtw.QLabel("Nombre del Alumno: ")
        label2=qtw.QLabel("DNI: ")
        
        # Crea los entries. 
        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QLineEdit()

        sugerenciasNombre=[]

        db.cur.execute("SELECT nombre_apellido FROM ALUMNOS WHERE CURSO IN ('7A', '7B')")

        for i in db.cur.fetchall():
            sugerenciasNombre.append(i[0])
            
        cuadroSugerenciasNombre=qtw.QCompleter(sugerenciasNombre, self)
        cuadroSugerenciasNombre.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry1.setCompleter(cuadroSugerenciasNombre)
        self.entry1.editingFinished.connect(lambda:self.cargarDNI(self.entry1.text()))
       
        # Se crea una lista de datos vacía en la que se introduciran los valores que pasaran por defecto a la ventana.
        datos = []

        self.entry1.setObjectName("modificar-entry")
        self.entry2.setObjectName("modificar-entry")

        # Se crea el boton de confirmar, y se le da la función de confirmarr.
        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))
        botonConfirmar.clicked.connect(lambda: self.confirmarIndividual(datos))

        layoutMenuPase = qtw.QGridLayout()
        layoutMenuPase.addWidget(titulo, 0, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layoutMenuPase.addWidget(label1, 1, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layoutMenuPase.addWidget(label2, 2, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layoutMenuPase.addWidget(self.entry1, 1, 1)
        layoutMenuPase.addWidget(self.entry2, 2, 1)
        layoutMenuPase.addWidget(botonConfirmar, 3, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        # Se le da el layout a la ventana.
        self.menuPase.setLayout(layoutMenuPase)
        # Se muestra la ventana
        self.menuPase.show()

    def cargarDNI(self, nombre):
        db.cur.execute("SELECT DNI FROM ALUMNOS WHERE nombre_apellido = ?", (nombre,))

        sugerenciasDNI=[]

        for i in db.cur.fetchall():
            sugerenciasDNI.append(str(i[0]))

        cuadroSugerenciasDNI=qtw.QCompleter(sugerenciasDNI, self)
        cuadroSugerenciasDNI.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry2.setCompleter(cuadroSugerenciasDNI)

    # Función confirmar: se añaden o cambian los datos de la tabla en base al parámetro datos.
    def confirmarIndividual(self, datos):
        resp = m.mostrarMensaje("Pregunta", "Atención", 
        "¿Está seguro que desea pasar a este alumno al registro histórico? Esto no se puede deshacer")
        if resp:
            db.cur.execute("SELECT * FROM ALUMNOS WHERE DNI = ? AND CURSO IN ('7A', '7B')",(self.entry2.text(),))
            datos=db.cur.fetchall()
            if not datos:
                return m.mostrarMensaje("Error", "Error", "El DNI no coincide con el alumno. Por favor, intente nuevamente.")
            db.cur.execute("INSERT INTO ALUMNOS_HISTORICOS VALUES(?, ?, ?, ?, ?, ?) ", (
                    datos[0][0], datos[0][1], datos[0][2], datos[0][3],
                    dt.date.today().strftime("%Y/%m/%d"), datos[0][4]
            ))
            db.cur.execute("DELETE FROM ALUMNOS WHERE ID = ?", (datos[0][0],))
            registrarCambios("Pase historico individual", "Alumnos historicos", datos[0][0], f"{datos[0]}", None,)
            db.con.commit()
            m.mostrarMensaje("Information", "Aviso",
                        "Se ha pasado un alumno al registro histórico.")    
            #Se refrescan los datos.
            self.mostrarDatos()
            self.menuPase.close()

    def paseHistoricoGrupal(self):
        # Se crea el widget que va a funcionar como ventana.
        self.menuPase = qtw.QWidget()
        # Se le da el título a la ventana, que por defecto es agregar.
        self.menuPase.setWindowTitle("Realizar Pase Histórico Grupal de Alumnos")
        self.menuPase.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))

        titulo=qtw.QLabel("Seleccione los alumnos que desea egresar y dejar registrados históricamente.")
        titulo.setObjectName("subtitulo")
        
        
        # Crea los entries. 
        self.barraBusquedaPase = qtw.QLineEdit()
        self.barraBusquedaPase.setObjectName("buscar")
        # Se introduce un botón a la derecha que permite borrar la busqueda con un click.
        self.barraBusquedaPase.setClearButtonEnabled(True)
        # Se le pone el texto por defecto a la barra de búsqueda
        self.barraBusquedaPase.setPlaceholderText("Buscar...")
        # Se importa el ícono de lupa para la barra.
        iconoLupa=qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        # Se crea un label que va a contener el ícono.
        contenedorIconoLupa=qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        # Se le da la función de buscarPase los datos introducidos.
        self.barraBusquedaPase.textEdited.connect(lambda: self.mostrarDatosPase())

        self.tablaListaAlumnos=qtw.QTableWidget()
        self.tablaListaAlumnos.setMaximumSize(400, 345)

        self.camposPase = ["", "Nombre y Apellido", "DNI", "Curso"]
                                
        # Se establece el número de columnas que va a tener. 
        self.tablaListaAlumnos.setColumnCount(len(self.camposPase))
        self.tablaListaAlumnos.setColumnWidth(0, 15)   
        self.tablaListaAlumnos.setColumnWidth(1, 125)   
        # Se introducen los títulos en la tabla.
        self.tablaListaAlumnos.setHorizontalHeaderLabels(self.camposPase)
        self.tablaListaAlumnos.verticalHeader().hide()
        self.mostrarDatosPase()

        # Se crea el boton de confirmar, y se le da la función de confirmarr.
        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))
        botonConfirmar.clicked.connect(lambda: self.confirmarPase())
        botonConfirmar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        layoutMenuPase = qtw.QGridLayout()
        layoutMenuPase.addWidget(titulo, 0, 0, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layoutMenuPase.addWidget(self.barraBusquedaPase, 1, 0)
        layoutMenuPase.addWidget(contenedorIconoLupa,1,0)
        layoutMenuPase.addWidget(self.tablaListaAlumnos, 2, 0, 1, 4)
        layoutMenuPase.addWidget(botonConfirmar, 3, 0)
        layoutMenuPase.addWidget(botonConfirmar, 3, 0, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        # Se le da el layout a la ventana.
        self.menuPase.setLayout(layoutMenuPase)
        # Se muestra la ventana
        self.menuPase.show()
    
    def mostrarDatosPase(self, consulta="Normal"):
        cursosPase=["7A", "7B"]
        # Si el tipo de consulta es buscar, muestra las filas que contengan lo buscado en la tabla de la base de datos.
        if consulta=="Buscar":
            #Se hace la consulta: selecciona cada fila que cumpla con el requisito de que al menos una celda suya contenga el valor pasado por parámetro.
            db.cur.execute("""
            SELECT nombre_apellido, DNI, CURSO
            FROM ALUMNOS
            WHERE CURSO IN (?, ?)
            AND nombre_apellido LIKE ?
            OR DNI LIKE ?
            OR CURSO LIKE ?
            ORDER BY CURSO, ID""", (cursosPase[0], cursosPase[1], 
            self.barraBusquedaPase.text(), self.barraBusquedaPase.text(), self.barraBusquedaPase.text()))
        elif consulta=="Normal":
            db.cur.execute("""
            SELECT nombre_apellido, DNI, CURSO
            FROM ALUMNOS
            WHERE CURSO IN (?, ?)
            ORDER BY CURSO, ID""", (cursosPase[0], cursosPase[1],))
        # Si la consulta es otra, se pasa por consola que un boludo escribió la consulta mal :) y termina la ejecución de la función.
        else:
            print("Error crítico: un bobolon escribio la consulta mal.")
            return
        # Se guarda la consulta en una variable.
        consulta = db.cur.fetchall()
        # Se establece la cantidad de filas que va a tener la tabla
        self.tablaListaAlumnos.setRowCount(len(consulta))
        # Bucle: por cada fila de la consulta obtenida, se guarda su id y se genera otro bucle que inserta todos los datos en la fila de la tabla de la ui.
        # Además, se insertan dos botones al costado de cada tabla: uno para editarla y otro para eliminarla.
        for i in range(len(consulta)):
            # Bucle: se introduce en cada celda el elemento correspondiente de la fila.
            check=qtw.QCheckBox()
            check.setObjectName("check")
            check.toggle()
            self.tablaListaAlumnos.setCellWidget(i, 0, check)
            for j in range(len(consulta[i])):
                self.tablaListaAlumnos.setItem(i, j+1, qtw.QTableWidgetItem(str(consulta[i][j])))

            self.tablaListaAlumnos.setRowHeight(i, 35)
    
    def confirmarGrupal(self):
        for i in range(self.tablaListaAlumnos.rowCount()):
            datosGrupales=[]
            if self.tablaListaAlumnos.cellWidget(i, 0).isChecked():
                db.cur.execute("SELECT * FROM ALUMNOS WHERE DNI = ?", (int(self.tablaListaAlumnos.item(i, 2).text())))
                datos=db.cur.fetchall()
                db.cur.execute("INSERT INTO ALUMNOS_HISTORICOS VALUES(?, ?, ? , ?, ?, ?)", (
                    datos[0][0], datos[0][1], datos[0][2], datos[0][3], 
                    dt.date.today().strftime("%Y/%m/%d"), datos[0][4]
                ))
                datosGrupales.append(datos[0][0])
                db.cur.execute("DELETE FROM ALUMNOS WHERE ID = ?", (datos[0][0],))
        registrarCambios(
            "Pase historico grupal", "Alumnos historicos", datos[0][0], f"{datosGrupales}", None
            )
        db.con.commit()

        