from multiprocessing import Queue, Process
import time
"""
Realiza el ejercicio anterior pero esta vez va a haber 
otra función que lea los números de un fichero. En el 
fichero habrá un número por línea. En este caso, tienes que 
llevar a cabo una comunicación entre los dos procesos 
utilizando colas (Queue), de forma que la función que se encarga 
de leer los números los guarde en la cola, y la función que 
realiza la suma, recibirá la cola y tomará de ahí los números. 
La función que lee el fichero, una vez haya terminado de leer y 
de añadir elementos a la cola, debe añadir un objeto None para 
que el receptor sepa cuándo terminar de leer de la cola.
"""
#función que se encarga de sumar todos los nº desde el 1 hasta el nº que se
#indica por parámetros
def sumar_numeros(queue_entrada, queue_salida):
    salir = True
    #variable inicializada a 0
    suma_numeros = 0
    #mientras sea true
    while salir:
        #si lo siguiente que tiene la cola es nada
        if (queue_entrada.get() is None):
            #iguala la variable a false para poder salir del bucle
            salir = False
        #si la cola todavia tiene cosas
        else:
            #se suma lo que haya en la cola a la variable
            suma_numeros += queue_entrada.get()
    #y se le pone a la cola de salida
    queue_salida.put(suma_numeros)

#función que se encarga de leer líneas de un fichero
def leer_numeros_fichero(queue):
    with open(r"C:\Users\ana.montero\Documents\GitHub\SERVICIOS-Y-PROCESOS\TEMA3\EJERCICIOS\numeros.txt", "r", encoding="utf-8") as f:
        for linea in f:
            numero = int(linea.strip())
            print(numero)
            queue.put(numero)

if __name__ == '__main__':
    queue = Queue()
    #cola para obtener el resultado final
    queue_resultado = Queue()
    #se determinan los procesos
    p1 = Process(target=leer_numeros_fichero, args=(queue,))
    p2 = Process(target=sumar_numeros, args=(queue, queue_resultado))
    
    inicio = time.perf_counter()
    #se empiezan y terminan los procesos
    p1.start()
    p2.start()
    p1.join()
    queue.put(None)
    p2.join()
    fin = time.perf_counter()
    #el resultado final se iguala a lo que hay en la cola
    resultado_final = queue_resultado.get()
    #tiempo empleado en los procesos
    tiempo = fin - inicio
    #se muestra el resultado
    print("Se han terminado los procesos")
    print(f"La suma total de todos los numeros del fichero es: {resultado_final}")
    print(f"Y han tardado {tiempo} segundos")