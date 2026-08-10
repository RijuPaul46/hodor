from objects.hash_object import HashObject
from objects.redis_object import RedisObject


class HashCommands:

    def __init__(self, db):
        self.db = db

    def hset(self, key, field, value):

        obj = self.db.get(key)

        if obj is None:

            hash_object = HashObject()

            hash_object.set(field, value)

            redis_object = RedisObject(
                "HASH",
                hash_object
            )

            self.db.set(key, redis_object)

        else:

            if obj.type != "HASH":
                return "WRONG TYPE"

            obj.value.set(field, value)

        return "OK"

    def hget(self, key, field):

        obj = self.db.get(key)

        if obj is None:
            return None

        if obj.type != "HASH":
            return "WRONG TYPE"

        return obj.value.get(field)