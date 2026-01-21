from multiprocessing import Process, Pipe

"""
En este caso, vuelve a realizar la comunicación entre procesos 
pero usando tuberías (Pipe), de forma que la función que se 
encarga de leer los números del fichero se los envíe (send) al 
proceso que los suma. El proceso que suma los números tiene que 
recibir (recv) los dos números y realizar la suma entre ellos.
"""

#funcion que se encarga de leer el fichero a la cual le entra
#el nombre del fichero y la conexion
def leer_fichero(nombre_fichero, conexion):
    #se abre el fichero en modo lectura
    with open(nombre_fichero, 'r') as f:
        #se hace un for para leer todas las lineas del fichero
        for linea in f:
            #se crean 2 variables que almacenarán respectivamente
            num1, num2 = map(int, linea.split())
            #y se envian ambos numeros por la tubería
            conexion.send((num1, num2))

    #señal de que ha acabado enviando None
    conexion.send(None)
    #y se cierra la conexión
    conexion.close()

#función que se encarga de sumar los valores a la cuál le entra
def sumar_valores(conexion):
    
    #función auxiliar para salir del bucle
    salir = True
    #mientras salir sea true se sigue el bucle
    while salir:
        #se reciben los datos de la tubería
        datos = conexion.recv()
        #si los datos son None iguala salir a false
        if datos is None:
            salir = False
            #si no es None entonces se igualan los dos números a las variables
        else:
            numero1, numero2 = datos

            if numero1 > numero2:
                mayor = numero1
                menor = numero2
            else:
                mayor = numero2
                menor = numero1

            suma = sum(range(menor, mayor + 1))
            print(f"Suma entre {numero1} y {numero2}: {suma}")

    conexion.close()


if __name__ == '__main__':
    #se crean las conexiones de la tubería
    conn_padre, conn_hijo = Pipe()
    #se crean los procesos
    p_lector = Process(target=leer_fichero, args=("numeros.txt", conn_hijo))
    p_sumador = Process(target=sumar_valores, args=(conn_padre,))
    #se inician los procesos
    p_lector.start()
    p_sumador.start()
    #se espera a que terminen los procesos
    p_lector.join()
    p_sumador.join()

    print("Todos los procesos han terminado")
