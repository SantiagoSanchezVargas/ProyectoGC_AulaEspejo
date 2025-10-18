import mysql.connector

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="proyecto_gc"  # o el nombre de tu BD
)

print("Conexión exitosa:", conexion.is_connected())
