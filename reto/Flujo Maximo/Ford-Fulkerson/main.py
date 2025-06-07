from abc import ABC, abstractmethod
from collections import defaultdict

class Grafo(ABC):
    @abstractmethod
    def ingresar(self, clave, objeto):
        #  Ingresa un nuevo nodo al grafo. 
        pass

    @abstractmethod
    def eliminar(self, clave):
        #  Elimina un nodo del grafo. 
        pass

    @abstractmethod
    def buscar(self, clave):
        #  Busca un nodo en el grafo y devuelve su objeto si existe. 
        pass

    @abstractmethod
    def agregar_arista(self, origen, destino, objeto=None):
        #  Agrega una arista entre dos nodos. 
        pass

    @abstractmethod
    def perfilamiento(self, clave):
        #  Devuelve el objeto del nodo y los nodos a los que apunta y los que apuntan a él. 
        pass


class ListaAdyacencia(Grafo):
    def __init__(self):
        self.nodos = {}
        self.aristas = defaultdict(dict)  # {origen: {destino: capacidad}}
        self.flujo = defaultdict(dict)   # {origen: {destino: flujo}}

    def ingresar(self, clave, objeto=None):
        # Ingresa un nuevo nodo al grafo. 
        if clave not in self.nodos:
            self.nodos[clave] = objeto
        else:
            print(f"El nodo {clave} ya existe.")

    def eliminar(self, clave):
        # Elimina un nodo del grafo. 
        if clave in self.nodos:
            # Eliminar aristas relacionadas
            del self.nodos[clave]
            for origen in list(self.aristas.keys()):
                if clave in self.aristas[origen]:
                    del self.aristas[origen][clave]
                if origen == clave:
                    del self.aristas[origen]
            # Eliminar flujos relacionados
            for origen in list(self.flujo.keys()):
                if clave in self.flujo[origen]:
                    del self.flujo[origen][clave]
                if origen == clave:
                    del self.flujo[origen]
        else:
            print(f"El nodo {clave} no existe.")

    def buscar(self, clave):
        # Busca un nodo en el grafo y devuelve su objeto si existe. 
        return self.nodos.get(clave, None)

    def agregar_arista(self, origen, destino, capacidad):
        # Agrega una arista entre dos nodos con capacidad dada. 
        if origen in self.nodos and destino in self.nodos:
            self.aristas[origen][destino] = capacidad
            self.flujo[origen][destino] = 0  # Flujo inicial 0
            # Asegurar arista reversa para el algoritmo
            if destino not in self.aristas or origen not in self.aristas[destino]:
                self.aristas[destino][origen] = 0
                self.flujo[destino][origen] = 0
        else:
            print("Uno o ambos nodos no existen.")

    def perfilamiento(self, clave):
        # Devuelve información del nodo y sus conexiones. 
        if clave not in self.nodos:
            return None
            
        return {
            'objeto': self.nodos[clave],
            'adyacentes': list(self.aristas[clave].keys()),
            'nodos_que_apuntan_a_el': [origen for origen in self.aristas 
                                      if clave in self.aristas[origen]]
        }

    def capacidad_residual(self, origen, destino):
        # Calcula la capacidad residual de una arista. 
        return self.aristas[origen].get(destino, 0) - self.flujo[origen].get(destino, 0)

    def actualizar_flujo(self, origen, destino, incremento):
        # Actualiza el flujo en una arista y su reversa. 
        self.flujo[origen][destino] += incremento
        self.flujo[destino][origen] -= incremento


class FordFulkerson:
    def __init__(self, grafo):
        self.grafo = grafo
        self.flujo_maximo = 0
        self.visitado = set()
        self.padre = {}

    def dfs(self, u, sumidero, flujo_camino):
        # Búsqueda en profundidad para encontrar un camino aumentante. 
        self.visitado.add(u)
        
        if u == sumidero:
            return flujo_camino
            
        for v in self.grafo.aristas[u]:
            capacidad_residual = self.grafo.capacidad_residual(u, v)
            if v not in self.visitado and capacidad_residual > 0:
                self.padre[v] = u
                flujo = min(flujo_camino, capacidad_residual)
                resultado = self.dfs(v, sumidero, flujo)
                if resultado > 0:
                    return resultado
        return 0

    def calcular_flujo_maximo(self, fuente, sumidero):
        # Calcula el flujo máximo desde la fuente al sumidero.
        self.flujo_maximo = 0
        iteracion = 1

        while True:
            self.visitado = set()
            self.padre = {}
            flujo_aumentante = self.dfs(fuente, sumidero, float('inf'))
            
            if flujo_aumentante == 0:
                break
                
            # Mostrar información del camino
            camino = self._reconstruir_camino(fuente, sumidero)
            print(f"\nIteración {iteracion}:")
            print(f"Camino encontrado: {' -> '.join(map(str, camino))}")
            print(f"Flujo aumentante: {flujo_aumentante}")

            # Actualizar flujos a lo largo del camino
            v = sumidero
            while v != fuente:
                u = self.padre[v]
                self.grafo.actualizar_flujo(u, v, flujo_aumentante)
                v = u

            self.flujo_maximo += flujo_aumentante
            iteracion += 1

        return self.flujo_maximo

    def _reconstruir_camino(self, fuente, sumidero):
        # Reconstruye el camino desde el sumidero hasta la fuente.
        camino = []
        v = sumidero
        while v != fuente:
            camino.append(v)
            v = self.padre[v]
        camino.append(fuente)
        camino.reverse()
        return camino


def leer_grafo_desde_archivo(nombre_archivo, grafo):

    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                # Ignorar líneas vacías
                if not linea.strip():
                    continue
                    
                # Dividir la línea en componentes
                partes = linea.strip().split()
                
                # Verificar que tenga exactamente 3 componentes
                if len(partes) != 3:
                    print(f"Formato incorrecto en línea: {linea.strip()} - Se esperaban 3 valores")
                    continue
                
                try:
                    origen = int(partes[0])
                    destino = int(partes[1])
                    capacidad = int(partes[2])
                    
                    # Asegurarse de que los nodos existan
                    if origen not in grafo.nodos:
                        grafo.ingresar(origen)
                    if destino not in grafo.nodos:
                        grafo.ingresar(destino)
                        
                    # Agregar la arista
                    grafo.agregar_arista(origen, destino, capacidad)
                    
                except ValueError:
                    print(f"Error al convertir valores en línea: {linea.strip()}")
                    
        print(f"Grafo cargado correctamente desde {nombre_archivo}")
        
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no fue encontrado")
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {str(e)}")


if __name__ == "__main__":
    # Crear grafo
    grafo = ListaAdyacencia()
    
    # Cargar datos desde archivo
    leer_grafo_desde_archivo('reto\Flujo Maximo\Ford-Fulkerson\entrada.txt', grafo)
    
    # Definir fuente y sumidero (ajustar según tu problema)
    fuente = 0
    sumidero = 12
    
    # Ejecutar Ford-Fulkerson
    ff = FordFulkerson(grafo)
    flujo_max = ff.calcular_flujo_maximo(fuente, sumidero)
    
    print(f"\nEl flujo máximo desde {fuente} hasta {sumidero} es: {flujo_max}")