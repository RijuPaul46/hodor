from objects.redis_object import RedisObject


class StringCommands:

    def __init__(self, db):
        self.db = db

    def set(self, *args):

        if len(args) < 2:
            return "ERR wrong number of arguments"

        key = args[0]
        value = args[1]

        ttl = None

        # SET key value EX seconds
        if len(args) > 2:

            if len(args) != 4:
                return "ERR syntax error"

            if args[2].upper() != "EX":
                return "ERR syntax error"

            try:
                ttl = int(args[3])
            except ValueError:
                return "ERR invalid TTL"

            if ttl <= 0:
                return "ERR invalid TTL"

        obj = RedisObject(
            "STRING",
            value
        )

        self.db.set(
            key,
            obj,
            ttl
        )

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