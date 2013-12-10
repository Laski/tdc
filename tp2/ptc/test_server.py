#!/usr/bin/python
# -*- coding: utf-8 -*- 

from ptc import *
import time
import sys

archivo = open(sys.argv[1])
data = archivo.read()
server = PTCServer('127.0.0.1', 5559)
print ("Voy a esperar una conexión.")
server.accept()
print ("Me conecté.")
data = server.recv(len(data))
print ("Recibí los datos.")
