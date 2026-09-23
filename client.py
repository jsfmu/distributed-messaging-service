import socket

HOST = "127.0.0.1"
PORT = 5001


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to Mini Discord TCP server
        client_socket.connect((HOST, PORT))
        print(f"Connected to Mini Discord server at {HOST}:{PORT}")

        while True:
            command = input("> ")

            # Don't send an empty command
            if not command.strip():
                continue

            # Send command to server
            client_socket.sendall(command.encode("utf-8"))

            # Optional local exit command
            if command.lower() == "quit":
                break

            # Wait for response from server
            response = client_socket.recv(4096)

            # recv() returning b"" means the server disconnected
            if not response:
                print("Server disconnected.")
                break

            print(response.decode("utf-8"))

    except ConnectionRefusedError:
        print("Could not connect to the server.")

    except ConnectionResetError:
        print("Connection to server was lost.")

    except KeyboardInterrupt:
        print("\nClosing client.")

    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()