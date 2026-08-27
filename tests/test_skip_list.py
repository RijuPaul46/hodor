from datastructures.skip_list import SkipList


sl = SkipList()

sl.insert(100, "Riju")
sl.insert(100, "Aman")
sl.insert(150, "Rahul")
sl.insert(250, "Karan")
sl.insert(100, "Zoya")
sl.insert(100,"Riju")


print("Sorted:")

for score, member in sl.items():

    print(score, member)


print("\nSearch:")

node = sl.search(150, "Rahul")

print(node.score, node.member)


print("\nDelete:")

print(
    sl.delete(
        100,
        "Aman"
    )
)


print("\nAfter deletion:")

for score, member in sl.items():

    print(score, member)