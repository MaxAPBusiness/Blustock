"""Este módulo contiene funciones miscelánea útiles para el programa.

Funciones
---------
    mostrarContrasena(boton, entry: QtWidgets.QLineEdit):
        Muestra o esconde lo ingresado en el campo de contraseña
        vinculado dependiendo del estado de activación del botón.

    insertarFilas(tabla: QtWidgets.QTableWidget,
                  funcGuardar: types.FunctionType,
                  funcEliminar: types.FunctionType,
                  campos: tuple,
                  sugerencias: tuple | list | None = None,
                  funcEspecial: types.FunctionType | None = None):
        Inserta una nueva fila en una tabla de una gestión.

    generarBotones(funcGuardar: types.FunctionType,
                   funcEliminar: types.FunctionType,
                   tabla: QtWidgets.QTableWidget, numFila: int):
        Genera botones para guardar cambios y eliminar filas y los
        inserta en una fila de una tabla de la UI.
    
    cargarFuentes():
        Carga fuentes a la aplicación.
"""
import os
import types
from PyQt6 import QtWidgets, QtGui, QtCore
from ui.presets.popup import PopUp
from ui.presets.param_edit import ParamEdit
from ui.presets.boton import BotonFila

def mostrarContrasena(boton: QtWidgets.QCheckBox, entry: QtWidgets.QLineEdit):
    """Este método muestra o esconde lo ingresado en el campo de
    contraseña vinculado dependiendo del estado de activación del 
    botón.

    Parámetros
    ----------
        boton: QtWidgets.QCheckBox
            El botón que esconde/muestra la contraseña.
        entry : QtWidgets.QLineEdit
            El entry de contraseña vinculado al botón.
    """
    # Si el botón está presionado
    if boton.isChecked():
        # Muestra lo ingresado en el campo.
        entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        # Cambia el ícono.
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}esconder.png'
        pixmap = QtGui.QPixmap(path)
    else:
        # Cifra lo ingresado en el campo.
        entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
        pixmap = QtGui.QPixmap(path)
    boton.setIcon(QtGui.QIcon(pixmap))
    boton.setIconSize(QtCore.QSize(25, 25))

