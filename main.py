from funciones import *
from funciones import verificar_tablas_existen, insertar_datos_SUMMARY
import pyodbc
import pandas as pd
import csv
import os


try:
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-3H6HKSS\SQLEXPRESS;DATABASE=fut_usm;Trusted_Connection=yes;')
    cursor = conexion.cursor()
    
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

            cursor.execute(""" 
            SELECT Year AS Año, Champion AS Campeon
            FROM SUMMARY
            """)

            data = cursor.fetchall()
            campeones_resultados = pd.DataFrame.from_records(data, columns=["Año","Campeon"])
            print(campeones_resultados.to_string(index=False))
            print('\n')
     
        elif respuesta == "2":

            cursor.execute("""
            SELECT TOP 5 Team AS Equipo, SUM(Goals_For) AS Total_Goles
            FROM FIFA
            GROUP BY Team
            ORDER BY SUM(Goals_for) DESC;
            """)

            data = cursor.fetchall()
            goleadores = pd.DataFrame.from_records(data, columns=["Equipo","Goles_totales"])
            print(goleadores.to_string(index=False))
            print('\n')
            
        elif respuesta == "3":

            cursor.execute("""
            SELECT TOP 5 Third_place AS Tercer_lugar, COUNT(Third_place) AS cantidad_tercer_lugar
            FROM SUMMARY
            GROUP BY Third_place
            ORDER BY COUNT(Third_place) DESC;
            """)

            data = cursor.fetchall()
            tercer_lugar = pd.DataFrame.from_records(data, columns=["Equipo","Cantidad"])
            print("Top 5 equipos con mayor tercer lugar: \n")
            print(tercer_lugar.to_string(index=False))
            print('\n')
            
        elif respuesta == "4":
            print("Hasta pronto")
            
        elif respuesta == "5":
            print("Hasta pronto")
            
        elif respuesta == "6":
            print("Hasta pronto")
            
        elif respuesta == "7":
            print("Hasta pronto")
            
        elif respuesta == "8":

            cursor.execute("""
            SELECT Year AS Año, Host AS Anfitrion, Champion AS Campeon
            FROM SUMMARY
            WHERE Host = Champion;
            """)

            data = cursor.fetchall()
            paises_ganando_en_casa_resultado = pd.DataFrame.from_records(data, columns=["Año","Anfitrion","Campeon"])
            print("Paises ganando en casa: ")
            print(paises_ganando_en_casa_resultado.to_string(index=False))
            print('\n')
        
        elif respuesta == "9":
            print("Hasta pronto")
            
        elif respuesta == "10":
            print("Hasta pronto")
            
        elif respuesta == "0":
            print("¡Hasta pronto!")
            break
        
        else:
            print("Opcion no valida, ingresa una nueva opcion")
            
    cursor.close()
    conexion.close()

except Exception as e:
    print("Ocurrio un error al conectar a SQL Server: ", e)

'''
    -- Crear una vista que muestra los nombres de los estudiantes y los nombres de los cursos que están tomando
    CREATE VIEW StudentCourses AS
    SELECT Students.StudentName, Courses.CourseName
    FROM Students
    JOIN Courses ON Students.CourseID = Courses.CourseID;

    -- Consultar la vista para obtener los nombres de los estudiantes y los nombres de los cursos que están tomando
    SELECT * FROM StudentCourses;
'''