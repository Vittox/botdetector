# tests.py - Pruebas basicas

from datetime import datetime, timedelta
from model.ventana import Ventana
from model.arbol import Arbol
from model.analizadores import AnalizadorLogin, AnalizadorPuertos

def test_ventana():
    v = Ventana(segundos=60)
    t = datetime(2026, 1, 1, 12, 0, 0)
    v.anadir(t, "1.1.1.1")
    v.anadir(t + timedelta(seconds=120), "1.1.1.1")
    assert v.tamano() == 1  # el viejo se borra
    print("OK - ventana")

def test_arbol():
    a = Arbol()
    a.insertar("10.20.30.1")
    a.insertar("10.20.30.2")
    a.insertar("10.20.30.3")
    a.insertar("172.16.0.5")
    subs = a.buscar_subredes()
    assert "10.20.30.0/24" in subs
    assert "172.16.0.0/24" not in subs
    print("OK - arbol")

def test_login():
    a = AnalizadorLogin()
    linea = "Oct 15 10:32:14 server sshd[123]: Failed password for root from 203.0.113.45 port 22 ssh2"
    r = a.analizar(linea)
    assert r is not None and r["ip"] == "203.0.113.45"
    assert a.analizar("Oct 15 10:32:14 server sshd[1]: Accepted password for root from 1.1.1.1 port 22") is None
    print("OK - login")

def test_puertos():
    a = AnalizadorPuertos()
    base = "Oct 15 10:35:00 server kernel: Connection attempt from 9.9.9.9 to port "
    assert a.analizar(base + "22") is None
    assert a.analizar(base + "23") is None
    assert a.analizar(base + "25") is None
    r = a.analizar(base + "80")
    assert r is not None
    print("OK - puertos")

if __name__ == "__main__":
    test_ventana()
    test_arbol()
    test_login()
    test_puertos()
    print("\nTodo OK")
