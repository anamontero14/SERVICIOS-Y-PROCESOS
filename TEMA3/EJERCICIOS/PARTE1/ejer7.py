from multiprocessing import Process, Queue

"""
Realiza el ejercicio anterior pero esta vez va a 
haber otra función que lea los números de un fichero. 
En el fichero habrá dos números por línea separados por 
un espacio. En este caso, tienes que llevar a cabo una
comunicación entre los dos procesos utilizando colas (Queue), 
de forma que la función que se encarga de leer los números los 
guarde en la cola, y la función que realiza la suma, recibirá 
la cola y tomará de ahí los dos números.
"""

#función que se encarga de leer el fichero a la que le entra el NOMBRE del
#fichero y la cola
def leer_fichero(nombre_fichero, cola):
    #se abre el fichero con opción de lectura
    with open(nombre_fichero, 'r') as f:
        #se hace un for para leer todas las lineas del fichero
        for linea in f:
            #se crean 2 variables que almacenarán respectivamente
            #los números que haya en la línea partidos con el split
            num1, num2 = map(int, linea.split())
            #y se ponen ambos numeros a la cola
            cola.put((num1, num2))

    #al acabar se pone None a la cola para indicar que ha acabado
    cola.put(None)

#función que se encarga de sumar los valores a la cuál le entra la
#cola por parámetros
def sumar_valores(cola):
    #variable auxiliar que sirve para salir del bucle
    salir = True
    
    #mientras que salir sea true
    while salir:
        #se almacena el primer número que haya en la cola en la variable
        datos = cola.get()

        #si en la variable ha almacenado None iguala la variable salir
        #a false
        if datos is None:
            salir = False
        else:
            #si NO tiene None entonces iguala los dos primeros numeros a las variables
            numero1, numero2 = datos

            #se hace un if para comprobar cuál de los dos números es mayor y cuál menor
            if numero1 > numero2:
                numeroMayor = numero1
                numeroMenor = numero2
            else:
                numeroMayor = numero2
                numeroMenor = numero1
            #se hace la suma de los numeros y se igualan a la variable
            suma = sum(range(numeroMenor, numeroMayor + 1))
            #se anuncia el resultado
            print(f"Suma entre {numero1} y {numero2}: {suma}")


if __name__ == '__main__':
    #se crea la cola
    cola = Queue()

    #se crean los procesos
    p_lector = Process(target=leer_fichero, args=("numeros.txt", cola))
    p_sumador = Process(target=sumar_valores, args=(cola,))
    #se inician los procesos
    p_lector.start()
    p_sumador.start()
    #se espera a que terminen los procesos
    p_lector.join()
    p_sumador.join()
    #se le muestra al usuario que los procesos han terminado
    print("Todos los procesos han terminado")