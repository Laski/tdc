#!/usr/bin/python
# -*- coding: utf-8 -*- 

from ptc import *
import time

archivo = open("data.txt")
data = archivo.read()
server = PTCServer('127.0.0.1', 5559)
print ("Voy a esperar una conexión.")
server.accept()
print ("Me conecté.")
time.sleep(10)
data = server.recv(len(data))
print (data)
print ("Recibí los datos.")
