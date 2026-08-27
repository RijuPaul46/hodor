from datastructures.sorted_set import SortedSet


class SortedSetCommands:

    def __init__(self, db):

        self.db = db

        # key -> SortedSet
        self.sorted_sets = {}

    # --------------------------------------------------
    # ZADD key score member
    # --------------------------------------------------

    def zadd(self, key, score, member):

        score = float(score)

        if key not in self.sorted_sets:

            self.sorted_sets[key] = SortedSet()

        zset = self.sorted_sets[key]

        return zset.add(
            member,
            score
        )

    # --------------------------------------------------
    # ZSCORE key member
    # --------------------------------------------------

    def zscore(self, key, member):

        zset = self.sorted_sets.get(key)

        if zset is None:

            return None

        return zset.score(
            member
        )

    # --------------------------------------------------
    # ZREM key member
    # --------------------------------------------------

    def zrem(self, key, member):

        zset = self.sorted_sets.get(key)

        if zset is None:

            return 0

        result = zset.remove(
            member
        )

        # If SortedSet becomes empty,
        # remove the entire key.
        if len(zset.member_to_score) == 0:

            del self.sorted_sets[key]

        return result

    # --------------------------------------------------
    # ZRANGE key start stop
    # --------------------------------------------------

    def zrange(self, key, start, stop):

        zset = self.sorted_sets.get(key)

        if zset is None:

            return []

        start = int(start)
        stop = int(stop)

        return zset.range(
            start,
            stop
        )