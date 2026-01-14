from multiprocessing import Pool
import time
"""
Modifica el ejercicio anterior para que el 
programa principal use un Pool para lanzar 
varios procesos de forma concurrente. Cambia 
el valor del número de procesos y compara los 
tiempos que tarda en ejecutarse en los distintos casos.
"""

#función que se encarga de sumar todos los nº desde el 1 hasta el nº que se
#indica por parámetros
def sumarNumeros(numero):
    sumaDeNumeros = 0
    for i in range(numero+1):
        sumaDeNumeros += i
    return sumaDeNumeros

#se crea el main
if __name__ == '__main__':
    #se determinan en el pool que se van a ejecutar 3 procesos
    with Pool(processes=3) as pool:
        #me creo una lista con varios numeros
        numeros = [1, 2, 3, 4, 5, 6]
        inicio = time.perf_counter()
        #la variable resultados será igualada al resultado de todos los procesos
        result = pool.map(sumarNumeros, numeros)
        fin = time.perf_counter()
    #se calculan los procesos
    tiempo_procesos = fin-inicio
    #se printean todos los procesos
    print(f"Resultados: {result}. Tiempo: {tiempo_procesos} segundos")