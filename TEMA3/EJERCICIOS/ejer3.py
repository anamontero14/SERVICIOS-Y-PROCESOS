from multiprocessing import Queue
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
def sumar_numeros(numero):
    #variable inicializada a 0
    suma_numeros = 0
    #bucle for que llega hasta el numero introducido por parámetros + 1
    for i in range(numero+1):
        #se le suma el numero actual a la variable
        suma_numeros += i
    #se devuelve la variable antes inicializada
    return suma_numeros

#función que se encarga de leer líneas de un fichero
def leer_numeros_fichero():
    #lista que almacenará los números que contiene el fichero
    lista_numeros = []
    with open("archivo.txt", "r", encoding="utf-8") as f:
        for linea in f:
            print(linea.strip())

if __name__ == '__main__':
    queue = Queue()