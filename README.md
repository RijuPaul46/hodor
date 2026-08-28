# Hodor

A Redis-inspired in-memory key-value database built from scratch in Python, focusing on
data structures, memory management, networking, serialization, expiration, concurrency,
and persistence.

Hodor provides a TCP client-server interface, a custom Hodor Serialization Protocol (HSP),
multiple data types, O(1) LRU eviction, TTL-based expiration, Sorted Sets implemented
using a Skip List, and Append-Only File (AOF) persistence with command replay and recovery.

---

## Features

### Core Data Types

Hodor supports the following data types:

- String
- Hash
- List
- Set
- Sorted Set

Commands are implemented through a modular command execution layer that separates command
handling from the underlying database engine.

---

## Memory Management

Hodor implements configurable memory capacity with **O(1) LRU eviction**.

The LRU cache combines:

- HashMap for O(1) key-to-node lookup
- Doubly Linked List for maintaining MRU/LRU ordering

The most recently used key is maintained at the front of the list, while the least
recently used key is maintained at the tail.

When the database exceeds its configured capacity, the key at the tail is evicted.

### Complexity

| Operation | Complexity |
|-----------|------------|
| Key lookup | O(1) average |
| Move key to MRU | O(1) |
| Remove LRU key | O(1) |

---

## TTL-Based Key Expiration

Hodor supports key expiration using TTL.

Expiration is handled using two mechanisms:

### Lazy Expiration

When a key is accessed, Hodor checks whether its expiration time has passed.

If the key has expired, it is deleted before returning the result.

### Active Expiration

A background worker continuously checks for keys whose expiration time has arrived
and removes them automatically.

A **min-heap** is used to efficiently identify the key with the earliest expiration time.

Expiration entries contain:

```text
(expiration_time, version, key)