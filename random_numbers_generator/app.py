import math

# Xn+1 = (a⋅sin(Xn)+b⋅log(1+∣Xn∣)+c) mod m COMBINACIÓN DE FUNCIONES TRIGONOMÉTRICAS Y LOGARÍTMICAS
# sen aporta periodicidad, log aporta aleatoriedad, c aporta desplazamiento, m aporta escalado

class TrigLogPRNG:
    def __init__(self, seed, a=10**6, b=10**5, c=10**4, m=2**30):
        self.x = seed  # Semilla inicial
        self.a = a
        self.b = b
        self.c = c
        self.m = m

    def next(self):
        log_component = math.log(1 + abs(self.x))  # Evitar log(0)
        self.x = int((self.a * math.sin(self.x) + self.b * log_component + self.c) % self.m)
        return self.x  # Devuelve un número entero

# Uso del generador de números enteros
prng = TrigLogPRNG(seed=123456) # Con la misma semilla, generará la misma secuencia
for _ in range(10):
    print(prng.next())
