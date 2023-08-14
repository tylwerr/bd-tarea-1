import pyodbc

def crear_tabla(conexion):
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
        Team NVARCHAR(50) PRIMARY KEY NOT NULL,
        Games_Played SMALLINT NOT NULL,
        Win SMALLINT NOT NULL,
        Draw SMALLINT NOT NULL,
        Loss SMALLINT NOT NULL, 
        Goals_For SMALLINT NOT NULL,
        Goals_Against SMALLINT NOT NULL,
        Goal_Difference SMALLINT NOT NULL,
        Points SMALLINT NOT NULL,
        Year SMALLINT NOT NULL FOREIGN KEY REFERENCES SUMMARY(Year)
    );
    '''
    
    cursor.execute(create_table_query)
    conexion.commit()
    cursor.close()


try:
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-3H6HKSS\SQLEXPRESS;DATABASE=fut_usm;Trusted_Connection=yes;')
    crear_tabla(conexion)
    conexion.close()
    

    
except Exception as e:
    print("Ocurrió un error al conectar a SQL Server: ", e)

    