from multiprocessing import Process, Pool
import random
import time

"""
En este ejercicio debes implementar los siguientes procesos y el Main como
se explica a continuación:
a. Proceso 1: Genera 6 números aleatorios entre 1 y 10, ambos
   inclusive, y los guarda en un fichero. Estos números deben contener
   decimales. La ruta a este fichero se le indicará como parámetro de
   entrada. Estos 6 números representan las notas de un alumno.
b. Proceso 2: Lee un fichero pasado por parámetro que contiene las
   notas de un alumno, cada una en una línea distinta, y realiza la media
   de las notas. También recibe como parámetro el nombre del alumno.
   Esta media se almacenará en un fichero de nombre medias.txt. Al
   lado de cada media debe aparecer el nombre del alumno, separados
   por un espacio.
c. Proceso 3: Lee el fichero medias.txt. En cada línea del fichero
   aparecerá una nota, un espacio y el nombre del alumno. Este proceso
   debe leer el fichero y obtener la nota máxima. Imprimirá por pantalla la
   nota máxima junto con el nombre del alumno que la ha obtenido.
"""

#función que genera 6 notas aleatorias y las guarda en un fichero
def generar_notas(ruta_fichero):
    #se abre el fichero en modo escritura
    with open(ruta_fichero, 'w') as f:
        #se hace un for para generar 6 notas
        for i in range(6):
            #se genera una nota aleatoria entre 1 y 10 con decimales
            nota = round(random.uniform(1, 10), 2)
            #se escribe la nota en el fichero
            f.write(f"{nota}\n")

#función que calcula la media de las notas de un alumno
def calcular_media(ruta_fichero, nombre_alumno):
    #variable que almacena la suma de las notas
    suma_notas = 0
    #variable que cuenta el número de notas
    contador = 0
    #se abre el fichero en modo lectura
    with open(ruta_fichero, 'r') as f:
        #se hace un for para leer todas las líneas del fichero
        for linea in f:
            #se convierte la línea a float y se suma
            suma_notas += float(linea.strip())
            #se incrementa el contador
            contador += 1
    #se calcula la media
    media = suma_notas / contador
    #se redondea la media a 2 decimales
    media = round(media, 2)
    #se abre el fichero medias.txt en modo append para añadir la media
    with open('medias.txt', 'a') as f:
        #se escribe la media y el nombre del alumno
        f.write(f"{media} {nombre_alumno}\n")

#función que obtiene la nota máxima del fichero medias.txt
def obtener_nota_maxima():
    #variable que almacena la nota máxima
    nota_maxima = 0
    #variable que almacena el nombre del alumno con la nota máxima
    alumno_maxima = ""
    #se abre el fichero medias.txt en modo lectura
    with open('medias.txt', 'r') as f:
        #se hace un for para leer todas las líneas del fichero
        for linea in f:
            #se parte la línea por el espacio
            nota, alumno = linea.strip().split(' ')
            #se convierte la nota a float
            nota = float(nota)
            #si la nota es mayor que la nota máxima se actualiza
            if nota > nota_maxima:
                nota_maxima = nota
                alumno_maxima = alumno
    #se imprime el resultado
    print(f"\nLa nota máxima es {nota_maxima} y la tiene {alumno_maxima}")

if __name__ == '__main__':
    #se borra el fichero medias.txt si existe para empezar de cero
    try:
        open('medias.txt', 'w').close()
    except:
        pass
    
    #se mide el tiempo que tardan en ejecutarse los procesos
    inicio = time.perf_counter()
    
    #OPCIÓN 1: USANDO BUCLES FOR
    print("=== OPCIÓN 1: USANDO BUCLES FOR ===\n")
    
    #lista para almacenar los procesos del proceso 1
    procesos_p1 = []
    #se hace un for para crear 10 procesos que generen las notas
    for i in range(1, 11):
        #se crea el nombre del fichero
        nombre_fichero = f"Alumno{i}.txt"
        #se crea el proceso
        p = Process(target=generar_notas, args=(nombre_fichero,))
        #se añade el proceso a la lista
        procesos_p1.append(p)
        #se inicia el proceso
        p.start()
    
    #se espera a que terminen todos los procesos del proceso 1
    for p in procesos_p1:
        p.join()
    
    print("Se han generado todos los ficheros de notas\n")
    
    #lista para almacenar los procesos del proceso 2
    procesos_p2 = []
    #se hace un for para crear 10 procesos que calculen las medias
    for i in range(1, 11):
        #se crea el nombre del fichero
        nombre_fichero = f"Alumno{i}.txt"
        #se crea el nombre del alumno
        nombre_alumno = f"Alumno{i}"
        #se crea el proceso
        p = Process(target=calcular_media, args=(nombre_fichero, nombre_alumno))
        #se añade el proceso a la lista
        procesos_p2.append(p)
        #se inicia el proceso
        p.start()
    
    #se espera a que terminen todos los procesos del proceso 2
    for p in procesos_p2:
        p.join()
    
    print("Se han calculado todas las medias\n")
    
    #se lanza el proceso 3 para obtener la nota máxima
    p3 = Process(target=obtener_nota_maxima)
    p3.start()
    p3.join()
    
    #se calcula el tiempo final
    fin = time.perf_counter()
    #se calcula el tiempo total
    tiempo_total = fin - inicio
    #se imprime el tiempo total
    print(f"\nTiempo con bucles for: {tiempo_total} segundos")
    
    #OPCIÓN 2: USANDO POOL
    print("\n\n=== OPCIÓN 2: USANDO POOL ===\n")
    
    #se borra el fichero medias.txt para empezar de cero
    open('medias.txt', 'w').close()
    
    #se mide el tiempo que tardan en ejecutarse los procesos
    inicio2 = time.perf_counter()
    
    #se crea una lista con los nombres de los ficheros
    ficheros_p1 = [f"Alumno{i}.txt" for i in range(1, 11)]
    
    #se usa Pool para generar las notas de forma concurrente
    with Pool(processes=10) as pool:
        pool.map(generar_notas, ficheros_p1)
    
    print("Se han generado todos los ficheros de notas\n")
    
    #se crea una lista con tuplas de (fichero, nombre_alumno)
    datos_p2 = [(f"Alumno{i}.txt", f"Alumno{i}") for i in range(1, 11)]
    
    #se usa Pool para calcular las medias de forma concurrente
    with Pool(processes=10) as pool:
        pool.starmap(calcular_media, datos_p2)
    
    print("Se han calculado todas las medias\n")
    
    #se lanza el proceso 3 para obtener la nota máxima
    obtener_nota_maxima()
    
    #se calcula el tiempo final
    fin2 = time.perf_counter()
    #se calcula el tiempo total
    tiempo_total2 = fin2 - inicio2
    #se imprime el tiempo total
    print(f"\nTiempo con Pool: {tiempo_total2} segundos")