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

            # Don't send empty commands
            if not command.strip():
                continue

            # Send newline-delimited command
            client_socket.sendall(
                (command + "\n").encode("utf-8")
            )

            # Local exit command
            if command.lower() == "quit":
                break

            # Wait for server response
            response = client_socket.recv(4096)

            # b"" means the server disconnected
            if not response:
                print("Server disconnected.")
                break

            print(response.decode("utf-8").strip())

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