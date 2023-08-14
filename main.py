import pyodbc

try:
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-3H6HKSS\SQLEXPRESS;DATABASE=fut_usm')
    print("Conexión exitosa a SQL Server")
    
except Exception as e:
    print("Ocurrió un error al conectar a SQL Server: ", e)