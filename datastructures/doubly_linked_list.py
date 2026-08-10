class Node:
    def __init__(self, key, value):
        self.key = key                # Dictionary key
        self.value = value            # RedisObject

        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = Node(None,None)             # Dummy Node at begin
        self.tail = Node(None,None)             # Dummy Node at end
        self.head.next=self.tail 
        self.tail.prev=self.head            
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def add_to_front(self, node):
        """
        Insert node just after the Head.
        """

        temp=self.head.next
        temp.prev=node
        node.next=temp
        self.head.next=node
        node.prev=self.head
        self.size += 1

    def remove(self, node):
        """
        Remove any node inside the list.
        """

        if node is None:
            return

        prev=node.prev
        next=node.next
        prev.next=next
        next.prev=prev
        node.next=None
        node.prev=None
        self.size -= 1

    def move_to_front(self, node):
        """
        Move an existing node to the head.
        """

        if node == self.head.next:
            return

        self.remove(node)
        self.add_to_front(node)

    def remove_tail(self):
        """
        Remove and return the least recently used node.
        """
        if self.size==0:
            return None

        old_tail = self.tail.prev
        self.remove(old_tail)
        return old_tail

    def print_list(self):
        """
        Utility function for debugging.
        """

        cur = self.head.next

        while cur != self.tail:
            print(cur.key, end="")
            cur = cur.next
            if cur != self.tail:
                print(" <-> ", end="")
            print()