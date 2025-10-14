"""
Crea un programa en python que cree un fichero 
en modo escritura. A continuación, irá leyendo 
línea a línea de teclado hasta que el usuario 
introduzca la cadena “fin”. Debe escribir cada 
línea en el fichero creado.
"""

#creacion del fichero
f = open('FicheroLineaALinea', 'w+', encoding="utf8")

#le pido la linea a escribir en el fichero
lineaTeclado = input("Introduzca una cadena para añadirla al fichero: ")

#mientras que la cadena no sea igual a "fin"
while (lineaTeclado != "fin"):
    #escribo la linea en el fichero
    f.write(lineaTeclado)

    #hago un salto de linea
    f.write('\n')

    #le pido la linea a escribir en el fichero
    lineaTeclado = input("Introduzca una cadena para añadirla al fichero: ")

#vuelvo al inicio del fichero
f.seek(0)

for lineaFichero in f.readlines():
    print(lineaFichero, end="")

#cierro el fichero
f.close