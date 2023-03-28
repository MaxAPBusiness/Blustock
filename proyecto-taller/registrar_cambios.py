"""Este módulo crea una función para registrar los cambios realizados
en la base de datos en el historial, y una lista para guardar los datos
del usuario actual.

Funciones
---------
    registrarCambios(tipo: str, tablas: str, idd: any, 
    datosViejos: str, datosNuevos: str):
        Registra los cambios realizados en la base de datos por el
        usuario en el historial.
"""
import datetime as dt
import db.inicializar_bbdd as db

userInfo = ["", 0]


def registrarCambios(tipo: str, tablas: str, idd: any, datosViejos: str, datosNuevos: str):
    """Esta función registra los cambios realizados en la base de datos
    por el usuario en el historial."""
    global userInfo

    # Si el tipo de usuario es administrador, selecciona el id de
    # administradores. Sino, lo selecciona de usuarios.
    if userInfo[1]:
        db.cur.execute(
            "SELECT ID FROM administradores WHERE usuario = ?", (userInfo[0],))
    else:
        db.cur.execute(
            "SELECT ID FROM usuarios WHERE usuario = ?", (userInfo[0],))
    userId = db.cur.fetchall()[0][0]

    # Ingresa el id del usuario, el rol, la fecha y hora actuales, el
    # tipo de modificación, las tablas modificadas, el id de la fila
    # modificada, los datos previos a la modificacion y los datos
    # nuevos.
    db.cur.execute("INSERT INTO HISTORIAL_DE_CAMBIOS VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                   (userId, userInfo[1], dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    tipo, tablas, str(idd), datosViejos, datosNuevos,))
