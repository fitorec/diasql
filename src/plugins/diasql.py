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

import dia
import sys
import os
import string
import re
import datetime


class BD:
    # Constructor
    def __init__(self, name):
        self._name = name
        self.tables = {}
# Add a table

    def addTable(self, tableProperties):
        name = ""
        if "name" in tableProperties:
            name = tableProperties["name"].value
        elif "text" in tableProperties:
            name = tableProperties["text"].value.text
        elif len(name) == 0 or string.find(name, " ") >= 0:
            return None
        if name not in self.tables:
            self.tables[name] = Table(name, tableProperties)
# toString

    def __str__(self):
        out = '-- Created by DiaSql Version 0.02(Beta)\n'
        out += '-- Filename: %s\n' % (self._name)
        for key in self.tables.keys():
            out += str(self.tables[key])
        out += '-- End SQL-Dump\n'
        return out


class Table:
    # constructor
    def __init__(self, name, tableProperties):
        self._name = name
        self.columns = {}
        self.colsPositions = []
        self._comment = ""
        if (len(tableProperties["comment"].value) > 1):
            self._comment = tableProperties["comment"].value
        columns = tableProperties['attributes'].value
        for i in range(0, len(columns)):
            col = Column(columns[i])
            if col._name not in self.columns:
                self.columns[col._name] = col
                self.colsPositions.append(col._name)

# toString
    def __str__(self):
        out = '\n-- %s --\nDROP TABLE IF EXISTS `%s`;\n' % (
            self._name, self._name)
        out += 'CREATE TABLE `%s` (\n' % self._name
        cols = []
        for key in self.colsPositions:
            cols.append(str(self.columns[key]))
        out += ",\n".join(cols)
        out += '\n) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1'
        if (len(self._comment) > 1):
            out += ' COMMENT "' + self._comment + '"'
        out += ';\n'
        return out


class Column:
    # Append a column list of atributes:
    # 0 name
    # 1 type
    # 2 Comment
    # 3 0 None, 1 AUTO_INCREMENT
    # 4 0 NOT NULL, 1 DEFAULT NULL
    # 5 0 none, 1 UNIQUE KEY
    def __init__(self, atributes):
        # 0 name
        self._name = atributes[0]
        # 1 type
        if re.match('.*enum\\(.*', atributes[1], re.I):
            self._type = atributes[1]
        else:
            self._type = atributes[1].upper()
        # 1  AUTO_INCREMENT
        self._auto_increment = False
        if (atributes[3] == 1 and re.match('.*int.*', self._type, re.I)):
            self._auto_increment = True
        # 2  Comments
        self._comment = ""
        if (len(atributes[2]) > 1):
            self._comment = atributes[2]
        # 3  Primary key
        self._primary_key = False
        if atributes[3] == 1:
            self._primary_key = True
        # 4 NULL and NOT NULL
        self._not_null = False
        if atributes[4] == 0:
            self._not_null = True
        # 5 Unique Key
        self._unique_key = False
        if atributes[5] == 1 and self._primary_key is False:
            self._unique_key = True
        if self._primary_key or self._unique_key:
            self._not_null = True

# toString
    def __str__(self):
        out = '\t`%s` %s' % (self._name, self._type)
        if self._not_null:
            out += ' NOT'
        out += ' NULL'
        if self._auto_increment:
            out += ' AUTO_INCREMENT'
        if self._primary_key:
            out += ' PRIMARY KEY'
        if self._unique_key:
            out += ' UNIQUE KEY'
        if (len(self._comment) > 1):
            out += ' COMMENT "%s"' % (self._comment)
        return out


class SQLRenderer:
    def __init__(self):
        self.f = None
        self.bd = None

    def begin_render(self, data, filename):
        self.f = open(filename, "w")
        name = os.path.split(filename)[1]
        self.bd = BD(name)
        for layer in data.layers:
            self.WriteTables(layer)

    def WriteTables(self, layer):
        for o in layer.objects:
            if o.type.name == 'Database - Table':
                self.bd.addTable(o.properties)
        self.f.write(str(self.bd))

    def end_render(self):
        self.f.close()


# reference
dia.register_export("SICASQL generado de esquema en SQL", "sql", SQLRenderer())
