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

from multiprocessing import Process, Queue

def leer_fichero(nombre_fichero, cola):
    """
    Lee el fichero y mete en la cola pares de números
    """
    with open(nombre_fichero, 'r') as f:
        for linea in f:
            num1, num2 = map(int, linea.split())
            cola.put((num1, num2))

    # Señal de fin (importante)
    cola.put(None)


def sumar_valores(cola):
    """
    Lee pares de números desde la cola y muestra la suma
    """
    while True:
        datos = cola.get()

        if datos is None:
            break

        numero1, numero2 = datos

        if numero1 > numero2:
            mayor = numero1
            menor = numero2
        else:
            mayor = numero2
            menor = numero1

        suma = sum(range(menor, mayor + 1))
        print(f"Suma entre {numero1} y {numero2}: {suma}")


if __name__ == '__main__':
    cola = Queue()

    p_lector = Process(target=leer_fichero, args=("numeros.txt", cola))
    p_sumador = Process(target=sumar_valores, args=(cola,))

    p_lector.start()
    p_sumador.start()

    p_lector.join()
    p_sumador.join()

    print("Todos los procesos han terminado")