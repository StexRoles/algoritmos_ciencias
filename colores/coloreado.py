def es_seguro(grafo, nodo, color_actual, colores):
    """
    Verifica si es seguro asignar `color_actual` al `nodo`.
    Un color es seguro si ninguno de los vecinos del nodo tiene ese mismo color.

    Args:
        grafo (dict): El grafo en representación de lista de adyacencia.
        nodo: El nodo al que se le quiere asignar un color.
        color_actual (int): El color que se está intentando asignar.
        colores (dict): Un diccionario que mapea nodos a sus colores ya asignados.

    Returns:
        bool: True si es seguro colorear, False en caso contrario.
    """
    for vecino in grafo.get(nodo, []):
        if colores.get(vecino) == color_actual:
            return False
    return True

def resolver_coloreado(grafo, m, nodos, colores, nodo_idx):
    """
    Función recursiva de backtracking para resolver el problema de coloreado.

    Args:
        grafo (dict): El grafo.
        m (int): El número de colores que se están probando actualmente.
        nodos (list): La lista de nodos del grafo.
        colores (dict): Mapeo de nodos a colores.
        nodo_idx (int): El índice del nodo que estamos intentando colorear.

    Returns:
        bool: True si el grafo se puede colorear con m colores, False en caso contrario.
    """
    # Caso base: si todos los nodos tienen un color, hemos encontrado una solución.
    if nodo_idx == len(nodos):
        return True

    nodo_actual = nodos[nodo_idx]

    # Probar cada uno de los m colores para el nodo actual.
    for c in range(1, m + 1):
        if es_seguro(grafo, nodo_actual, c, colores):
            # Asignar el color
            colores[nodo_actual] = c

            # Llamada recursiva para el siguiente nodo.
            if resolver_coloreado(grafo, m, nodos, colores, nodo_idx + 1):
                return True

            # Backtracking: si la asignación no llevó a una solución, la deshacemos.
            colores[nodo_actual] = 0
    
    # Si ningún color funciona para este nodo, regresamos False.
    return False

def encontrar_numero_cromatico(grafo):
    """
    Encuentra el número mínimo de colores necesarios para colorear el grafo.

    Args:
        grafo (dict): El grafo en representación de lista de adyacencia.

    Returns:
        int: El número cromático del grafo.
    """
    if not grafo:
        return 0
        
    nodos = list(grafo.keys())
    num_nodos = len(nodos)
    
    # Probar colorear con 1, 2, 3, ..., num_nodos colores.
    # El primer 'm' que funcione es el número cromático.
    for m in range(1, num_nodos + 2):
        colores = {nodo: 0 for nodo in nodos} # 0 significa sin color
        if resolver_coloreado(grafo, m, nodos, colores, 0):
            print(f"\nColoreado final encontrado con {m} colores:")
            print(colores)
            return m
            
    return num_nodos # Por si algo falla, aunque no debería llegar aquí.

# --- Ejemplo de Uso ---
if __name__ == "__main__":
    # Grafo de ejemplo (un pentágono con un nodo central conectado a todos)
    # Visualmente: Un 'pastel' de 5 rebanadas. Se necesitan 3 colores.
    grafo_ejemplo_1 = {
        'A': ['B', 'E', 'F'],
        'B': ['A', 'C', 'F'],
        'C': ['B', 'D', 'F'],
        'D': ['C', 'E', 'F'],
        'E': ['D', 'A', 'F'],
        'F': ['A', 'B', 'C', 'D', 'E']
    }
    
    print("Analizando Grafo 1:")
    min_colores = encontrar_numero_cromatico(grafo_ejemplo_1)
    print(f"--> El número mínimo de colores necesarios es: {min_colores}")
    
    print("-" * 30)
    
    # Grafo de ejemplo 2 (el del principio de la explicación)
    # Se necesitan 3 colores.
    grafo_ejemplo_2 = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['A', 'B', 'C']
    }
    
    print("Analizando Grafo 2:")
    min_colores_2 = encontrar_numero_cromatico(grafo_ejemplo_2)
    print(f"--> El número mínimo de colores necesarios es: {min_colores_2}")

    print("-" * 30)

    # Grafo de ejemplo 3 (lineal, un camino)
    # Se necesitan 2 colores.
    grafo_ejemplo_3 = {
        'A': ['B'],
        'B': ['A', 'C'],
        'C': ['B', 'D'],
        'D': ['C']
    }

    print("Analizando Grafo 3:")
    min_colores_3 = encontrar_numero_cromatico(grafo_ejemplo_3)
    print(f"--> El número mínimo de colores necesarios es: {min_colores_3}")

    print("-" * 30)

    # Grafo de ejemplo 4 (K5, un grafo no plano)
    # Se necesitan 5 colores.
    grafo_k5 = {
        'A': ['B', 'C', 'D', 'E'],
        'B': ['A', 'C', 'D', 'E'],
        'C': ['A', 'B', 'D', 'E'],
        'D': ['A', 'B', 'C', 'E'],
        'E': ['A', 'B', 'C', 'D']
    }

    print("Analizando Grafo K5 (no plano):")
    min_colores_k5 = encontrar_numero_cromatico(grafo_k5)
    print(f"--> El número mínimo de colores necesarios es: {min_colores_k5}")