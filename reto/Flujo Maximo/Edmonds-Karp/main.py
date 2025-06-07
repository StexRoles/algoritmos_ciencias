from collections import deque, defaultdict
from abc import ABC, abstractmethod

class Grafo(ABC):
    @abstractmethod
    def ingresar(self, clave, objeto):
        pass

    @abstractmethod
    def eliminar(self, clave):
        pass

    @abstractmethod
    def buscar(self, clave):
        pass

    @abstractmethod
    def agregar_arista(self, origen, destino, objeto=None):
        pass

    @abstractmethod
    def perfilamiento(self, clave):
        pass


class ListaAdyacencia(Grafo):
    def __init__(self):
        self.nodos = {}
        self.aristas = defaultdict(dict)  # {origen: {destino: capacidad}}

    def ingresar(self, clave, objeto=None):
        if clave not in self.nodos:
            self.nodos[clave] = objeto

    def eliminar(self, clave):
        if clave in self.nodos:
            del self.nodos[clave]
            for origen in list(self.aristas.keys()):
                if clave in self.aristas[origen]:
                    del self.aristas[origen][clave]
                if origen == clave:
                    del self.aristas[origen]

    def buscar(self, clave):
        return self.nodos.get(clave, None)

    def agregar_arista(self, origen, destino, capacidad):
        if origen in self.nodos and destino in self.nodos:
            self.aristas[origen][destino] = capacidad
            # Asegurar arista reversa para el algoritmo
            if destino not in self.aristas or origen not in self.aristas[destino]:
                self.aristas[destino][origen] = 0

    def perfilamiento(self, clave):
        if clave not in self.nodos:
            return None
            
        return {
            'objeto': self.nodos[clave],
            'adyacentes': list(self.aristas[clave].keys()),
            'nodos_que_apuntan_a_el': [origen for origen in self.aristas 
                                      if clave in self.aristas[origen]]
        }

    def obtener_capacidad(self, origen, destino):
        return self.aristas.get(origen, {}).get(destino, 0)

    def actualizar_capacidad(self, origen, destino, delta):
        if origen in self.aristas and destino in self.aristas[origen]:
            self.aristas[origen][destino] += delta


def leer_grafo_desde_archivo(nombre_archivo, grafo):
    
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea_num, linea in enumerate(archivo, 1):
                linea = linea.strip()
                if not linea:
                    continue
                
                partes = linea.split()
                if len(partes) != 3:
                    print(f"Error línea {linea_num}: Formato incorrecto - {linea}")
                    continue
                
                try:
                    origen = int(partes[0])
                    destino = int(partes[1])
                    capacidad = int(partes[2])
                    
                    grafo.ingresar(origen)
                    grafo.ingresar(destino)
                    grafo.agregar_arista(origen, destino, capacidad)
                    
                except ValueError:
                    print(f"Error línea {linea_num}: Valores no numéricos - {linea}")
                    
        print(f"Grafo cargado correctamente desde {nombre_archivo}")
        
    except FileNotFoundError:
        print(f"Error: Archivo {nombre_archivo} no encontrado")
    except Exception as e:
        print(f"Error al leer archivo: {str(e)}")


class EdmondsKarp:
    def __init__(self, grafo):
        self.grafo = grafo
        self.flujo_maximo = 0
        self.padre = {}

    def bfs(self, fuente, sumidero):
        # Búsqueda en anchura para encontrar camino aumentante.
        visitado = set()
        cola = deque([fuente])
        visitado.add(fuente)
        self.padre = {fuente: None}

        while cola:
            u = cola.popleft()
            for v in self.grafo.aristas.get(u, {}):
                if v not in visitado and self.grafo.obtener_capacidad(u, v) > 0:
                    self.padre[v] = u
                    if v == sumidero:
                        return True
                    visitado.add(v)
                    cola.append(v)
        return False

    def calcular_flujo_maximo(self, fuente, sumidero):
        # Calcula el flujo máximo desde la fuente al sumidero.
        self.flujo_maximo = 0
        iteracion = 1

        while self.bfs(fuente, sumidero):
            # Calcular flujo del camino
            camino_flujo = float('inf')
            v = sumidero
            while v != fuente:
                u = self.padre[v]
                camino_flujo = min(camino_flujo, self.grafo.obtener_capacidad(u, v))
                v = u

            # Actualizar capacidades
            v = sumidero
            while v != fuente:
                u = self.padre[v]
                self.grafo.actualizar_capacidad(u, v, -camino_flujo)
                self.grafo.actualizar_capacidad(v, u, camino_flujo)
                v = u

            # Mostrar información del camino
            camino = self._reconstruir_camino(fuente, sumidero)
            print(f"\nIteración {iteracion}:")
            print(f"Camino encontrado: {' -> '.join(map(str, camino))}")
            print(f"Flujo transportado: {camino_flujo}")

            self.flujo_maximo += camino_flujo
            iteracion += 1

        return self.flujo_maximo

    def _reconstruir_camino(self, fuente, sumidero):
        # Reconstruye el camino desde sumidero hasta fuente.
        camino = []
        v = sumidero
        while v is not None:
            camino.append(v)
            v = self.padre.get(v, None)
        camino.reverse()
        return camino


if __name__ == "__main__":
    # Crear y cargar grafo
    grafo = ListaAdyacencia()
    leer_grafo_desde_archivo('reto\Flujo Maximo\Edmonds-Karp\entrada.txt', grafo)
    
    # Definir fuente y sumidero (ajustar según necesidades)
    FUENTE = 0
    SUMIDERO = 12
    
    # Ejecutar algoritmo
    ek = EdmondsKarp(grafo)
    flujo_max = ek.calcular_flujo_maximo(FUENTE, SUMIDERO)
    
    print(f"\nFLUJO MÁXIMO: {flujo_max} (Desde {FUENTE} hasta {SUMIDERO})")