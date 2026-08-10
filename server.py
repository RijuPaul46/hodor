import socket
import main


HOST = "127.0.0.1"
PORT = 6379


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))

server.listen(1)

print(f"HODOR is running on {HOST}:{PORT}")

client, address = server.accept()

print(f"Client connected, address: {address}")

data = client.recv(1024)
if not data:
    client.close()
else:

    text = data.decode()

    result = main.process_command(text)

    print(result)

    client.send(result.encode())

    client.close()
    server.close()