from datastructures.sorted_set import SortedSet


class SortedSetCommands:

    def __init__(self, db):

        self.db = db

    # --------------------------------------------------
    # Get existing SortedSet
    # --------------------------------------------------

    def _get_zset(self, key):

        node = self.db.store.get(key)

        if node is None:
            return None

        return node.value

    # --------------------------------------------------
    # ZADD key score member
    # --------------------------------------------------

    def zadd(self, key, score, member):

        score = float(score)

        node = self.db.store.get(key)

        # ----------------------------------------------
        # Create SortedSet if key doesn't exist
        # ----------------------------------------------

        if node is None:

            zset = SortedSet()

            node = Node(
                key,
                zset
            )

            self.db.store[key] = node

            self.db.lru.add_to_front(node)

        else:

            zset = node.value

            if not isinstance(zset, SortedSet):

                return "WRONGTYPE"

            self.db.lru.move_to_front(node)

        # ----------------------------------------------
        # Add member
        # ----------------------------------------------

        return zset.add(
            member,
            score
        )

    # --------------------------------------------------
    # ZSCORE key member
    # --------------------------------------------------

    def zscore(self, key, member):

        zset = self._get_zset(key)

        if zset is None:

            return None

        if not isinstance(zset, SortedSet):

            return "WRONGTYPE"

        return zset.score(
            member
        )

    # --------------------------------------------------
    # ZREM key member
    # --------------------------------------------------

    def zrem(self, key, member):

        zset = self._get_zset(key)

        if zset is None:

            return 0

        if not isinstance(zset, SortedSet):

            return "WRONGTYPE"

        result = zset.remove(
            member
        )

        # ----------------------------------------------
        # SortedSet became empty
        # ----------------------------------------------

        if len(zset.member_to_score) == 0:

            self.db.delete(key)

        return result

    # --------------------------------------------------
    # ZRANGE key start stop
    # --------------------------------------------------

    def zrange(self, key, start, stop):

        zset = self._get_zset(key)

        if zset is None:

            return []

        if not isinstance(zset, SortedSet):

            return "WRONGTYPE"

        return zset.range(
            int(start),
            int(stop)
        )