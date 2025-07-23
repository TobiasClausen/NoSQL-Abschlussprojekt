# Dokumentation zu Aufgabe 6.1

## Vorgegebene Filestruktur

```
├── dao_room.py  
├── main.py  
└── room.py
```

## room.py

```python
class Room:
    def __init__(self, name, seats, is_reservable, _id=None):
        if _id is not None:
            self._id = _id
        self.name = name
        self.seats = seats
        self.is_reservable = is_reservable
```

Die Klasse `Room` repräsentiert einen Raum mit den Eigenschaften:
- `name`: Name des Raums (z. B. „Matterhorn“)
- `seats`: Anzahl Sitzplätze
- `is_reservable`: Ob der Raum reservierbar ist
- `_id`: MongoDB-Primärschlüssel (optional)

## dao_room.py

```python
from pymongo import MongoClient
from room import Room

class Dao_room:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        self.col.insert_one(room.__dict__)

    def read(self):
        room = Room(**self.col.find_one())
        return room

    def update(self, room_id, updated_fields):
        self.col.update_one({"_id": room_id}, {"$set": updated_fields})

    def delete(self, room_id):
        self.col.delete_one({"_id": room_id})
```

### Implementierte Methoden:
- `create(room)`: Fügt ein neues `Room`-Objekt in die Datenbank ein.
- `read()`: Liest einen Raum aus der Datenbank (hier nur den ersten Treffer).
- `update(room_id, updated_fields)`: Aktualisiert Felder eines Raums anhand der ID.
- `delete(room_id)`: Löscht einen Raum anhand der ID.

## main.py

```python
from room import Room
from dao_room import Dao_room

import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()
env_connection_string = os.getenv('connection_string')

dao_room = Dao_room(env_connection_string)

# Raum erstellen
room_create = Room("Matterhorn", 12, True)
dao_room.create(room_create)

# Raum lesen
room_read = dao_room.read()
print("Gelesener Raum:")
print(vars(room_read))

# Raum aktualisieren
if hasattr(room_read, "_id"):
    update_fields = {"seats": 20, "is_reservable": False}
    dao_room.update(room_read._id, update_fields)
    print("\nRaum wurde aktualisiert.")

    updated_room = dao_room.read()
    print("Aktualisierter Raum:")
    print(vars(updated_room))

# Raum löschen
if hasattr(room_read, "_id"):
    dao_room.delete(room_read._id)
    print("\nRaum wurde gelöscht.")
```

### Ablauf in main.py:
1. Verbindung zur Datenbank wird über `.env` hergestellt.
2. Ein Raum (`"Matterhorn"`) wird erstellt.
3. Der Raum wird gelesen und angezeigt.
4. Wenn eine `_id` vorhanden ist:
   - wird der Raum aktualisiert (`seats`, `is_reservable`)
   - danach erneut gelesen und angezeigt.
5. Abschließend wird der Raum gelöscht.

## Fazit

Dieses Setup zeigt den klassischen CRUD-Zyklus (Create, Read, Update, Delete) in Kombination mit einer MongoDB-Datenbank und einer einfachen Klassenstruktur in Python. Durch die Nutzung von `__dict__` und `ObjectId` können Objekte leicht in die MongoDB gespeichert und aktualisiert werden.
