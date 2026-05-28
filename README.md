# Bot Detector — Detector d'Ataques de Força Bruta

## Descripció breu

Bot Detector és un sistema que analitza els logs d'un servidor i detecta
automàticament atacs de força bruta i escanejats de ports. Quan una IP
supera un límit d'intents en poc temps, la bloqueja i avisa.

## Integrants del grup

- Víctor Castro
- Oscar Fernández

## Context i problemàtica

Els servidors connectats a Internet reben constantment atacs automàtics on un
atacant (o un bot) prova milers de combinacions d'usuari i contrasenya fins a
encertar (atac de força bruta). Revisar els logs manualment és inviable pel
volum de dades que generen.

Aquest projecte aborda el problema automatitzant la detecció: llegeix el log
línia per línia, identifica patrons d'atac (intents fallits repetitius,
connexions a múltiples ports) i bloqueja les IPs perilloses. A més, agrupa
les IPs en un arbre jeràrquic per detectar quan una subxarxa sencera (/24)
està sent utilitzada de forma coordinada per atacar, cosa que indica una
botnet o un atac distribuït.

Té sentit dins la ciberseguretat perquè és exactament el que fan eines reals
com fail2ban o els sistemes IDS: monitoritzar, detectar i respondre.

## Funcionalitats principals

- **Lectura de logs:** processa l'arxiu de log línia per línia.
- **Detecció de força bruta:** compta els intents fallits de login per IP dins
  d'una finestra temporal configurable (per defecte 60 segons) i bloqueja les
  que superen el límit (per defecte 5 intents).
- **Detecció d'escaneig de ports:** detecta IPs que proven 4 o més ports
  diferents, utilitzant una funció recursiva per comptar-los.
- **Agrupació per subxarxes:** utilitza un arbre N-ari per agrupar les IPs
  bloquejades per subxarxa /24 i detectar atacs coordinats (3+ IPs de la
  mateixa subxarxa bloquejades).
- **Generació de logs de prova:** inclou un generador que crea logs sintètics
  amb 4 escenaris (tràfic normal, força bruta, atac coordinat, escaneig de
  ports) per poder provar el sistema sense un servidor real.

### Patró MVC

El codi segueix el patró Model-Vista-Controlador:

- **Model** (`source/model/`): conté les estructures de dades i la lògica
  (la ventana, l'arbre i els analitzadors).
- **Vista** (`source/view/`): només s'encarrega de mostrar coses per pantalla.
  No pren cap decisió.
- **Controlador** (`source/controller/`): llegeix el log, coordina els
  analitzadors (model) i les alertes (vista).

  
  ### Estructura del repositori

```
.
├── README.md
├── source/
│   ├── main.py                  # Punt d'entrada: arranca el programa
│   ├── generador.py             # Crea un log de prova sintètic
│   ├── tests.py                 # 4 proves del sistema
│   │
│   ├── model/                   # MODEL: dades i lògica
│   │   ├── ventana.py           # Cua lliscant (deque)
│   │   ├── arbol.py             # Arbre N-ari de subxarxes (recursiu)
│   │   └── analizadores.py      # POO: classe pare + 2 filles
│   │
│   ├── view/                    # VISTA: pantalla
│   │   └── vista.py             # Mostra alertes i resums
│   │
│   └── controller/              # CONTROLADOR: coordinació
│       └── controlador.py       # Llegeix log, crida analitzadors, bloqueja
│
├── build/                       # (Opcional)
│
└── docs/                        # Documentació
    ├── uml.png                  # Diagrama UML de classes
    ├── flux_funcionalitat_1.png # Diagrama de flux: processament del log
    ├── flux_funcionalitat_2.png # Diagrama de flux: detecció de subxarxes
    ├── estudi_complexitat.pdf   # Anàlisi teòrica + temps mitjans + millores
    └── conclusions_i_propostes_futur.pdf


