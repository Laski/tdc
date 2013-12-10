#!/usr/bin/python
# -*- coding: utf-8 -*- 

from ptc import *
import sys
import time

client = PTCClient('127.0.0.1', 6069)
archivo = open(sys.argv[1])
data = archivo.read()
print("Voy a tratar de conectarme.")
client.connect('10.2.2.3', 5559)
print("Me conecté.")
client.send(data)
print("Mandé los datos.")
#client.close()
#print("Cerré conexión.")
while True:
    pass
