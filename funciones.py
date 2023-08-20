import main
import pyodbc
import pandas as pd
import csv
import os

'''
NOMBRE DE LA FUNCION
———————–
VARIABLE: TIPO
————————
BREVE DESCRIPCION DE LA FUNCION
'''
def verificar_tablas_existen(conexion, table_names):
    cursor = conexion.cursor()
    
    existing_tables = [table[2] for table in cursor.tables(tableType='TABLE')]
    
    for table_name in table_names:
        if table_name in existing_tables:
            return True
            
    return False

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

def insertar_datos_SUMMARY(conexion):
    cursor = conexion.cursor()
    
    datos_summary = [
        (1930,'Uruguay','Uruguay','Argentina','United States',13,16,70,3.6),
        (1934,'Italy','Italy','Czechoslovakia','Germany',16,17,70,4.1),
        (1938,'France','Italy','Hungary','Brazil',15,18,84,4.7),
        (1950,'Brazil','Uruguay','Brazil','Sweden',13,22,88,4),
        (1954,'Switzerland','West Germany','Hungary','Austria',16,26,140,5.4),
        (1958,'Sweden','Brazil','Sweden','France',16,35,126,3.6),
        (1962,'Chile','Brazil','Czechoslovakia','Chile',16,32,89,2.8),
        (1966,'England','England','West Germany','Portugal',16,32,89,2.8),
        (1970,'Mexico','Brazil','Italy','West Germany',16,32,95,3),
        (1974,'West Germany','West Germany','Netherlands','Poland',16,38,97,2.6),
        (1978,'Argentina','Argentina','Netherlands','Brazil',16,38,102,2.7),
        (1982,'Spain','Italy','West Germany','Poland',24,52,146,2.8),
        (1986,'Mexico','Argentina','West Germany','France',24,52,132,2.5),
        (1990,'Italy','West Germany','Argentina','Italy',24,52,115,2.2),
        (1994,'United States','Brazil','Italy','Sweden',24,52,141,2.7),
        (1998,'France','France','Brazil','Croatia',32,64,171,2.7),
        (2002,"South Korea, Japan",'Brazil','Germany','Turkey',32,64,161,2.5),
        (2006,'Germany','Italy','France','Germany',32,64,147,2.3),
        (2010,'South Africa','Spain','Netherlands','Germany',32,64,145,2.3),
        (2014,'Brazil','Germany','Argentina','Netherlands',32,64,171,2.7),
        (2018,'Russia','France','Croatia','Belgium',32,64,169,2.6),
        (2022,'Qatar','Argentina','France','Croatia',32,64,172,2.7)
    ]
    
    insert_query_summary = '''
    INSERT INTO SUMMARY (Year, Host, Champion, Runner_up, Third_place, Teams, Matches_played, Goals_scored, Avg_goals_per_game)
    VALUES (?,?,?,?,?,?,?,?,?)
    '''
    
    try:
        for datos in datos_summary:
            cursor.execute(insert_query_summary,datos)
            conexion.commit()
        
    except pyodbc.Error as ex:
        print("Ocurrió un error al insertar datos:", ex)
        
    finally:
        cursor.close()

def insertar_datos_FIFA(conexion,ruta,year):
    global i
    cursor = conexion.cursor()

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
                VALUES ({position}, '{team}', {games_played}, {win}, {draw}, {loss}, {goals_for}, {goals_against}, {goal_difference}, {points}, {year}, {i})
                '''
                cursor.execute(insert_query)
                i += 1
            
            conexion.commit()
        
    except pyodbc.Error as ex:
        print("Ocurrió un error al insertar datos:", ex)
        
    finally:
        cursor.close()