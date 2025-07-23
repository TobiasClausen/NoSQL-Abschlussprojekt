# RestaurantExplorer – MongoDB CLI-Anwendung

Dieses Python-Programm ermöglicht es, eine MongoDB-Datenbank mit Restaurantdaten über eine benutzerfreundliche Kommandozeilenoberfläche zu durchsuchen, auszuwerten und zu erweitern.

## Voraussetzungen

- Python 3
- MongoDB-Datenbank mit `restaurants`-Collection
- `.env` Datei mit Verbindungszeichenfolge (`connection_string`)
- Abhängigkeiten:
  - `pymongo`
  - `python-dotenv`

Installation der Abhängigkeiten:

```bash
pip install pymongo python-dotenv
```

## .env Datei

Erstelle eine Datei `.env` im selben Verzeichnis mit folgendem Inhalt:

```
connection_string=mongodb+srv://<user>:<passwort>@cluster0.mongodb.net/?retryWrites=true&w=majority
```

## Anwendung starten

```bash
python3 RestaurantDatabase.py
```

## Funktionsübersicht

Nach dem Start erscheint das folgende Menü:

```
--- Restaurant-Datenbank ---
1. Alle Stadtbezirke anzeigen
2. Top 3 Restaurants nach Rating anzeigen
3. Nächstgelegenes Restaurant zu 'Le Perigord' finden
4. Restaurants suchen
5. Restaurant bewerten
6. Beenden
```

### 1. Alle Stadtbezirke anzeigen

Zeigt alle einzigartigen Werte des Felds `borough` aus der Datenbank an.

Beispielausgabe:

```
Einzigartige Stadtbezirke:
- Bronx
- Brooklyn
- Manhattan
- Missing
- Queens
- Staten Island
```

### 2. Top 3 Restaurants nach durchschnittlichem Rating

Berechnet den Durchschnitt aller Bewertungen pro Restaurant und gibt die besten 3 Restaurants aus.

Beispielausgabe:

```
Top 3 Restaurants nach durchschnittlichem Rating:
1. Juice It Health Bar - Durchschnittsrating: 75.00
2. Golden Dragon Cuisine - Durchschnittsrating: 73.00
3. Palombo Pastry Shop - Durchschnittsrating: 69.00
```

### 3. Nächstgelegenes Restaurant zu 'Le Perigord'

- Findet ein Restaurant namens **Le Perigord**
- Sucht das am nächsten gelegene Restaurant mithilfe von `2dsphere`-Geodaten
- Gibt den Namen und die Entfernung in Metern aus

Beispiel:

```
Das Restaurant 'Subway' ist am nächsten zu 'Le Perigord'
Entfernung: 55.30 Meter
```

### 4. Restaurants suchen

Führt eine Suche nach Name und/oder Küche durch (regex-basiert, Groß-/Kleinschreibung wird ignoriert).

Beispiel:

```
Name des Restaurants: Le Perigord
Küche:
Suchergebnisse:
1. Le Perigord - French
```

### 5. Restaurant bewerten

- Suche nach Restaurant (wie in Punkt 4)
- Gib eine Bewertung (0–100) ein
- Daraus wird automatisch ein `grade` berechnet:
  - A: 75–100
  - B: 50–74
  - C: 0–49
- Fügt das Bewertungsobjekt zum `grades`-Array des Restaurants hinzu

Beispiel:

```
Bewertung (0-100): 66
Bewertung für Le Perigord erfolgreich hinzugefügt.
```

### 6. Beenden

Beendet die Anwendung.

## Klassenübersicht

### `RestaurantExplorer`

Zentrale Klasse zur Verwaltung der MongoDB-Datenbank.

**Methodenübersicht:**

| Methode                                | Beschreibung                                                            |
|----------------------------------------|-------------------------------------------------------------------------|
| `__init__()`                           | Initialisiert Verbindung zur MongoDB                                   |
| `display_unique_boroughs()`           | Gibt alle einzigartigen Stadtbezirke aus                               |
| `display_top_3_restaurants_by_avg_score()` | Gibt die Top 3 Restaurants basierend auf durchschnittlichem Score aus |
| `find_nearest_restaurant_to_le_perigord()` | Findet das nächste Restaurant zu „Le Perigord“                        |
| `search_restaurants()`                | Interaktive Suche nach Namen/Küche                                     |
| `add_rating_to_restaurant()`          | Bewertet ein Restaurant nach Auswahl                                   |
| `main_menu()`                         | Führt das Hauptmenü aus                                                |

## Beispiel-Dokumentstruktur (MongoDB)

```json
{
  "_id": ObjectId("..."),
  "name": "Le Perigord",
  "borough": "Manhattan",
  "cuisine": "French",
  "address": {
    "building": "405",
    "street": "E 52nd St",
    "zipcode": "10022",
    "coord": [-73.9675, 40.7595]
  },
  "grades": [
    {
      "date": ISODate("2023-07-15T00:00:00Z"),
      "grade": "B",
      "score": 66
    }
  ]
}
```

## Beispielhafte Anwendungsausgabe

```
--- Restaurant-Datenbank ---
1. Alle Stadtbezirke anzeigen
2. Top 3 Restaurants nach Rating anzeigen
3. Nächstgelegenes Restaurant zu 'Le Perigord' finden
4. Restaurants suchen
5. Restaurant bewerten
6. Beenden
Auswahl: 1

Einzigartige Stadtbezirke:
- Bronx
- Brooklyn
- Manhattan
- Missing
- Queens
- Staten Island
```

## Autor

Tobias Clausen  
MacBook Pro – Python CLI MongoDB Projekt
