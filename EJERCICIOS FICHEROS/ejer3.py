"""
Diseña una aplicación que pida al usuario su 
nombre y edad. Estos datos deben guardarse en 
el fichero datos.txt. Si este fichero existe, 
deben añadirse al final en una nueva línea, y 
en caso de no existir, debe crearse.
"""

#abro un fichero o lo creo
f = open('datos.txt', 'a', encoding='utf8')

#le pido al usuario sus datos
nombre = input("Introduzca su nombre: ")
edad = int(input("Introduzca su edad: "))

#escribo sus datos en el fichero
f.write(nombre + ' ' + str(edad) + '\n')

#muevo el cursor al principio del documento
f.seek(0)

"""#muestro el contenido del fichero
for lineaFichero in f.readlines():
    print(lineaFichero)"""

#cierro el fichero
f.close