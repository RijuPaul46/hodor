from datastructures.doubly_linked_list import Node
from datastructures.doubly_linked_list import DoublyLinkedList


class Database:
    def __init__(self, capacity):
        self.capacity = capacity
        self.store = {}
        self.dll = DoublyLinkedList()

    def set(self, key, redis_object):

        # ----------------------------
        # Key already exists
        # ----------------------------
        if key in self.store:

            node = self.store[key]

            # Update the value
            node.value = redis_object

            # Recently used
            self.dll.move_to_front(node)

            return

        # ----------------------------
        # Memory full
        # ----------------------------
        if self.dll.size == self.capacity:

            victim = self.dll.remove_tail()

            if victim is not None:
                del self.store[victim.key]

        # ----------------------------
        # Insert new key
        # ----------------------------
        node = Node(key, redis_object)

        self.dll.add_to_front(node)

        self.store[key] = node

    def get(self, key):

        if key not in self.store:
            return None

        node = self.store[key]

        # Mark as recently used
        self.dll.move_to_front(node)

        return node.value

    def delete(self, key):

        if key not in self.store:
            return 0

        node = self.store[key]

        self.dll.remove(node)

        del self.store[key]

        return 1

    def exists(self, key):
        return key in self.store

    def size(self):
        return len(self.store)

    def print_lru(self):
        self.dll.print_list()