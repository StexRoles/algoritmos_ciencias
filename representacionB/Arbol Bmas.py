class Nodo:
    def __init__(self, clave, dato):
        self.clave = clave
        self.dato = dato
        self.siguiente = None  # Para enlazar nodos en las hojas


class Pagina:
    def __init__(self, es_hoja):
        self.nodos = []  # Lista de claves (y datos si es hoja)
        self.hijos = []  # Lista de hijos (si no es hoja)
        self.es_hoja = es_hoja
        self.cantidad = 0
        self.siguiente = None  # Para enlazar páginas hoja


class ArbolBPlus:
    def __init__(self, grado):
        self.raiz = None
        self.grado = grado

    def insertar(self, clave, dato):
        if self.raiz is None:
            self.raiz = Pagina(True)
            self.raiz.nodos.append(Nodo(clave, dato))
            self.raiz.cantidad += 1
        else:
            if self.raiz.cantidad == (2 * self.grado) - 1:
                nueva_pagina = Pagina(False)
                nueva_pagina.hijos.append(self.raiz)
                self._dividir_pagina(nueva_pagina, 0)
                self.raiz = nueva_pagina
            self._insertar_no_lleno(self.raiz, clave, dato)

    def _insertar_no_lleno(self, pagina, clave, dato):
        i = pagina.cantidad - 1
        if pagina.es_hoja:
            # Insertar en la hoja
            pagina.nodos.append(None)
            while i >= 0 and clave < pagina.nodos[i].clave:
                pagina.nodos[i + 1] = pagina.nodos[i]
                i -= 1
            pagina.nodos[i + 1] = Nodo(clave, dato)
            pagina.cantidad += 1
            # Enlazar la hoja con la siguiente
            if i + 1 < pagina.cantidad - 1:
                pagina.nodos[i + 1].siguiente = pagina.nodos[i + 2]
        else:
            # Insertar en un nodo interno
            while i >= 0 and clave < pagina.nodos[i]:
                i -= 1
            i += 1
            if pagina.hijos[i].cantidad == (2 * self.grado) - 1:
                self._dividir_pagina(pagina, i)
                if clave > pagina.nodos[i]:
                    i += 1
            self._insertar_no_lleno(pagina.hijos[i], clave, dato)

    def _dividir_pagina(self, pagina, indice):
        grado = self.grado
        hijo = pagina.hijos[indice]
        nueva_pagina = Pagina(hijo.es_hoja)
        pagina.hijos.insert(indice + 1, nueva_pagina)
        if hijo.es_hoja:
            # Dividir una hoja
            pagina.nodos.insert(indice, hijo.nodos[grado - 1].clave)
            nueva_pagina.nodos = hijo.nodos[grado:(2 * grado) - 1]
            hijo.nodos = hijo.nodos[0:grado - 1]
            # Enlazar la nueva hoja
            nueva_pagina.siguiente = hijo.siguiente
            hijo.siguiente = nueva_pagina
        else:
            # Dividir un nodo interno
            pagina.nodos.insert(indice, hijo.nodos[grado - 1])
            nueva_pagina.nodos = hijo.nodos[grado:(2 * grado) - 1]
            hijo.nodos = hijo.nodos[0:grado - 1]
            nueva_pagina.hijos = hijo.hijos[grado:(2 * grado)]
            hijo.hijos = hijo.hijos[0:grado]
        hijo.cantidad = len(hijo.nodos)
        nueva_pagina.cantidad = len(nueva_pagina.nodos)
        pagina.cantidad += 1

    def eliminar(self, clave):
        if self.raiz is None:
            print("El árbol está vacío")
            return
        self._eliminar(self.raiz, clave)
        if self.raiz.cantidad == 0:
            if self.raiz.es_hoja:
                self.raiz = None
            else:
                self.raiz = self.raiz.hijos[0]

    def _eliminar(self, pagina, clave):
        i = 0
        while i < pagina.cantidad and clave > (pagina.nodos[i].clave if pagina.es_hoja else pagina.nodos[i]):
            i += 1
        if pagina.es_hoja:
            if i < pagina.cantidad and clave == pagina.nodos[i].clave:
                self._eliminar_de_hoja(pagina, i)
            else:
                print(f"La clave {clave} no está en el árbol")
        else:
            if i < pagina.cantidad and clave == pagina.nodos[i]:
                self._eliminar_de_no_hoja(pagina, i)
            else:
                if pagina.hijos[i].cantidad < self.grado:
                    self._llenar(pagina, i)
                if i > pagina.cantidad:
                    self._eliminar(pagina.hijos[i - 1], clave)
                else:
                    self._eliminar(pagina.hijos[i], clave)

    def _eliminar_de_hoja(self, pagina, indice):
        pagina.nodos.pop(indice)
        pagina.cantidad -= 1
        # Actualizar enlaces entre hojas
        if indice < pagina.cantidad:
            pagina.nodos[indice].siguiente = pagina.nodos[indice + 1] if indice + 1 < pagina.cantidad else None

    def _eliminar_de_no_hoja(self, pagina, indice):
        clave = pagina.nodos[indice]
        if pagina.hijos[indice].cantidad >= self.grado:
            predecesor = self._obtener_predecesor(pagina.hijos[indice])
            pagina.nodos[indice] = predecesor.clave if pagina.hijos[indice].es_hoja else predecesor
            self._eliminar(pagina.hijos[indice], predecesor.clave if pagina.hijos[indice].es_hoja else predecesor)
        elif pagina.hijos[indice + 1].cantidad >= self.grado:
            sucesor = self._obtener_sucesor(pagina.hijos[indice + 1])
            pagina.nodos[indice] = sucesor.clave if pagina.hijos[indice + 1].es_hoja else sucesor
            self._eliminar(pagina.hijos[indice + 1], sucesor.clave if pagina.hijos[indice + 1].es_hoja else sucesor)
        else:
            self._fusionar(pagina, indice)
            self._eliminar(pagina.hijos[indice], clave)

    def _obtener_predecesor(self, pagina):
        while not pagina.es_hoja:
            pagina = pagina.hijos[pagina.cantidad]
        return pagina.nodos[pagina.cantidad - 1]

    def _obtener_sucesor(self, pagina):
        while not pagina.es_hoja:
            pagina = pagina.hijos[0]
        return pagina.nodos[0]

    def _fusionar(self, pagina, indice):
        hijo = pagina.hijos[indice]
        hermano = pagina.hijos[indice + 1]
        if hijo.es_hoja:
            hijo.nodos.extend(hermano.nodos)
            hijo.siguiente = hermano.siguiente
        else:
            hijo.nodos.append(pagina.nodos[indice])
            hijo.nodos.extend(hermano.nodos)
            hijo.hijos.extend(hermano.hijos)
        pagina.nodos.pop(indice)
        pagina.hijos.pop(indice + 1)
        hijo.cantidad += hermano.cantidad + (0 if hijo.es_hoja else 1)
        pagina.cantidad -= 1

    def _llenar(self, pagina, indice):
        if indice != 0 and pagina.hijos[indice - 1].cantidad >= self.grado:
            self._prestar_de_anterior(pagina, indice)
        elif indice != pagina.cantidad and pagina.hijos[indice + 1].cantidad >= self.grado:
            self._prestar_de_siguiente(pagina, indice)
        else:
            if indice != pagina.cantidad:
                self._fusionar(pagina, indice)
            else:
                self._fusionar(pagina, indice - 1)

    def _prestar_de_anterior(self, pagina, indice):
        hijo = pagina.hijos[indice]
        hermano = pagina.hijos[indice - 1]
        if hijo.es_hoja:
            hijo.nodos.insert(0, hermano.nodos[hermano.cantidad - 1])
            pagina.nodos[indice - 1] = hermano.nodos[hermano.cantidad - 2].clave
        else:
            hijo.nodos.insert(0, pagina.nodos[indice - 1])
            pagina.nodos[indice - 1] = hermano.nodos[hermano.cantidad - 1]
            hijo.hijos.insert(0, hermano.hijos[hermano.cantidad])
        hermano.nodos.pop(hermano.cantidad - 1)
        hijo.cantidad += 1
        hermano.cantidad -= 1

    def _prestar_de_siguiente(self, pagina, indice):
        hijo = pagina.hijos[indice]
        hermano = pagina.hijos[indice + 1]
        if hijo.es_hoja:
            hijo.nodos.append(hermano.nodos[0])
            pagina.nodos[indice] = hermano.nodos[0].clave
        else:
            hijo.nodos.append(pagina.nodos[indice])
            pagina.nodos[indice] = hermano.nodos[0]
            hijo.hijos.append(hermano.hijos[0])
        hermano.nodos.pop(0)
        hijo.cantidad += 1
        hermano.cantidad -= 1

    def inorden_pila(self):
        if self.raiz is None:
            return
        pila = []
        actual = self.raiz
        while True:
            if actual is not None:
                pila.append(actual)
                actual = actual.hijos[0] if actual.hijos else None
            elif pila:
                actual = pila.pop()
                if actual.es_hoja:
                    for nodo in actual.nodos:
                        print(nodo.clave, end=" ")
                else:
                    for i in range(actual.cantidad):
                        print(actual.nodos[i], end=" ")
                actual = actual.hijos[-1] if actual.hijos else None
            else:
                break
        print()

    def mostrar_arbol(self, pagina=None, nivel=0):
        if pagina is None:
            pagina = self.raiz
        print(f"Nivel {nivel}: ", end="")
        if pagina.es_hoja:
            for nodo in pagina.nodos:
                print(nodo.clave, end=" ")
        else:
            for i in range(pagina.cantidad):
                print(pagina.nodos[i], end=" ")
        print()
        if not pagina.es_hoja:
            for hijo in pagina.hijos:
                self.mostrar_arbol(hijo, nivel + 1)


# Ejemplo de uso
arbol = ArbolBPlus(2)
arbol.insertar(10, "Dato1")
arbol.insertar(20, "Dato2")
arbol.insertar(5, "Dato3")
arbol.insertar(6, "Dato4")
arbol.insertar(12, "Dato5")
arbol.insertar(30, "Dato6")

print("Recorrido inorden con pila:")
arbol.inorden_pila()

print("Mostrar árbol:")
arbol.mostrar_arbol()

arbol.eliminar(20)
print("Mostrar árbol después de eliminar 20:")
arbol.mostrar_arbol()