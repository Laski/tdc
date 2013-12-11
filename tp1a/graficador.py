#! /usr/bin/python

from matplotlib import pyplot as plt
from matplotlib import numpy as np
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
	#tuplas_txt = tuplas_txt[0:250:2]
	
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

def torta(ips, sin_repetidas):
	sizes = [(ip,ips.count(ip)) for ip in sin_repetidas]
	    
	sizes = sorted(sizes, key=lambda tup: tup[1])
	
	sin_repetidas = [tup[0] for tup in sizes]
	sizes = [tup[1] for tup in sizes]
    
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'blue', 'red', 'orange', 'yellow', 'white'] * 10
	plt.pie(sizes, labels=sin_repetidas, autopct='%1.1f%%', shadow=True, colors=colors)
	plt.axis('equal')
	plt.show()

def histograma(todos):
	hosts = get_host_lista(todos)
	n, bins, patches = plt.hist(hosts)
	plt.xlabel('Cantidad de paquetes')
	plt.ylabel('IPs (ultimos 8 bits)')
	#plt.plt(n)
	#plt.subplots_adjust(left=0.15)
	plt.show()

def histograma2d(senders, recievers):
	senders_hosts = get_host_lista(senders)
	recievers_hosts = get_host_lista(recievers)
	H, xedges, yedges = np.histogram2d(recievers_hosts, senders_hosts, bins=50)
	#plt.colorbar()
	extent = [0, 255, 255, 0]
	plt.xlabel("Emisores")
	plt.ylabel("Receptores")
	plt.imshow(H, extent=extent, interpolation='nearest')
	plt.colorbar()
	plt.show()

def barras(sin_repetidas, senders, recievers):
	senders_hosts = get_host_lista(senders)
	recievers_hosts = get_host_lista(recievers)
	todas_hosts = get_host_lista(sin_repetidas)
	todas_hosts = list(set(todas_hosts))
	todas_hosts.sort()


	cant_ips = len(todas_hosts)
	count_senders = [senders_hosts.count(ip) for ip in todas_hosts]
	count_recievers = [recievers_hosts.count(ip) for ip in todas_hosts]

	fig, ax = plt.subplots()
	index = np.arange(cant_ips)
	bar_width = 0.3
	opacity = 0.4
	rects1 = plt.bar(index, count_senders, bar_width,
	                 alpha=opacity,
	                 color='b',
	                 label='Emisores')
	rects2 = plt.bar(index + bar_width, count_recievers, bar_width,
	                 alpha=opacity,
	                 color='g',
	                 label='Receptores')
	plt.xlabel('IPs (ultimos 8 bits)')
	plt.ylabel('Cantidad de paquetes')
	plt.xticks(index + bar_width, todas_hosts)
	plt.legend()
	plt.tight_layout()
	plt.show()

senders, recievers, types = leer_entrada()
todos = senders + recievers
sin_repetidas = list(set(todos))
sr_senders = list(set(senders))
sr_rec = list(set(recievers))
#barras(sin_repetidas, senders, recievers)
#torta(todos, sin_repetidas)
#torta(senders, sr_senders)
#torta(recievers, sr_rec)
#histograma(todos)
histograma2d(senders, recievers)
