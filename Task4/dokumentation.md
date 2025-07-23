# Aufgabe 4: Connection-String & Umgebungsvariablen in Python

## Ziel
Der Datenbank-Connection-String soll nicht im Quellcode stehen, sondern sicher über Umgebungsvariablen geladen werden.

---

## Teil 1: Umgebungsvariablen lesen

### Beispiel: PATH-Variable ausgeben

**`path_reader.py`**
```python
import os

def read_path_variable():
    path_variable = os.environ.get("PATH")
    if not path_variable:
        print("PATH-Umgebungsvariable nicht gefunden.")
        return

    separator = ";" if os.name == "nt" else ":"
    paths = path_variable.split(separator)

    print("Inhalt der PATH-Umgebungsvariable:")
    print("=" * 40)
    for i, path in enumerate(paths, 1):
        print(f"{i}. {path}")
    print("=" * 40)
    print(f"Gesamt: {len(paths)} Pfade gefunden.")

if __name__ == "__main__":
    read_path_variable()
```

**Beispielausgabe:**
```
Inhalt der PATH-Umgebungsvariable:
========================================
1. /Users/tobiasclausen/.config/herd-lite/bin
2. /Users/tobiasclausen/.nvm/versions/node/v20.18.3/bin
3. /Library/Frameworks/Python.framework/Versions/3.12/bin
4. /opt/homebrew/bin
5. /opt/homebrew/sbin
6. /usr/local/bin
7. /System/Cryptexes/App/usr/bin
8. /usr/bin
9. /bin
10. /usr/sbin
11. /sbin
12. /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin
13. /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin
14. /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin
15. /Library/Apple/usr/bin
16. /Library/TeX/texbin
17. /Applications/VMware Fusion.app/Contents/Public
18. /usr/local/share/dotnet
19. ~/.dotnet/tools
20. /Users/tobiasclausen/Library/Application Support/JetBrains/Toolbox/scripts
21. file
22. ///Users/tobiasclausen/sqlmap-dev
========================================
Gesamt: 22 Pfade gefunden.

```

---

## Teil 2: MongoDB-Verbindung mit Umgebungsvariable

### Warum?
- Keine sensiblen Daten im Quelltext
- Einfache Anpassung je nach Umgebung (Dev, Test, Prod)
- Standardpraxis für Konfigurationsmanagement

### Vorbereitung

**Benötigte Pakete:**
```bash
pip install pymongo python-dotenv
```

**Dateien:**

- **`.env`**
```env
MONGO_URI=mongodb://localhost:27017/test
```

- **`example.env`**
```env
MONGO_URI="Your_Mongosh_URI"
```

> Die `.env`-Datei sollte in `.gitignore` aufgenommen werden.

---

### Refaktorisierte Verbindungstests

**`mongodb_connector.py`**
```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def load_mongo_uri():
    load_dotenv()
    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        print("Fehler: MONGO_URI Umgebungsvariable nicht gefunden!")
        print("Bitte setzen Sie die Umgebungsvariable mit einem gültigen MongoDB Connection-String.")
    return mongo_uri

def connect_to_mongo(uri):
    return MongoClient(uri, serverSelectionTimeoutMS=5000)

def test_mongodb_connection():
    mongo_uri = load_mongo_uri()
    if not mongo_uri:
        return False

    client = None
    try:
        client = connect_to_mongo(mongo_uri)
        client.admin.command('ping')
        print("Erfolgreich mit MongoDB verbunden!")
        print(f"Server-Informationen: {client.server_info()}")
        databases = client.list_database_names()
        print(f"Verfügbare Datenbanken: {', '.join(databases)}")
        return True
    except ConnectionFailure as e:
        print(f"Fehler bei der Verbindung zur MongoDB: {e}")
        return False
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        return False
    finally:
        if client:
            client.close()
            print("Verbindung geschlossen.")

if __name__ == "__main__":
    test_mongodb_connection()
```

---

## Anwendung

### 1. Konfiguration vorbereiten
```bash
cp example.env .env
# .env editieren und URI eintragen
```

### 2. Programme ausführen
```bash
python pathReader.py
python mongodbConnector.py
```

---

## Zusammenfassung
- Keine sensiblen Daten im Code
- `.env` als lokale Konfiguration
- `.gitignore` schützt geheime Infos

