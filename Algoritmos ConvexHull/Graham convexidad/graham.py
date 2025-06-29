import math
import matplotlib.pyplot as plt

def cruz(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])

decicion = input("¿Usar archivo de entrada? (s/n): ").strip().lower()
if decicion == 's':
    with open("Algoritmos ConvexHull\Graham convexidad\input", "r", encoding="utf-8") as f:
        n = int(f.readline().strip())
        puntos = [tuple(map(float, f.readline().strip().split())) for _ in range(n)]
else:
    print("Ingrese los puntos:")
    n = int(input("Ingrese número de nodos: "))
    puntos = []
    for i in range(n):
        x = float(input(f"x del nodo {i+1}: "))
        y = float(input(f"y del nodo {i+1}: "))
        puntos.append((x, y))

# Encontrar el punto base (más abajo, o más a la izquierda en caso de empate)
p0 = min(puntos, key=lambda p: (p[1], p[0]))

# Función para ordenar por ángulo con respecto a p0
def angulo(p):
    return math.atan2(p[1] - p0[1], p[0] - p0[0])

# Ordenar puntos en sentido antihorario alrededor de p0
puntos = sorted(puntos, key=lambda p: (angulo(p), (p[0] - p0[0])**2 + (p[1] - p0[1])**2))

# Construcción del envolvente convexo usando Graham Scan
pila = [puntos[0], puntos[1]]
for p in puntos[2:]:
    while len(pila) > 1 and cruz(pila[-2], pila[-1], p) <= 0:
        pila.pop()
    pila.append(p)

print("Puntos en el envolvente convexo:")
for i, p in enumerate(pila):
    print(f"{i+1}: {p}")
    


# Separar coordenadas para graficar
x_all, y_all = zip(*puntos)
x_hull, y_hull = zip(*pila + [pila[0]])  # Cerrar el polígono

plt.figure(figsize=(8, 6))
plt.scatter(x_all, y_all, color='blue', label='Puntos')
plt.plot(x_hull, y_hull, color='red', linewidth=2, label='Envolvente Convexa')
plt.scatter(*p0, color='green', s=100, label='Punto base')
plt.title('Envolvente Convexa (Graham Scan)')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()

