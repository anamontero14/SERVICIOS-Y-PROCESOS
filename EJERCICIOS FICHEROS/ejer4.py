"""
Implementa un programa que lea números 
enteros no ordenados de un archivo, con 
un número por línea, y los almacene en una 
lista. A continuación, debe guardar los 
números de la lista en otro fichero distinto 
pero ordenados de forma ascendente.
"""

#creo la lista que almacenará los números del archivo
listaNumeros = []

#abro el fichero para leer
l = open('EJERCICIOS FICHEROS\\NumerosAleatorios.txt', 'rt')

#voy añadiendo los numeros a la lista
for lineaFichero in l.readlines():
    listaNumeros.append(lineaFichero)

#cierro el fichero porque no lo voy a necesitar mas
l.close

#abro el fichero en el que voy a escribir los numeros ordenados
w = open('NumerosAleatoriosOrdenados.txt', 'a+', encoding='utf8')

#ordeno la lista de los numeros
listaNumeros.sort()

#recorro la lista y voy escribiendo los numeros en el fichero
for numero in listaNumeros:
    w.write(str(numero))

#cierro el fichero
w.close