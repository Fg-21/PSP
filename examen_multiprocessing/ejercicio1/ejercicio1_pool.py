from multiprocessing import Pool
import random
import os


def generar_temperaturas(dia):
    """Genera temperaturas para un día específico"""
    nombre_fichero = f"{dia:02d}-12.txt"
    
    with open(nombre_fichero, 'w') as f:
        for _ in range(24):
            temperatura = random.uniform(0, 20)
            f.write(f"{temperatura:.2f}\n")
    
    return f"✓ Día {dia} generado"


def calcular_maxima(dia):
    """Calcula la temperatura máxima de un día"""
    nombre_fichero = f"{dia:02d}-12.txt"
    fecha = f"{dia:02d}-12"
    
    with open(nombre_fichero, 'r') as f:
        temperaturas = [float(linea.strip()) for linea in f]
    
    temperatura_maxima = max(temperaturas)
    
    with open("maximas.txt", 'a') as f:
        f.write(f"{fecha}:{temperatura_maxima:.2f}\n")
    
    return f"✓ Máxima día {dia}: {temperatura_maxima:.2f}°C"


def calcular_minima(dia):
    """Calcula la temperatura mínima de un día"""
    nombre_fichero = f"{dia:02d}-12.txt"
    fecha = f"{dia:02d}-12"
    
    with open(nombre_fichero, 'r') as f:
        temperaturas = [float(linea.strip()) for linea in f]
    
    temperatura_minima = min(temperaturas)
    
    with open("minimas.txt", 'a') as f:
        f.write(f"{fecha}:{temperatura_minima:.2f}\n")
    
    return f"✓ Mínima día {dia}: {temperatura_minima:.2f}°C"


def main():    
    # Limpiar archivos anteriores
    for archivo in ["maximas.txt", "minimas.txt"]:
        if os.path.exists(archivo):
            os.remove(archivo)
    
    print("=" * 70)
    print(" EJERCICIO 1 CON Pool() - Versión Alternativa")
    print("=" * 70)
    
    # Lista de días (1 a 31)
    dias = list(range(1, 32))
    
    # ========================================================================
    # FASE 1: Generar temperaturas usando Pool
    # ========================================================================
    print("\nFASE 1: Generando temperaturas...")
    print("-" * 70)
    
    # Con Pool indicamos que vamos a tener 3 procesos en paralelo
    # (ajustar según el número de CPUs disponibles)
    with Pool(processes=8) as pool:
        # map() aplica generar_temperaturas a cada día
        # Devuelve una lista con los resultados
        resultados = pool.map(generar_temperaturas, dias)
        
        # Mostrar algunos resultados
        for resultado in resultados[:5]:
            print(resultado)
        print(f"... ({len(resultados)} días procesados)")
    
    print("\nFase 1 completada")
    
    # ========================================================================
    # FASE 2: Calcular máximas y mínimas usando Pool
    # ========================================================================
    print("\nFASE 2: Calculando máximas y mínimas...")
    print("-" * 70)
    
    with Pool(processes=8) as pool:
        # Calcular máximas en paralelo
        resultados_max = pool.map(calcular_maxima, dias)
        
        # Calcular mínimas en paralelo
        resultados_min = pool.map(calcular_minima, dias)
    
    print("\nFase 2 completada")
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    print("\n" + "=" * 70)
    print(" PROCESO COMPLETADO CON Pool()")
    print("=" * 70)
    print("\nVentajas de Pool():")
    print("  • Código más conciso que Process individual")
    print("  • Gestión automática del pool de procesos")
    print("  • map() distribuye el trabajo automáticamente")
    print("  • Ideal para aplicar la misma función a múltiples datos")
    print("=" * 70)


if __name__ == "__main__":
    main()
