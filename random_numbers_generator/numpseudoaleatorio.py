import time
from collections import Counter

def obtener_n_digito(semilla, n):
    semilla_str = str(abs(semilla))  
    if len(semilla_str) >= n > 0:
        return int(semilla_str[n - 1]) 
    else:
        return int(semilla_str[0])  

def generar_numero_pseudoaleatorio():
    inicio = time.perf_counter_ns() 
    _ = [x**2 for x in range(1000)]  
    semilla = time.perf_counter_ns() - inicio  

    tercer_digito = obtener_n_digito(semilla, 3)  

    for _ in range(tercer_digito):
        semilla = semilla * semilla 

    num = semilla ^ (semilla >> 3)

    return obtener_n_digito(num, tercer_digito) 

print(generar_numero_pseudoaleatorio())
