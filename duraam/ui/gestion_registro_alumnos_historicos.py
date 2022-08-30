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
import sqlite3 as db
import os
import datetime as dt

# Se importa la función mostrarMensaje.
from mostrar_mensaje import mostrarMensaje
from cursos import cursos
# Se hace una conexión a la base de datos
os.chdir(f"{os.path.abspath(__file__)}/../../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()


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
        self.buscar = qtw.QLineEdit()
        self.buscar.setObjectName("buscar")
        # Se introduce un botón a la derecha que permite borrar la busqueda con un click.
        self.buscar.setClearButtonEnabled(True)
        # Se le pone el texto por defecto a la barra de búsqueda
        self.buscar.setPlaceholderText("Buscar...")
        # Se importa el ícono de lupa para la barra.
        lupa=qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        # Se crea un label que va a contener el ícono.
        icono=qtw.QLabel()
        icono.setObjectName("lupa")
        icono.setPixmap(lupa)

        # Se le da la función de buscar los datos introducidos.
        self.buscar.returnPressed.connect(lambda: self.mostrarDatos("Buscar"))
        # Se crean 3 botones de radio y un label para dar contexto.
        self.label2= qtw.QLabel("Ordenar por: ")
        self.radio1 = qtw.QRadioButton("Nombre")
        self.radio2 = qtw.QRadioButton("DNI")
        self.radio3 = qtw.QRadioButton("Fecha de salida")

        self.radio1.setObjectName("Radio1")
        self.radio2.setObjectName("Radio2")
        self.radio3.setObjectName("Radio3")

        # Se le da a los botones de radio la función de mostrar datos en un orden específico.
        self.radio1.toggled.connect(lambda: self.mostrarDatos("Nombre"))
        self.radio2.toggled.connect(lambda: self.mostrarDatos("DNI"))
        self.radio3.toggled.connect(lambda: self.mostrarDatos("Fecha"))


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
        layout.addWidget(self.buscar, 1, 0)
        layout.addWidget(icono,1,0)
        layout.addWidget(self.label2, 1, 1)
        layout.addWidget(self.radio1, 1, 2)
        layout.addWidget(self.radio2, 1, 3)
        layout.addWidget(self.tabla, 2, 0, 1, 9)
        layout.addWidget(self.botonPase, 3, 0)

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
            # Se crea una lista para pasar por parámetro lo buscado en la query de la tabla de la base de datos.
            busqueda=[]
            # Por cada campo de la tabla, se añade un valor con el que se comparará.
            for i in range(4): 
                # El valor añadido es el texto en la barra de búsqueda.
                busqueda.append(f"%{self.buscar.text()}%")
            #Se hace la query: selecciona cada fila que cumpla con el requisito de que al menos una celda suya contenga el valor pasado por parámetro.
            cur.execute("""
            SELECT * FROM ALUMNOS_HISTORICOS 
            WHERE ID LIKE ? 
            OR DNI LIKE ? 
            OR NOMBRE_APELLIDO LIKE ? 
            OR EMAIL LIKE ? 
            """, busqueda)
        # Si el tipo es nombre, se hace una query que selecciona todos los elementos y los ordena por su nombre.
        elif consulta=="Nombre":
            cur.execute('SELECT * FROM ALUMNOS_HISTORICOS ORDER BY NOMBRE_APELLIDO')
        # Si el tipo es grupo, se hace una query que selecciona todos los elementos y los ordena por su grupo.
        elif consulta=="DNI":
            cur.execute('SELECT * FROM ALUMNOS_HISTORICOS ORDER BY DNI')
        # Si el tipo es grupo, se hace una query que selecciona todos los elementos y los ordena por su grupo.
        elif consulta=="Fecha":
            cur.execute('SELECT * FROM ALUMNOS_HISTORICOS ORDER BY FECHA_SALIDA')
        # Si el tipo no se cambia o no se introduce, simplemente se seleccionan todos los datos como venian ordenados. 
        elif consulta=="Normal":
            cur.execute('SELECT * FROM ALUMNOS_HISTORICOS')
        # Si la consulta es otra, se pasa por consola que un boludo escribió la consulta mal :) y termina la ejecución de la función.
        else:
            print("Error crítico: un bobolon escribio la consulta mal.")
            return
        # Se guarda la consulta en una variable.
        query = cur.fetchall()
        # Se establece la cantidad de filas que va a tener la tabla
        self.tabla.setRowCount(len(query))
        # Bucle: por cada fila de la consulta obtenida, se guarda su id y se genera otro bucle que inserta todos los datos en la fila de la tabla de la ui.
        # Además, se insertan dos botones al costado de cada tabla: uno para editarla y otro para eliminarla.
        for i in range(len(query)):

            # Bucle: se introduce en cada celda el elemento correspondiente de la fila.
            for j in range(len(query[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(query[i][j])))

            self.tabla.setRowHeight(i, 35)


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

        cur.execute("SELECT NOMBRE FROM ALUMNOS")

        for i in cur.fetchall():
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
        confirmar = qtw.QPushButton("Confirmar")
        confirmar.setObjectName("confirmar")
        confirmar.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))
        confirmar.clicked.connect(lambda: self.confirmarIndividual(datos))

        layoutMenuPase = qtw.QGridLayout()
        layoutMenuPase.addWidget(titulo, 0, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layoutMenuPase.addWidget(label1, 1, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layoutMenuPase.addWidget(label2, 2, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layoutMenuPase.addWidget(self.entry1, 1, 1)
        layoutMenuPase.addWidget(self.entry2, 2, 1)
        layoutMenuPase.addWidget(confirmar, 3, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        # Se le da el layout a la ventana.
        self.menuPase.setLayout(layoutMenuPase)
        # Se muestra la ventana
        self.menuPase.show()

    def cargarDNI(self, nombre):
        cur.execute("SELECT DNI FROM ALUMNOS WHERE NOMBRE_APELLIDO=?", (nombre,))

        sugerenciasDNI=[]

        for i in cur.fetchall():
            sugerenciasDNI.append(i[0])

        cuadroSugerenciasDNI=qtw.QCompleter(sugerenciasDNI, self)
        cuadroSugerenciasDNI.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry2.setCompleter(cuadroSugerenciasDNI)

    # Función confirmar: se añaden o cambian los datos de la tabla en base al parámetro datos.
    def confirmarIndividual(self, datos):
        global mostrarMensaje
        resp = mostrarMensaje("Pregunta", "Atención", 
        "¿Está seguro que desea pasar a este alumno al registro histórico? Esto no se puede deshacer")
        if resp:
            cur.execute("SELECT * FROM ALUMNOS WHERE DNI=?",(self.entry2.text(),))
            datos=cur.fetchall()
            cur.execute("INSERT INTO ALUMNOS_HISTORICOS VALUES(?, ?, ?, ?, ?, ?) ", (
                    datos[0][0], datos[0][1], datos[0][2], datos[0][3],
                    dt.date.today().strftime('%Y/%m/%d'), datos[0][4]
            ))
            cur.execute('DELETE FROM ALUMNOS WHERE ID=?', (datos[0][0]))

            mostrarMensaje("Information", "Aviso",
                        "Se ha pasado un alumno al registro histórico.")
            mostrarMensaje("Error", "Error", "El ID ingresado ya está registrado. Por favor, ingrese otro.")    
            #Se refrescan los datos.
            self.mostrarDatos()
            self.menuPase.close()

    def realizarPaseGrupal(self):
        # Se crea el widget que va a funcionar como ventana.
        self.menuPase = qtw.QWidget()
        # Se le da el título a la ventana, que por defecto es agregar.
        self.menuPase.setWindowTitle("Realizar Pase Histórico Grupal de Alumnos")
        self.menuPase.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))

        titulo=qtw.QLabel("Seleccione los alumnos que desea egresar y dejar registrados históricamente.")
        titulo.setObjectName("subtitulo")
        
        
        # Crea los entries. 
        self.buscar = qtw.QLineEdit()
        self.buscar.setObjectName("buscar")
        # Se introduce un botón a la derecha que permite borrar la busqueda con un click.
        self.buscar.setClearButtonEnabled(True)
        # Se le pone el texto por defecto a la barra de búsqueda
        self.buscar.setPlaceholderText("Buscar...")
        # Se importa el ícono de lupa para la barra.
        lupa=qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        # Se crea un label que va a contener el ícono.
        icono=qtw.QLabel()
        icono.setObjectName("lupa")
        icono.setPixmap(lupa)

        # Se le da la función de buscar los datos introducidos.
        self.buscar.editingFinished.connect(lambda: self.mostrarDatosPase("Buscar"))

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
        confirmar = qtw.QPushButton("Confirmar")
        confirmar.setObjectName("confirmar")
        confirmar.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))
        confirmar.clicked.connect(lambda: self.confirmarPase())
        confirmar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        layoutMenuPase = qtw.QGridLayout()
        layoutMenuPase.addWidget(titulo, 0, 0, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layoutMenuPase.addWidget(self.buscar, 1, 0)
        layoutMenuPase.addWidget(icono,1,0)
        layoutMenuPase.addWidget(self.tablaListaAlumnos, 2, 0, 1, 4)
        layoutMenuPase.addWidget(confirmar, 3, 0)
        layoutMenuPase.addWidget(confirmar, 3, 0, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        # Se le da el layout a la ventana.
        self.menuPase.setLayout(layoutMenuPase)
        # Se muestra la ventana
        self.menuPase.show()
    
    def mostrarDatosPase(self, consulta="Normal"):
        cursosPase=["7A", "7B"]
        # Si el tipo de consulta es buscar, muestra las filas que contengan lo buscado en la tabla de la base de datos.
        if consulta=="Buscar":
            #Se hace la query: selecciona cada fila que cumpla con el requisito de que al menos una celda suya contenga el valor pasado por parámetro.
            cur.execute("""
            SELECT NOMBRE_APELLIDO, DNI, CURSO
            FROM ALUMNOS
            WHERE CURSO IN (?, ?)
            AND NOMBRE_APELLIDO LIKE ?
            OR DNI LIKE ?
            OR CURSO LIKE ?
            ORDER BY CURSO, ID""", (cursosPase, self.buscar.text(), 
                            self.buscar.text(), self.buscar.text()))
        elif consulta=="Normal":
            cur.execute("""
            SELECT NOMBRE_APELLIDO, DNI, CURSO
            FROM ALUMNOS
            WHERE CURSO IN (?, ?)
            ORDER BY CURSO, ID""", (cursosPase,))
        # Si la consulta es otra, se pasa por consola que un boludo escribió la consulta mal :) y termina la ejecución de la función.
        else:
            print("Error crítico: un bobolon escribio la consulta mal.")
            return
        # Se guarda la consulta en una variable.
        query = cur.fetchall()
        # Se establece la cantidad de filas que va a tener la tabla
        self.tablaListaAlumnos.setRowCount(len(query))
        # Bucle: por cada fila de la consulta obtenida, se guarda su id y se genera otro bucle que inserta todos los datos en la fila de la tabla de la ui.
        # Además, se insertan dos botones al costado de cada tabla: uno para editarla y otro para eliminarla.
        for i in range(len(query)):
            # Bucle: se introduce en cada celda el elemento correspondiente de la fila.
            check=qtw.QCheckBox()
            check.setObjectName("check")
            check.toggle()
            self.tablaListaAlumnos.setCellWidget(i, 0, check)
            for j in range(len(query[i])):
                self.tablaListaAlumnos.setItem(i, j+1, qtw.QTableWidgetItem(str(query[i][j])))

            self.tablaListaAlumnos.setRowHeight(i, 35)
    
    def confirmarGrupal(self):
        for i in range(self.tablaListaAlumnos.rowCount()):
            if self.tablaListaAlumnos.cellWidget(i, 0).isChecked():
                cur.execute('SELECT * FROM ALUMNOS WHERE DNI=?', (int(self.tablaListaAlumnos.item(i, 2).text())))
                datos=cur.fetchall()
                cur.execute('INSERT INTO ALUMNOS_HISTORICOS VALUES(?, ?, ? , ?, ?, ?)', (
                    datos[0][0], datos[0][1], datos[0][2], datos[0][3], 
                    dt.date.today().strftime('%Y/%m/%d'), datos[0][4]
                ))
                cur.execute('DELETE FROM ALUMNOS WHERE ID=?', (datos[0][0],))
                con.commit()

        