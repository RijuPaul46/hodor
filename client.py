import socket

HOST = "127.0.0.1"
PORT = 6379

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

command = input("Hodor> ")

client.send(command.encode())

response = client.recv(1024)

print("Response:", response.decode())

client.close()