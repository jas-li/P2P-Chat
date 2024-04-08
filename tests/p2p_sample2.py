import socket
import threading

# Function to handle incoming connections from other peers
def handle_connection(conn, addr):
    print(f"Connected to {addr}")

    connect_to_peer(addr[0], addr[1])

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received message from {addr}: {data.decode()}")

    conn.close()
    print(f"Connection with {addr} closed")

# Function to connect to a peer
def connect_to_peer():
    peer_ip = input("Enter the IP address of the peer: ")
    peer_port = int(input("Enter the port number of the peer: "))

    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer_socket.connect((peer_ip, peer_port))
        print("Connected to peer successfully!")
        while True:
            message = input("Enter message to send: ")
            peer_socket.sendall(message.encode())
    except ConnectionRefusedError:
        print("Connection refused. Peer may not be available.")
    finally:
        peer_socket.close()

def main():
    # Start a thread for connecting to a peer
    connect_thread = threading.Thread(target=connect_to_peer)
    connect_thread.start()

    # Initialize socket for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12340))
    server_socket.listen(5)
    print("Listening for incoming connections...")

    while True:
        # Accept incoming connections
        conn, addr = server_socket.accept()
        # Start a new thread to handle the connection
        conn_thread = threading.Thread(target=handle_connection, args=(conn, addr))
        conn_thread.start()

if __name__ == "__main__":
    main()