# Creamos matrices que llevan la información del tipo de campo y el
# tipo de valor del campo, respectivamente.
camposStock=((2, 1, 1, 0, 0, 1, 2, 4, 3, 3), (0, 1, 0, 0, 0, 0, 0, 2, 2, 2))
camposAlumnos=((2, 1, 3, 1), (0, 1, 2, 0))
camposClases=((2, 1, 3), (0, 1, 2))
camposDeudas=((2, 2, 2, 2, 2, 2, 2, 2), (1, 0, 1, 0, 1, 0, 0, 1))
camposGrupos=((2, 1), (0, 1))
camposHistorial=((2, 2, 2, 2, 2, 2), (1, 1, 1, 1, 1, 1))
camposMovs=((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
            (0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1))
camposOtroPersonal=((2, 1, 3, 1), (0, 1, 2, 0))
camposSubgrupos=((2, 1, 3), (0, 1, 2))
camposTurnos=((2, 2, 2, 2, 2, 2, 2), (0, 1, 1, 1, 1, 1, 1))
camposUbis=((2, 1), (0, 1))
camposUsuarios=((2, 1, 3, 1, 1, 1), (0, 1, 2, 1, 1, 1))

def insertarFilas(tabla: QtWidgets.QTableWidget,
                  funcGuardar: types.FunctionType,
                  funcEliminar: types.FunctionType,
                  funcTabla: types.FunctionType, campos: tuple,
                  sugerencias: tuple | list | None = None,
                  funcEspecial: types.FunctionType | None = None):
    """Este método inserta una nueva fila en una tabla de una gestión.

    Parámetros
    ----------
        tabla: QtWidgets.QTableWidget
            La tabla a la que se le van a insertar los elementos.

        funcGuardar: types.FunctionType
            La función guardar que el botón guardar de la fila
            ejecutará.

        funcEliminar: types.FunctionType
            La función eliminar que el botón eliminar de la fila
            ejecutará.

        funcTabla: types.FunctionType | None = None
            La función que se conectará con la tabla, que se desconecta
            para evitar bugs.

        campos: tuple
            Una tupla que contenga cada campo de la tabla y su tipo.
            Para ver una lista de qué significa cada tipo de campo, ver
            el readme.

        sugerencias: tuple | list | None = None
            Una lista que debe contener una lista de sugerencia, que
            contenga todas las sugerencias, por cada campo que lleve un
            cuadro de sugerencia. Si se pasa None, se entenderá que la
            tabla no tiene cuadros de sugerencia.
            Default: None.

        funcEspecial: types.FunctionType | None = None
            Una función que se ejecutará al finalizar la edición de un
            campo determinado. Si se pasa None, se entenderá que la
            tabla no tiene campos de este tipo.
            Default: None.
    """
    # Desconectamos la tabla para que no genere problemas
    try:
        tabla.disconnect()
    except:
        pass
    tabla.setSortingEnabled(False)
    # Obtenemos el índice final, en el cual agregaremos la fila.
    indiceFinal = tabla.rowCount()

    # Antes de agregar la fila, queremos comprobar que la última
    # fila de la tabla no tenga campos vacíos. Esto lo hacemos
    # para que el usuario no pueda ingresar múltiples filas vacías
    # haciendo que el sistema detecte si la fila anterior está
    # vacía.
    ultimaFila = indiceFinal-1
    if ultimaFila >= 0:
        # Por cada campo...
        for nCampo, tipoCampo in enumerate(campos):
            # ... si el campo es obligatorio...
            if tipoCampo in {1, 3, 4}:
                # ...verificamos si el campo es un lineedit o una celda
                # normal, ya que el texto se obtiene de forma
                # diferente, y obtenemos el texto
                if tipoCampo == 1:
                    texto=tabla.item(ultimaFila, nCampo).text()
                else:
                    texto=tabla.cellWidget(ultimaFila, nCampo).text()
                # Si la celda/lineedit está vacía...
                if texto == "":
                    # Le pide al usuario que termine de llenar los
                    # campos y corta la función.
                    mensaje = "Ha agregado una fila y todavía no ha ingresado los datos de la fila anterior. Ingreselos, guardelos cambios e intente nuevamente."
                    return PopUp("Error", mensaje).exec()
                
    # Se añade la fila al final.
    tabla.insertRow(indiceFinal)
    # Movemos la barra hasta el final asi el usuario no tiene que bajar
    # la barra hasta el fondo sino que sea automático.
    tabla.scrollToItem(
        tabla.item(indiceFinal-1, 0),
        QtWidgets.QAbstractItemView.ScrollHint.PositionAtBottom)
    # Por cada número de campo y tipo de campo de la tabla...
    for nCampo, tipoCampo in enumerate(campos):
        # Si el tipo de campo no es con sugerencia...
        if tipoCampo in {0, 1, 2}:
            # Se crea el campo como un TableWidgetItem
            item=QtWidgets.QTableWidgetItem("")
            # Si el tipo de campo es no editable...
            if tipoCampo == 2:
                # Hacemos que el campo sea solo seleccionable.
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable |
                              QtCore.Qt.ItemFlag.ItemIsEnabled)
            # Agregamos el item a la celda específica.
            tabla.setItem(indiceFinal, nCampo, item)
        # Si no...
        else:
            # Significa que el campo es de sugerencia.
            # Creamos un contador para recorrer la lista de listas de
            # sugerencias.
            indice=0
            # Recorremos la lista de sugerencias fijándonos cuantos
            # campos de sugerencias hay en la tabla, ya que la cantidad
            # de listas de sugerencias es igual a la cantidad de campos
            # de sugerencia, y cada lista corresponde a cada campo de
            # antes a despues.
            for i, j in enumerate(campos):
                # ... recorremos cada tipo de campo de la tabla y
                # verificamos que sea con sugerencia...
                if j in {3, 4}:
                    #... si el campo que se quiere ingresar no está
                    # en ese índice...
                    if i < nCampo:
                        # Entendemos que su lista de sugerencia está
                        # después en la lista de listas, entonces
                        # sumamos 1 al índice en el que puede estar.
                        # Haciendo esto, obtenemos el índice de la
                        # lista de sugerencias relacionada con el campo
                        indice += 1
                    #...si está en ese índice, ya encontramos el campo
                    else:
                        #...y cortamos el bucle.
                        break
            # Creamos el lineedit con sugerencias usando el índice
            # obtenido en el bucle anterior.
            campoSugerido = ParamEdit(sugerencias[indice], "")
            # Si el tipo de campo es de una función especial...
            if tipoCampo == 4:
                # Conectamos el cuadro de sugerencias con la función
                # especial cuando se termine de editar.
                campoSugerido.textChanged.connect(funcEspecial)
            else:
                campoSugerido.textChanged.connect(lambda: funcTabla(None, None, tabla))
            # Añadimos el campo a la celda.
            tabla.setCellWidget(indiceFinal, nCampo, campoSugerido)
        
    # Añadimos botones a la fila
    generarBotones(funcGuardar, funcEliminar, tabla, indiceFinal)
    tabla.setSortingEnabled(True)
    # Conectamos a la tabla a su función anterior
    tabla.cellChanged.connect(funcTabla)
    tabla.setCurrentCell(indiceFinal, 1)

