import socket

from protocol.hsp_encoder import HSPEncoder
from protocol.hsp_parser import HSPParser


HOST = "127.0.0.1"
PORT = 6379


client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))


parser = HSPParser()


while True:

    text = input("Hodor> ")

    if text.lower() == "exit":
        break

    # ------------------------------------------
    # Convert user input into command parts
    # ------------------------------------------

    tokens = text.split()

    if not tokens:
        continue

    # ------------------------------------------
    # Convert command into HSP array
    # ------------------------------------------

    request = HSPEncoder.array(tokens)

    print("Sending:", request)

    # ------------------------------------------
    # Send HSP bytes
    # ------------------------------------------

    client.sendall(request)

    # ------------------------------------------
    # Receive response
    # ------------------------------------------

    while True:

        data = client.recv(1024)

        if not data:
            print("Server disconnected")
            break

        responses = parser.feed(data)

        if not responses:
            continue

        for response in responses:

            print("Response:", response)

        break


client.close()