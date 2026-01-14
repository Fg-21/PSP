from multiprocessing import Pool
import os
import time

#Suma todos los numeros hasta el pasado por parámetros, inicio y final inclusive
def sumaHastaNumero(numero: int) -> int:
    i = 1
    result = 0
    for i in range (numero + 1):
        result = result + i
    return result

#Lee las lineas de un fichero y las devuelve añadiendo al final de la lista un None
def reader() -> int[int]:
    with open("ej3.txt", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        lineas.append(None)
    return lineas
            


def main():
    pass

if __name__ == '__main__':
    inicio = time.perf_counter()
    with Pool(processes=3) as pool:
        numeros = [2,48,63,25,5]
        results = pool.map(sumaHastaNumero, numeros)

    fin = time.perf_counter()
    time_result = fin-inicio
    print(f"Todos los procesos han terminado: {results}")
    print(f"Tiempo de ejecución: {time_result}")

    main()