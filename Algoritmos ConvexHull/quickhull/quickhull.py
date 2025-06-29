import matplotlib.pyplot as plt
import random

def lado_del_punto(punto1, punto2, punto_evaluado):
    # Retorna si el punto está a la izquierda (>0), derecha (<0), o sobre (=0) de la línea punto1-punto2
    return (punto2[0] - punto1[0]) * (punto_evaluado[1] - punto1[1]) - (punto2[1] - punto1[1]) * (punto_evaluado[0] - punto1[0])


def distancia_perpendicular(punto1, punto2, punto_evaluado):
    # Calcula la distancia perpendicular desde el punto evaluado a la línea punto1-punto2.
    return abs(lado_del_punto(punto1, punto2, punto_evaluado))


def encontrar_envolvente(puntos_candidatos, punto_inicial, punto_final):
    if not puntos_candidatos:
        return []

    # Hallar el punto más lejano a la línea punto_inicial-punto_final
    punto_mas_lejano = max(puntos_candidatos, key=lambda punto: distancia_perpendicular(punto_inicial, punto_final, punto))

    # Formar triángulo y descartar puntos dentro
    puntos_lado_izquierdo = [punto for punto in puntos_candidatos if lado_del_punto(punto_inicial, punto_mas_lejano, punto) > 0]
    puntos_lado_derecho = [punto for punto in puntos_candidatos if lado_del_punto(punto_mas_lejano, punto_final, punto) > 0]

    # Recursivamente encontrar puntos en cada lado
    return encontrar_envolvente(puntos_lado_izquierdo, punto_inicial, punto_mas_lejano) + [punto_mas_lejano] + encontrar_envolvente(puntos_lado_derecho, punto_mas_lejano, punto_final)


def quickhull(conjunto_puntos):
    # Encontrar los dos puntos más extremos
    punto_minimo_x = min(conjunto_puntos, key=lambda punto: punto[0])
    punto_maximo_x = max(conjunto_puntos, key=lambda punto: punto[0])
    
    # Separar los puntos en dos subconjuntos
    conjunto_izquierdo = []
    conjunto_derecho = []

    for punto in conjunto_puntos:
        lado = lado_del_punto(punto_minimo_x, punto_maximo_x, punto)
        if lado > 0:
            conjunto_izquierdo.append(punto)
        elif lado < 0:
            conjunto_derecho.append(punto)

    # Construir recursivamente las partes superior e inferior
    envolvente_superior = encontrar_envolvente(conjunto_izquierdo, punto_minimo_x, punto_maximo_x)
    envolvente_inferior = encontrar_envolvente(conjunto_derecho, punto_maximo_x, punto_minimo_x)

    # Resultado final
    return [punto_minimo_x] + envolvente_superior + [punto_maximo_x] + envolvente_inferior

def dibujar_envolvente(puntos_originales, envolvente_convexa):
    # Dibujar puntos originales
    coordenadas_x, coordenadas_y = zip(*puntos_originales)
    plt.scatter(coordenadas_x, coordenadas_y, color='blue', label='Puntos')

    # Dibujar la envolvente convexa
    # Cerramos el polígono volviendo al primer punto
    envolvente_x, envolvente_y = zip(*(envolvente_convexa + [envolvente_convexa[0]]))
    plt.plot(envolvente_x, envolvente_y, color='red', linewidth=2, label='Envolvente convexa')

    plt.title("QuickHull - Envolvente convexa")
    plt.legend()
    plt.axis('equal')  # Relación 1:1 para que no se distorsione
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Generar puntos aleatorios
    random.seed(42) 
    puntos_entrada = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(500)]
    
    envolvente_resultado = quickhull(puntos_entrada)
    print("Puntos del convex hull:")
    for punto in envolvente_resultado:
        print(punto)

    dibujar_envolvente(puntos_entrada, envolvente_resultado)

