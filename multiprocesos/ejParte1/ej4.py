from multiprocessing import Process, Pipe
import os


def leer_numeros(fichero: str, conexion):
    """
    Proceso 1: Lectura de números desde fichero
    - Lee cada línea del fichero
    - Envía números por el Pipe
    - Envía None al finalizar (señal de terminación)
    - Cierra su extremo del Pipe
    """
    print(f"[Lector] Leyendo fichero: {fichero}")

    try:
        with open(fichero, 'r') as f:
            for linea in f:
                numero = int(linea.strip())
                conexion.send(numero)
                print(f"[Lector] Enviado: {numero}")

        conexion.send(None)  # Señal de fin
        print("[Lector] Lectura completada")

    except FileNotFoundError:
        print(f"[Lector] Error: Fichero no encontrado")
        conexion.send(None)
    finally:
        conexion.close()


def calcular_suma(numero: int) -> int:
    """
    Calcula la suma de 1 hasta numero usando la fórmula matemática
    Fórmula: n * (n + 1) / 2
    """
    return numero * (numero + 1) // 2


def sumar_numeros(conexion):
    """
    Proceso 2: Procesamiento de números
    - Recibe números del Pipe
    - Calcula la suma de 1 hasta ese número
    - Termina al recibir None
    - Cierra su extremo del Pipe
    """
    print("[Sumador] Esperando números...")

    numero = conexion.recv()

    # Procesar números hasta recibir None
    while numero is not None:
        print(f"[Sumador] Procesando: {numero}")

        total = calcular_suma(numero)
        print(f"[Sumador] Suma hasta {numero} = {total}")

        numero = conexion.recv()  # Leer siguiente número

    print("[Sumador] Finalizado")
    conexion.close()


if __name__ == "__main__":
    """
    Programa principal:
    1. Crea un Pipe (tubería bidireccional) para comunicación
    2. Lanza proceso lector (envía por conn_envio)
    3. Lanza proceso sumador (recibe por conn_recepcion)
    4. Cierra conexiones en proceso principal
    5. Espera a que ambos procesos terminen
    """

    # Crear Pipe: retorna dos conexiones (extremos de la tubería)
    conn_envio, conn_recepcion = Pipe()

    fichero = os.path.join("Ejercicios", "numeros.txt")

    print("=" * 60)
    print("EJERCICIO 4: Comunicación con Pipe")
    print("=" * 60)

    # Crear procesos
    lector = Process(target=leer_numeros, args=(fichero, conn_envio))
    sumador = Process(target=sumar_numeros, args=(conn_recepcion,))

    # Ejecutar procesos concurrentemente
    lector.start()
    sumador.start()

    # Cerrar conexiones en proceso principal (buena práctica)
    conn_envio.close()
    conn_recepcion.close()

    # Esperar finalización
    lector.join()
    sumador.join()

    print("=" * 60)
    print("Procesos finalizados")
    print("=" * 60)