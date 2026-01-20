from multiprocessing import Pool

def sumar_valores(numero1, numero2):
    suma_total = 0

    if numero1 > numero2:
        numeroMayor = numero1
        numeroMenor = numero2
    else:
        numeroMayor = numero2
        numeroMenor = numero1

    suma_total += numeroMenor

    for num in range(numeroMenor, numeroMayor + 1):
        suma_total += num

    print(f"Suma entre {numero1} y {numero2}: {suma_total}")
    return suma_total


if __name__ == '__main__':
    valores = [
        (1, 5),
        (10, 3),
        (7, 7)
    ]

    with Pool(processes=3) as pool:
        resultados = pool.starmap(sumar_valores, valores)

    print("Todos los procesos han terminado")
    print("Resultados:", resultados)
