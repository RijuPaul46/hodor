from engine.command import Command
from persistence.aof import AOF
from storage.database import Database

db = Database(capacity=2)


db.set("A", 10)
db.set("B", 20)

db.get("A")

evicted = db.set("C", 30)

print("Evicted:", evicted)