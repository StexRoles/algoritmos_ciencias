class BTree:
    def __init__(self, grado_minimo):
        self.t = grado_minimo
        self.raiz = None

    def insertar(self, clave):
        if self.raiz is None:
            self.raiz = [[clave], []]
            return
        
        if len(self.raiz[0]) == 2 * self.t - 1:
            nueva_raiz = [[], [self.raiz]]
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz
        self._insertar_no_lleno(self.raiz, clave)

    def _insertar_no_lleno(self, nodo, clave):
        i = len(nodo[0]) - 1
        if not nodo[1]:  # Nodo hoja
            while i >= 0 and clave < nodo[0][i]:
                i -= 1
            nodo[0].insert(i + 1, clave)
        else:            # Nodo interno
            while i >= 0 and clave < nodo[0][i]:
                i -= 1
            i += 1
            if len(nodo[1][i][0]) == 2 * self.t - 1:
                self._dividir_hijo(nodo, i)
                if clave > nodo[0][i]:
                    i += 1
            self._insertar_no_lleno(nodo[1][i], clave)

    def _dividir_hijo(self, padre, indice):
        hijo = padre[1][indice]
        nuevo_nodo = [[], []]
        
        # Dividir claves
        medio = self.t - 1
        clave_media = hijo[0][medio]
        nuevo_nodo[0] = hijo[0][medio + 1 :]
        hijo[0] = hijo[0][:medio]
        
        # Dividir hijos si no es hoja
        if hijo[1]:
            nuevo_nodo[1] = hijo[1][medio + 1 :]
            hijo[1] = hijo[1][:medio + 1]
        
        # Actualizar padre
        padre[0].insert(indice, clave_media)
        padre[1].insert(indice + 1, nuevo_nodo)

    def eliminar(self, clave):
        if not self.raiz:
            return
        
        self._eliminar(self.raiz, clave)
        
        if len(self.raiz[0]) == 0 and self.raiz[1]:
            self.raiz = self.raiz[1][0]

    def _eliminar(self, nodo, clave):
        idx = 0
        while idx < len(nodo[0]) and clave > nodo[0][idx]:
            idx += 1
        
        # Caso 1: Clave encontrada
        if idx < len(nodo[0]) and nodo[0][idx] == clave:
            if not nodo[1]:
                self._eliminar_de_hoja(nodo, idx)
            else:
                self._eliminar_de_interno(nodo, idx)
        else:
            if not nodo[1]:
                return  # Clave no existe
            
            self._asegurar_minimo(nodo, idx)
            if idx > len(nodo[0]):
                idx -= 1
            self._eliminar(nodo[1][idx], clave)

    def _eliminar_de_hoja(self, nodo, idx):
        nodo[0].pop(idx)

    def _eliminar_de_interno(self, nodo, idx):
        if len(nodo[1][idx][0]) >= self.t:
            predecesor = self._obtener_predecesor(nodo[1][idx])
            nodo[0][idx] = predecesor
            self._eliminar(nodo[1][idx], predecesor)
        elif len(nodo[1][idx + 1][0]) >= self.t:
            sucesor = self._obtener_sucesor(nodo[1][idx + 1])
            nodo[0][idx] = sucesor
            self._eliminar(nodo[1][idx + 1], sucesor)
        else:
            self._fusionar(nodo, idx)
            self._eliminar(nodo[1][idx], nodo[0][idx])

    def _obtener_predecesor(self, nodo):
        while nodo[1]:
            nodo = nodo[1][-1]
        return nodo[0][-1]

    def _obtener_sucesor(self, nodo):
        while nodo[1]:
            nodo = nodo[1][0]
        return nodo[0][0]

    def _asegurar_minimo(self, padre, idx):
        if idx > 0 and len(padre[1][idx - 1][0]) >= self.t:
            self._tomar_de_izquierda(padre, idx)
        elif idx < len(padre[1]) - 1 and len(padre[1][idx + 1][0]) >= self.t:
            self._tomar_de_derecha(padre, idx)
        else:
            if idx == len(padre[1]) - 1:
                self._fusionar(padre, idx - 1)
            else:
                self._fusionar(padre, idx)

    def _tomar_de_izquierda(self, padre, idx):
        hijo = padre[1][idx]
        hermano = padre[1][idx - 1]
        
        hijo[0].insert(0, padre[0][idx - 1])
        padre[0][idx - 1] = hermano[0].pop()
        
        if hermano[1]:
            hijo[1].insert(0, hermano[1].pop())

    def _tomar_de_derecha(self, padre, idx):
        hijo = padre[1][idx]
        hermano = padre[1][idx + 1]
        
        hijo[0].append(padre[0][idx])
        padre[0][idx] = hermano[0].pop(0)
        
        if hermano[1]:
            hijo[1].append(hermano[1].pop(0))

    def _fusionar(self, padre, idx):
        hijo = padre[1][idx]
        hermano = padre[1].pop(idx + 1)
        
        hijo[0].append(padre[0].pop(idx))
        hijo[0].extend(hermano[0])
        hijo[1].extend(hermano[1])

    def mostrar_arbol(self):
        self._mostrar_rec(self.raiz, 0)

    def _mostrar_rec(self, nodo, nivel):
        if nodo:
            print("Nivel", nivel, ":", nodo[0])
            for hijo in nodo[1]:
                self._mostrar_rec(hijo, nivel + 1)

# Ejemplo de uso
if __name__ == "__main__":
    arbol = BTree(2)
    
    # Insertar algunas claves
    for clave in [3, 7, 1, 4, 9, 2, 6, 5, 8, 0]:
        arbol.insertar(clave)
    
    print("Árbol después de inserciones:")
    arbol.mostrar_arbol()
    
    # Eliminar algunas claves
    for clave in [3, 6, 0]:
        arbol.eliminar(clave)
    
    print("\nÁrbol después de eliminaciones:")
    arbol.mostrar_arbol()