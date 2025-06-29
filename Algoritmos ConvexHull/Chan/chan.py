import random
import matplotlib.pyplot as plt
from functools import cmp_to_key

# 1. Generar 500 puntos aleatorios y guardarlos en un archivo
def generar_puntos(n, filename):
    with open(filename, 'w') as f:
        for _ in range(n):
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            f.write(f"{x} {y}\n")

# 2. Leer los puntos desde el archivo
def leer_puntos(filename):
    puntos = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(float, line.split())
            puntos.append((x, y))
    return puntos

# Funciones auxiliares para geometría computacional
def orientacion(p, q, r):
    """Determina la orientación del triplet (p, q, r).
    Devuelve:
        >0 si es antihorario (giro izquierda)
        <0 si es horario (giro derecha)
        =0 si son colineales
    """
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

def distancia_cuadrada(p, q):
    """Calcula la distancia cuadrada entre dos puntos."""
    return (q[0] - p[0])**2 + (q[1] - p[1])**2

# Algoritmo de Graham Scan para subconjuntos
def graham_scan(puntos):
    if len(puntos) <= 3:
        return puntos[:]
    
    # Encontrar el punto pivote (más bajo, más a la izquierda)
    pivote = min(puntos, key=lambda p: (p[1], p[0]))
    
    # Función de comparación para ordenar por ángulo polar
    def comparar(p1, p2):
        o = orientacion(pivote, p1, p2)
        if o == 0:
            return distancia_cuadrada(pivote, p2) - distancia_cuadrada(pivote, p1)
        return -1 if o > 0 else 1
    
    # Ordenar puntos (excepto el pivote)
    ordenados = sorted(puntos, key=cmp_to_key(comparar))
    ordenados.remove(pivote)
    ordenados.insert(0, pivote)
    
    # Construir la envolvente convexa
    stack = [ordenados[0], ordenados[1]]
    for i in range(2, len(ordenados)):
        while len(stack) >= 2 and orientacion(stack[-2], stack[-1], ordenados[i]) <= 0:
            stack.pop()
        stack.append(ordenados[i])
    
    return stack

# Algoritmo de Chan para envolvente convexa
def chan(puntos):
    n = len(puntos)
    if n < 3:
        return puntos
    
    # Encontrar el punto inicial (más abajo, más a la izquierda)
    p0 = min(puntos, key=lambda p: (p[1], p[0]))
    envolvente = [p0]
    
    t = 1
    while True:
        m = min(n, 2**(2**t))  # Tamaño máximo de grupo
        k = (n + m - 1) // m   # Número de grupos
        
        # Dividir puntos en grupos
        grupos = [puntos[i*m : (i+1)*m] for i in range(k)]
        
        # Calcular envolventes parciales
        envolventes_grupo = [graham_scan(grupo) for grupo in grupos]
        
        # Intentar construir la envolvente global
        for _ in range(m):
            candidatos = []
            actual = envolvente[-1]
            
            # Encontrar candidatos tangentes en cada envolvente parcial
            for env in envolventes_grupo:
                mejor = env[0]
                for punto in env[1:]:
                    o = orientacion(actual, mejor, punto)
                    # Preferir giro antihorario o colineal más lejano
                    if o > 0 or (o == 0 and distancia_cuadrada(actual, punto) > distancia_cuadrada(actual, mejor)):
                        mejor = punto
                candidatos.append(mejor)
            
            # Seleccionar el siguiente punto óptimo
            siguiente = candidatos[0]
            for cand in candidatos[1:]:
                o = orientacion(actual, siguiente, cand)
                if o > 0 or (o == 0 and distancia_cuadrada(actual, cand) > distancia_cuadrada(actual, siguiente)):
                    siguiente = cand
            
            # Verificar si se completó la envolvente
            if siguiente == p0:
                return envolvente
            envolvente.append(siguiente)
        
        t += 1
        if 2**(2**t) > n * n:  # Límite para evitar bucles infinitos
            return envolvente

# Función para imprimir los puntos de la envolvente convexa
def imprimir_envolvente(envolvente):
    print("\nPuntos de la envolvente convexa:")
    print("--------------------------------")
    for i, punto in enumerate(envolvente):
        print(f"Punto {i+1}: ({punto[0]:.6f}, {punto[1]:.6f})")
    print(f"Total de puntos en la envolvente: {len(envolvente)}")

# Visualizar resultados
def visualizar(puntos, envolvente):
    plt.figure(figsize=(10, 8))
    
    # Dibujar todos los puntos
    x = [p[0] for p in puntos]
    y = [p[1] for p in puntos]
    plt.scatter(x, y, color='blue', alpha=0.6, label='Puntos')
    
    # Dibujar la envolvente convexa
    if envolvente:
        envolvente_cerrada = envolvente + [envolvente[0]]  # Cerrar el polígono
        ex = [p[0] for p in envolvente_cerrada]
        ey = [p[1] for p in envolvente_cerrada]
        plt.plot(ex, ey, 'r-', linewidth=2, label='Envolvente convexa')
        plt.plot(ex, ey, 'ro', markersize=5)
        
        # Marcar los puntos de la envolvente con números
        for i, (x, y) in enumerate(envolvente):
            plt.text(x, y, str(i+1), fontsize=12, ha='center', va='bottom', color='darkred')
    
    plt.title('Envolvente Convexa (Algoritmo de Chan)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

# Ejecución principal
if __name__ == "__main__":
    # Configuración
    NUM_PUNTOS = 500
    ARCHIVO = "Algoritmos ConvexHull\Chan\puntos.txt"
    
    # Generar y guardar puntos
    generar_puntos(NUM_PUNTOS, ARCHIVO)
    print(f"Se generaron {NUM_PUNTOS} puntos en '{ARCHIVO}'")
    
    # Leer puntos
    puntos = leer_puntos(ARCHIVO)
    
    # Calcular envolvente convexa
    print("Calculando envolvente convexa con algoritmo de Chan...")
    envolvente = chan(puntos)
    
    # Imprimir puntos de la envolvente
    imprimir_envolvente(envolvente)
    
    # Visualizar resultados
    print("\nMostrando visualización...")
    visualizar(puntos, envolvente)