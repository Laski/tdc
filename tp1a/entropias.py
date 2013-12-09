#! /usr/bin/python

from matplotlib import pyplot as plt
from matplotlib import numpy as np
import sys
from math import log

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
	#tuplas_txt = tuplas_txt[0:50]
	
	senders = [tupla.split("'")[1] for tupla in tuplas_txt]
	recievers = [tupla.split("'")[3] for tupla in tuplas_txt]
	types = [int(tupla.split("', ")[2].rstrip(")")) for tupla in tuplas_txt]
	#print(tuplas_txt)
	return senders, recievers, types
	print(senders)
	print(recievers)
	print(types)

def get_host(ip):
	return int(ip.split(".")[3])

def get_host_lista(ips):
	return [get_host(ip) for ip in ips]

def entropia(ips):
	N = sum(ips.values())
	Ps = [ k/N for k in ips.values() ]
	H = -sum([ p*log(p,2) for p in Ps ])
	return H

def calcular_entropias(xs, ys):
	xs_sin_repes = list(set(xs))
	xs_hosts = get_host_lista(xs)
	ys_hosts = get_host_lista(ys)
	res = []
	for x in xs_sin_repes:
		ips = {}
		for i in range(len(ys)):
			if(xs[i] == x): 
				if not ips.has_key(ys[i]): ips[ys[i]] = 0.0
				ips[ys[i]]+= 1
		res.append(entropia(ips))
	
	return res 
	

senders, recievers, types = leer_entrada()
todos = senders + recievers
sin_repetidas = list(set(todos))

entropias_senders = calcular_entropias(senders, recievers)

print list(set(senders))
print entropias_senders

#barras(sin_repetidas, senders, recievers)
#torta(sin_repetidas)
#histograma(todos)
#histograma2d(senders, recievers)
