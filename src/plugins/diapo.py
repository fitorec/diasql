#    PyDiaPO.py : PO dump.
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


class PORenderer:
    def __init__(self):
        self.f = None
        self.msgids = []

    def camel_field(self, field):
        return string.capwords(field.replace('_', ' '))

    def append_nmsgid(self, msgid, msgstr):
        if msgid not in self.msgids:
            self.msgids.append(msgid)
            self.f.write('\nmsgid "%s"' % msgid)
            self.f.write('\nmsgstr "%s"' % msgstr)

    def begin_render(self, data, filename):
        self.f = open(filename, "w")
        name = os.path.split(filename)[1]
        self.f.write('''# Spanish Translation
# Copyright (C) 2010 - SICÁ www.mundosica.com
# Created by DiaPO - V 0.01
# Developed by fitorec -  <chanerec@gmail.com> 2010.
# Filename: %s
# Last-Modifield: %s\n
msgid ""
msgstr ""
"Project-Name: <Proyect-Name>\\n"
"Report-Msgid-Bugs-To: http://mundosica.com/support/contact/\\n"
"Last-Translator: %s \\n"
"Language-Team: sicá <contacto@mundosica.com>\\n"
"MIME-Version: 0.1\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"X-Poedit-Language: Spanish\\n"
"X-Poedit-Country: SPAIN\\n"
"X-Poedit-SourceCharset: utf-8\\n"''' % (
            name, datetime.date.today(), datetime.date.today())
        )
        for layer in data.layers:
            self.WriteTables(layer)

    def WriteTables(self, layer):
        tables = {}
        priority = {'fields': 0, 'foreign_keys': 100}
        for o in layer.objects:
            if o.type.name == 'Database - Table':
                if "name" in o.properties:
                    table = o.properties["name"].value
                    self.f.write('\n\n#Section %s\n#%s' % (table, "=" * 79))
                else:
                    continue
                if len(table) == 0 or string.find(table, " ") >= 0:
                    continue
                if table not in tables:
                    tables[table] = ''
                atributes = o.properties['attributes'].value

                for i in range(0, len(atributes)):
                    a = atributes[i]
                    if len(a[0]) < 1:
                        continue
                    # convirtiendo los campos de referencia 'table_id' a
                    # 'table'
                    inputName = re.sub('_id$', '', a[0], 1)

                    self.f.write('\n\n#%s.%s' % (table, inputName))
                    comment = a[2].split('\n')
                    if len(comment) > 0 and len(comment[0]) > 0:
                        self.append_nmsgid(
                            self.camel_field(inputName), comment[0])
                    if len(comment) > 1 and len(comment[1]) > 0:
                        self.append_nmsgid(table + '.' + inputName, comment[1])

    def end_render(self):
        self.f.close()


# reference
dia.register_export("SICACakePHP archivo de traducción", "po", PORenderer())
