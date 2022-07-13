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

import dia
import sys
import os
import string
import re
import datetime
import pprint


def rgbColor(color):
    r = int(255 * color.red)
    g = int(255 * color.green)
    b = int(255 * color.blue)
    return '"#%02X%02X%02X"' % (r, g, b)


class JSONRenderer:
    def __init__(self):
        self.f = None

    def begin_render(self, data, filename):
        self.f = open(filename, "w")
        name = os.path.split(filename)[1]
        self.f.write('''/* Created by DiaJSON-Dump Version 0.01(Beta)
 * Filename: %s\n */\n''' % (name))
        self.f.write("var tablas = [\n")
        for layer in data.layers:
            self.WriteTables(layer)

    def WriteTables(self, layer):
        tables = {}
        values = {}
        priority = {'fields': 0, 'foreign_keys': 100}
        n_tabla = 1
        miny = 500000
        minx = 500000
        # extract the minimum values
        for o in layer.objects:
            pos = o.properties["obj_pos"].value
            if pos.y < miny:
                miny = pos.y
            if pos.x < minx:
                minx = pos.x
        # for each object o into the diagram
        for o in layer.objects:
            if o.type.name == 'Database - Table':
                if "name" in o.properties:
                    table = o.properties["name"].value
                elif "text" in o.properties:
                    table = o.properties["text"].value.text
                else:
                    continue
                if len(table) == 0 or string.find(table, " ") >= 0:
                    continue
                if table not in tables:
                    tables[table] = ''
                # get position object
                pos = o.properties["obj_pos"].value
                # add orden(order) of the table
                values[table] = '"orden" : ' + str(n_tabla) + ',\n'
                n_tabla = n_tabla + 1
                # extract the dimensions
                w = int(o.properties["elem_width"].value * 30)
                h = int(o.properties["elem_height"].value * 30)
                values[table] += '"width" : ' + str(w) + ',\n'
                values[table] += '"height" : ' + str(h) + ',\n'
                # set the position
                values[table] += '"pos_x" : ' + \
                    str(int(pos.x - minx) * 16) + ',\n'
                values[table] += '"pos_y" : ' + \
                    str(int(pos.y - miny) * 16) + ',\n'
                # set color
                color = o.properties["fill_colour"].value
                fill_colour = rgbColor(color)
                values[table] += '"fill_colour" : ' + fill_colour + ',\n'
                #
                color = o.properties["text_colour"].value
                text_colour = rgbColor(color)
                values[table] += '"text_colour" : ' + text_colour + ',\n'
                #
                color = o.properties["line_colour"].value
                line_colour = rgbColor(color)
                values[table] += '"line_colour" : ' + line_colour + ',\n'

                atributes = o.properties['attributes'].value
                # set the diagram in json format
                for i in range(0, len(atributes)):
                    #
                    a = atributes[i]
                    tipo = ''
                    if re.match('.*enum\\(.*', a[1], re.I):
                        tipo = a[1]
                    else:
                        tipo = a[1].upper()
                    tables[table] += '%0.3d {"nombre": "%s", "tipo": "%s", ' % (
                      priority['fields'] + i, a[0], tipo
                    )
                    if a[3] == 1:
                        tables[table] += '"clave_primaria": true,'
                        tables[table] += '"clave_unica": true,'
                        tables[table] += '"es_null": false,'
                    else:
                        tables[table] += '"clave_primaria": false,'
                        if a[4] == 0:
                            tables[table] += '"es_null": false,'
                        else:
                            tables[table] += '"es_null": true,'
                        if a[5] == 1:
                            tables[table] += '"clave_unica": true,'
                        else:
                            tables[table] += '"clave_unica": false,'
                    # add  AUTO_INCREMENT
                    if (a[3] == 1 and re.match('.*INT.*', a[1], re.I)):
                        tables[table] += '"auto_increment": true'
                    else:
                        tables[table] += '"auto_increment": false'
                    tables[table] += '}\n'
            elif o.type.name == 'Database - Reference':
                # for p in o.properties.keys():
                # print p, '\t', o.properties[p]
                continue
        tbs = ''
        for k in tables.keys():
            tbs += '{\n"nombre" : "%s",\n' % k
            tbs += values[k]
            tbs += '"campos" : [\n'
            campos = sorted(tables[k].split('\n'))
            campos = [str(s[3:]) for s in campos if len(s) > 4]
            campos = ",\n".join(campos)
            tbs += '%s\n' % campos
            tbs += ' ]\n},\n'
        if len(tables) > 1:
            tbs = '%s' % tbs[0:-2]
        self.f.write(tbs)

    def end_render(self):
        self.f.write("\n]")
        self.f.close()
# reference


dia.register_export(
    "SICAJSON exportar datos en formato JSON(JavaScript Object Notation)",
    "js",
    JSONRenderer())
