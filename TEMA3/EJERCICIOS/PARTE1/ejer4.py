from multiprocessing import Pipe, Process

"""
En este caso, vuelve a realizar la comunicación entre 
procesos pero usando tuberías (Pipe), de forma que la 
función que se encarga de leer los números del fichero 
se los envíe (send) al proceso que se encarga de la suma. 
El proceso que suma los números tiene que recibir (recv) un 
número y realizar la suma. Una vez que el proceso que lee 
el fichero termine de leer números en el fichero, debe enviar 
un None. El que recibe números dejará de realizar sumas 
cuando reciba un None.
"""

def sumar_numeros(conn):

    salir = True

    suma_total = 0
    
    while salir:
        numero = conn.recv()
        
        if numero is None:
            print(f"\nSuma final: {suma_total}")
            conn.close()
            salir = False
        else:
            suma_total += numero
            print(f"Sumando: {numero}, Total parcial: {suma_total}")


def leer_numeros_fichero(conn):
    with open(r"C:\Users\USUARIO\Documents\GitHub\SERVICIOS-Y-PROCESOS\TEMA3\EJERCICIOS\numeros.txt", "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                numero = int(linea)
                conn.send(numero)
    
    # Enviar None para indicar que no hay más números
    conn.send(None)
    conn.close()

if __name__ == '__main__':
    receptor, emisor = Pipe()
    
    # Crear los procesos
    p_lector = Process(target=leer_numeros_fichero, args=(emisor,))
    p_sumador = Process(target=sumar_numeros, args=(receptor,))
    
    # Iniciar los procesos
    p_lector.start()
    p_sumador.start()
    
    receptor.close()
    emisor.close()
    
    # Esperar a que terminen
    p_lector.join()
    p_sumador.join()
    
    print("\nSe han terminado los procesos")