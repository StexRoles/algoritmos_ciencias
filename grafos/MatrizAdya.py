class Arista:
    def __init__(self, nombre, info, numero):
        self.__nombre = nombre
        self.__info = info
        self.__numero = numero
    
    def get_nombre(self):
        return self.__nombre
    
    def get_info(self):
        return self.__info
    
    def get_numero(self):
        return self.__numero


class MatrizAdyacencia:
    def __init__(self, dirigido=False):
        self.__dirigido = dirigido
        self.__aristas = [] 
        self.__matriz = []   

    def agregar_arista(self, arista):
        self.__aristas.append(arista)
        self.__expandir_matriz()

    def agregar_adyacencia(self, nombre_origen, nombre_destino, peso=1):
        i = self.__buscar_indice(nombre_origen)
        j = self.__buscar_indice(nombre_destino)

        if i is None or j is None:
            raise ValueError("Una o ambas aristas no existen.")

        self.__matriz[i][j] = peso
        if not self.__dirigido:
            self.__matriz[j][i] = peso

    def mostrar_matriz(self):
        print("   ", end="")
        for arista in self.__aristas:
            print(f"{arista.get_nombre():>5}", end=" ")
        print()
        for i, fila in enumerate(self.__matriz):
            print(f"{self.__aristas[i].get_nombre():>3} ", end="")
            for val in fila:
                print(f"{val:5}", end=" ")
            print()

    def __buscar_indice(self, nombre):
        for index, arista in enumerate(self.__aristas):
            if arista.get_nombre() == nombre:
                return index
        return None

    def __expandir_matriz(self):
        nuevo_tamano = len(self.__aristas)
        for fila in self.__matriz:
            fila.append(0)
        self.__matriz.append([0] * nuevo_tamano)

    def get_aristas(self):
        return self.__aristas[:]

    def get_matriz(self):
        return [fila[:] for fila in self.__matriz]