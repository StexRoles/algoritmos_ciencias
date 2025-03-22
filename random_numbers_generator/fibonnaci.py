from collections import deque

def fibonacci_rng(seed=1, j=24, k=55, modulus=2**8):
    # Inicialización del estado usando un LCG (Linear Congruential Generator)
    a = 1664525
    c = 1013904223
    m = modulus
    
    # Generar k números iniciales con el LCG
    state = []
    current = seed
    for _ in range(k):
        current = (a * current + c) % m
        state.append(current)
    
    # Configurar el deque para mantener los últimos k números
    dq = deque(state, maxlen=k)
    
    while True:
        next_val = (dq[-j] - dq[-k]) % modulus  # Operación de resta modular
        dq.append(next_val)
        yield next_val
        
# Crear el generador con una semilla
rng = fibonacci_rng(seed=42)

# Generar 10 números pseudoaleatorios
for _ in range(10):
    print(next(rng))