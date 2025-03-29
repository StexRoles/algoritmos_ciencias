class ArbolB:
    def __init__(self, grado_minimo):
        self.grado_minimo = grado_minimo
        self.raiz = self._crear_nodo(True)
    
    def _crear_nodo(self, hoja):
        return {"llaves": [], "hijos": [], "hoja": hoja}
    
    def insertar(self, llave):
        raiz = self.raiz
        if len(raiz["llaves"]) == (2 * self.grado_minimo) - 1:
            nueva_raiz = self._crear_nodo(False)
            nueva_raiz["hijos"].append(self.raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz
        self._insertar_no_lleno(self.raiz, llave)
    
    def _insertar_no_lleno(self, nodo, llave):
        i = len(nodo["llaves"]) - 1
        if nodo["hoja"]:
            nodo["llaves"].append(None)
            while i >= 0 and llave < nodo["llaves"][i]:
                nodo["llaves"][i + 1] = nodo["llaves"][i]
                i -= 1
            nodo["llaves"][i + 1] = llave
        else:
            while i >= 0 and llave < nodo["llaves"][i]:
                i -= 1
            i += 1
            if len(nodo["hijos"][i]["llaves"]) == (2 * self.grado_minimo) - 1:
                self._dividir_hijo(nodo, i)
                if llave > nodo["llaves"][i]:
                    i += 1
            self._insertar_no_lleno(nodo["hijos"][i], llave)
    
    def _dividir_hijo(self, padre, i):
        t = self.grado_minimo
        hijo = padre["hijos"][i]
        nuevo_nodo = self._crear_nodo(hijo["hoja"])
        padre["llaves"].insert(i, hijo["llaves"][t - 1])
        padre["hijos"].insert(i + 1, nuevo_nodo)
        nuevo_nodo["llaves"] = hijo["llaves"][t:]
        hijo["llaves"] = hijo["llaves"][:t - 1]
        if not hijo["hoja"]:
            nuevo_nodo["hijos"] = hijo["hijos"][t:]
            hijo["hijos"] = hijo["hijos"][:t]
    
    def eliminar(self, llave):
        self._eliminar(self.raiz, llave)
        if len(self.raiz["llaves"]) == 0 and not self.raiz["hoja"]:
            self.raiz = self.raiz["hijos"][0]
    
    def _eliminar(self, nodo, llave):
        if llave in nodo["llaves"]:
            if nodo["hoja"]:
                nodo["llaves"].remove(llave)
            else:
                idx = nodo["llaves"].index(llave)
                if len(nodo["hijos"][idx]["llaves"]) >= self.grado_minimo:
                    predecesor = self._obtener_predecesor(nodo["hijos"][idx])
                    nodo["llaves"][idx] = predecesor
                    self._eliminar(nodo["hijos"][idx], predecesor)
                elif len(nodo["hijos"][idx + 1]["llaves"]) >= self.grado_minimo:
                    sucesor = self._obtener_sucesor(nodo["hijos"][idx + 1])
                    nodo["llaves"][idx] = sucesor
                    self._eliminar(nodo["hijos"][idx + 1], sucesor)
                else:
                    self._fusionar(nodo, idx)
                    self._eliminar(nodo["hijos"][idx], llave)
        else:
            for i in range(len(nodo["llaves"])):
                if llave < nodo["llaves"][i]:
                    if len(nodo["hijos"][i]["llaves"]) < self.grado_minimo:
                        self._llenar(nodo, i)
                    self._eliminar(nodo["hijos"][i], llave)
                    return
            if len(nodo["hijos"][-1]["llaves"]) < self.grado_minimo:
                self._llenar(nodo, len(nodo["llaves"]))
            self._eliminar(nodo["hijos"][-1], llave)
    
    def _obtener_predecesor(self, nodo):
        while not nodo["hoja"]:
            nodo = nodo["hijos"][-1]
        return nodo["llaves"][-1]
    
    def _obtener_sucesor(self, nodo):
        while not nodo["hoja"]:
            nodo = nodo["hijos"][0]
        return nodo["llaves"][0]
    
    def _fusionar(self, nodo, idx):
        hijo = nodo["hijos"][idx]
        hermano = nodo["hijos"][idx + 1]
        hijo["llaves"].append(nodo["llaves"].pop(idx))
        hijo["llaves"].extend(hermano["llaves"])
        if not hijo["hoja"]:
            hijo["hijos"].extend(hermano["hijos"])
        nodo["hijos"].pop(idx + 1)
    
    def _llenar(self, nodo, idx):
        if idx > 0 and len(nodo["hijos"][idx - 1]["llaves"]) >= self.grado_minimo:
            self._pedir_prestado_de_anterior(nodo, idx)
        elif idx < len(nodo["hijos"]) - 1 and len(nodo["hijos"][idx + 1]["llaves"]) >= self.grado_minimo:
            self._pedir_prestado_de_siguiente(nodo, idx)
        else:
            if idx < len(nodo["hijos"]) - 1:
                self._fusionar(nodo, idx)
            else:
                self._fusionar(nodo, idx - 1)
    
    def _pedir_prestado_de_anterior(self, nodo, idx):
        hijo = nodo["hijos"][idx]
        hermano = nodo["hijos"][idx - 1]
        hijo["llaves"].insert(0, nodo["llaves"][idx - 1])
        nodo["llaves"][idx - 1] = hermano["llaves"].pop()
        if not hermano["hoja"]:
            hijo["hijos"].insert(0, hermano["hijos"].pop())
    
    def _pedir_prestado_de_siguiente(self, nodo, idx):
        hijo = nodo["hijos"][idx]
        hermano = nodo["hijos"][idx + 1]
        hijo["llaves"].append(nodo["llaves"][idx])
        nodo["llaves"][idx] = hermano["llaves"].pop(0)
        if not hermano["hoja"]:
            hijo["hijos"].append(hermano["hijos"].pop(0))
    
    def recorrer(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        print("  " * nivel + str(nodo["llaves"]))
        for hijo in nodo["hijos"]:
            self.recorrer(hijo, nivel + 1)

# Prueba
arbol = ArbolB(3)
arbol.insertar(10)
arbol.insertar(20)
arbol.insertar(5)
arbol.insertar(6)
arbol.insertar(12)
arbol.insertar(30)
arbol.insertar(7)
arbol.insertar(17)
arbol.insertar(29)
arbol.recorrer()
print("\nEliminando 6")
arbol.eliminar(6)
arbol.recorrer()

