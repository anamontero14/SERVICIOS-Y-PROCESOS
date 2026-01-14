from multiprocessing import Process
import time
"""
Crea una función en Python que sea capaz de sumar todos 
los números desde el 1 hasta un valor introducido por parámetro, 
incluyendo ambos valores y mostrar el resultado por pantalla.

Desde el programa principal crea varios procesos que ejecuten
la función anterior. El programa principal debe imprimir un 
mensaje indicando que todos los procesos han terminado después 
de que los procesos hayan impreso el resultado.
"""

#función que se encarga de sumar todos los nº desde el 1 hasta el nº que se
#indica por parámetros
def sumarNumeros(numero):
    sumaDeNumeros = 0
    for i in range(numero+1):
        sumaDeNumeros += i
    print(sumaDeNumeros)

if __name__ == '__main__':
    #queue = Queue()
    p1 = Process(target=sumarNumeros, args=(4,))
    p2 = Process(target=sumarNumeros, args=(7,))
    p3 = Process(target=sumarNumeros, args=(10,))
    p4 = Process(target=sumarNumeros, args=(2,))
    
    #se mide el tiempo que tardan en ejecutarse los procesos
    inicio = time.perf_counter()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p1.join()
    #queue.put(None)
    p2.join()
    p3.join()
    p4.join()
    fin = time.perf_counter()
    #se calcula el tiempo que tardan los procesos
    tiempo_proceso = fin - inicio
    print(f"Se han terminado los procesos y han tardado {tiempo_proceso} segundos")