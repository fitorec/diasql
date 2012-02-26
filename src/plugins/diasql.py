#    PyDia SQL.py : SQL dump.
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

class SQLRenderer :
	def __init__ (self) :
		self.f = None
		
	def begin_render (self, data, filename) :
		self.f = open(filename, "w")
		name = os.path.split(filename)[1]
		self.f.write ('''-- Created by DiaSql-Dump Version 0.01(Beta)
-- Filename: %s\n''' % (name))
		for layer in data.layers :
			self.WriteTables (layer)
	
	def WriteTables (self, layer):
		tables = {}
		priority = {'fields' : 0 , 'foreign_keys' :100}
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
				atributes = o.properties['attributes'].value
				for i in range(0,len(atributes)):
					a = atributes[i]
					tipo = ''
					if re.match('.*enum\(.*',a[1],re.I) :
						tipo = a[1]
					else :
						tipo = a[1].upper()
					tables[table] +=  '%0.3d\t`%s` %s' % (priority['fields']+i, a[0], tipo)
					if a[3] == 1 :
						tables[table] += ' PRIMARY KEY'

					if a[4] == 0 :
						tables[table] += ' NOT NULL'
					else:
						tables[table] += ' DEFAULT NULL'

					if a[5] == 1 :
						tables[table] += ' UNIQUE'
					#add  AUTO_INCREMENT 
					if (a[3] == 1 and re.match('.*int.*',a[1],re.I)) :
						tables[table] += ' AUTO_INCREMENT'
					tables[table] += '\n'
			elif o.type.name == 'Database - Reference':
				continue
				'''src = o.properties['start_point_desc'].value.split('.')
				desc = o.properties['end_point_desc'].value.split('.')
				if len(src) != 2 and len(desc) != 2:
					continue
				if not tables.has_key(desc[0]):
					tables[desc[0]] = ''
				tables[desc[0]] += '%0.3d\tFOREIGN KEY (%s) REFERENCES %s(%s)\n' % (priority['foreign_keys'],desc[1],src[0],src[1])'''
		for k in tables.keys():
			self.f.write('\n-- %s --\nDROP TABLE IF EXISTS `%s`;\n' % (k,k) )
			self.f.write ('CREATE TABLE IF NOT EXISTS `%s` (\n' % k)
			sentences = sorted( tables[k].split('\n') )
			sentences = [str(s[3:]) for s in sentences if len(s)>4]
			sentences = ",\n".join( sentences)
			self.f.write ('%s\n' % sentences)
			self.f.write (') ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;\n')
	def end_render (self) :
		self.f.write ('-- End SQL-Dump\n')
		self.f.close()
# reference
dia.register_export ("SICASQL generado de esquema en SQL", "sql", SQLRenderer())
