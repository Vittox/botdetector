

from model.ventana import Ventana
from model.arbol import Arbol
from model.analizadores import AnalizadorLogin, AnalizadorPuertos

class Controlador:
    def __init__(self, vista, limite=5, segundos=60):
        self.vista = vista
        self.limite = limite
        self.ventana = Ventana(segundos)
        self.arbol = Arbol()
        self.bloqueadas = set()
        self.analizadores = [AnalizadorLogin(), AnalizadorPuertos()]

    def procesar(self, ruta):
        lineas = 0
        f = open(ruta, "r")
        for linea in f:
            lineas += 1
            self._analizar(linea.strip())
        f.close()

        subredes = self.arbol.buscar_subredes()
        for s in subredes:
            self.vista.subred(s)
        return lineas, self.bloqueadas, subredes

    def _analizar(self, linea):
        for analizador in self.analizadores:
            evento = analizador.analizar(linea) 
            if evento is None:
                continue
            ip = evento["ip"]
            if ip in self.bloqueadas:
                continue
            self.ventana.anadir(evento["fecha"], ip)
            n = self.ventana.contar_ip(ip)
            if n >= self.limite:
                self.bloqueadas.add(ip)
                self.arbol.insertar(ip)
                self.vista.alerta(ip, n, evento["tipo"])
