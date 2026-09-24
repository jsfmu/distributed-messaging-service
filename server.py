import socket
import threading
import json

from store import users


HOST = "127.0.0.1"
PORT = 5001


def handle_client(client_socket, client_address):

    print(f"Client connected: {client_address}")

    try:

        while True:

            # Receive data from client
            data = client_socket.recv(1024)

            # Client disconnected
            if not data:
                break

            # Convert bytes into a string
            message = data.decode("utf-8").strip()

            print(f"{client_address}: {message}")

            # Split command into pieces
            #
            # "REGISTER joe"
            #
            # becomes:
            #
            # ["REGISTER", "joe"]

            parts = message.split()

            # Empty command
            if not parts:
                continue

            command = parts[0].upper()

            # --------------------------------
            # REGISTER <username>
            # --------------------------------

            if command == "REGISTER":

                # Make sure username was provided
                if len(parts) != 2:

                    response = {
                        "status": "error",
                        "message": "Usage: REGISTER <username>"
                    }

                else:

                    username = parts[1]

                    # Check if user already exists
                    if username in users:

                        response = {
                            "status": "error",
                            "message": "Username already exists"
                        }

                    else:

                        # Add user to shared state
                        users[username] = {
                            "username": username
                        }

                        response = {
                            "status": "ok",
                            "username": username
                        }

            # --------------------------------
            # Unknown command
            # --------------------------------

            else:

                response = {
                    "status": "error",
                    "message": "Unknown command"
                }

            # Convert dictionary → JSON
            response_json = json.dumps(response)

            # Send response to client
            client_socket.sendall(
                (response_json + "\n").encode("utf-8")
            )

    except ConnectionResetError:

        print(f"Client connection lost: {client_address}")

    finally:

        client_socket.close()

        print(f"Client disconnected: {client_address}")


# --------------------------------
# Create TCP server socket
# --------------------------------

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


# --------------------------------
# Bind
# --------------------------------

server_socket.bind((HOST, PORT))


# --------------------------------
# Listen
# --------------------------------

server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")


# --------------------------------
# Accept clients
# --------------------------------

while True:

    client_socket, client_address = server_socket.accept()

    # Give each client its own thread
    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    client_thread.start()