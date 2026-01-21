from multiprocessing import Process, Queue
import random
import time

"""
En este ejercicio vamos a lanzar varios procesos, cuyas entradas y salidas
están enlazadas. Para ello tendremos tres procesos distintos:
● Proceso 1: Va a generar 10 direcciones IP de forma aleatoria y se las
  enviará al Proceso 2.
● Proceso 2: Va a leer las direcciones IP que recibe del Proceso 1 y va
  a enviar al Proceso 3 únicamente aquellas que pertenezcan a las
  clases A, B o C.
● Proceso 3: Va a leer las direcciones IP procedentes del Proceso 2 (no
  se sabe qué número llegarán) y va a imprimir por consola la dirección
  IP y a continuación la clase a la que pertenece.
"""

#función que genera 10 IPs aleatorias y las mete en la cola
def generar_ips(cola):
    #se hace un for para generar 10 IPs
    for i in range(10):
        #se generan los 4 octetos de la IP de forma aleatoria
        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        #se imprime la IP generada
        print(f"IP generada: {ip}")
        #se mete la IP en la cola
        cola.put(ip)
    #se mete None en la cola para indicar que ha terminado
    cola.put(None)

#función que filtra las IPs de clase A, B o C y las envía al proceso 3
def filtrar_ips(cola_entrada, cola_salida):
    #variable auxiliar para salir del bucle
    salir = True
    #mientras salir sea true
    while salir:
        #se obtiene la IP de la cola de entrada
        ip = cola_entrada.get()
        #si la IP es None se iguala salir a false
        if ip is None:
            salir = False
        else:
            #se parte la IP por el punto y se obtiene el primer octeto
            primer_octeto = int(ip.split('.')[0])
            #se comprueba si la IP es de clase A, B o C
            #clase A: primer octeto entre 1 y 126
            if 1 <= primer_octeto <= 126:
                cola_salida.put((ip, 'A'))
            #clase B: primer octeto entre 128 y 191
            elif 128 <= primer_octeto <= 191:
                cola_salida.put((ip, 'B'))
            #clase C: primer octeto entre 192 y 223
            elif 192 <= primer_octeto <= 223:
                cola_salida.put((ip, 'C'))
    #se mete None en la cola de salida para indicar que ha terminado
    cola_salida.put(None)

#función que imprime las IPs con su clase
def imprimir_ips(cola):
    #variable auxiliar para salir del bucle
    salir = True
    #mientras salir sea true
    while salir:
        #se obtiene el dato de la cola
        dato = cola.get()
        #si el dato es None se iguala salir a false
        if dato is None:
            salir = False
        else:
            #se obtiene la IP y la clase
            ip, clase = dato
            #se imprime la IP y su clase
            print(f"IP: {ip} - Clase: {clase}")

if __name__ == '__main__':
    #se crean las dos colas para la comunicación entre procesos
    cola1 = Queue()
    cola2 = Queue()
    
    #se crean los tres procesos
    p1 = Process(target=generar_ips, args=(cola1,))
    p2 = Process(target=filtrar_ips, args=(cola1, cola2))
    p3 = Process(target=imprimir_ips, args=(cola2,))
    
    #se mide el tiempo que tardan en ejecutarse los procesos
    inicio = time.perf_counter()
    
    #se inician los procesos en orden
    p1.start()
    p2.start()
    p3.start()
    
    #se espera a que terminen los procesos
    p1.join()
    p2.join()
    p3.join()
    
    #se calcula el tiempo final
    fin = time.perf_counter()
    #se calcula el tiempo total
    tiempo_total = fin - inicio
    #se imprime el mensaje final
    print(f"\nSe han terminado los procesos y han tardado {tiempo_total} segundos")