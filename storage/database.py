import threading
import time
import heapq

from datastructures.doubly_linked_list import (
    Node,
    DoublyLinkedList
)

from engine.command import Command


class Database:

    def __init__(self, capacity=1000):

        # --------------------------------------------------
        # Main storage
        # key -> Node
        # --------------------------------------------------

        self.store = {}

        # --------------------------------------------------
        # LRU
        # --------------------------------------------------

        self.capacity = capacity
        self.lru = DoublyLinkedList()

        # --------------------------------------------------
        # TTL
        # key -> expiry timestamp
        # --------------------------------------------------

        self.expiry = {}

        # --------------------------------------------------
        # Min heap
        # (expiry_time, version, key)
        # --------------------------------------------------

        self.expiry_heap = []

        # --------------------------------------------------
        # Expiry version
        # Used to invalidate old heap entries
        # --------------------------------------------------

        self.expiry_version = {}

        # --------------------------------------------------
        # Thread safety
        # --------------------------------------------------

        self.lock = threading.Lock()

        # --------------------------------------------------
        # Mutation callback
        #
        # Somebody outside the database can register a
        # function here.
        #
        # Example:
        #
        # db.set_mutation_callback(my_function)
        #
        # Whenever Database internally deletes something
        # because of eviction/TTL, we can notify that function.
        # --------------------------------------------------

        self.on_mutation = None

        # --------------------------------------------------
        # Expiry worker
        # --------------------------------------------------

        self.expiry_thread = threading.Thread(
            target=self._expiry_worker,
            daemon=True
        )

        self.expiry_thread.start()

    # ======================================================
    # MUTATION CALLBACK
    # ======================================================

    def set_mutation_callback(self, callback):

        self.on_mutation = callback

    def _notify_mutation(self, command):

        if self.on_mutation is not None:

            self.on_mutation(command)

    # ======================================================
    # SET
    # ======================================================

    def set(self, key, value, ttl=None):

        mutation = None

        with self.lock:

            # --------------------------------------------------
            # Existing key
            # --------------------------------------------------

            if key in self.store:

                node = self.store[key]

                node.value = value

                self.lru.move_to_front(node)

            # --------------------------------------------------
            # New key
            # --------------------------------------------------

            else:

                node = Node(
                    key,
                    value
                )

                self.store[key] = node

                self.lru.add_to_front(node)

            # --------------------------------------------------
            # TTL handling
            # --------------------------------------------------

            if ttl is not None:

                expires_at = (
                    time.monotonic() + ttl
                )

                self.expiry[key] = expires_at

                version = (
                    self.expiry_version.get(
                        key,
                        0
                    ) + 1
                )

                self.expiry_version[key] = version

                heapq.heappush(
                    self.expiry_heap,
                    (
                        expires_at,
                        version,
                        key
                    )
                )

            else:

                # SET without TTL means
                # key lives forever.

                self.expiry.pop(
                    key,
                    None
                )

                self.expiry_version[key] = (
                    self.expiry_version.get(
                        key,
                        0
                    ) + 1
                )

            # --------------------------------------------------
            # LRU eviction
            # --------------------------------------------------

            if len(self.store) > self.capacity:

                old_node = self.lru.remove_tail()

                if old_node is not None:

                    old_key = old_node.key

                    del self.store[old_key]

                    self.expiry.pop(
                        old_key,
                        None
                    )

                    self.expiry_version[old_key] = (
                        self.expiry_version.get(
                            old_key,
                            0
                        ) + 1
                    )

                    # We DON'T call the callback while
                    # holding the database lock.
                    #
                    # We only remember what happened.
                    mutation = Command(
                        "DEL",
                        [old_key]
                    )

        # --------------------------------------------------
        # Database lock has now been released.
        #
        # Now it is safe to notify outside systems.
        # --------------------------------------------------

        if mutation is not None:

            self._notify_mutation(mutation)

        # Return the evicted key because your existing
        # tests/useful logic may depend on it.
        if mutation is not None:

            return mutation.arguments[0]

        return None

    # ======================================================
    # GET
    # ======================================================

    def get(self, key):

        with self.lock:

            node = self.store.get(key)

            if node is None:

                return None

            # --------------------------------------------------
            # Check expiration
            # --------------------------------------------------

            if self._is_expired(key):

                self._delete_no_lock(key)

                return None

            # --------------------------------------------------
            # Mark as recently used
            # --------------------------------------------------

            self.lru.move_to_front(node)

            return node.value

    # ======================================================
    # DELETE
    # ======================================================

    def delete(self, key):

        with self.lock:

            if key not in self.store:

                return 0

            self._delete_no_lock(key)

            return 1

    # ======================================================
    # INTERNAL DELETE
    # ======================================================

    def _delete_no_lock(self, key):

        node = self.store.get(key)

        if node is None:

            return False

        self.lru.remove(node)

        del self.store[key]

        self.expiry.pop(
            key,
            None
        )

        # --------------------------------------------------
        # Invalidate old heap entry
        # --------------------------------------------------

        self.expiry_version[key] = (
            self.expiry_version.get(
                key,
                0
            ) + 1
        )

        return True

    # ======================================================
    # EXPIRATION CHECK
    # ======================================================

    def _is_expired(self, key):

        expires_at = self.expiry.get(key)

        if expires_at is None:

            return False

        return (
            time.monotonic() >= expires_at
        )

    # ======================================================
    # EXPIRY WORKER
    # ======================================================

    def _expiry_worker(self):

        while True:

            # --------------------------------------------------
            # Find next expiration
            # --------------------------------------------------

            with self.lock:

                if not self.expiry_heap:

                    sleep_time = 1

                    entry = None

                else:

                    entry = self.expiry_heap[0]

                    expires_at = entry[0]

                    now = time.monotonic()

                    sleep_time = (
                        expires_at - now
                    )

            # --------------------------------------------------
            # Nothing currently needs processing
            # --------------------------------------------------

            if entry is None:

                time.sleep(sleep_time)

                continue

            # --------------------------------------------------
            # Earliest key hasn't expired
            # --------------------------------------------------

            if sleep_time > 0:

                time.sleep(sleep_time)

                continue

            # --------------------------------------------------
            # Earliest key has expired
            # --------------------------------------------------

            mutation = None

            with self.lock:

                if not self.expiry_heap:

                    continue

                expires_at, version, key = (
                    heapq.heappop(
                        self.expiry_heap
                    )
                )

                # --------------------------------------------------
                # Check stale heap entry
                # --------------------------------------------------

                current_version = (
                    self.expiry_version.get(
                        key,
                        0
                    )
                )

                if current_version != version:

                    continue

                current_expiry = (
                    self.expiry.get(key)
                )

                if current_expiry != expires_at:

                    continue

                # --------------------------------------------------
                # Current expiration
                # --------------------------------------------------

                deleted = self._delete_no_lock(
                    key
                )

                if deleted:

                    print(
                        f"Expired key: {key}"
                    )

                    mutation = Command(
                        "DEL",
                        [key]
                    )

            # --------------------------------------------------
            # Lock is released.
            #
            # Notify outside systems now.
            # --------------------------------------------------

            if mutation is not None:

                self._notify_mutation(
                    mutation
                )