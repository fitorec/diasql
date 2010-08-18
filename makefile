#!/usr/bin/make -f
# -*- makefile -*-
#

install:build
	
build: diasql.pyc
	mkdir -p /usr/share/dia/python
	cp diasql.pyc /usr/share/dia/python
	cp diasql.py /usr/share/dia/python

diasql.pyc: 
	python -m compileall diasql.py
binary:
	
clean: diasql.pyc
	rm diasql.pyc
