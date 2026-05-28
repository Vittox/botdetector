# analizadores.py - Clases para detectar ataques en el log
# Clase padre Analizador + dos hijas (polimorfismo)

from datetime import datetime

class Analizador:
    # clase padre, las hijas tienen que hacer su propio analizar()
    def __init__(self, nombre):
        self.nombre = nombre

    def analizar(self, linea):
        return None

    def sacar_fecha(self, linea):
        # las fechas del log son tipo "Oct 15 10:32:14"
        partes = linea.split()
        try:
            texto = partes[0] + " " + partes[1] + " " + partes[2]
            return datetime.strptime("2026 " + texto, "%Y %b %d %H:%M:%S")
        except:
            return None


class AnalizadorLogin(Analizador):
    # detecta lineas tipo "Failed password for root from 1.2.3.4"
    def __init__(self):
        super().__init__("login")

    def analizar(self, linea):
        if "Failed password" not in linea:
            return None
        partes = linea.split()
        if "from" not in partes:
            return None
        pos = partes.index("from")
        ip = partes[pos + 1]
        fecha = self.sacar_fecha(linea)
        if fecha is None:
            return None
        return {"ip": ip, "fecha": fecha, "tipo": "login"}


class AnalizadorPuertos(Analizador):
    # detecta si una IP esta probando muchos puertos distintos
    def __init__(self):
        super().__init__("puertos")
        self.historico = {}  # ip -> lista de puertos

    def analizar(self, linea):
        if "Connection attempt" not in linea:
            return None
        partes = linea.split()
        if "from" not in partes or "port" not in partes:
            return None
        ip = partes[partes.index("from") + 1]
        puerto = partes[partes.index("port") + 1]
        fecha = self.sacar_fecha(linea)
        if fecha is None:
            return None

        if ip not in self.historico:
            self.historico[ip] = []
        self.historico[ip].append(puerto)

        # contar puertos distintos con recursividad
        n = self._distintos(self.historico[ip], 0, [])
        if n >= 4:
            self.historico[ip] = []
            return {"ip": ip, "fecha": fecha, "tipo": "puertos"}
        return None

    def _distintos(self, lista, i, vistos):
        # caso base: llegamos al final
        if i >= len(lista):
            return len(vistos)
        if lista[i] not in vistos:
            vistos = vistos + [lista[i]]
        return self._distintos(lista, i + 1, vistos)
