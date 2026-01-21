from multiprocessing import Pool

"""
Crea una función en Python que sea capaz de sumar todos 
los números comprendidos entre dos valores, incluyendo ambos 
valores y mostrar el resultado por pantalla. Estos valores se 
les pasará como argumentos. Hay que tener presente que el 
primer argumento puede ser mayor que el segundo, y habrá que 
tenerlo presente para realizar la suma.

Desde el programa principal crea varios procesos que ejecuten la 
función anterior. El programa principal debe imprimir un mensaje 
indicando que todos los procesos han terminado después de que los 
procesos hayan impreso el resultado.

Modifica el ejercicio anterior para usar un Pool para lanzar varios 
procesos de forma concurrente. Recuerda que al tener dos argumentos 
debes usar el método starmap en vez de map.
"""

#función que se encarga de sumar dos numeros
def sumar_valores(numero1, numero2):
    #variable que almacenará cuál de los 2 números es mayor
    numeroMayor = 0
    #variable que almacenará cuál de los 2 números es menor
    numeroMenor = 0
    #variable que almacenará la suma total de todos los números
    suma_total = 0

    #if para comprobar cuál de los dos números es mayor y cuál menor
    if numero1 > numero2:
        numeroMayor = numero1
        numeroMenor = numero2
    else:
        numeroMayor = numero2
        numeroMenor = numero1
    #se le suma el número menor
    suma_total += numeroMenor
    #se hace un bucle para ir sumando todos los números comprendidos
    for num in range(numeroMenor, numeroMayor + 1):
        suma_total += num
    #se anuncia el resultado
    print(f"Suma entre {numero1} y {numero2}: {suma_total}")
    return suma_total

if __name__ == '__main__':
    #diccionario de valores
    valores = [
        (1, 5),
        (10, 3),
        (7, 7)
    ]
    #pool de procesos para automatizarlo
    with Pool(processes=3) as pool:
        resultados = pool.starmap(sumar_valores, valores)
    
    print("Todos los procesos han terminado")
    print("Resultados:", resultados)
