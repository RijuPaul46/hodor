from storage.database import Database


def mutation_listener(command):

    print(
        "MUTATION:",
        command.command,
        command.arguments
    )


db = Database(
    capacity=2
)

db.set_mutation_callback(
    mutation_listener
)


print("\n--- SET A ---")

db.set(
    "A",
    "10"
)


print("\n--- SET B ---")

db.set(
    "B",
    "20"
)


print("\n--- SET C ---")

db.set(
    "C",
    "30"
)


print("\n--- GET B ---")

db.get("B")


print("\n--- SET D ---")

db.set(
    "D",
    "40"
)