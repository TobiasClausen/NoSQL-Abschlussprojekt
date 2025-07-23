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
