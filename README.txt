Datos personales:
	- Nombre: Daniel Maturana
	- ROL USM: 202173575-5

   	- Nombre: Carlos Arévalo
    	- ROL USM: 202173501-1
	

Detalles de uso del programa:
	- En la ruta donde se encuentran los archivos, ejecutar el comando "python main.py" para correr el programa.

Consideraciones:
	- Los archivos csv deben estar en una carpeta llamada "archivos_csv" para posterior lectura de estos.

	- Las tablas fueron creadas con campos NOT NULL, ya que un país si estuvo en el mundial debería tener datos (aunque sean solo 0).

	- La funcion sql fue creada desde SQL Server Management Studio, despues se guardo el archivo junto al main,
	al hacerlo desde ahi quedo funcional, mientras que al intentar hacerla desde python lanzaba errores.
	Se uso en la opcion 7, para calcular la tasa.

	- Las funciones python se separaron en un archivo aparte y estan importadas al main para mejor orden.

	- Se hizo una "opcion 0" en la que el usuario puede escoger para salir del programa, al igual que en el caso de
	la funcion mostrar_menu_equipos solo que esta usa la letra "s" para salir.

	- En la "opcion 5", como el usuario debe ingresar el equipo deseado, decidimos crear un sub-menu mostrando todos los equipos
	disponibles que estan registrados en la base de datos, este menu estara ordenado alfabeticamente, por lo cual ayuda de alguna
	manera a encontrar al equipo deseado, haciendo mas eficiente la deteccion de errores en esta opcion.

	- En todas las "opciones" se utilizo la libreria pandas, más especificamente la consulta "DataFrame.from_records", para poder
	mostrar la informacion por pantalla y asi dar una visualizacion más clara de los resultados obtenidos.
	
Detalles de las herramientas usadas:
	- Sistema Operativo (SO):
		Edición	Windows 10 Home Single Language
		Versión	22H2
		Compilación del sistema operativo	19045.3324
		Experiencia	Windows Feature Experience Pack 1000.19041.1000.0

	- Python 3.9.4

	- SQL Server Express:
		SQL Server Management Studio:	19.1.56.0
		SQL Server Management Objects (SMO): 16.200.48044.0+eeb184ee48a91ebc6a27a5d192c0d67bdfaae8b6
		Microsoft T-SQL Parser: 17.0.8.0+3c5555b8bd579d12add8f155f1dbc871e3e734c4
		Microsoft Analysis Services Client Tools:	16.0.20010.0
		Microsoft Data Access Components (MDAC):	10.0.19041.3208
		Microsoft MSXML:	3.0 6.0 
		Microsoft .NET Framework:	4.0.30319.42000
		Operating System:	10.0.19045

	- Librerias:
		pandas==2.0.3
		pyodbc==4.0.39
