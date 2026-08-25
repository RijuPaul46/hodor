import socket
import threading
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


def handle_client(client, address):

    print(f"Client connected: {address}")

    # Create ONE session for this connection
    session = main.create_session()

    try:

        while True:

            data = client.recv(1024)

            if not data:
                break

            # Give the data to main
            response = main.process(
                session,
                data
            )

            if response is not None:

                client.sendall(response)

    except ConnectionResetError:

        print(
            f"Connection reset: {address}"
        )

    finally:

        client.close()

        print(
            f"Client disconnected: {address}"
        )


while True:

    client, address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client, address),
        daemon=True
    )

    thread.start()