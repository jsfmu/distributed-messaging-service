import socket

HOST = "127.0.0.1"
PORT = 9000


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

client_socket.sendall(b"REGISTER joseph\n")

response = client_socket.recv(1024)

print(response.decode())

client_socket.close()