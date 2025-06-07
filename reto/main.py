from collections import defaultdict

listaAdyacencia = defaultdict(list)

def actualizar_capacidad(u, v, delta):
    for vecino in listaAdyacencia[u]:
        if vecino[0] == v:
            vecino[1] += delta
            if vecino[1] == 0:
                listaAdyacencia[u].remove(vecino)
            return True
    # Si no existe la arista, la creamos (esto es para la arista residual)
    if delta > 0:
        listaAdyacencia[u].append([v, delta])
    return False

def dfs(nodo, nodoFinal, visitados):
    if nodo == nodoFinal:
        return [nodo]
    
    if nodo not in visitados:
        visitados.add(nodo)
        for vecino, capacidad in listaAdyacencia[nodo]:
            if capacidad > 0:
                camino = dfs(vecino, nodoFinal, visitados)
                if camino:
                    return [nodo] + camino
    return []

# Leer archivo de entrada
with open('reto\entrada2.txt', 'r') as archivo:
    lineas = archivo.read().strip().split('\n')

i = int(lineas[0])  # Número de nodos
j = int(lineas[1])  # Número de aristas

# Leer las aristas
for k in range(2, 2 + j):
    nodo1, nodo2, capacidad = lineas[k].split()
    listaAdyacencia[nodo1].append([nodo2, int(capacidad)])
    

    
    
    
# Leer nodos de inicio y fin
nodoInicio = '0'
nodoFinal = '12'
print(dfs(nodoInicio, nodoFinal, set()))

# Flujo máximo (estilo Ford-Fulkerson)
flujo_total = 0

while True:
    camino = dfs(nodoInicio, nodoFinal, set())
    if not camino:
        break

    cuelloBotella = float('inf')
    for i in range(len(camino) - 1):
        for vecino in listaAdyacencia[camino[i]]:
            if vecino[0] == camino[i + 1]:
                cuelloBotella = min(vecino[1], cuelloBotella)
                break

    flujo_total += cuelloBotella

    print(f"\nCamino encontrado: {' -> '.join(camino)}")
    print(f"Cuello de botella: {cuelloBotella}")

    # Actualiza capacidades directas e inversas (residuales)
    for u, v in zip(camino, camino[1:]):
        actualizar_capacidad(u, v, -cuelloBotella)
        actualizar_capacidad(v, u, cuelloBotella)

print(f"\nFlujo máximo: {flujo_total}")

