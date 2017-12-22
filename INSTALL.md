"Politik bei uns"-OParl basiert auf Flask und stellt somit eine WSGI/Applikation bereit. Folgende Komponenten werden hierfür benötigt:

* Ein Linux (getestet mit Ubuntu 16.04 und Debian 9.0)
* Python 3 (getestet mit Python 3.5)
* MongoDB 3 (getestet mit MongoDB 3.2 und 3.4)
* Minio
* Ein HTTP-Server (getestet mit Nginx)

Um "Politik bei uns"-OParl zu installieren, brauchen wir zunächst die Dateien

```bash
$ mkdir oparl
$ cd oparl
$ git clone https://github.com/politik-bei-uns/oparl.git .
```

Anschließend benötigen wir ein Virtual Environment und alle Pakete:
```bash
$ virtualenv -p python3 venv 
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Des weiteren muss die Konfigurationsdatei erstellt werden:
```
$ cp webapp/config-dist.py webapp/config.py
$ vim webapp/config.py
```

Anschließend kann "Politik bei uns"-OParl testweise gestartet werden. Auf Port 5000 lauscht dann der Development-Server und stellt dort eine OParl-API bereit.
```
$ python runserver.py
```

Wenn man die SSH-Verbindung geschlossen hat, muss man immer erst wieder in das Virtual Enviroment zurück und kann dann wie gewohnt weiterarbeiten:
```
$ source venv/bin/activate
$ python runserver.py
```

Um "Politik bei uns"-OParl dauerhaft zu verwenden, empfiehlt sich z.B. die Einrichtung von `gunicorn` als WSGI-Server und Nginx als Reverse Proxy.

Außerdem braucht "Politik bei uns"-OParl natürlich Daten in der MongoDB und in Minio, damit etwas vernünftiges ausgegeben werden kann. Diese können z.B. via "Politik bei uns"-Daemon dort eingefügt werden.