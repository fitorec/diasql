#    PyDia Json.py : JSON dump.
#    Copyright (c) 2010 fitorec  <chanerec@gmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import dia, sys, os, string, re, datetime
import pprint

class JSONRenderer :
	def __init__ (self) :
		self.f = None
	
	def begin_render (self, data, filename) :
		self.f = open(filename, "w")
		name = os.path.split(filename)[1]
		self.f.write ('''/* Created by DiaJSON-Dump Version 0.01(Beta)
 * Filename: %s
 * Created: %s*/\n''' % (name,datetime.date.today()))
		self.f.write ("var tablas = [\n")
		for layer in data.layers :
			self.WriteTables (layer)
	
	def WriteTables (self, layer):
		tables = {}
		values = {}
		priority = {'fields' : 0 , 'foreign_keys' :100}
		n_tabla = 1
		miny=500000
		minx=500000
		#obtenemos los minimos en x y y respectivamente.
		#if o.type.name == 'Database - Table':
		for o in layer.objects :
			pos = o.properties["obj_pos"].value
			if pos.y < miny :
				miny = pos.y
			if pos.x<minx :
				minx = pos.x
		#pra cada tabla en la base de datos
		for o in layer.objects :
			if o.type.name == 'Database - Table' :
				if o.properties.has_key ("name") :
					table = o.properties["name"].value
				elif o.properties.has_key ("text") :
					table = o.properties["text"].value.text
				else :
					continue
				if len(table) == 0 or string.find (table, " ") >= 0 :
					continue
				if not tables.has_key(table):
					tables[table] = ''
				#
				#for p in o.properties.keys(): 
				#	print p, '\t', o.properties[p]
				#posicion en X y Y de la tabla
				print ("*"*80)+"\ntabla "+table
				pos = o.properties["obj_pos"].value
				#agregando orden de la tabla
				values[table] = '"orden" : '+str(n_tabla)+',\n'
				n_tabla = n_tabla+1
				#Extrayendo las medidas
				w = int(o.properties["elem_width"].value*30)
				h = int(o.properties["elem_height"].value*30)
				values[table] += '"width" : '+str(w)+',\n'
				values[table] += '"height" : '+str(h)+',\n'
				#Las posiciones
				values[table] += '"pos_x" : '+str(int(pos.x-minx)*16)+',\n'
				values[table] += '"pos_y" : '+str(int(pos.y-miny)*16)+',\n'
				#Los colores
				color = o.properties["fill_colour"].value
				fill_colour='"#%02X%02X%02X"' % (int(255 * color.red), int(color.green * 255), int(color.blue * 255))
				values[table] += '"fill_colour" : '+fill_colour+',\n'
				#
				color = o.properties["text_colour"].value
				text_colour='"#%02X%02X%02X"' % (int(255 * color.red), int(color.green * 255), int(color.blue * 255))
				values[table] += '"text_colour" : '+text_colour+',\n'
				#
				color = o.properties["line_colour"].value
				line_colour='"#%02X%02X%02X"' % (int(255 * color.red), int(color.green * 255), int(color.blue * 255))
				values[table] += '"line_colour" : '+line_colour+',\n'
				
				atributes = o.properties['attributes'].value
				print "tamaño anchoXalto=("+str(w)+"X"+str(h)+')'
				#vamos a formar los datos en formato json
				for i in range(0,len(atributes)):
					#cada atributo(campo) se abre({) con nombre  y se cierra con 
					a = atributes[i]
					tipo = ''
					if re.match('.*enum\(.*',a[1],re.I) :
						tipo = a[1]
					else :
						tipo = a[1].upper()
					tables[table] +=  '%0.3d {"nombre" : "%s", "tipo": "%s", ' % (priority['fields']+i, a[0], tipo)
					if a[3] == 1 :
						tables[table] += '"clave_primaria": true,'
						tables[table] += '"clave_unica": true,'
						tables[table] += '"es_null": false,'
					else:
						tables[table] += '"clave_primaria": false,'
						if a[4] == 0 :
							tables[table] += '"es_null": false,'
						else:
							tables[table] += '"es_null": true,'
						if a[5] == 1 :
							tables[table] += '"clave_unica": true,'
						else:
							tables[table] += '"clave_unica": false,'
					#add  AUTO_INCREMENT 
					if (a[3] == 1 and re.match('.*INT.*',a[1],re.I)) :
						tables[table] += '"auto_increment": true'
					else:
						tables[table] += '"auto_increment": false'
					tables[table] += '}\n'
			elif o.type.name == 'Database - Reference':
				#for p in o.properties.keys(): 
				#	print p, '\t', o.properties[p]
				continue
		tbs=''
		for k in tables.keys():
			tbs += '{\n"nombre" : "%s",\n' % k
			tbs += values[k]
			tbs += '"campos" : [\n'
			campos = sorted( tables[k].split('\n') )
			campos = [str(s[3:]) for s in campos if len(s)>4] #
			campos = ",\n".join( campos)
			tbs +=  '%s\n' % campos
			tbs += ' ]\n},\n'
		if len(tables)>1 :
			tbs = '%s' % tbs[0:-2]
		self.f.write (tbs)
	def end_render (self) :
		self.f.write ("\n]")
		self.f.close()
# reference
	def rgb (color) :
		#convierte un color en una cadena en formato rgb hexadecimal
		#print color
		rgb = "#%02X%02X%02X" #% (int(255 * color.red), int(color.green * 255), int(color.blue * 255))
		return rgb
dia.register_export ("SICAJSON exportar datos en formato JSON(JavaScript Object Notation)", "js", JSONRenderer())
