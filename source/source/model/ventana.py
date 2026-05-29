

from collections import deque
from datetime import timedelta

class Ventana:
    def __init__(self, segundos=60):
        self.segundos = segundos
        self.cola = deque()

    def anadir(self, fecha, ip):
        self.cola.append((fecha, ip))
        # borrar los viejos
        limite = fecha - timedelta(seconds=self.segundos)
        while self.cola and self.cola[0][0] < limite:
            self.cola.popleft()

    def contar_ip(self, ip):
        total = 0
        for f, ip_guardada in self.cola:
            if ip_guardada == ip:
                total += 1
        return total

    def tamano(self):
        return len(self.cola)
