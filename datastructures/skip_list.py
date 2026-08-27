import random


class SkipListNode:

    def __init__(self, score, member, height):

        self.score = score
        self.member = member

        # forward[i] = next node at level i
        self.forward = [None] * height


class SkipList:

    MAX_LEVEL = 16
    P = 0.5

    def __init__(self):

        # Number of levels currently being used
        self.level = 1

        # Dummy head
        self.head = SkipListNode(
            float("-inf"),
            "",
            self.MAX_LEVEL
        )

    # --------------------------------------------------
    # Decide random height for a new node
    # --------------------------------------------------

    def random_height(self):

        height = 1

        while (
            height < self.MAX_LEVEL
            and random.random() < self.P
        ):
            height += 1

        return height

    # --------------------------------------------------
    # Compare two (score, member) pairs
    # --------------------------------------------------

    def less(self, score1, member1, score2, member2):

        if score1 != score2:

            return score1 < score2

        return member1 < member2

    # --------------------------------------------------
    # INSERT
    # --------------------------------------------------

    def insert(self, score, member):

        # update[i] will contain the predecessor
        # of the new node at level i
        update = [None] * self.MAX_LEVEL

        current = self.head

        # ----------------------------------------------
        # Find predecessor at every level
        # ----------------------------------------------

        for level in range(
            self.level - 1,
            -1,
            -1
        ):

            while (
                current.forward[level] is not None
                and self.less(
                    current.forward[level].score,
                    current.forward[level].member,
                    score,
                    member
                )
            ):

                current = current.forward[level]

            update[level] = current

        # ----------------------------------------------
        # Check duplicate
        # ----------------------------------------------

        next_node = update[0].forward[0]

        if (
            next_node is not None
            and next_node.score == score
            and next_node.member == member
        ):

            return False

        # ----------------------------------------------
        # Generate height
        # ----------------------------------------------

        height = self.random_height()

        # If new node is taller than current Skip List
        if height > self.level:

            for level in range(
                self.level,
                height
            ):

                update[level] = self.head

            self.level = height

        # ----------------------------------------------
        # Create node
        # ----------------------------------------------

        new_node = SkipListNode(
            score,
            member,
            height
        )

        # ----------------------------------------------
        # Connect new node
        # ----------------------------------------------

        for level in range(height):

            new_node.forward[level] = (
                update[level].forward[level]
            )

            update[level].forward[level] = new_node

        return True

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def search(self, score, member):

        current = self.head

        # Start from highest level
        for level in range(
            self.level - 1,
            -1,
            -1
        ):

            while (
                current.forward[level] is not None
                and self.less(
                    current.forward[level].score,
                    current.forward[level].member,
                    score,
                    member
                )
            ):

                current = current.forward[level]

        # Candidate at level 0
        current = current.forward[0]

        if (
            current is not None
            and current.score == score
            and current.member == member
        ):

            return current

        return None

    # --------------------------------------------------
    # DELETE
    # --------------------------------------------------

    def delete(self, score, member):

        update = [None] * self.MAX_LEVEL

        current = self.head

        # ----------------------------------------------
        # Find predecessor at every level
        # ----------------------------------------------

        for level in range(
            self.level - 1,
            -1,
            -1
        ):

            while (
                current.forward[level] is not None
                and self.less(
                    current.forward[level].score,
                    current.forward[level].member,
                    score,
                    member
                )
            ):

                current = current.forward[level]

            update[level] = current

        # Candidate
        current = current.forward[0]

        # ----------------------------------------------
        # Not found
        # ----------------------------------------------

        if (
            current is None
            or current.score != score
            or current.member != member
        ):

            return False

        # ----------------------------------------------
        # Remove from every level
        # ----------------------------------------------

        for level in range(self.level):

            if update[level].forward[level] != current:

                break

            update[level].forward[level] = (
                current.forward[level]
            )

        # ----------------------------------------------
        # Remove empty upper levels
        # ----------------------------------------------

        while (
            self.level > 1
            and self.head.forward[self.level - 1] is None
        ):

            self.level -= 1

        return True

    # --------------------------------------------------
    # Iterate everything in sorted order
    # --------------------------------------------------

    def items(self):

        current = self.head.forward[0]

        while current is not None:

            yield (
                current.score,
                current.member
            )

            current = current.forward[0]