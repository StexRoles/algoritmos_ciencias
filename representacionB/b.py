class NodoArbolB:
    def __init__(self, t, hoja=False):
        self.t = t
        self.claves = []
        self.hijos = []
        self.hoja = hoja
        self.id = id(self)

class ArbolB:
    def __init__(self, t):
        self.raiz = NodoArbolB(t, hoja=True)
        self.t = t
        self.nodos = [self.raiz]
        self.matriz_adyacencia = {}

    def _actualizar_matriz_adyacencia(self):
        self.matriz_adyacencia = {}
        for nodo in self.nodos:
            self.matriz_adyacencia[nodo.id] = []
            for hijo in nodo.hijos:
                self.matriz_adyacencia[nodo.id].append(hijo.id)

    def buscar(self, clave, nodo=None):
        if nodo is None:
            nodo = self.raiz
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1
        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return nodo, i
        elif nodo.hoja:
            return None
        else:
            return self.buscar(clave, nodo.hijos[i])

    def insertar(self, clave):
        raiz = self.raiz
        if len(raiz.claves) == 2 * self.t - 1:
            nueva_raiz = NodoArbolB(self.t)
            nueva_raiz.hijos.insert(0, self.raiz)
            self.raiz = nueva_raiz
            self.nodos.append(nueva_raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self._insertar_no_lleno(nueva_raiz, clave)
        else:
            self._insertar_no_lleno(raiz, clave)
        self._actualizar_matriz_adyacencia()

    def _insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1
        if nodo.hoja:
            nodo.claves.append(None)
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = clave
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            if len(nodo.hijos[i].claves) == 2 * self.t - 1:
                self._dividir_hijo(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], clave)

    def _dividir_hijo(self, padre, i):
        t = self.t
        y = padre.hijos[i]
        z = NodoArbolB(t, hoja=y.hoja)
        self.nodos.append(z)

        padre.claves.insert(i, y.claves[t - 1])
        padre.hijos.insert(i + 1, z)

        z.claves = y.claves[t:(2 * t - 1)]
        y.claves = y.claves[0:t - 1]

        if not y.hoja:
            z.hijos = y.hijos[t:2 * t]
            y.hijos = y.hijos[0:t]

    def imprimir_arbol(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        print("Nivel", nivel, "Claves:", nodo.claves)
        for hijo in nodo.hijos:
            self.imprimir_arbol(hijo, nivel + 1)

    def mostrar_matriz_adyacencia(self):
        print("Matriz de Adyacencia (por ID de nodo):")
        for id_padre, ids_hijos in self.matriz_adyacencia.items():
            print(f"{id_padre}: {ids_hijos}")

    def imprimir_arbol_bonito(self):
        def _imprimir(nodo, prefijo="", es_ultimo=True):
            conector = "└── " if es_ultimo else "├── "
            print(prefijo + conector + str(nodo.claves))
            if nodo.hijos:
                for i, hijo in enumerate(nodo.hijos):
                    es_ultimo_hijo = i == len(nodo.hijos) - 1
                    _imprimir(hijo, prefijo + ("    " if es_ultimo else "│   "), es_ultimo_hijo)

        print("Árbol B (estructura visual):")
        _imprimir(self.raiz)

    def eliminar(self, clave):
        self._eliminar_interno(self.raiz, clave)
        if len(self.raiz.claves) == 0 and not self.raiz.hoja:
            self.raiz = self.raiz.hijos[0]
        self._actualizar_matriz_adyacencia()

    def _eliminar_interno(self, nodo, clave):
        t = self.t
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and nodo.claves[i] == clave:
            if nodo.hoja:
                nodo.claves.pop(i)
            else:
                if len(nodo.hijos[i].claves) >= t:
                    pred = self._obtener_predecesor(nodo.hijos[i])
                    nodo.claves[i] = pred
                    self._eliminar_interno(nodo.hijos[i], pred)
                elif len(nodo.hijos[i+1].claves) >= t:
                    succ = self._obtener_sucesor(nodo.hijos[i+1])
                    nodo.claves[i] = succ
                    self._eliminar_interno(nodo.hijos[i+1], succ)
                else:
                    self._fusionar(nodo, i)
                    self._eliminar_interno(nodo.hijos[i], clave)
        else:
            if nodo.hoja:
                return
            bandera = (i == len(nodo.claves))
            if len(nodo.hijos[i].claves) < t:
                self._rellenar(nodo, i)
            if bandera and i > len(nodo.claves):
                self._eliminar_interno(nodo.hijos[i - 1], clave)
            else:
                self._eliminar_interno(nodo.hijos[i], clave)

    def _obtener_predecesor(self, nodo):
        while not nodo.hoja:
            nodo = nodo.hijos[-1]
        return nodo.claves[-1]

    def _obtener_sucesor(self, nodo):
        while not nodo.hoja:
            nodo = nodo.hijos[0]
        return nodo.claves[0]

    def _fusionar(self, padre, i):
        hijo = padre.hijos[i]
        hermano = padre.hijos[i + 1]

        hijo.claves.append(padre.claves[i])
        hijo.claves.extend(hermano.claves)
        if not hijo.hoja:
            hijo.hijos.extend(hermano.hijos)

        padre.claves.pop(i)
        padre.hijos.pop(i + 1)

        self.nodos.remove(hermano)

    def _rellenar(self, nodo, i):
        if i != 0 and len(nodo.hijos[i - 1].claves) >= self.t:
            self._tomar_prestado_de_anterior(nodo, i)
        elif i != len(nodo.hijos) - 1 and len(nodo.hijos[i + 1].claves) >= self.t:
            self._tomar_prestado_de_siguiente(nodo, i)
        else:
            if i != len(nodo.hijos) - 1:
                self._fusionar(nodo, i)
            else:
                self._fusionar(nodo, i - 1)

    def _tomar_prestado_de_anterior(self, nodo, i):
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i - 1]

        hijo.claves = [nodo.claves[i - 1]] + hijo.claves
        if not hijo.hoja:
            hijo.hijos = [hermano.hijos.pop()] + hijo.hijos

        nodo.claves[i - 1] = hermano.claves.pop()

    def _tomar_prestado_de_siguiente(self, nodo, i):
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i + 1]

        hijo.claves.append(nodo.claves[i])
        if not hijo.hoja:
            hijo.hijos.append(hermano.hijos.pop(0))

        nodo.claves[i] = hermano.claves.pop(0)


arbol = ArbolB(t=3)

for clave in range(1, 30):
    arbol.insertar(clave)

print("Impresión del árbol")
arbol.imprimir_arbol_bonito()
print("Búsqueda de la clave 6")
resultado = arbol.buscar(6)
print("Resultado búsqueda:", resultado[0].claves if resultado else "No encontrado")

print("Eliminación de la clave 6")
arbol.eliminar(6)
print("Impresión del árbol")
arbol.imprimir_arbol_bonito()
print("Búsqueda de la clave 6 después de eliminarla")
resultado = arbol.buscar(6)
print("Resultado búsqueda:", resultado[0].claves if resultado else "No encontrado")
