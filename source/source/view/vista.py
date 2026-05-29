
class Vista:
    def titulo(self, texto):
        print("\n" + "=" * 50)
        print("  " + texto)
        print("=" * 50)

    def info(self, texto):
        print(texto)

    def alerta(self, ip, intentos, tipo):
        print("  [!] " + ip + " bloqueada (" + str(intentos) + " intentos, " + tipo + ")")

    def subred(self, s):
        print("  [!!] Subred atacada: " + s)

    def resumen(self, lineas, bloqueadas, subredes):
        self.titulo("RESUMEN")
        print("  Lineas: " + str(lineas))
        print("  Bloqueadas: " + str(len(bloqueadas)))
        print("  Subredes: " + str(len(subredes)))
        for ip in sorted(bloqueadas):
            print("    - " + ip)
        for s in subredes:
            print("    - " + s)
