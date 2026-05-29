# main.py - Arranca el programa

import os
from view.vista import Vista
from controller.controlador import Controlador
import generador

def main():
    vista = Vista()

    vista.titulo("BOT DETECTOR")
    ruta = "log_prueba.txt"
    n = generador.generar(ruta)
    vista.info("Log creado: " + str(n) + " lineas")

    vista.titulo("ANALIZANDO")
    ctrl = Controlador(vista, limite=5, segundos=60)
    lineas, bloqueadas, subredes = ctrl.procesar(ruta)

    vista.resumen(lineas, bloqueadas, subredes)
    os.remove(ruta)

if __name__ == "__main__":
    main()
