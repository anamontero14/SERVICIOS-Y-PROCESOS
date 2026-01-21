from multiprocessing import Process
import time

"""
Crea un proceso que cuente las vocales de un fichero de texto. Para ello crea
una función que reciba una vocal y devuelva cuántas veces aparece en un
fichero. Lanza el proceso de forma paralela para las 5 vocales. Tras lanzarse
se imprimirá el resultado por pantalla.
"""

#función que cuenta cuántas veces aparece una vocal en el fichero
def contar_vocal(vocal):
    #variable que almacena el contador de veces que aparece
    contador = 0
    #se abre el fichero en modo lectura
    with open("texto.txt", "r", encoding="utf-8") as f:
        #se hace un for para leer todas las líneas del fichero
        for linea in f:
            #se hace otro for para recorrer cada caracter de la línea
            for caracter in linea.lower():
                #si el caracter es igual a la vocal se suma 1 al contador
                if caracter == vocal:
                    contador += 1
    #se imprime el resultado
    print(f"La vocal '{vocal}' aparece {contador} veces")

if __name__ == '__main__':
    #lista con las 5 vocales
    vocales = ['a', 'e', 'i', 'o', 'u']
    #lista para almacenar los procesos
    procesos = []
    
    #se mide el tiempo que tardan en ejecutarse los procesos
    inicio = time.perf_counter()
    
    #se hace un for para crear un proceso por cada vocal
    for vocal in vocales:
        #se crea el proceso
        p = Process(target=contar_vocal, args=(vocal,))
        #se añade el proceso a la lista
        procesos.append(p)
        #se inicia el proceso
        p.start()
    
    #se hace un for para esperar a que terminen todos los procesos
    for p in procesos:
        p.join()
    
    #se calcula el tiempo final
    fin = time.perf_counter()
    #se calcula el tiempo total
    tiempo_total = fin - inicio
    #se imprime el mensaje final
    print(f"\nSe han terminado los procesos y han tardado {tiempo_total} segundos")