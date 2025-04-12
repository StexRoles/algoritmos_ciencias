class ListaAdyacencia:
    def __init__(self):
        self.nodos = {}

    def ingresar(self, clave, objeto):
        """Agrega un nodo al grafo."""
        if clave not in self.nodos:
            self.nodos[clave] = {'objeto': objeto, 'adyacentes': {}}
        else:
            print(f"El nodo {clave} ya existe.")

    def eliminar(self, clave):
        """Elimina un nodo y todas las aristas asociadas."""
        if clave in self.nodos:
            # Eliminar las aristas que apuntan al nodo
            for nodo in self.nodos:
                if clave in self.nodos[nodo]['adyacentes']:
                    del self.nodos[nodo]['adyacentes'][clave]
            # Eliminar el nodo
            del self.nodos[clave]
        else:
            print(f"El nodo {clave} no existe.")

    def buscar(self, clave):
        """Busca un nodo y devuelve su objeto asociado."""
        if clave in self.nodos:
            return self.nodos[clave]['objeto']
        else:
            print(f"El nodo {clave} no existe.")
            return None

    def agregar_arista(self, origen, destino, peso=1):
        """Agrega una arista entre dos nodos con un peso opcional."""
        if origen in self.nodos and destino in self.nodos:
            self.nodos[origen]['adyacentes'][destino] = peso
        else:
            print("Uno o ambos nodos no existen.")

    def eliminar_arista(self, origen, destino):
        """Elimina una arista entre dos nodos."""
        if origen in self.nodos and destino in self.nodos[origen]['adyacentes']:
            del self.nodos[origen]['adyacentes'][destino]
        else:
            print("La arista no existe.")

    def perfilamiento(self, clave):
        """Devuelve información sobre un nodo: objeto, adyacentes y nodos entrantes."""
        if clave in self.nodos:
            objeto = self.nodos[clave]['objeto']
            adyacentes = self.nodos[clave]['adyacentes']
            entrantes = [
                nodo for nodo in self.nodos if clave in self.nodos[nodo]['adyacentes']
            ]
            return {
                'objeto': objeto,
                'adyacentes': adyacentes,
                'nodos_que_apuntan_a_el': entrantes
            }
        else:
            print(f"El nodo {clave} no existe.")
            return None

    def mostrar(self):
        """Muestra el grafo completo."""
        for nodo, datos in self.nodos.items():
            print(f"{nodo} -> {datos['adyacentes']}")

# Ejemplo de uso
grafo = ListaAdyacencia()
grafo.ingresar("A", "Nodo A")
grafo.ingresar("B", "Nodo B")
grafo.ingresar("C", "Nodo C")

grafo.agregar_arista("A", "B", 5)
grafo.agregar_arista("A", "C", 10)
grafo.agregar_arista("B", "C", 2)

grafo.mostrar()

print("\nPerfil del nodo A:")
print(grafo.perfilamiento("A"))

print("\nEliminando nodo B...")
grafo.eliminar("B")
grafo.mostrar()