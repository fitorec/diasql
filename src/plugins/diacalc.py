#    PyDia calc.py : calc dump.
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


class CalcRender:
    def __init__(self):
        self.f = None
        self.count = 0
        self.fileName = None

    def begin_render(self, data, filename):
        self.f = open(filename, "w")
        self.f.write(
            '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="es-mx">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
<table>
<tr>''')
        try:
            self.fileName = name = os.path.split(filename)[1]
            self.fileName = re.findall('([^.]*)\\.', self.fileName)[0]
            for layer in data.layers:
                self.WriteTables(layer)
        except BaseException:
            pass

    def WriteTables(self, layer):
        for o in layer.objects:
            if o.type.name == 'Database - Table':
                if "name" not in o.properties:
                    continue
                if not o.properties["name"].value == self.fileName:
                    continue
                atributes = o.properties['attributes'].value
                for i in range(0, len(atributes)):
                    a = atributes[i]
                    if len(a[0]) < 1:
                        continue
                    inputName = a[0]
                    comment = a[2].split('\n')
                    if len(comment) > 0 and len(comment[0]) > 0:
                        inputName = comment[0]
                    if len(inputName) < 1:
                        continue
                    self.f.write(
                        '\n\t<th width="%spx">%s</th>' %
                        (10 * len(inputName), inputName))
                    self.count = self.count + 1

    def end_render(self):
        # Me latio esta implementacion se me hiso bastante H4ck!
        self.f.write(
            '\n</tr>\n<tr>%s\n</tr>\n</table>' %
            ('\n\t<td></td>' * self.count))
        self.f.write('\n</body>\n</html>')
        self.f.close()
# Bind reference


dia.register_export("SICAODS Hoja Calculo para el oocalc", "ods", CalcRender())
