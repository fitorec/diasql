#!/bin/bash
#autor:		fitorec <chanerec@gmail.com>
#descripcion:	Este script instala el programa dia-gnome y ferret 2 herramientas para el modelado de BD
#             . --- .
#           /        \
#          |  O  _  O |
#          |  ./   \. |
#          /  `-._.-'  \
#        .' /         \ `.
#    .-~.-~/           \~-.~-.
#.-~ ~    |             |    ~ ~-.
#`- .     |             |     . -'
#     ~ - |             | - ~
#         \             /
#       ___\           /___
#      ~;_  >- . . -<  _i~
#          `'         `'


if [ `id -g` -ne 0 ]
then
  echo "Usage:  ./$0 root group"
  exit $E_BADARGS
fi

#Instalando Dia y los paquetes necesarios para trabajar en SICA
#apt-get update -y
#packages=(dia-gnome mysql mysqldump)
#for package in ${packages[@]}
#do
#	apt-get --force-yes -y build-dep $package
#	apt-get --force-yes -y install $package
#done;

#dia Splash
echo "Cambiando Splash  (este se ve mas bonito :¬D)"
cp dia-splash.png /usr/share/dia/dia-splash.png

#dia plugins
plugins=(diasql diapo diacalc diajson)
for plugin in ${plugins[@]}
do
	echo "Compilando & copiando plugin " $plugin
	#chmod 644 $plugin.py
	chmod 644 ./src/plugins/$plugin.py
	#gene new 
	rm -f /usr/share/dia/python/$plugin.py /usr/share/dia/python/$plugin.py
	cp ./src/plugins/$plugin.py /usr/share/dia/python/$plugin.py
	python -m compileall /usr/share/dia/python/$plugin.py
	#permisos adecuados
	chmod 644 /usr/share/dia/python/$plugin.py*
done;

zenity --info --text="La instalacion ha concluido de forma exitosa"

