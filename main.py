from funciones import *
from funciones import verificar_tablas_existen, insertar_datos_SUMMARY
import pyodbc
import pandas as pd
import csv
import os


try:
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-3H6HKSS\SQLEXPRESS;DATABASE=fut_usm;Trusted_Connection=yes;')
    
    tablas_a_crear = ["SUMMARY", "FIFA"]
    if not verificar_tablas_existen(conexion, tablas_a_crear):
        crear_tablas(conexion)

        # Obtiene una lista de todos los archivos .csv
        directorio_csv = os.path.abspath('./archivos_csv')
        archivos_csv = [archivo for archivo in os.listdir(directorio_csv) if archivo.endswith('.csv')]
        
        # Insertar datos a la tabla SUMMARY
        ruta = os.path.join(directorio_csv, archivos_csv[-1])
        insertar_datos_SUMMARY(conexion,ruta)

        i = 1 # Contador para ID (primary key)
        for archivo in archivos_csv:
            if "Summary" not in archivo:
                ruta = os.path.join(directorio_csv, archivo)
                year = int(archivo[7:11])
                i = insertar_datos_FIFA(conexion,ruta,year,i)

    while True:
        print("Menu Fut-USM: ")
        print("1. Mostrar Campeones")
        print("2. Mostrar goleadores")
        print("3. Mostrar Tercer Lugar más veces")
        print("4. Mostrar Pais mas goles recibidos")
        print("5. Buscar un pais")
        print("6. Top 3 paises en el mundial")
        print("7. Mayor cantidad ganados")
        print("8. Paises ganando en casa")
        print("9. Mas veces en el podio")
        print("10. Mayores rivales")
        print("0. Salir")
        print()
        respuesta = input("Seleccione una opcion: ")
        print()
        
        if respuesta == "1":
            campeones_query = """ 
            SELECT Year AS Año, Champion AS Campeon
            FROM SUMMARY
            """
            
            campeones_resultados = pd.read_sql_query(campeones_query,conexion)
            print(campeones_resultados.to_string(index=False))
            print('\n')
     
        elif respuesta == "2":
            print("Hasta pronto")
            
        elif respuesta == "3":
            print("Hasta pronto")
            
        elif respuesta == "4":
            print("Hasta pronto")
            
        elif respuesta == "5":
            print("Hasta pronto")
            
        elif respuesta == "6":
            print("Hasta pronto")
            
        elif respuesta == "7":
            print("Hasta pronto")
            
        elif respuesta == "8":
            paises_ganando_en_casa_query = """
            SELECT Year AS Año, Host AS Anfitrion, Champion AS Campeon
            FROM SUMMARY
            WHERE Host = Champion;
            """
            
            paises_ganando_en_casa_resultado = pd.read_sql_query(paises_ganando_en_casa_query,conexion)
            print("Paises ganando en casa: ")
            print(paises_ganando_en_casa_resultado.to_string(index=False))
            print('\n')
        
        elif respuesta == "9":
            print("Hasta pronto")
            
        elif respuesta == "10":
            print("Hasta pronto")
            
        elif respuesta == "0":
            print("Hasta pronto")
            break
        
        else:
            print("Opcion no valida, ingresa una nueva opcion")
            
    conexion.close()

except Exception as e:
    print("Ocurrió un error al conectar a SQL Server: ", e)

'''
    -- Crear una vista que muestra los nombres de los estudiantes y los nombres de los cursos que están tomando
    CREATE VIEW StudentCourses AS
    SELECT Students.StudentName, Courses.CourseName
    FROM Students
    JOIN Courses ON Students.CourseID = Courses.CourseID;

    -- Consultar la vista para obtener los nombres de los estudiantes y los nombres de los cursos que están tomando
    SELECT * FROM StudentCourses;
'''