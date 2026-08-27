from datastructures.sorted_set import SortedSet


zset = SortedSet()


print(
    "Add Riju:",
    zset.add("Riju", 100)
)

print(
    "Add Aman:",
    zset.add("Aman", 100)
)

print(
    "Add Rahul:",
    zset.add("Rahul", 200)
)

print(
    "Add Karan:",
    zset.add("Karan", 150)
)


print("\nScores:")

print(
    "Riju:",
    zset.score("Riju")
)

print(
    "Rahul:",
    zset.score("Rahul")
)


print("\nRange:")

print(
    zset.range(0, -1)
)


print("\nUpdate Riju:")

print(
    zset.add("Riju", 250)
)


print(
    zset.range(0, -1)
)


print("\nRemove Aman:")

print(
    zset.remove("Aman")
)


print(
    zset.range(0, -1)
)