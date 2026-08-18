import socket
import threading
import main


HOST = "127.0.0.1"
PORT = 6379


def handle_client(client, address):

    print(f"Client connected: {address}")

    while True:

        data = client.recv(1024)

        if not data:
            print(f"Client disconnected: {address}")
            break

        text = data.decode().strip()

        if not text:
            continue

        print(f"Received from {address}: {text}")

        result = main.process_command(text)

        print(f"Result for {address}: {result}")

        client.send(str(result).encode())

    client.close()


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))

server.listen()

print(f"HODOR is running on {HOST}:{PORT}")


while True:

    client, address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client, address)
    )

    thread.start()