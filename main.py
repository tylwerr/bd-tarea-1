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

    # Menu y opciones
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
            CREATE VIEW CampeonesView AS
            SELECT 
                Year AS Año,
                Champion AS Campeon 
            FROM
                SUMMARY
            """)

            cursor.execute("SELECT * FROM CampeonesView")
            data = cursor.fetchall()
            campeones_resultados = pd.DataFrame.from_records(data, columns=["Año","Campeon"])
            print(campeones_resultados.to_string(index=False))
            print('\n')
     
        elif respuesta == "2":

            cursor.execute("""
            SELECT TOP 5 
                Team AS Equipo,
                SUM(Goals_For) AS Total_Goles
            FROM
                FIFA
            GROUP BY 
                Team
            ORDER BY 
                SUM(Goals_for) DESC;
            """)

            data = cursor.fetchall()
            goleadores = pd.DataFrame.from_records(data, columns=["Equipo","Goles_marcados"])
            print(goleadores.to_string(index=False))
            print('\n')
            
        elif respuesta == "3":

            cursor.execute("""
            SELECT TOP 5 
                Third_place AS Tercer_lugar,
                COUNT(Third_place) AS cantidad_tercer_lugar
            FROM
                SUMMARY
            GROUP BY 
                Third_place
            ORDER BY 
                COUNT(Third_place) DESC;
            """)

            data = cursor.fetchall()
            tercer_lugar = pd.DataFrame.from_records(data, columns=["Equipo","Cantidad"])
            print("Top 5 equipos con mayor tercer lugar: \n")
            print(tercer_lugar.to_string(index=False))
            print('\n')
            
        elif respuesta == "4":

            cursor.execute("""
            SELECT TOP 5 
                Team AS Equipo,
                SUM(Goals_Against) AS Goles_en_contra
            FROM 
                FIFA
            GROUP BY 
                Team
            ORDER BY 
                SUM(Goals_Against) DESC;
            """)
            
            data = cursor.fetchall()
            goles_en_contra = pd.DataFrame.from_records(data, columns=["Equipo","Goles_recibidos"])
            print(goles_en_contra.to_string(index=False))
            print('\n')
            
        elif respuesta == "5":
            
            salir = True
            while salir:
                respuesta = mostrar_menu_equipos(conexion)

                if respuesta == 's':
                    salir = False
                else:
                    mostrar_info_equipo(conexion,respuesta)
            
        elif respuesta == "6":

            cursor.execute("""
            SELECT TOP 3 
                Team AS Equipo,
                COUNT(Team) AS Cantidad_mundiales_jugados
            FROM 
                FIFA
            GROUP BY 
                Team
            ORDER BY 
                COUNT(Team) DESC;
            """)
            
            data = cursor.fetchall()
            cantidad_mundiales = pd.DataFrame.from_records(data, columns=["Equipo","Mundiales_jugados"])
            print(cantidad_mundiales.to_string(index=False))
            print('\n')
            
        elif respuesta == "7":

            cursor.execute("""
            SELECT TOP 1 
                Team AS Equipo,
                CONCAT(CAST(dbo.calcularTasa(SUM(Win),SUM(Games_Played)) AS DECIMAL(10,2) ), '%') AS Tasa_partidos_ganados
            FROM
                FIFA
            GROUP BY 
                Team
            ORDER BY 
                Tasa_partidos_ganados DESC;
            """
            )
 
            data = cursor.fetchall()
            promedio_partidos_ganados = pd.DataFrame.from_records(data, columns=["Equipo", "Tasa_partidos_ganados"])
            print(promedio_partidos_ganados.to_string(index=False))
            print('\n')

        elif respuesta == "8":

            cursor.execute("""
            SELECT 
                Year AS Año,
                Host AS Anfitrion,
                Champion AS Campeon
            FROM 
                SUMMARY
            WHERE 
                Host = Champion;
            """)

            data = cursor.fetchall()
            paises_ganando_en_casa_resultado = pd.DataFrame.from_records(data, columns=["Año","Anfitrion","Campeon"])
            print("Paises ganando en casa: ")
            print(paises_ganando_en_casa_resultado.to_string(index=False))
            print('\n')
        
        elif respuesta == "9":
            
            cursor.execute("""   
            SELECT TOP 1 Team, COUNT(*) AS Veces_podio
            FROM (
                SELECT Champion AS Team FROM SUMMARY
                UNION ALL
                SELECT Runner_up AS Team FROM SUMMARY
                UNION ALL
                SELECT Third_Place AS Team FROM SUMMARY
            ) AS Podio
            GROUP BY Team
            ORDER BY Veces_podio DESC;
            """)
            
            data = cursor.fetchall()
            podio = pd.DataFrame.from_records(data, columns=["Pais","Veces_en_el_podio"])
            print(podio.to_string(index=False))
            print('\n')
            
        elif respuesta == "10":
            
            cursor.execute("""
            WITH Parejas AS(
                SELECT
                    CASE WHEN Champion < Runner_up THEN Champion ELSE Runner_up END AS Equipo1,
                    CASE WHEN Champion < Runner_up THEN Runner_up ELSE Champion END AS Equipo2
                FROM 
                    SUMMARY
            )
            SELECT TOP 1
                Equipo1,
                Equipo2,
                COUNT(*) AS Veces_Repetidos
            FROM 
                Parejas
            GROUP BY 
                Equipo1,
                Equipo2
            ORDER BY 
                Veces_Repetidos DESC;
            """)

            data = cursor.fetchall()
            mayores_rivales = pd.DataFrame.from_records(data,columns=["Pais1","Pais2","Veces_Rivales"])
            mayores_rivales['Rivales'] = mayores_rivales["Pais1"] + '-' + mayores_rivales["Pais2"]  # Se juntan los paises en una sola tabla
            mayores_rivales.drop(['Pais1', 'Pais2'], axis=1, inplace=True)
            mayores_rivales = mayores_rivales[['Rivales', 'Veces_Rivales']] # Cambiar el orden de las columnas
            print("Paises que han sido los mayores rivales: \n")
            print(mayores_rivales.to_string(index=False))
            print('\n')

        elif respuesta == "0":
            print("¡Hasta pronto!")
            break

        else:
            print("Opcion no valida, ingresa una nueva opcion")
            
    cursor.close()
    conexion.close()

except Exception as e:
    print("Ocurrio un error al conectar a SQL Server: ", e)