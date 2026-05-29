
import random
from datetime import datetime, timedelta

def generar(ruta):
    random.seed(1)
    lineas = []
    t = datetime(2026, 10, 15, 10, 30, 0)
    users = ["root", "admin", "test", "guest"]


    for _ in range(10):
        ip = "10.0.0." + str(random.randint(20, 200))
        lineas.append(t.strftime("%b %d %H:%M:%S") + " server sshd[" +
            str(random.randint(1000, 9999)) + "]: Accepted password for " +
            random.choice(users) + " from " + ip + " port 50000 ssh2")
        t += timedelta(seconds=random.randint(2, 6))


    for _ in range(8):
        lineas.append(t.strftime("%b %d %H:%M:%S") + " server sshd[" +
            str(random.randint(1000, 9999)) + "]: Failed password for " +
            random.choice(users) + " from 203.0.113.45 port 22 ssh2")
        t += timedelta(seconds=random.randint(1, 3))

  
    for ip_final in [10, 11, 12, 13]:
        for _ in range(6):
            lineas.append(t.strftime("%b %d %H:%M:%S") + " server sshd[" +
                str(random.randint(1000, 9999)) + "]: Failed password for " +
                random.choice(users) + " from 192.168.50." + str(ip_final) +
                " port 22 ssh2")
            t += timedelta(seconds=random.randint(1, 3))


    for p in [21, 22, 23, 25, 80]:
        lineas.append(t.strftime("%b %d %H:%M:%S") +
            " server kernel: Connection attempt from 198.51.100.22 to port " + str(p))
        t += timedelta(seconds=1)

    f = open(ruta, "w")
    f.write("\n".join(lineas) + "\n")
    f.close()
    return len(lineas)
