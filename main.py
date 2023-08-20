from funciones import *
import pyodbc
import pandas as pd
import csv
import os


try:
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-3H6HKSS\SQLEXPRESS;DATABASE=fut_usm;Trusted_Connection=yes;')
    
    tablas_a_crear = ["SUMMARY", "FIFA"]
    if not verificar_tablas_existen(conexion, tablas_a_crear):
        crear_tablas(conexion)
        insertar_datos_SUMMARY(conexion)

        # Obtiene una lista de todos los archivos .csv
        directorio_csv = os.path.abspath('./archivos_csv')
        archivos_csv = [archivo for archivo in os.listdir(directorio_csv) if archivo.endswith('.csv')]
        i = 1 # Contador para id (primary key)
        for archivo in archivos_csv:
            ruta = os.path.join(directorio_csv, archivo)
            year = int(archivo[7:11])
            insertar_datos_FIFA(conexion,ruta,year)

    conexion.close()

except Exception as e:
    print("Ocurrió un error al conectar a SQL Server: ", e)