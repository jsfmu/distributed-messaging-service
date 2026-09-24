import socket
import threading
import json

from store import users
from store import channels


HOST = "127.0.0.1"
PORT = 5001


def handle_client(client_socket, client_address):

    print(f"Client connected: {client_address}")

    # Tracks which user is logged in on THIS connection
    current_user = None

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

            parts = message.split()

            # Empty command
            if not parts:
                continue

            command = parts[0].upper()

            if command == "REGISTER":

                # Make sure username was provided
                if len(parts) != 2:

                    response = {
                        "status": "error",
                        "code": "BAD_REQUEST",
                        "message": "Usage: REGISTER <username>"
                    }

                else:

                    username = parts[1]

                    # Check if user already exists
                    if username in users:

                        response = {
                            "status": "error",
                            "code": "CONFLICT",
                            "message": "Username already exists"
                        }

                    else:

                        # Add user to shared state
                        users[username] = {
                            "username": username
                        }

                        response = {
                            "status": "ok",
                            "operation": "register",
                            "username": username
                        }

            elif command == "LOGIN":

                # Make sure username was provided
                if len(parts) != 2:

                    response = {
                        "status": "error",
                        "code": "BAD_REQUEST",
                        "message": "Usage: LOGIN <username>"
                    }

                else:

                    username = parts[1]

                    # User must already be registered
                    if username not in users:

                        response = {
                            "status": "error",
                            "code": "NOT_FOUND",
                            "message": "User does not exist"
                        }

                    else:

                        # Associate this TCP connection
                        # with this username
                        current_user = username

                        response = {
                            "status": "ok",
                            "operation": "login",
                            "username": username
                        }

            elif command == "JOIN":

                # User must be logged in first
                if current_user is None:

                    response = {
                        "status": "error",
                        "code": "UNAUTHORIZED",
                        "message": "You must login first"
                    }

                elif len(parts) != 2:

                    response = {
                        "status": "error",
                        "code": "BAD_REQUEST",
                        "message": "Usage: JOIN <channel>"
                    }

                else:

                    channel_name = parts[1]

                    # Create the channel if it doesn't exist
                    if channel_name not in channels:

                        channels[channel_name] = {
                            "members": set()
                        }

                    # Add logged-in user to channel
                    channels[channel_name]["members"].add(current_user)

                    response = {
                        "status": "ok",
                        "operation": "join",
                        "channel": channel_name
                    }

            else:

                response = {
                    "status": "error",
                    "code": "BAD_REQUEST",
                    "message": "Unknown command"
                }

            # Convert dictionary -> JSON
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


server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:

    client_socket, client_address = server_socket.accept()

    # Give each client its own thread
    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    client_thread.start()