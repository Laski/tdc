#! /usr/bin/python
from matplotlib import pyplot as plt
from matplotlib import numpy as nm
import sys

def leer_entrada():
	if not len(sys.argv) == 2:
		print ("Usage: " + sys.argv[0] + " nombre_de_archivo")
		exit(1)		
	archivo = open(sys.argv[1], 'r')
	lista_start = archivo.read().find("Todos")
	archivo.seek(lista_start)
	archivo.readline()
	capturas_txt = archivo.readline()
	tuplas_txt = [tupla for tupla in capturas_txt.split("), ")]
	tuplas_txt[0] = tuplas_txt[0].strip("[")
	tuplas_txt[-1] = tuplas_txt[-1].rstrip(")]\n")
	tuplas_txt = [tupla + ")" for tupla in tuplas_txt]
	senders = [tupla.split("'")[1] for tupla in tuplas_txt]
	recievers = [tupla.split("'")[3] for tupla in tuplas_txt]
	types = [int(tupla.split("', ")[2].rstrip(")")) for tupla in tuplas_txt]
	#print(tuplas_txt)
	return senders, recievers, types
	print(senders)
	print(recievers)
	print(types)

senders, recievers, types = leer_entrada()
todos = senders + recievers

sin_repetidas = list(set(todos))
sizes = [todos.count(ip) for ip in sin_repetidas]
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'blue', 'red', 'orange', 'yellow', 'white'] * 10
plt.pie(sizes, labels=sin_repetidas, autopct='%1.1f%%', shadow=True, colors=colors)
plt.axis('equal')
plt.show()

hosts = [int(ip.split(".")[3]) for ip in todos]
n, bins, patches = plt.hist(hosts)
plt.xlabel('Apariciones')
plt.ylabel('Ultimos 8 bits de las IPs')
#plt.plt(n)
#plt.subplots_adjust(left=0.15)
plt.show()

senders_hosts = [int(ip.split(".")[3]) for ip in senders]
recievers_hosts = [int(ip.split(".")[3]) for ip in recievers]
H, xedges, yedges = nm.histogram2d(senders_hosts, recievers_hosts, bins=40)
#plt.colorbar()
extent = [0, 255, 255, 0]
plt.imshow(H, extent=extent, interpolation='nearest')
plt.colorbar()
plt.show()