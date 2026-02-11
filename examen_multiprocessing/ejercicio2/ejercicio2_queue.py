from multiprocessing import Process, Queue


def proceso1_filtrar_departamento(departamento, cola_salida):
    try:
        with open("salarios.txt", 'r', encoding='utf-8') as f:
            contador = 0
            
            for linea in f:
                partes = linea.strip().split(';')
                
                if len(partes) == 4 and partes[3] == departamento:
                    # Poner en la cola: Nombre;Apellido;Salario
                    datos = f"{partes[0]};{partes[1]};{partes[2]}"
                    cola_salida.put(datos)  # put() inserta en la cola
                    contador += 1
        
        # Señal de fin (None al final)
        cola_salida.put(None)
        
        print(f"✓ Proceso 1: {contador} empleados del departamento '{departamento}' enviados")
    
    except IOError as e:
        print(f"✗ Error en Proceso 1: {e}")
        cola_salida.put(None)


def proceso2_filtrar_salario(salario_minimo, cola_entrada, cola_salida):
    try:
        contador = 0
        
        while True:
            # get() obtiene el siguiente elemento de la cola
            # Bloquea hasta que haya un elemento disponible
            datos = cola_entrada.get()
            
            # Si recibimos None, terminamos
            if datos is None:
                break
            
            partes = datos.split(';')
            
            if len(partes) == 3:
                salario = float(partes[2])
                
                if salario >= salario_minimo:
                    cola_salida.put(datos)
                    contador += 1
        
        # Señal de fin
        cola_salida.put(None)
        
        print(f"✓ Proceso 2: {contador} empleados con salario >= {salario_minimo} enviados")
    
    except Exception as e:
        print(f"✗ Error en Proceso 2: {e}")
        cola_salida.put(None)


def proceso3_escribir_resultados(cola_entrada):
    try:
        contador = 0
        
        with open("empleados.txt", 'w') as f:
            while True:
                # Obtener elemento de la cola
                datos = cola_entrada.get()
                
                if datos is None:
                    break
                
                partes = datos.split(';')
                
                if len(partes) == 3:
                    nombre = partes[0]
                    apellido = partes[1]
                    salario = partes[2]
                    
                    # Formato: Apellido Nombre, Salario
                    f.write(f"{apellido} {nombre}, {salario}\n")
                    contador += 1
        
        print(f"✓ Proceso 3: {contador} empleados escritos en empleados.txt")
    
    except Exception as e:
        print(f"✗ Error en Proceso 3: {e}")


def main():
    
    print("=" * 70)
    print(" EJERCICIO 2 CON Queue() - Versión Alternativa")
    print("=" * 70)
    print()
    
    departamento = input("📝 Introduce el nombre del departamento: ").strip()
    salario_minimo = float(input("💰 Introduce el salario mínimo: ").strip())
    
    print("\n🔄 Procesando...")
    print("-" * 70)
    
    # ==================================================================
    # Crear las Queues para comunicación
    # ===========================================================
    # Queue() crea una cola FIFO (First In, First Out)
    # "el primero que llega, el primero que sale"
    
    cola1 = Queue()  # Entre Proceso1 y Proceso2
    cola2 = Queue()  # Entre Proceso2 y Proceso3
    
    # ==============================================================
    # Crear los procesos
    # ==================================================================
    
    p1 = Process(
        target=proceso1_filtrar_departamento,
        args=(departamento, cola1)
    )
    
    p2 = Process(
        target=proceso2_filtrar_salario,
        args=(salario_minimo, cola1, cola2)
    )
    
    p3 = Process(
        target=proceso3_escribir_resultados,
        args=(cola2,)
    )
    
    # ======================================================================
    # Iniciar y esperar
    # ===================================================================
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()
    
    # ======================================================================
    # Mostrar resultados
    # ========================================================================
    print("-" * 70)
    print("\nPROCESO COMPLETADO CON Queue()")
    print("\nResultado guardado en: empleados.txt")
    print("\nContenido:")
    print("-" * 70)
    
    try:
        with open("empleados.txt", 'r') as f:
            contenido = f.read()
            if contenido.strip():
                print(contenido)
            else:
                print("  (vacío - no se encontraron empleados con esos criterios)")
    except FileNotFoundError:
        print("  (no se generó el archivo)")
    
    print("\n" + "=" * 70)
    print(" Ventajas de Queue():")
    print("  • Comunicación segura entre procesos (thread-safe)")
    print("  • Patrón FIFO: First In, First Out")
    print("  • Más simple que Pipe() para múltiples prod/cons")
    print("  • Métodos simples: put() y get()")
    print("=" * 70)


if __name__ == "__main__":
    main()
