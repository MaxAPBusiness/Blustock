"""Este módulo crea la ventana principal y ejecuta la aplicación.

Clases:
    MainWindow(qtw.QMainWindow):
"""
# Importamos las librerías de python que vamos a usar en el módulo.
# * sys: Para arrancar, la aplicación necesita unos parámetros del
# sistema. No se porqué, pero si no los pones se bugea asi que para eso
# está.
import sys
# * PyQt6.QtWidgets: contiene los widgets de qt que usaremos en el
#                    módulo. Se importa con el alias qtw.
# * PyQt6.QtCore: contiene las clases núcleo de qt. La usaremos para
#                 obtener funcionalidades especiales. Se importa con el
#                 alias qtc.
# * PyQt6.QtGui: contiene clases que manejan los gráficos 2d, ventanas,
#                imágenes y fuentes. Se importa con el alias qtg.
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
# * os: permite manejar las rutas de archivos.
import os

# Se importan los módulos lógicos de la aplicación:
# * inicializar_bbdd: se encarga de la conexión a la base de datos.
#                     Se importa con el nombre de db.
# * mostrar_mensaje: contiene una función que muestra un popup en la
#                    pantalla.
# * cambiar_icono: cambia el icono del boton de ordenar.
# * registrar_cambios: guarda los cambios a la tabla en el historial.
import db.inicializar_bbdd as db
from crypt import encriptar, decriptar
import registrar_cambios as rc

# Se importan los módulos de ui: la cabecera, el menú izquierdo, las
# gestiones y demás pantallas.
from ui.cabecera import Cabecera
from ui.menu_izquierdo import MenuIzquierdo
from ui.iniciarSesion import IniciarSesion
from ui.registrarse import Registrarse
from ui.gestion_movimientos_herramientas import GestionMovimientosHerramientas
from ui.gestion_herramientas import GestionHerramientas
from ui.gestion_turnos import GestionTurnos
from ui.gestion_alumnos import GestionAlumnos
from ui.gestion_profesores import GestionProfesores
from ui.gestion_grupos import GestionGrupos
from ui.gestion_subgrupos import GestionSubgrupos
from ui.gestion_registro_alumnos_historicos import GestionRegistroAlumnosHistoricos
from ui.gestion_registro_profesores_historicos import GestionRegistroProfesoresHistoricos
from ui.solicitudes import Solicitudes
from ui.gestion_usuarios import GestionUsuarios
from ui.gestion_administradores import GestionAdministradores
from ui.historial_de_cambios import HistorialDeCambios
import ui.mostrar_mensaje as m


