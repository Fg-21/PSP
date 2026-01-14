from multiprocessing import Process
import os
import time

def sumaHastaNumero(numero: int) -> None:
    i = 1
    result = 0
    for i in range (numero + 1):
        result = result + i
    print (result)       

def main():
    pass

if __name__ == '__main__':
    
    p = Process(target=sumaHastaNumero, args=())
    p2 = Process(target=sumaHastaNumero, args=(7,))

    p.start()
    p2.start()
    p.join()
    p2.join()

    print("Todos los procesos han terminado")

    main()