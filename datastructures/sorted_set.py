from datastructures.skip_list import SkipList


class SortedSet:

    def __init__(self):

        # member -> score
        self.member_to_score = {}

        # Stores (score, member) in sorted order
        self.skip_list = SkipList()

    # --------------------------------------------------
    # ZADD
    # --------------------------------------------------

    def add(self, member, score):

        is_new = member not in self.member_to_score

        if not is_new:

            old_score = self.member_to_score[member]

            if old_score == score:
                return 0

            self.skip_list.delete(
                old_score,
                member
            )

        self.member_to_score[member] = score

        self.skip_list.insert(
            score,
            member
        )

        return 1 if is_new else 0

    # --------------------------------------------------
    # ZSCORE
    # --------------------------------------------------

    def score(self, member):

        return self.member_to_score.get(
            member
        )

    # --------------------------------------------------
    # ZREM
    # --------------------------------------------------

    def remove(self, member):

        if member not in self.member_to_score:

            return 0

        score = self.member_to_score[member]

        self.skip_list.delete(
            score,
            member
        )

        del self.member_to_score[member]

        return 1

    # --------------------------------------------------
    # ZRANGE
    # --------------------------------------------------

    def range(self, start, stop):

        items = list(
            self.skip_list.items()
        )

        # Redis-style negative indexes
        n = len(items)

        if start < 0:
            start = n + start

        if stop < 0:
            stop = n + stop

        # Clamp boundaries
        start = max(
            start,
            0
        )

        stop = min(
            stop,
            n - 1
        )

        if start > stop or start >= n:

            return []

        return [
            member
            for score, member
            in items[start:stop + 1]
        ]