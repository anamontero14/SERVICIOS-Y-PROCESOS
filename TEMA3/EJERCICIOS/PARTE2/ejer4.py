from multiprocessing import Process, Pipe
import time

"""
Para realizar este ejercicio es necesario que definas 2 procesos distintos y un
Main:
● Proceso 1: Recibe como parámetros una ruta de fichero y un año. El
  proceso leerá el fichero el cual almacena en cada línea la información
  de una película: nombre y año de estreno separados por punto y
  coma (;).
  Debe enviar al siguiente proceso únicamente aquellas películas que se
  hayan estrenado en el año introducido por parámetro.
● Proceso 2: Recibirá un número indeterminado de películas y debe
  almacenarlas en un fichero de nombre peliculasXXXX, donde XXXX es
  el año de estreno de las películas.
● Main: Pide al usuario que introduzca un año por teclado, debe ser
  menor al actual. También solicitará la ruta al fichero donde se
  encuentran almacenadas las películas.
"""

#función que lee el fichero de películas y filtra por año
def filtrar_peliculas(ruta_fichero, año, conexion):
    #se abre el fichero en modo lectura
    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        #se hace un for para leer todas las líneas del fichero
        for linea in f:
            #se elimina el salto de línea
            linea = linea.strip()
            #si la línea no está vacía
            if linea:
                #se parte la línea por el punto y coma
                datos = linea.split(';')
                #se obtiene el nombre de la película
                nombre_pelicula = datos[0]
                #se obtiene el año de la película
                año_pelicula = int(datos[1])
                #si el año de la película coincide con el año buscado
                if año_pelicula == año:
                    #se envía la película por la tubería
                    conexion.send((nombre_pelicula, año_pelicula))
    #se envía None para indicar que ha terminado
    conexion.send(None)
    #se cierra la conexión
    conexion.close()

#función que recibe las películas y las guarda en un fichero
def guardar_peliculas(conexion, año):
    #se crea el nombre del fichero con el año
    nombre_fichero = rf"C:\Users\ana.montero\Documents\GitHub\SERVICIOS-Y-PROCESOS\TEMA3\EJERCICIOS\PARTE2\peliculas{año}.txt"
    #se abre el fichero en modo escritura
    with open(nombre_fichero, 'w', encoding='utf-8') as f:
        #variable auxiliar para salir del bucle
        salir = True
        #mientras salir sea true
        while salir:
            #se recibe la película de la tubería
            dato = conexion.recv()
            #si el dato es None se iguala salir a false
            if dato is None:
                salir = False
            else:
                #se obtiene el nombre y el año de la película
                nombre, año_pelicula = dato
                #se escribe la película en el fichero
                f.write(f"{nombre};{año_pelicula}\n")
                #se imprime el mensaje
                print(f"Película guardada: {nombre} ({año_pelicula})")
    #se cierra la conexión
    conexion.close()
    #se imprime el mensaje final
    print(f"\nPelículas guardadas en el fichero {nombre_fichero}")

if __name__ == '__main__':
    #se pide al usuario que introduzca un año
    año = int(input("Introduce un año (menor al actual): "))
    #ruta del fichero de películas
    ruta_fichero = r"C:\Users\ana.montero\Documents\GitHub\SERVICIOS-Y-PROCESOS\TEMA3\EJERCICIOS\PARTE2\peliculas.txt"
    
    #se mide el tiempo que tardan en ejecutarse los procesos
    inicio = time.perf_counter()
    
    #se crea la tubería para la comunicación entre procesos
    conn_padre, conn_hijo = Pipe()
    
    #se crean los dos procesos
    p1 = Process(target=filtrar_peliculas, args=(ruta_fichero, año, conn_hijo))
    p2 = Process(target=guardar_peliculas, args=(conn_padre, año))
    
    #se inician los procesos
    p1.start()
    p2.start()
    
    #se espera a que terminen los procesos
    p1.join()
    p2.join()
    
    #se calcula el tiempo final
    fin = time.perf_counter()
    #se calcula el tiempo total
    tiempo_total = fin - inicio
    #se imprime el tiempo total
    print(f"\nSe han terminado los procesos y han tardado {tiempo_total} segundos")