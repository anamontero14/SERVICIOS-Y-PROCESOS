from multiprocessing import Pipe, Process

"""
En este caso, vuelve a realizar la comunicación 
entre procesos pero usando tuberías (Pipe), de forma
que la función que se encarga de leer los números 
del fichero se los envíe (send) al proceso que se 
encarga de la suma. El proceso que suma los números
tiene que recibir (recv) un número y realizar la suma. 
Una vez que el proceso que lee el fichero termine de leer 
números en el fichero, debe enviar un None. El que 
recibe números dejará de realizar sumas cuando reciba un None.
"""

#función que se encarga de sumar todos los nº desde el 1 hasta el nº que se
#indica por parámetros
def sumar_numeros(conn):
    #variable que almacena el numero que se le manda
    numero = conn.recv()
    #variable que almacena la suma de todos los numeros
    suma_numeros = 0
    #se suma el numero que le llega
    suma_numeros += numero
    conn.close()


#función que se encarga de leer líneas de un fichero
def leer_numeros_fichero(conn):
    with open(r"C:\Users\ana.montero\Documents\GitHub\SERVICIOS-Y-PROCESOS\TEMA3\EJERCICIOS\numeros.txt", "r", encoding="utf-8") as f:
        for linea in f:
            numero = int(linea.strip())
            print(numero)
            conn.send(numero)
    conn.close

if __name__ == '__main__':

    left, right = Pipe()

    #se determinan los procesos
    p1 = Process(target=leer_numeros_fichero, args=(left,))
    p2 = Process(target=sumar_numeros, args=(right,))
    
    #se empiezan y terminan los procesos
    p1.start()
    p2.start()
    p1.join()
    
    p2.join()
    #el resultado final se iguala a lo que hay en la cola
    resultado_final = queue_resultado.get()
    #se muestra el resultado
    print("Se han terminado los procesos")
    print(f"La suma total de todos los numeros del fichero es: {resultado_final}")