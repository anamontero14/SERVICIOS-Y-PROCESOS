"""
Crea con un editor el fichero de texto Alumnos.txt 
y escribe en él los nombres, edades y estaturas de 
los alumnos de un grupo, cada uno en una línea:
	juan 22 1.77
	luis 21 1.80
	pedro 20 1.73
	…
Implementa un programa que lea del fichero los datos, muestre
los nombres y calcule la media de la edad y de las 
estaturas, mostrándolas por pantalla.
"""

#variable para el fichero
f = open('Alumnos.txt', 'w+', encoding="utf8")

#variable que tendra lo que se escriba en el fichero
alumno = ""
#variable que almacenará la media de la altura
mediaAltura : int = 0
#variable que almacenará la media de la edad
mediaEdad : int = 0
#contador para contar cuantos alumnos hay y así hacer la media
contador : int = 0

#almaceno el alumno a añadir en el fichero
alumno = input("Introduce un nuevo alumno: ")

#mientras que alumno no sea nada
while (alumno != ""):
    #escribo al alumno en el fichero
    f.write(alumno)
    #hago un salto de línea
    f.write('\n')
    #escribo otro alumno
    alumno = input("Introduce un nuevo alumno: ")

f.seek(0)

#leo el fichero línea por línea
for linea in f.readlines():
    print(linea, end="")

    #aumento el contador porque se ha mostrado 1 alumno
    contador += 1

    #separo el alumno en partes para poder coger la edad y altura
    alumnoCadena = linea.split()

    #sumo el valor que se encuentre en la posicion correspondiente
    mediaEdad += int(alumnoCadena[1])
    mediaAltura += float(alumnoCadena[2])

resultadoEdad = mediaEdad / contador
resultadoAltura = mediaAltura / contador

print("Media de la edad de los alumnos: " + str(resultadoEdad) +"\nMedia de la altura de los alumnos:" + str(resultadoAltura))

#cierro el fichero
f.close