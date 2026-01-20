from multiprocessing import Pool

def square(numero):
    """Función que calcule el cuadrado del número"""
    return numero*numero


if __name__ == '__main__':
    with Pool(processes=3) as pool:
        numeros = [1, 2, 3, 4, 5, 6]
        result = pool.map(square, numeros)
    print("Resultados: ", result)