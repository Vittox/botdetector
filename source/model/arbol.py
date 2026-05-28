


class Nodo:
    def __init__(self):
        self.hijos = {}
        self.es_ip = False

class Arbol:
    def __init__(self):
        self.raiz = Nodo()

    # insertar una IP en el arbol (recursivo)
    def insertar(self, ip):
        trozos = ip.split(".")
        if len(trozos) == 4:
            self._insertar(self.raiz, trozos, 0)

    def _insertar(self, nodo, trozos, nivel):
        if nivel == 4:
            nodo.es_ip = True
            return
        t = trozos[nivel]
        if t not in nodo.hijos:
            nodo.hijos[t] = Nodo()
        self._insertar(nodo.hijos[t], trozos, nivel + 1)

    # buscar subredes con 3 o mas IPs bloqueadas (recursivo)
    def buscar_subredes(self):
        resultado = []
        self._buscar(self.raiz, [], resultado)
        return resultado

    def _buscar(self, nodo, camino, resultado):
        # cuando llegamos al tercer nivel, miramos cuantas IPs hay
        if len(camino) == 3:
            contador = 0
            for hijo in nodo.hijos.values():
                if hijo.es_ip:
                    contador += 1
            if contador >= 3:
                resultado.append(".".join(camino) + ".0/24")
            return
        for trozo, hijo in nodo.hijos.items():
            self._buscar(hijo, camino + [trozo], resultado)
