import pyodbc
import pandas as pd
import csv
import os


'''
mostrar_info_equipo
————————
conexion: Connection
equipo_seleccionado: string
————————
Toma el equipo seleccionado y se obtiene toda su informacion de la tabla, excluyendo su nombre e ID.
'''
def mostrar_info_equipo(conexion, equipo_seleccionado):
    cursor = conexion.cursor()

    try:
        cursor.execute("""
        SELECT *
        FROM FIFA
        WHERE Team = ?
        ORDER BY Year;
        """, equipo_seleccionado)
        
        info_equipo = cursor.fetchall()

        if info_equipo:
            print(f"\nInformacion del equipo {equipo_seleccionado}:\n")
            df = pd.DataFrame.from_records(info_equipo, columns=[desc[0] for desc in cursor.description])
            columns_to_exclude = ["ID", "Team"]
            df.drop(columns=columns_to_exclude, inplace=True)
            for year, grupo_df in df.groupby("Year"):
                print(f"Año {year}:")
                print(grupo_df.to_string(index=False))
                print('\n')
    except Exception as e:
        print("error", e)


'''
mostrar_menu_equipos
————————
conexion: Connection
————————
Toma los nombres de los equipos, los enumera y ordena alfabeticamente, luego los muestra por pantalla y permite escoger uno
de ellos. Se retorna el equipo escogido o 's' en caso de salir.
'''
def mostrar_menu_equipos(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
    SELECT DISTINCT Team
    FROM FIFA;
    """)
    
    equipos = cursor.fetchall()
    print("Seleccione un equipo segun su numero:")
    
    contador = 0
    for i, equipo in enumerate(equipos, start=1):
        equipo_str = ', '.join(str(elemento) for elemento in equipo)
        print(f"{i}. {equipo_str}")
        contador = i
    print('\n')

    while True:
        numero_equipo = input("Ingrese su respuesta('s' para salir): ")
        if numero_equipo == 's':
            return 's'
        elif numero_equipo.isdigit():
            numero_equipo = int(numero_equipo)

            if numero_equipo > 0  and numero_equipo <= contador:
                return equipos[numero_equipo-1][0]
            else:
                print("Opcion no valida")
                print('\n')
            
        else:
            print("Opcion no valida")
            print('\n')


'''
verificar_tablas_existen
————————
conexion: Connection
table_names: lista de strings
————————
Toma table_names y la recorre para verificar que los nombres dentro de esta coincidan con las tablas
existentes en la base de datos, si existen ambas retorna True en caso contrario False.
'''
def verificar_tablas_existen(conexion, table_names):
    cursor = conexion.cursor()
    
    existing_tables = [table[2] for table in cursor.tables(tableType='TABLE')]
    existen = 0
    
    for table_name in table_names:
        if table_name in existing_tables:
            existen += 1

    if existen == 2:
        return True
    else:
        return False


'''
crear_tablas
————————
conexion: Connection
————————
Se hace un query para crear dos tablas, SUMMARY y FIFA respectivamente, cada una representada con
la informacion correspondiente, en el caso de FIFA se agrega una columna ID para crear una llave
primaria a esa tabla.
'''
def crear_tablas(conexion):
    cursor = conexion.cursor()
    create_table_query = '''
    CREATE TABLE SUMMARY (
        Year SMALLINT PRIMARY KEY NOT NULL,
        Host NVARCHAR(50) NOT NULL,
        Champion NVARCHAR(50) NOT NULL,
        Runner_up NVARCHAR(50) NOT NULL,
        Third_place NVARCHAR(50) NOT NULL,
        Teams SMALLINT NOT NULL,
        Matches_played SMALLINT NOT NULL,
        Goals_scored SMALLINT NOT NULL,
        Avg_goals_per_game FLOAT NOT NULL
    );
    
    CREATE TABLE FIFA (
        Position SMALLINT NOT NULL,
        Team NVARCHAR(50) NOT NULL,
        Games_Played SMALLINT NOT NULL,
        Win SMALLINT NOT NULL,
        Draw SMALLINT NOT NULL,
        Loss SMALLINT NOT NULL, 
        Goals_For SMALLINT NOT NULL,
        Goals_Against SMALLINT NOT NULL,
        Goal_Difference SMALLINT NOT NULL,
        Points SMALLINT NOT NULL,
        Year SMALLINT NOT NULL FOREIGN KEY REFERENCES SUMMARY(Year),
        ID SMALLINT NOT NULL PRIMARY KEY
    );
    '''
    cursor.execute(create_table_query)
    conexion.commit()
    cursor.close()


'''
insertar_datos_SUMMARY
————————
conexion: Connection
ruta: string
————————
Lee el archivo de sumario usando ruta, salta la primera linea y luego hacee el query insertando
los datos a la tabla SUMMARY.
'''
def insertar_datos_SUMMARY(conexion,ruta):
    cursor = conexion.cursor()

    try:
        with open(ruta, 'r') as archivo:
            leer_csv = csv.reader(archivo)
            next(leer_csv)  # Salta la primera linea

            for fila in leer_csv:
                Year, Host, Champion, Runner_up, Third_place, Teams, Matches_played, Goals_scored, Avg_goals_per_game = fila
                Year = int(Year)
                               
                insert_query = f'''
                INSERT INTO SUMMARY (Year, Host, Champion, Runner_up, Third_place, Teams, Matches_played, Goals_scored, Avg_goals_per_game)
                VALUES ({Year}, '{Host}', '{Champion}', '{Runner_up}', '{Third_place}', {Teams}, {Matches_played}, {Goals_scored}, {Avg_goals_per_game})
                '''
                cursor.execute(insert_query)
            
            conexion.commit()

    except pyodbc.Error as ex:
        print("Ocurrió un error al insertar datos:", ex)
        
    finally:
        cursor.close()
    

'''
insertar_datos_FIFA
————————
conexion: Connection
ruta: string
year: int
i: int
————————
Abre el archivo usando ruta, lee cada fila sin contar la primera, corrobora que esté bien escrita
y hace el query para insertar los datos a la tabla FIFA, se hace un contador de las filas el cual
incrementa por fila insertada (esto para tener una llave primaria llamada ID, que es el contador).
Finalmente retorna el contador para los archivos siguientes.
'''    
def insertar_datos_FIFA(conexion,ruta,year,i):
    cursor = conexion.cursor()
    j = i # variable incremento para ID

    try:
        with open(ruta, 'r') as archivo:
            leer_csv = csv.reader(archivo)
            next(leer_csv)  # Salta la primera linea

            for fila in leer_csv:
                position, team, games_played, win, draw, loss, goals_for, goals_against, goal_difference, points = fila
                
                # Verifica que tenga el simbolo especial y reemplazarlo
                if 'âˆ’' in goal_difference:
                    goal_difference = goal_difference.replace('âˆ’','-')
                    goal_difference = int(goal_difference)

                if '*' in team:
                    team = team.replace('*','')
                
                insert_query = f'''
                INSERT INTO FIFA (Position, Team, Games_Played, Win, Draw, Loss, Goals_For, Goals_Against, Goal_Difference, Points, Year, ID)
                VALUES ({position}, '{team}', {games_played}, {win}, {draw}, {loss}, {goals_for}, {goals_against}, {goal_difference}, {points}, {year}, {j})
                '''
                cursor.execute(insert_query)
                j += 1
            
            conexion.commit()
        
    except pyodbc.Error as ex:
        print("Ocurrió un error al insertar datos:", ex)
        
    finally:
        cursor.close()
        return j