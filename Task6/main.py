from room import Room
from dao_room import Dao_room

import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

env_connection_string = os.getenv('connection_string')

dao_room = Dao_room(env_connection_string)

room_create = Room("Matterhorn", 12, True)
dao_room.create(room_create)

room_read = dao_room.read()
print("Gelesener Raum:")
print(vars(room_read))

if hasattr(room_read, "_id"):
    update_fields = {"seats": 20, "is_reservable": False}
    dao_room.update(room_read._id, update_fields)
    print("\nRaum wurde aktualisiert.")

    updated_room = dao_room.read()
    print("Aktualisierter Raum:")
    print(vars(updated_room))

if hasattr(room_read, "_id"):
    dao_room.delete(room_read._id)
    print("\nRaum wurde gelöscht.")
