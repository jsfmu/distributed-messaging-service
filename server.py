import socket

HOST = "127.0.0.1"
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()

    print(f"Client connected: {client_address}")

    while True:
        data = client_socket.recv(4096)

        if not data:
            break

        message = data.decode("utf-8")
        print(f"Received: {message}")

        response = f"Server received: {message}"
        client_socket.sendall(response.encode("utf-8"))

    client_socket.close()