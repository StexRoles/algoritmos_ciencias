class ArbolBMas:
    def __init__(self, orden):
        self.orden = orden
        self.raiz = self._crear_nodo(True)
    
    def _crear_nodo(self, hoja):
        return {"claves": [], "hijos": [], "hoja": hoja, "siguiente": None}
    
    def insertar(self, clave):
        raiz = self.raiz
        if len(raiz["claves"]) == self.orden - 1:
            nueva_raiz = self._crear_nodo(False)
            nueva_raiz["hijos"].append(self.raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz
        self._insertar_no_lleno(self.raiz, clave)
    
    def _insertar_no_lleno(self, nodo, clave):
        if nodo["hoja"]:
            nodo["claves"].append(clave)
            nodo["claves"].sort()
        else:
            i = 0
            while i < len(nodo["claves"]) and clave > nodo["claves"][i]:
                i += 1
            if len(nodo["hijos"][i]["claves"]) == self.orden - 1:
                self._dividir_hijo(nodo, i)
                if clave > nodo["claves"][i]:
                    i += 1
            self._insertar_no_lleno(nodo["hijos"][i], clave)
    
    def _dividir_hijo(self, padre, i):
        orden = self.orden
        hijo = padre["hijos"][i]
        nuevo_nodo = self._crear_nodo(hijo["hoja"])
        medio = orden // 2
        
        if hijo["hoja"]:
            nuevo_nodo["claves"] = hijo["claves"][medio:]
            hijo["claves"] = hijo["claves"][:medio]
            nuevo_nodo["siguiente"] = hijo["siguiente"]
            hijo["siguiente"] = nuevo_nodo
            padre["claves"].insert(i, nuevo_nodo["claves"][0])
        else:
            padre["claves"].insert(i, hijo["claves"][medio])
            nuevo_nodo["claves"] = hijo["claves"][medio + 1:]
            hijo["claves"] = hijo["claves"][:medio]
            nuevo_nodo["hijos"] = hijo["hijos"][medio + 1:]
            hijo["hijos"] = hijo["hijos"][:medio + 1]
        
        padre["hijos"].insert(i + 1, nuevo_nodo)
    
    def eliminar(self, clave):
        self._eliminar(self.raiz, clave)
        if len(self.raiz["claves"]) == 0 and not self.raiz["hoja"]:
            self.raiz = self.raiz["hijos"][0]
    
    def _eliminar(self, nodo, clave):
        if nodo["hoja"]:
            if clave in nodo["claves"]:
                nodo["claves"].remove(clave)
        else:
            i = 0
            while i < len(nodo["claves"]) and clave > nodo["claves"][i]:
                i += 1
            if i < len(nodo["claves"]) and clave == nodo["claves"][i]:
                nodo["claves"].remove(clave)
            else:
                self._eliminar(nodo["hijos"][i], clave)
    
    def recorrer(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        print("  " * nivel + str(nodo["claves"]))
        if not nodo["hoja"]:
            for hijo in nodo["hijos"]:
                self.recorrer(hijo, nivel + 1)
    
    def recorrer_hojas(self):
        nodo = self.raiz
        while not nodo["hoja"]:
            nodo = nodo["hijos"][0]
        while nodo:
            print(nodo["claves"], end=" -> ")
            nodo = nodo["siguiente"]
        print("None")

# Ejemplo de uso
arbol = ArbolBMas(3)
arbol.insertar(10)
arbol.insertar(20)
arbol.insertar(5)
arbol.insertar(6)
arbol.insertar(12)
arbol.insertar(30)
arbol.insertar(7)
arbol.insertar(17)

arbol.recorrer()
print("\nRecorrido en orden por hojas:")
arbol.recorrer_hojas()

print("\nEliminando 6")
arbol.eliminar(6)
arbol.recorrer()
print("\nRecorrido en orden por hojas después de eliminar:")
arbol.recorrer_hojas()
