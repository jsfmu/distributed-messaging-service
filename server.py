import socket

HOST = "127.0.0.1"
PORT = 9000


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Listening on {HOST}:{PORT}")

client_socket, client_address = server_socket.accept()

print(f"Connected: {client_address}")

data = client_socket.recv(1024)

print(f"Received: {data}")

client_socket.sendall(b'{"status":"ok"}\n')

client_socket.close()
server_socket.close()