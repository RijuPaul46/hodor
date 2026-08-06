from storage.database import Database
from objects.redis_object import RedisObject

db = Database()

obj = RedisObject("STRING", "Riju")

db.set("name", obj)

print(db.get("name").value)
print(db.delete("name"))
print(db.get("name"))