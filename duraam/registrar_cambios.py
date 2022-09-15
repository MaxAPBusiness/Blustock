import datetime as dt
import db.inicializar_bbdd as db
userInfo=["", 0]

def registrarCambios(tipo, tablas, idd, datosViejos, datosNuevos):
    global userInfo
    if userInfo[1]:
        db.cur.execute("SELECT ID FROM administradores WHERE usuario = ?",(userInfo[0],))
    else:
        db.cur.execute("SELECT ID FROM usuarios WHERE usuario = ?",(userInfo[0],))
    userId=db.cur.fetchall()[0][0]
    db.cur.execute("INSERT INTO HISTORIAL_DE_CAMBIOS VALUES(?, ?, ?, ?, ?, ?, ?, ?)", 
    (userId, userInfo[1], dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
    tipo, tablas, idd, datosViejos, datosNuevos,))
