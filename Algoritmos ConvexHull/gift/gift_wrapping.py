import random

def giro(p, q, r):
    """Devuelve la orientación de p, q, r.
    0 --> recta
    1 --> sentido horario
    2 --> sentido antihorario
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 2 if val > 0 else 1

def gift_wrapping(puntos):
    if len(puntos) < 3:
        return []

    # Lista para la envolvente
    env = []

    # Encuentra el punto más a la izquierda
    p_izq = 0
    for i in range(1, len(puntos)):
        if puntos[i][0] < puntos[p_izq][0]:
            p_izq = i

    p = p_izq
    while True:
        env.append(puntos[p])
        q = (p + 1) % len(puntos)

        for r in range(len(puntos)):
            if giro(puntos[p], puntos[q], puntos[r]) == 2:
                q = r

        p = q

        if p == p_izq:  # Volvimos al primer punto
            break

    return env

#puntos = [(3, 8), (7, 6), (1, 1), (-2, 1), (-2, 2), (-2, 3), (2, 4), (1, 5), (0, 3), (3, 4), (0, 7), (-2, 8), (4, -2), (6, 2), (2, 6), (5, 4), (4, 3)]

random.seed(42)
puntos = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(500)]

print("Puntos generados:")
for p in puntos:
    print(p)

envolvente = gift_wrapping(puntos)
print("Puntos en la envolvente convexa:")
for p in envolvente:
    print(p)
