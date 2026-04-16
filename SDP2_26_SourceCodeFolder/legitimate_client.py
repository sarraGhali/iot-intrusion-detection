import socket
import sys

def main(client_id):
    # Server address and port
    server_address = ("192.168.0.143",8888)

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(server_address)

    try:
        # Send data to the server
        message = f"Hello, server! I am client {client_id}".encode()
        client_socket.sendall(message)

    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python legitimate_client.py <client_id>")
        sys.exit(1)

    client_id = int(sys.argv[1])
    main(client_id)