# Creamos la ventana principal
class MainWindow(qtw.QMainWindow):
    """Esta clase crea la ventana principal.
    
    Hereda: PyQt6.QtWidgets.QMainWindow
    
    Atributos
    ---------
        cabecera : Cabecera
            La cabecera de la ventana.
        menuIzquierdo : MenuIzquierdo
            El menú izquierdo de la ventana.
        stack : QStackedWidget
            El widget central de la ventana, que contiene todas las
            pantallas de la ui.
        iniciarSesion : QWidget
            La pantalla para iniciar sesión.
        registrarse : QWidget
            La pantalla para registrarse.
        pantallas : tuple
            Una colección de pantallas para automatizar procesos.
    
    Métodos
    -------
        __init__(self):
            El constructor de la clase MainWindow.

            Crea la ventana principal con una cabecera, un menú
            izquierdo (inicialmente escondido) y una colección de
            pantallas.
        
        cambiarPantalla(self, i: int):
            Muestra la pantalla de la gestión seleccionada en la
            ventana.
        
        confirmarInicio(self):
            Realiza el inicio de sesión del usuario.
        
        registrar(self):
            Registra la solicitud de usuario en la tabla solicitudes.
        
        informacionUsuario(self, nombre: str, usuario: str):
            Crea un menú de contexto de usuario.
        
        cerrarSesion(self):
            Cierra la sesión del usuario.
        
        salir(self):
            Cierra la aplicación.
        
        closeEvent(self):
            Cierra todas las ventanas de la aplicación.
    """
    # Este es el constructor. El constructor de una clase es como una
    # función pero que se ejecuta apenas se crea el objeto de la clase.
    def __init__(self):
        # Se inicializa la clase de la que hereda la ventana principal.
        # Esto lo explico en el video.
        super().__init__()

        # Cambiamos el tamaño de la ventana.
        # Método resize: cambia el tamaño de la ventana. Los argumentos
        # son dos números int que representan los pixeles en ancho y en
        # alto.
        self.resize(1280, 1024)

        # Se establece el ícono de la ventana. 
        # Método setWindowIcon: establece el ícono de una ventana. 
        # Recibe como parámetro un objeto QIcon.
        self.setWindowIcon(
            qtg.QIcon(
                f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"
                )
            )

        # Se crea la cabecera.
        self.cabecera = Cabecera()

        # Se le pone el nombre de objeto para personalizarla más tarde
        # con estilos. Método setObjectName: le pone un tag al objeto
        # para reconocerlo y poder aplicarle cambios de estilo.
        self.cabecera.setObjectName("cabecera")
        self.addToolBar(qtc.Qt.ToolBarArea.TopToolBarArea, self.cabecera)

        # Creamos el objeto de menú izquierdo.
        self.menuIzquierdo = MenuIzquierdo()

        # Le damos un ancho fijo. Esto impide que se agrande o se
        # achique en el eje x.
        # Método setFixedWidth: le da un ancho fijo a un widget.
        self.menuIzquierdo.setFixedWidth(300)

        # Escondemos el menú al inicio para que el usuario no pueda
        # navegar por la app sin iniciar sesión.
        # Método toggleViewAction: esconde o muestra un widget.
        # Método setChecked: cambia el valor de una acción. Nosotros
        # lo ponemos en False para que no se vea.
        self.menuIzquierdo.toggleViewAction().setChecked(False)

        # Despues hacemos dos triggers para que se efectúe el cambio
        # porque sino a Qt le da ansiedad y no esconde el menú.
        # Método trigger: realiza una acción de qt.
        self.menuIzquierdo.toggleViewAction().trigger()
        self.menuIzquierdo.toggleViewAction().trigger()
        self.addToolBar(qtc.Qt.ToolBarArea.LeftToolBarArea, self.menuIzquierdo)

        # Creamos la colección de pantallas
        # QStackedWidget: es un widget que almacena varios widgets uno
        # encima de otro y permite elegir cual se muestra. Nosotros lo
        # usamos para tener todas las gestiones en una pantalla y poder
        # navegarlas.
        self.stack = qtw.QStackedWidget()

       
        # Creamos todas las pantallas de las gestiones.
        self.iniciarSesion = IniciarSesion()
        self.registrarse = Registrarse()
        herramientas = GestionHerramientas()
        movimientos = GestionMovimientosHerramientas()
        turnos = GestionTurnos()
        alumnos = GestionAlumnos()
        profesores = GestionProfesores()
        grupos = GestionGrupos()
        subgrupos = GestionSubgrupos()
        alumnosHistoricos = GestionRegistroAlumnosHistoricos()
        profesoresHistoricos = GestionRegistroProfesoresHistoricos()
        solicitudes = Solicitudes()
        usuarios = GestionUsuarios()
        administradores = GestionAdministradores()
        historialDeCambios = HistorialDeCambios()

        # Añadimos las pantallas a la colección. Para no añadir una a
        # una manualmente, creamos una tupla y hacemos un bucle que lo
        # haga automáticamente.
        # Nota: una tupla funciona igual a una lista pero sus valores
        # no pueden cambiar y, a cambio, es más eficiente en memoria.
        self.pantallas = (
            self.iniciarSesion, self.registrarse, herramientas, movimientos,
            turnos, alumnos, profesores, grupos, subgrupos,
            alumnosHistoricos, profesoresHistoricos, solicitudes, usuarios,
            administradores, historialDeCambios
        )
        for i in self.pantallas:
            self.stack.addWidget(i)

        # Se le da la funcionalidad a los botones de iniciar sesión:
        # Al presionar enter al terminar de escribir la contraseña o al 
        # presionar el boton confirmar, intenta iniciar sesión.
        self.iniciarSesion.entry2.returnPressed.connect(
            lambda: self.confirmarInicio())
        self.iniciarSesion.confirmar.clicked.connect(
            lambda: self.confirmarInicio())
        # Al presionar el boton de registrarse, lleva a la pantalla de
        # registrarse.
        self.iniciarSesion.registrarse.clicked.connect(
            lambda: self.stack.setCurrentIndex(1))

        # Al presionar el boton de iniciar sesión, lleva a la pantalla
        # de iniciar sesión.
        self.registrarse.ingresar.clicked.connect(
            lambda: self.stack.setCurrentIndex(0))
        self.registrarse.confirmar.clicked.connect(lambda: self.registrar())

        # Conecta a todos los botones del menú para cambiar la pantalla
        # a su gestión específica. Me encantaría poder hacerlo de forma
        # automática con un bucle pero qt no te deja. :(.
        self.menuIzquierdo.gestion1.toggled.connect(
            lambda: self.cambiarPantalla(2))
        self.menuIzquierdo.gestion2.toggled.connect(
            lambda: self.cambiarPantalla(3))
        self.menuIzquierdo.gestion3.toggled.connect(
            lambda: self.cambiarPantalla(4))
        self.menuIzquierdo.gestion4.toggled.connect(
            lambda: self.cambiarPantalla(5))
        self.menuIzquierdo.gestion5.toggled.connect(
            lambda: self.cambiarPantalla(6))
        self.menuIzquierdo.gestion6.toggled.connect(
            lambda: self.cambiarPantalla(7))
        self.menuIzquierdo.gestion7.toggled.connect(
            lambda: self.cambiarPantalla(8))
        self.menuIzquierdo.gestion8.toggled.connect(
            lambda: self.cambiarPantalla(9))
        self.menuIzquierdo.gestion9.toggled.connect(
            lambda: self.cambiarPantalla(10))
        self.menuIzquierdo.gestion10.toggled.connect(
            lambda: self.cambiarPantalla(11))
        self.menuIzquierdo.gestion11.toggled.connect(
            lambda: self.cambiarPantalla(12))
        self.menuIzquierdo.gestion12.toggled.connect(
            lambda: self.cambiarPantalla(13))
        self.menuIzquierdo.gestion13.toggled.connect(
            lambda: self.cambiarPantalla(14))

        # Añadimos la colección a la ventana
        # Método setCentralWidget: establece un widget como el widget
        # central de la ventana.
        self.setCentralWidget(self.stack)
        # Hacemos que el stack se puede agrandar al agrandar la pantalla
        # Método setSizePolicy: permite que un widget se expanda. Toma
        # como parámetros variables de qt que significan si se expande
        # o no, una en el ancho y la otra en el alto.
        self.stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding,)

    def cambiarPantalla(self, i: int):
        """Este método muestra la pantalla de la gestión seleccionada
        en la ventana.
        
        Primero actualiza la tabla para refrescar los datos.
        
        Parámetros
        ----------
        i : int
            El índice de la pantalla en la lista de pantallas.
        """
        self.pantallas[i].mostrarDatos()
        self.stack.setCurrentIndex(i)

    def confirmarInicio(self):
        """Este método realiza el inicio de sesión del usuario.
        
        Busca si el usuario está ingresado en la tabla administradores.
        Si lo encuentra, comprueba las contraseñas. Si coinciden,
        inicia sesión con los privilegios de administrador. Si no, le
        notifica al usuario de que su usuario y la contraseña no
        coinciden. Si no encontró el usuario, repite el mismo proceso 
        con la tabla usuarios. Al iniciar sesión, en este caso, lo hace
        sin privilegios. Si no lo encontró, repite el proceso en la
        tabla solicitudes. Si lo encuentra y la solicitud está
        pendiente aún de verificación, le notifica. Si la solicitud fue
        rechazada, se lo notifica y elimina la solicitud de la tabla.
        Si no lo encuentra, le notifica al usuario de que los datos no
        están ingresados.
        """
        # Busca al usuario en la tabla administradores. 
        # Aviso que cur se refiere al cursor de la base de datos. Si no
        # saben, el cursor funciona como si una persona escribiera
        # codigo en la base de datos.
        db.cur.execute("SELECT usuario, contrasena, nombre_apellido FROM administradores WHERE usuario = ?",
                       (self.iniciarSesion.entry1.text(),))
        # Obtenemos el resultado de la consulta. Método fetchall: 
        # obtiene los datos de la consulta y lo transforma en una lista.
        consultaAdministradores = db.cur.fetchall()
        
        # Si la consulta devolvió datos, sigue con el código.
        # Si se dan cuenta, el if no tiene parametros. Esto lo que 
        # significa es que analiza si el dato es verdadero o no.
        # Pero, ¿como verificas si una lista es verdadera o no? Simple:
        # si la lista tiene datos, devuelve verdadero. Sino, devuelve
        # falso.
        if consultaAdministradores:
            # Intenta transformar el string en bytes. Si ya habían
            # bytes guardados en vez de texto, no lo transforma.
            try:
                truePass = consultaAdministradores[0][1].encode()
            except:
                truePass = consultaAdministradores[0][1]

            # Si la contraseña decriptada es igual al texto del campo
            # contraseña, sigue con el código.
            if decriptar(truePass) == self.iniciarSesion.entry2.text():
                # Le notifica al usuario de que ingresó con éxito. Más
                # info de cómo funciona la función mostrarMensaje en el
                # módulo mostrar_mensaje.py
                m.mostrarMensaje(
                    "Aviso", "Aviso", f"Ha ingresado con éxito. Bienvenido, {consultaAdministradores[0][2]}.")
                
                # Muestra el menú izquierdo.
                self.menuIzquierdo.toggleViewAction().trigger()

                # Añade el botón de usuario a la cabecera y le da un
                # menú cuando el usuario le hace click derecho.
                self.cabecera.contenedorLayout.addWidget(self.cabecera.usuario)
                self.cabecera.usuario.clicked.connect(
                    lambda: self.informacionUsuario(consultaAdministradores[0][2], consultaAdministradores[0][0]))
                
                # Le añade al menú izquierdo los botones de gestión de
                # usuarios, administradores y el historial de cambios.
                self.menuIzquierdo.contenedorLayout.addWidget(
                    self.menuIzquierdo.gestion10, self.menuIzquierdo.contador+2, 0)
                self.menuIzquierdo.contenedorLayout.addWidget(
                    self.menuIzquierdo.gestion11, self.menuIzquierdo.contador+3, 0)
                self.menuIzquierdo.contenedorLayout.addWidget(
                    self.menuIzquierdo.gestion12, self.menuIzquierdo.contador+4, 0)
                
                # Cambia el widget central a la primera gestión.
                self.stack.setCurrentIndex(2)

                # Guarda el usuario y el rol para poder registrar sus
                # cambios en el historial. El 1 se refiere a que el rol
                # es administrador.
                rc.userInfo = [consultaAdministradores[0][0], 1]

                # Refresca los entries del inicio de sesión.
                self.iniciarSesion.entry1.setText("")
                self.iniciarSesion.entry2.setText("")

                # Termina la ejecución de la función.
                return None
            # Si no coinciden, avisa que el usuario y la contraseña
            # no coinciden.
            else:
                return m.mostrarMensaje("Advertencia", "Error",
                                            "El usuario y la contraseña no coinciden. Por favor, asegúrese que los datos sean correctos e ingrese nuevamente.")

        # Hace el mismo procedimiento de arriba pero con la tabla
        # usuarios.
        db.cur.execute("SELECT usuario, contrasena, nombre_apellido FROM usuarios WHERE usuario = ?",
                       (self.iniciarSesion.entry1.text(),))
        consultaUsuarios = db.cur.fetchall()
        if consultaUsuarios:
            try:
                truePass = consultaUsuarios[0][1].encode()
            except:
                truePass = consultaUsuarios[0][1]

            if decriptar(truePass) == self.iniciarSesion.entry2.text():
                m.mostrarMensaje(
                    "Aviso", "Aviso", f"Ha ingresado con éxito. Bienvenido, {consultaUsuarios[0][2]}.")
                self.menuIzquierdo.toggleViewAction().trigger()
                self.cabecera.contenedorLayout.addWidget(self.cabecera.usuario)
                self.cabecera.usuario.clicked.connect(
                    lambda: self.informacionUsuario(consultaUsuarios[0][2], consultaUsuarios[0][0]))
                self.stack.setCurrentIndex(2)
                # Nótese que el rol registrado es usuario y que no se
                # añaden los botones para ver las gestiones de usuario,
                # administrador ni solicutudes.
                rc.userInfo = [consultaUsuarios[0][0], 0]
                self.iniciarSesion.entry1.setText("")
                self.iniciarSesion.entry2.setText("")
                return None
            else:
                return m.mostrarMensaje("Advertencia", "Error",
                                            "El usuario y la contraseña no coinciden. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")

        # Si no lo encuentra en ninguna de las dos tablas, busca en las
        # solicitudes.
        db.cur.execute("SELECT usuario, contrasena, ESTADO FROM solicitudes WHERE usuario = ?",
                       (self.iniciarSesion.entry1.text(),))
        consultaSolicitudes = db.cur.fetchall()
        if consultaSolicitudes:
            try:
                truePass = consultaSolicitudes[0][1].encode()
            except:
                truePass = consultaSolicitudes[0][1]

            if decriptar(truePass) == self.iniciarSesion.entry2.text():
                # Si el estado es 1, significa que la cuenta
                # no fue verificada. En este caso, el if tampoco tiene
                # una comparación, pero como el campo es un número
                # la regla es así: si el numero es 0 devuelve false, si
                # es cualquier otro devuelve true. El número 1 hace
                # referencia a que el estado esta pendiente y el 0
                # significa que fue rechazado.
                if consultaSolicitudes[0][2]:
                    return m.mostrarMensaje("Advertencia", "Aviso",
                                            "Su cuenta todavía no fue verificada. Por favor, espere a que su cuenta sea verificada. Si tiene inconvenientes, póngase en contacto con algún administrador.")
                else:
                    m.mostrarMensaje("Advertencia", "Aviso",
                                     "La solicitud de registro de su cuenta fue rechazada. Si tiene algún inconveniente, póngase en contacto con algún administrador.")
                    db.cur.execute(
                        "DELETE FROM solicitudes WHERE usuario = ?", (consultaSolicitudes[0][0],))
                    return None
            else:
                return m.mostrarMensaje("Advertencia", "Error",
                                        "El usuario y la contraseña no coinciden. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")
        else:
            return m.mostrarMensaje("Advertencia", "Error",
                                    "El usuario no está registrado. Por favor, asegúrese que los datos son correctos e ingrese nuevamente.")

    def registrar(self):
        """Este método registra la solicitud de usuario en la tabla
        solicitudes.
        
        Primero, verifica que el usuario y la contraseña tengan al
        menos 8 carácteres y que las contraseñas coincidan. Luego,
        verifica que el usuario no este registrado en administradores
        ni en usuarios ni en solicitudes. Después, verifica que haya
        datos en la tabla administradores. Si hay, registra la 
        solicitud. Si no, directamente lo ingresa como administrador
        porque es el primer usuario.
        """
        # Verifica que la longitud del usuario y la cntraseña sean de,
        # al menos, 8 caracteres.
        if len(self.registrarse.entry2.text()) < 8:
            return m.mostrarMensaje("Error", "Aviso", "El usuario es demasiado corto. Por favor, ingrese uno más largo.")
        elif len(self.registrarse.entry3.text()) < 8:
            return m.mostrarMensaje("Error", "Aviso", "La contraseña es demasiado corta. Por favor, ingrese una más larga.")
        
        # Verifica que las contraseñas coincidan.
        elif self.registrarse.entry3.text() != self.registrarse.entry4.text():
            return m.mostrarMensaje("Error", "Aviso", "Las contraseñas no coinciden. Por favor, revise los datos e ingrese nuevamente.")

        # Verifica que el usuario no esté ya registrado en ninguna
        # tabla.
        db.cur.execute("SELECT usuario FROM usuarios WHERE usuario = ?",
                       (self.registrarse.entry2.text(),))
        usuarioEncontrado = db.cur.fetchall()
        db.cur.execute("SELECT usuario FROM solicitudes WHERE usuario = ?",
                       (self.registrarse.entry2.text(),))
        solicitudEncontrada = db.cur.fetchall()
        db.cur.execute("SELECT usuario FROM administradores WHERE usuario = ?",
                       (self.registrarse.entry2.text(),))
        adminEncontrado = db.cur.fetchall()
        if usuarioEncontrado or solicitudEncontrada or adminEncontrado:
            return m.mostrarMensaje("Error", "Error", "El usuario ya está ingresado. Por favor, ingrese un usuario distinto.")

        db.cur.execute("SELECT * FROM administradores")
        password = encriptar(self.registrarse.entry3.text())
        # Si encontró administradores, registra la solicitud.
        if db.cur.fetchall():
            db.cur.execute("INSERT INTO solicitudes VALUES (?, ?, ?, 'Pendiente')",
                           (self.registrarse.entry2.text(), password,
                           self.registrarse.entry1.text().upper(),))
            m.mostrarMensaje("Aviso", "Información",
                             "El registro se realizó correctamente. Recuerde que el administrador debe verificar su registro para que su usuario esté habilitado y pueda acceder.")
        # Si no, registra al usuario como administrador.
        else:
            db.cur.execute("INSERT INTO administradores VALUES(NULL, ?, ?, ?)",
                           (self.registrarse.entry2.text(), password,
                           self.registrarse.entry1.text().upper(),))
            m.mostrarMensaje("Aviso", "Información",
                "Eres el primer usuario! Bienvenido!.")
        db.con.commit()

    def informacionUsuario(self, nombre: str, usuario: str):
        """Este método crea un menú de contexto de usuario.
        
        Parámetros
        ----------
            nombre : str
                El nombre y apellido del usuario.
            usuario : str
                El nombre de usuario.
        """
        # QMenu: un menú de contexto.
        menu = qtw.QMenu(self)
        menu.setObjectName("menu")

        labelNombre = qtw.QLabel(nombre)
        labelUsuario = qtw.QLabel(usuario)

        # QAction: una acción. Se puede añadir a un menú para que
        # funcione como un botón de menú.
        botonCerrarSesion = qtg.QAction("Cerrar sesión")

        # Cuando se hace click, cierra la sesión del usuario.
        # Método triggered: una señal que se dispara cuando se ejecuta
        # la acción.
        botonCerrarSesion.triggered.connect(lambda: self.cerrarSesion())

        botonSalir = qtg.QAction("Salir")
        botonSalir.triggered.connect(lambda: self.salir())

        # Esto es para poder insertar widgets al menú. Por defecto, el
        # menú solo permite insertar acciones. Entonces, transformamos
        # el widget en una acción.
        # Método QWidgetAction: crea una acción que puede contener un
        # widget.
        insertarNombre = qtw.QWidgetAction(menu)
        insertarUsuario = qtw.QWidgetAction(menu)

        # Método setDefaultWidget: inserta el widget en la
        # QWidgetAction
        insertarNombre.setDefaultWidget(labelNombre)
        insertarUsuario.setDefaultWidget(labelUsuario)

        # Añadimos las acciones al menú.
        # Método addAction: añade una acción.
        menu.addAction(insertarNombre)
        menu.addAction(insertarUsuario)

        # Añadimos un separador.
        # Método addSeparator: añade un separador a un menú
        menu.addSeparator()
        menu.addAction(botonCerrarSesion)
        menu.addAction(botonSalir)

        # Ejecuta el menú.
        menu.exec(qtg.QCursor.pos())

    def cerrarSesion(self):
        """Este método cierra la sesión del usuario."""
        # Les explico para qué está esto. Ocurría un bug que hacía que
        # el menu apareciera de vuelta aunque cambiara la pantalla y
        # eso podía generar demasiados problemas. El disconnect
        # soluciona ese bug.
        # Método disconnect: quita la funcionalidad de una señal.
        self.cabecera.usuario.clicked.disconnect()
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                "¿Está seguro de que desea cerrar la sesión?")
        # Si el usuario respondió que si, ejecuta el código.
        # Nota: esto: "qtw.QMessageBox.StandardButton.Yes" significa
        # que el usuario clickeó el boton de sí. No pude hacer que se
        # viera más legible.
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            # Esto saca al botón de usuario de la cabecera.
            # Método setParent: hace que el widget pertenezca a otro
            # widget. Si ponemos None, como en este caso, hacemos que
            # no pertenezca a ninguno.
            self.cabecera.usuario.setParent(None)

            # Hacemos que no se vea el menú.
            self.menuIzquierdo.toggleViewAction().trigger()

            # Quitamos los privilegios de administrador (por las dudas).
            self.menuIzquierdo.contenedorLayout.removeWidget(
                self.menuIzquierdo.gestion10)
            self.menuIzquierdo.contenedorLayout.removeWidget(
                self.menuIzquierdo.gestion11)
            self.menuIzquierdo.contenedorLayout.removeWidget(
                self.menuIzquierdo.gestion12)
            
            # Volvemos a la pantalla de inicio de sesión.
            self.stack.setCurrentIndex(0)

    def salir(self):
        """Este método cierra la aplicación."""
        global app
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                "¿Está seguro de que desea salir?")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            # Cierra la aplicación
            # Método quit: cierra la app.
            app.quit()
    
    def closeEvent(self, event: qtc.QEvent):
        """Este método cierra todas las ventanas de la aplicación.
        
        Qt lo ejecuta cuando finaliza la ejecución de la aplicación.
        
        Parámetros
        ----------
            event : qtc.QEvent
                El evento que lanza qt. Nota: este parámetro no se usa
                en el método pero debe existir porque Qt siempre lo
                devuelve por defecto.
        """
        # Obtiene el objeto de la aplicación para poder usarlo adentro
        # de la clase.
        # Lo que hace el global es obtener una variable global para
        # poder usarla adentro de una función o clase, porque sino no
        # te deja python. :/
        global app

        # Método closeAllWindows: cierra todas las ventanas abiertas de
        # la aplicación.
        app.closeAllWindows()


# Si se ejecuta el módulo, no si se importa (esto es importante para
# evitar bugs, aparte es buena práctica)
if __name__ == "__main__":
    # Se crea la app.
    app = qtw.QApplication(sys.argv)

    # Se crea la ventana principal.
    window = MainWindow()

    # Se le aplican los estilos. Lo que hace el código de abajo es
    # abrir el archivo qss como un archivo de texto bajo el alias qss y
    # aplicarlo como hoja de estilos.
    with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/gestion.qss", "r") as qss:
        # Método setStyleSheet: establece los estilos de un widget.
        app.setStyleSheet(qss.read())
    
    # Muestra la ventana.
    # Método show: muestra un widget.
    window.show()

    # Ejecuta la aplicación.
    app.exec()
