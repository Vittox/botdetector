# Bot Detector — Detector de Ataques de Fuerza Bruta

## Descripción breve

Bot Detector es un sistema que analiza los logs de un servidor y detecta
automáticamente ataques de fuerza bruta y escaneos de puertos. Cuando una IP
supera un límite de intentos en poco tiempo, la bloquea y avisa.

## Integrantes del grupo

- Víctor Castro
- Oscar Fernández

## Contexto y problemática

Los servidores reciben constantemente ataques automáticos donde un atacante
prueba miles de contraseñas hasta acertar (fuerza bruta). Detectar estos
ataques a mano leyendo los logs es imposible por el volumen de datos. Este
proyecto automatiza esa detección: lee el log, identifica patrones de ataque y
bloquea las IPs peligrosas, agrupándolas además por subredes para detectar
ataques coordinados.