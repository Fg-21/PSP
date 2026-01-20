from multiprocessing import Process, Queue
import os


def leer_numeros(fichero: str, cola: Queue):
    """
    Proceso 1: Lectura de números desde fichero
    - Lee cada línea del fichero
    - Convierte a entero y añade a la cola
    - Envía None al finalizar (señal de terminación)
    """
    print(f"[Lector] Leyendo fichero: {fichero}")

    try:
        with open(fichero, 'r') as f:
            for linea in f:
                numero = int(linea.strip())
                cola.put(numero)
                print(f"[Lector] Enviado: {numero}")

        cola.put(None)  # Señal de fin
        print("[Lector] Lectura completada")

    except FileNotFoundError:
        print(f"[Lector] Error: Fichero no encontrado")
        cola.put(None)


def calcular_suma(numero: int) -> int:
    """
    Calcula la suma de 1 hasta numero usando la fórmula matemática
    Fórmula: n * (n + 1) / 2
    """
    return numero * (numero + 1) // 2


def sumar_numeros(cola: Queue):
    """
    Proceso 2: Procesamiento de números
    - Lee números de la cola
    - Calcula la suma de 1 hasta ese número
    - Termina al recibir None
    """
    print("[Sumador] Esperando números...")

    numero = cola.get()

    # Procesar números hasta recibir None
    while numero is not None:
        print(f"[Sumador] Procesando: {numero}")

        total = calcular_suma(numero)
        print(f"[Sumador] Suma hasta {numero} = {total}")

        numero = cola.get()  # Leer siguiente número

    print("[Sumador] Finalizado")

if __name__ == "__main__":
    """
    Programa principal:
    1. Crea una Queue para comunicación entre procesos
    2. Lanza proceso lector (lee fichero y envía a Queue)
    3. Lanza proceso sumador (recibe de Queue y procesa)
    4. Espera a que ambos terminen
    """

    # Configuración
    cola = Queue()
    fichero = os.path.join("Ejercicios", "numeros.txt")

    print("=" * 60)
    print("EJERCICIO 3: Comunicación con Queue")
    print("=" * 60)

    # Crear procesos
    lector = Process(target=leer_numeros, args=(fichero, cola))
    sumador = Process(target=sumar_numeros, args=(cola,))

    # Ejecutar procesos concurrentemente
    lector.start()
    sumador.start()

    # Esperar finalización
    lector.join()
    sumador.join()

    print("=" * 60)
    print("Procesos finalizados")
    print("=" * 60)