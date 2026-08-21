import socket
import main


HOST = "127.0.0.1"
PORT = 6379


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))
server.listen()

print(f"HODOR is running on {HOST}:{PORT}")


while True:

    client, address = server.accept()

    print(f"Client connected: {address}")

    while True:

        data = client.recv(1024)

        if not data:
            break

        response = main.process_data(data)

        if response is not None:
            client.sendall(response)

    client.close()

    print(f"Client disconnected: {address}")