Dia SQL
===========================================================================

> Plugins para el modelador de diagramas de base de datos


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
	|-- README.md <- Archivo REAME
	`-- src
		`-- plugins
			|-- diacalc.py <- Plugin para exportar en Hojas de calculo de *libreOffice*
			|-- diajson.py <- Plugin para exportar en en _json_
			|-- diapo.py <- Plugin para exportar archivo de traducción _.po_.
			`-- diasql.py <- Plugin para exportar en SQL
			
###Video Muestra del DIA
<script type="text/javascript" src="http://s3.www.universalsubtitles.org/embed.js">
  ({
       video_url: "http://www.youtube.com/watch?v=tViDesD4Adw&feature=fvsr",
       video_config: {
           color1: '0xFF0000',
           width: 640,
           height: 480
       }
  })
</script>

Para mayores informes usted puede consultar las [Ligas de interés](/fitorec/diasql/blob/master/doc/bookmarks.md)
