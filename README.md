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


  ### Estructura del repositori

```
.
├── README.md
├── source/
│   ├── main.py                  
│   ├── generador.py             
│   ├── tests.py                 
│   │
│   ├── model/                   
│   │   ├── ventana.py           
│   │   ├── arbol.py             
│   │   └── analizadores.py      
│   │
│   ├── view/                    
│   │   └── vista.py             
│   │
│   └── controller/              
│       └── controlador.py                            
│
└── docs/                        
    ├── uml.png                  
    ├── flux_funcionalitat_1.png 
    ├── flux_funcionalitat_2.png 
    ├── estudi_complexitat.pdf   
    └── conclusions_i_propostes_futur.pdf

``` 

### Patró MVC

El codi segueix el patró Model-Vista-Controlador:

- **Model** (`source/model/`): conté les estructures de dades i la lògica
  (la ventana, l'arbre i els analitzadors).
- **Vista** (`source/vista/`): només s'encarrega de mostrar coses per pantalla.
  No pren cap decisió.
- **Controlador** (`source/controlador/`): llegeix el log, coordina els
  analitzadors (model) i les alertes (vista).
## Com funciona el flux d'execució

Quan executes `python main.py`, passa el següent:

**1.** `main.py` crea un objecte `Vista` i crida a `generador.generar()`, que
escriu un fitxer de log fals amb 47 línies (4 escenaris d'atac mesclats).

**2.** `main.py` crea un `Controlador` passant-li la vista, i li diu:
`ctrl.procesar("log_prueba.txt")`.

**3.** El controlador obre l'arxiu i va línia per línia. Per cada línia,
la passa a **tots els analitzadors** (polimorfisme):

- `AnalizadorLogin` mira si la línia conté "Failed password". Si és que sí,
  treu la IP partint la línia per espais (`split`) i buscant la paraula que
  va després de "from".
- `AnalizadorPuertos` mira si conté "Connection attempt". Si és que sí,
  guarda el port en una llista per aquella IP i crida una **funció recursiva**
  per comptar quants ports diferents ha provat. Si en porta 4 o més, avisa.

**4.** Quan un analitzador detecta alguna cosa, el controlador:
- Guarda l'event a la `Ventana` (una cua que només manté els últims 60 segons).
- Compta quants intents porta aquella IP dins la finestra.
- Si supera el límit (5), la bloqueja: l'afegeix al `set` de bloquejades i
  la insereix a l'`Arbol` de subxarxes.
- Demana a la `Vista` que mostri l'alerta per pantalla.

**5.** Quan acaba de llegir tot el log, el controlador demana a l'arbre que
busqui subxarxes /24 amb 3 o més IPs bloquejades (mitjançant una **cerca
recursiva** en profunditat). Si en troba, mostra l'alerta de subxarxa.

**6.** Finalment, la `Vista` mostra el resum: quantes línies s'han analitzat,
quantes IPs s'han bloquejat i quines subxarxes estan compromeses.

## Instruccions d'execució i dependències

### Dependències

Cap. El projecte utilitza **només la llibreria estàndard de Python**. No cal
instal·lar res amb pip.

- **Requisit:** Python 3.8 o superior.

Per comprovar la teva versió:

```bash
python --version
```

### Execució

```bash
cd source
python main.py
```

Això genera un log de prova, l'analitza i mostra les IPs bloquejades i les
subxarxes atacades per pantalla.

Per executar les proves:

```bash
cd source
python tests.py
```

##  Enllaç al vídeo demostratiu

(https://enticat-my.sharepoint.com/:f:/g/personal/oscar_fernandez_estudiant_enti_cat/IgCDXWFjItHWQ6_lZ6Elxf_wAeR2I3dU-_Cx7DBoed5btB4?e=4KrjzQ)


## Ús d'eines externes i IA

No hem fet servir cap llibreria externa, el projecte funciona només amb la llibreria estàndard de Python.

Vam començar escrivint tot el codi en un sol arxiu, amb tota la lògica barrejada. Funcionava, però era difícil d'entendre i de repartir la feina entre els dos. Vam buscar ajuda per saber com organitzar-ho millor.

L'assistent ens va recomanar separar el codi seguint el patró MVC (Model-Vista-Controlador), que a més és el que el professor ens va explicar a classe. Ens va ajudar a entendre com repartir les classes entre carpetes i com fer que els imports funcionessin entre mòduls.

Així hem pogut aplicar els algoritmes aplictas a classe i coneixements que ja habiem après l'any passat en Introducció a la Programació, només  ens ha orientat en l'estructura que és la part que només l'experiencia com a programador et por donar.


