#!/usr/bin/python
# -*- coding: utf-8 -*- 

from ptc import *

client = PTCClient('127.0.0.1', 6069)
archivo = open("data.txt")
data = archivo.read()
print("Voy a tratar de conectarme.")
client.connect('127.0.0.1', 5559)
print("Me conecté.")
client.send(data)
print("Mandé los datos.")
#client.close()
#print("Cerré conexión.")
while True:
    pass