def generarBotones(funcGuardar: types.FunctionType, funcEliminar: types.FunctionType,
                   tabla: QtWidgets.QTableWidget, numFila: int):
        """Este método genera botones para guardar cambios y eliminar
        filas y los inserta en una fila de una tabla de la UI

        Parámetros
        ----------
            funcGuardar: types.FunctionType
                La función que estará vinculada al botón guardar.
            funcEliminar: types.FunctionType
                La función que estará vinculada al botón eliminar.
            tabla: QtWidgets.QTableWidget
                La tabla a la que se le añadirán los botones.
            numFila: int
                La fila en la que se insertarán los botones.
        """
        # Se crean dos botones: uno de editar y uno de eliminar
        guardar = BotonFila("guardar")
        # Conectamos el botón a su función guardar correspondiente.
        guardar.clicked.connect(funcGuardar)
        # Lo dejamos desactivado por defecto para que el usuario solo
        # pueda guardar si modifica algo.
        guardar.setEnabled(False)
        # Hacemos lo mismo con el boton eliminar, pero no lo
        # desactivamos
        borrar = BotonFila("eliminar")
        borrar.clicked.connect(funcEliminar)

        # Se añaden los botones a cada fila.
        tabla.setCellWidget(numFila, tabla.columnCount() - 2, guardar)
        tabla.setCellWidget(numFila, tabla.columnCount() - 1, borrar)

def cargarFuentes():
    """Esta función carga fuentes a la aplicación."""
    # Por cada fuente en la carpeta de fuentes...
    for fuente in os.listdir(os.path.join(os.path.abspath(os.getcwd()),
                                          f'ui{os.sep}rsc{os.sep}fonts')):
        #...la cargamos.
        QtGui.QFontDatabase.addApplicationFont(
            os.path.join(os.path.abspath(os.getcwd()),
                        f'ui{os.sep}rsc{os.sep}fonts{os.sep}{fuente}'))

def refresh(tabla, funcFetch):
    """Este método revisa si se hicieron cambios en la tabla y avisa al
    usuario antes de refrescar la pantalla."""
    for row in range(tabla.rowCount()):
        if tabla.cellWidget(row, tabla.columnCount()-2).isEnabled():
            resp=PopUp('Pregunta', 'Esta acción refrescará la tabla y hay cambios sin guardar. Si realiza esta acción, los cambios no guardados se perderán.\n¿Desea refrescar y descartar los cambios?')
            if resp==QtWidgets.QMessageBox.StandardButton.Yes:
                funcFetch()
                return
    funcFetch()
    return