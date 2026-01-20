from multiprocessing import Process, Pipe

def leer_fichero(nombre_fichero, conexion):
    """
    Lee el fichero y envía los pares de números por la tubería
    """
    with open(nombre_fichero, 'r') as f:
        for linea in f:
            num1, num2 = map(int, linea.split())
            conexion.send((num1, num2))

    # Señal de fin
    conexion.send(None)
    conexion.close()


def sumar_valores(conexion):
    """
    Recibe pares de números desde la tubería y realiza la suma
    """
    while True:
        datos = conexion.recv()

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

    conexion.close()


if __name__ == '__main__':
    conn_padre, conn_hijo = Pipe()

    p_lector = Process(target=leer_fichero, args=("numeros.txt", conn_hijo))
    p_sumador = Process(target=sumar_valores, args=(conn_padre,))

    p_lector.start()
    p_sumador.start()

    p_lector.join()
    p_sumador.join()

    print("Todos los procesos han terminado")
