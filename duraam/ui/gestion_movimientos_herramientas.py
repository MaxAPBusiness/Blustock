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

# Se importa la función mostrarMensaje.
from mostrar_mensaje import mostrarMensaje

# Se hace una conexión a la base de datos
os.chdir(f"{os.path.abspath(__file__)}/../../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()


# clase GestiónHerramientas: ya explicada. Es un widget que después se ensambla en un stackwidget en main.py.
class GestionMovimientosHerramientas(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        self.titulo=qtw.QLabel("GESTIÓN DE MOVIMIENTOS DE HERRAMIENTAS")
        self.titulo.setObjectName("titulo")

        # Se crea la tabla.
        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")

        # Se crean los títulos de las columnas de la tabla y se introducen en esta.
        self.campos = ["ID", "Herramienta", "Alumno", "Fecha", "Cantidad", 
                        "Tipo", "Turno de Pañol", "", ""]      
                                
        # Se establece el número de columnas que va a tener. 
        self.tabla.setColumnCount(len(self.campos))
        # Se introducen los títulos en la tabla.
        self.tabla.setHorizontalHeaderLabels(self.campos)

        # Se esconden los números de fila de la tabla que vienen por defecto para evitar confusión con el campo ID.
        self.tabla.verticalHeader().hide()
        # Se cambia el ancho de las dos últimas columnas, porque son las que van a tener los botones de editar y eliminar.
        self.tabla.setColumnWidth(7, 35)
        self.tabla.setColumnWidth(8, 35)

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
        self.radio1 = qtw.QRadioButton("Herramienta")
        self.radio2 = qtw.QRadioButton("Alumno")
        self.radio3 = qtw.QRadioButton("Fecha")
        self.radio1.setObjectName("Radio1")
        self.radio2.setObjectName("Radio2")
        self.radio3.setObjectName("Radio3")
        # Se le da a los botones de radio la función de mostrar datos en un orden específico.
        self.radio1.toggled.connect(lambda: self.mostrarDatos("Herramienta"))
        self.radio2.toggled.connect(lambda: self.mostrarDatos("Alumno"))
        self.radio3.toggled.connect(lambda: self.mostrarDatos("Fecha"))

        # Se crea el boton de agregar herramientas nuevas.
        self.agregar = qtw.QPushButton("Agregar")
        self.agregar.setObjectName("agregar")
        # Se le da la función.
        self.agregar.clicked.connect(
            lambda: self.modificarLinea('agregar'))
        # Cuando el cursor pasa por el botón, cambia de forma.
        self.agregar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

        # Se crea el layout y se le añaden todos los widgets anteriores.
        layout = qtw.QGridLayout()
        layout.addWidget(self.titulo, 0, 1)
        layout.addWidget(self.buscar, 1, 1)
        layout.addWidget(icono,1,1)
        layout.addWidget(self.label2, 1, 2)
        layout.addWidget(self.radio1, 1, 3)
        layout.addWidget(self.radio2, 1, 4)
        layout.addWidget(self.radio3, 1, 5)
        layout.addWidget(self.tabla, 2, 1, 1, 9)
        layout.addWidget(self.agregar, 3, 1)

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
            for i in range(7): 
                # El valor añadido es el texto en la barra de búsqueda.
                busqueda.append(f"%{self.buscar.text()}%")
            #Se hace la query: selecciona cada fila que cumpla con el requisito de que al menos una celda suya contenga el valor pasado por parámetro.
            cur.execute("""
            SELECT M.ID, H.DESC_LARGA, A.NOMBRE_APELLIDO,
            M.FECHA, M.CANTIDAD, M.TIPO, M.ID_TURNO_PANOL
            FROM MOVIMIENTOS_HERRAMIENTAS M, HERRAMIENTAS H, ALUMNOS A
            WHERE M.ID_HERRAMIENTA = H.ID AND M.ID_ALUMNO = A.ID
            AND (H.DESC_LARGA LIKE ? 
            OR A.NOMBRE_APELLIDO LIKE ? 
            OR M.ID LIKE ?
            OR M.FECHA LIKE ? 
            OR M.CANTIDAD LIKE ? 
            OR M.TIPO LIKE ? 
            OR M.ID_TURNO_PANOL LIKE ?)""", busqueda)
        # Si el tipo es nombre, se hace una query que selecciona todos los elementos y los ordena por su nombre.
        elif consulta=="Herramienta":
            cur.execute("""
            SELECT M.ID, H.DESC_LARGA, A.NOMBRE_APELLIDO,
            M.FECHA, M.CANTIDAD, M.TIPO, M.ID_TURNO_PANOL
            FROM MOVIMIENTOS_HERRAMIENTAS M, HERRAMIENTAS H, ALUMNOS A
            WHERE M.ID_HERRAMIENTA = H.ID AND M.ID_ALUMNO = A.ID ORDER BY H.DESC_LARGA
            """)
        # Si el tipo es grupo, se hace una query que selecciona todos los elementos y los ordena por su grupo.
        elif consulta=="Alumno":
            cur.execute("""
            SELECT M.ID, H.DESC_LARGA, A.NOMBRE_APELLIDO,
            M.FECHA, M.CANTIDAD, M.TIPO, M.ID_TURNO_PANOL
            FROM MOVIMIENTOS_HERRAMIENTAS M, HERRAMIENTAS H, ALUMNOS A
            WHERE M.ID_HERRAMIENTA = H.ID AND M.ID_ALUMNO = A.ID ORDER BY A.NOMBRE_APELLIDO
            """)
        # Si el tipo es subgrupo, se hace una query que selecciona todos los elementos y los ordena por su subgrupo.
        elif consulta=="Fecha":
            cur.execute("""
            SELECT M.ID, H.DESC_LARGA, A.NOMBRE_APELLIDO,
            M.FECHA, M.CANTIDAD, M.TIPO, M.ID_TURNO_PANOL
            FROM MOVIMIENTOS_HERRAMIENTAS M, HERRAMIENTAS H, ALUMNOS A
            WHERE M.ID_HERRAMIENTA = H.ID AND M.ID_ALUMNO = A.ID ORDER BY M.FECHA
            """)
        # Si el tipo no se cambia o no se introduce, simplemente se seleccionan todos los datos como venian ordenados. 
        elif consulta=="Normal":
            cur.execute("""
            SELECT M.ID, H.DESC_LARGA, A.NOMBRE_APELLIDO,
            M.FECHA, M.CANTIDAD, M.TIPO, M.ID_TURNO_PANOL
            FROM MOVIMIENTOS_HERRAMIENTAS M, HERRAMIENTAS H, ALUMNOS A
            WHERE M.ID_HERRAMIENTA = H.ID AND M.ID_ALUMNO = A.ID
            """)
        # Si la consulta es otra, se pasa por consola que un boludo escribió la consulta mal :) y termina la ejecución de la función.
        else:
            print("Error crítico: un bobi escribio la consulta mal.")
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

            # Se crea el boton de editar, se le da la función de editar y se lo introduce después de introducir los datos.
            botonEditar = qtw.QPushButton()
            botonEditar.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/editar.png")))
            botonEditar.setIconSize(qtc.QSize(25, 25))
            botonEditar.setObjectName("editar")
            botonEditar.clicked.connect(lambda: self.modificarLinea('editar'))
            botonEditar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, 7, botonEditar)

            # Se crea el boton de eliminar, se le da la función de eliminar la tabla con su id correspondiente y se introduce el boton al final de la fila.
            botonEliminar = qtw.QPushButton()
            botonEliminar.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/eliminar.png")))
            botonEliminar.setIconSize(qtc.QSize(25, 25))
            botonEliminar.setObjectName("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar(query[i][0]))
            botonEliminar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, 8, botonEliminar)

    # Función modificarLinea: muestra un mensaje con un formulario que permite editar o ingresar los elementos a la tabla.
    # Parametros: tipo: pregunta de que tipo va a ser la edición. Valores posibles:
    # # editar: se creará una ventana con un f0rmulario y al enviar los datos se modifican los datos de la fila en la que se pulsó el boton de edición.
    # # crear / insertar / None: crea una ventana con un formulario que insertará los datos en la tabla. 
    # # Identica a la de editar pero no viene con datos por defecto.
    def modificarLinea(self, tipo):
        # Se crea el widget que va a funcionar como ventana.
        self.edita = qtw.QWidget()
        # Se le da el título a la ventana, que por defecto es agregar.
        self.edita.setWindowTitle("Agregar Movimiento De Herramienta")
        self.edita.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))

        # Se crea el layout.
        layoutEditar = qtw.QGridLayout()

        # Inserta un label por cada campo.
        for i in range(1, len(self.campos)-2):
            label = qtw.QLabel(self.campos[i])
            label.setObjectName("modificar-label")
            layoutEditar.addWidget(label, i-1, 0)
        
        # Crea los entries.
        self.entry1 = qtw.QLineEdit()
        cur.execute("SELECT DESC_LARGA FROM HERRAMIENTAS")
        sugerenciasHerramientas=[]
        for i in cur.fetchall():
            sugerenciasHerramientas.append(i[0])
        cuadroSugerenciasHerramientas=qtw.QCompleter(sugerenciasHerramientas, self)
        cuadroSugerenciasHerramientas.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry1.setCompleter(cuadroSugerenciasHerramientas)

        self.entry2 = qtw.QLineEdit()
        cur.execute("SELECT NOMBRE_APELLIDO FROM ALUMNOS")
        sugerenciasAlumnos=[]
        for i in cur.fetchall():
            sugerenciasAlumnos.append(i[0])
        cuadroSugerenciasAlumnos=qtw.QCompleter(sugerenciasAlumnos, self)
        cuadroSugerenciasAlumnos.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry2.setCompleter(cuadroSugerenciasAlumnos)
        
        self.entry3Dia = qtw.QSpinBox()
        self.entry3Mes = qtw.QSpinBox()
        self.entry3Año = qtw.QSpinBox()
        self.entry3Dia.setMaximum(31)
        self.entry3Mes.setMaximum(12)
        self.entry3Año.setMaximum(2022)

        self.entry4 = qtw.QSpinBox()
        self.entry5 = qtw.QLineEdit()
        self.entry6 = qtw.QSpinBox()
        self.entry4.setMaximum(9999)
        self.entry6.setMaximum(9999)

        # Se crea una lista de datos vacía en la que se introduciran los valores que pasaran por defecto a la ventana.
        datos = []

        # Si el tipo es editar, se crea la pantalla de editar.
        if tipo == 'editar':
            # Se obtiene la posición del boton clickeado: 
            # primero se obtiene cual fue último widget clickeado (en este caso el boton)
            botonClickeado = qtw.QApplication.focusWidget()
            # luego se obtiene la posicion del boton.
            posicion = self.tabla.indexAt(botonClickeado.pos())
            
            # Se añaden a la lista los valores de la fila, recorriendo cada celda de la fila. Cell se refiere a la posición de cada celda en la fila.
            for cell in range(0, len(self.campos)):
                datos.append(posicion.sibling(posicion.row(), cell).data())
            

            # Se crea la ventana de edición, pasando como parámetros los títulos de los campos de la tabla y los datos por defecto para que se muestren
            # Si se ingresaron datos, se muestran por defecto. Además, se muestra el id.
            # Se les añade a los entries sus valores por defecto.
            self.entry1.setText(datos[1])
            self.entry2.setText(datos[2])
            fecha=datos[3].split("/")
            self.entry3Dia.setValue(int(fecha[2]))
            self.entry3Mes.setValue(int(fecha[1]))
            self.entry3Año.setValue(int(fecha[0]))
            self.entry4.setValue(int(datos[4]))
            self.entry5.setText(datos[5])
            self.entry6.setValue(int(datos[6]))
            self.edita.setWindowTitle("Editar")

        layoutEditar.addWidget(self.entry1, 0, 1, 1, 5)
        layoutEditar.addWidget(self.entry2, 1, 1, 1, 5)
        layoutEditar.addWidget(self.entry3Dia, 2, 1, 1, 1)
        layoutEditar.addWidget(qtw.QLabel("/"), 2, 2, 1, 1)
        layoutEditar.addWidget(self.entry3Mes, 2, 3, 1, 1)
        layoutEditar.addWidget(qtw.QLabel("/"), 2, 4, 1, 1)
        layoutEditar.addWidget(self.entry3Año, 2, 5, 1, 1)
        layoutEditar.addWidget(self.entry4, 3, 1, 1, 5)
        layoutEditar.addWidget(self.entry5, 4, 1, 1, 5)
        layoutEditar.addWidget(self.entry6, 5, 1, 1, 5)

        entries=[self.entry1, self.entry2, self.entry4, self.entry5, self.entry6]
        for i in entries:
            i.setObjectName("modificar-entry")

        self.entry3Dia.setObjectName("modificar-entryDate")
        self.entry3Mes.setObjectName("modificar-entryDate")
        self.entry3Año.setObjectName("modificar-entryDate")
        # Se crea el boton de confirmar, y se le da la función de confirmarr.
        confirmar = qtw.QPushButton("Confirmar")
        confirmar.setObjectName("confirmar")
        confirmar.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))
        confirmar.clicked.connect(lambda: self.confirmarr(datos))
        layoutEditar.addWidget(confirmar, 6, 0, 1, 6, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        # Se le da el layout a la ventana.
        self.edita.setLayout(layoutEditar)
        # Se muestra la ventana
        self.edita.show()

    # Función confirmar: se añaden o cambian los datos de la tabla en base al parámetro datos.
    def confirmarr(self, datos):
        # Se hace una referencia a la función de mensajes fuera de la clase y a la ventana principal.
        global mostrarMensaje

        cur.execute("""
        SELECT ID
        FROM HERRAMIENTAS
        WHERE DESC_LARGA=? 
        LIMIT 1""", (self.entry1.text().upper(),))

        herramienta=cur.fetchall()

        if not herramienta:
            mostrarMensaje("Error", "Error", 
            "La herramienta no esta ingresada. Por favor, verifique que la herramienta ingresada es correcta.")
            return
        
        cur.execute("""
        SELECT ID
        FROM ALUMNOS
        WHERE NOMBRE_APELLIDO=?
        LIMIT 1
        """, (self.entry2.text().upper(),))

        alumno=cur.fetchall()

        if not alumno:
            mostrarMensaje("Error", "Error", 
            "El alumno no está ingresado. Por favor, verifique que el alumno ingresado es correcta.")
            return
        
        cur.execute("""
        SELECT ID
        FROM TURNO_PANOL
        WHERE ID=?
        LIMIT 1
        """, (self.entry6.value(),))

        turnoPanol=cur.fetchall()

        if not turnoPanol:
            mostrarMensaje("Error", "Error", 
            "El turno no está registrado. Por favor, verifique que el turno registrado es correcto.")
            return
        
        if self.entry3Mes.value() < 10:
            mes=f"0{self.entry3Mes.value()}"
        else:
            mes=self.entry3Mes.value()
        if self.entry3Dia.value() < 10:
            dia=f"0{self.entry3Dia.value()}"
        else:
            dia=self.entry3Dia.value()  

        if self.entry3Año.value()<1000:
            año=f"0{self.entry1Año.value()}"
            for i in range(4-len(año)): 
                año=f"0{año}"
        else:
            año=self.entry3Año.value()
        fecha=f"{año}/{mes}/{dia}"

        # Si habían datos por defecto, es decir, si se quería editar una fila, se edita la fila en la base de datos y muestra el mensaje.
        if datos:
            # Se actualiza la fila con su id correspondiente en la tabla de la base de datos.
            cur.execute("""
            UPDATE MOVIMIENTOS_HERRAMIENTAS
            SET ID_HERRAMIENTA=?,
            ID_ALUMNO=?,
            FECHA=?,
            CANTIDAD=?,
            TIPO=?,
            ID_TURNO_PANOL=?
            WHERE ID=?
            """, (
                herramienta[0][0], alumno[0][0], fecha, self.entry4.text(), self.entry5.text(), turnoPanol[0][0], datos[0],
            ))

            con.commit()
            # Se muestra el mensaje exitoso.
            mostrarMensaje("Information", "Aviso",
                        "Se ha actualizado el movimiento.")           

        # Si no, se inserta la fila en la tabla de la base de datos.
        else:
            cur.execute("INSERT INTO MOVIMIENTOS_HERRAMIENTAS VALUES(NULL,?,?,?,?,?,?)", (
                herramienta[0][0], alumno[0][0], fecha, self.entry4.text(), self.entry5.text(), turnoPanol[0][0],
            ))
            con.commit()

            mostrarMensaje("Information", "Aviso",
                        "Se ha ingresado una herramienta.")
            
        
        #Se refrescan los datos.
        self.mostrarDatos()

    # Función eliminar: elimina la fila de la tabla de la base de datos y de la tabla de la ui. Parámetro:
    # - idd: el id de la fila que se va a eliminar.
    def eliminar(self, idd):
        # se obtiene la función definida fuera de la clase.
        global mostrarMensaje
        # se le pregunta al usuario si desea eliminar la fila.
        resp = mostrarMensaje('Pregunta', 'Advertencia',
                              '¿Está seguro que desea eliminar estos datos?')
        # si pulsó el boton de sí:
        if resp == qtw.QMessageBox.StandardButton.Yes:
            # elimina la fila con el id correspondiente de la tabla de la base de datos.
            cur.execute('DELETE FROM MOVIMIENTOS_HERRAMIENTAS WHERE ID_HERRAMIENTA=?', (idd,))
            con.commit()

            #elimina la fila de la tabla de la ui.
            boton = qtw.QApplication.focusWidget()
            i = self.tabla.indexAt(boton.pos())
            self.tabla.removeRow(i.row())

    # Función: closeEvent: funcion de qtmainwindow que se ejecuta automáticamente cuando se cierra la ventana principal. 
    # Cuando esto ocurra, también cerrara las demás ventanas que hayan quedado abiertas.
    def closeEvent(self, event):
        # Si hay una ventana de edición abierta, la cierra. 
        # Por esto estaba en el init la variable inicializada con None, porque si no se inicializa no existe y al no existir tira error.
        if self.edita:
            self.edita.close()