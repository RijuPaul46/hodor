from objects.redis_object import RedisObject


class StringCommands:

    def __init__(self, db):
        self.db = db

    def set(self, key, value):

        obj = RedisObject(
            "STRING",
            value
        )

        self.db.set(key, obj)

        return "OK"

    def get(self, key):

        obj = self.db.get(key)

        if obj is None:
            return None

        if obj.type != "STRING":
            return "WRONG TYPE"

        return obj.value

    def delete(self, key):

        return self.db.delete(key)