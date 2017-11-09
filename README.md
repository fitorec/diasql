Dia SQL - 0.02(Beta)
===========================================================================

> Plugins para el modelador de diagramas de base de datos

## Install on Windows.

### Software:
- Install Python 2.3.5 is available from http://python.org/ftp/python/2.3.5/Python-2.3.5.exe>http://dia-installer.de>
- Install DIA <http://dia-installer.de>
- Install PyCairo 1.0.2. <http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/1.0/pycairo-1.0.2-1.win32-py2.3.exe>
- Install PyGtk 2.8.6. It is available from <http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.8/pygtk-2.8.6-1.win32-py2.3.exe>

Put de files in the directory: `C:\Users\[USER]\.dia\python`.
Open DIA, create a Database Diagram and export how SQL file.

##Dia SQL te permite generar.

 - Generador de código SQL
 - Hojas de calculo de *libreOffice* para las tablas.
 - Objeto exportar el digrama en _json_ (formato ideal para importar en la web).
 - Archivo de traducción _.po_.

##instalación.
	
####opteniendo el proyecto
Desde git

	#descargar el paquete
	git clone git@github.com:fitorec/diasql.git

Tambien lo puede descargar desde la web y descomprimir posteriormente 

####Instalando plugins y archivos dia

	#una vez
	cd diasql
	sudo ./install.sh

###Estructura actual de archivos

	.
	|-- dia-splash.png <- nuevo splash
	|-- install.sh <- instalador
	|-- README.md <- Archivo README
	`-- src
		`-- plugins
			|-- diacalc.py <- Plugin para exportar en Hojas de calculo de *libreOffice*
			|-- diajson.py <- Plugin para exportar en en _json_
			|-- diapo.py <- Plugin para exportar archivo de traducción _.po_.
			`-- diasql.py <- Plugin para exportar en SQL

Para mayores informes usted puede consultar las [Ligas de interés](/fitorec/diasql/blob/master/doc/bookmarks.md)
