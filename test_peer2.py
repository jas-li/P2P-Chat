import socket
import json
import time
import threading

def register_with_server(server_ip, server_port, peer_id, ip_address, peer_port):
    """
    Registers the peer with the discovery server.
    
    :param server_ip: The IP address of the discovery server.
    :param server_port: The port number of the discovery server.
    :param peer_id: A unique identifier for the peer.
    :param ip_address: The IP address of the peer.
    :param port: port
    """
    # Construct the registration message
    message = json.dumps({
        'type': 'register',
        'peer_id': peer_id,
        'ip_address': ip_address,
        'port': peer_port,
        'timestamp': time.time()
    })

    # Connect to the discovery server and send the registration message
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))
        sock.sendall(message.encode('utf-8'))

def query_peer(server_ip, server_port, query_id):
    query_message = json.dumps({
        'type': 'query',
        'peer_id': 'my_peer123',  # This could be used by the server for logging or authentication.
        'query_id': query_id  # The ID of the peer we're asking about.
    })

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))
        sock.sendall(query_message.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')  # Assuming the response is not longer than 1024 bytes
        
        # Parse the server's response
        response_data = json.loads(response)
        return response_data  # This might include the peer's IP address, status, etc.

def get_users(server_ip, server_port):
    query_message = json.dumps({
        'type': 'query-all',
    })

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))
        sock.sendall(query_message.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')  # Assuming the response is not longer than 1024 bytes
        
        # Parse the server's response
        response_data = json.loads(response)
        return response_data 

def send_keep_alive(server_ip, server_port, peer_id, ip_address, peer_port):
    message = json.dumps({
        'type': 'keep_alive',
        'peer_id': peer_id,
        'ip_address': ip_address,
        'port': peer_port,
        'timestamp': time.time()
    })

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))
        sock.sendall(message.encode('utf-8'))

def start_keep_alive_scheduler(server_ip, server_port, peer_id, peer_ip, peer_port, interval=10):
    def scheduler():
        while True:
            send_keep_alive(server_ip, server_port, peer_id, peer_ip, peer_port)
            time.sleep(interval)
    
    threading.Thread(target=scheduler, daemon=True).start()

def start_peer_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    
    def handle_peer_connection(client_socket):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"New message: {message}")
                else:
                    break
        finally:
            client_socket.close()

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_peer_connection, args=(client_socket,)).start()

def run_peer_server(host, port):
    threading.Thread(target=start_peer_server, args=(host, port), daemon=True).start()

def send_message_to_peer(peer_ip, peer_port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((peer_ip, peer_port))
        sock.sendall(message.encode('utf-8'))

def main():
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 12345
    PEER_IP = '0.0.0.0'
    PEER_PORT = 54320  
    username = input("Please enter a username: ")

    register_with_server(SERVER_IP, SERVER_PORT, username, PEER_IP, PEER_PORT)
    print(f"\nUser {username} registered with the discovery server at {SERVER_IP}:{SERVER_PORT}\n")

    start_keep_alive_scheduler(SERVER_IP, SERVER_PORT, username, PEER_IP, PEER_PORT)

    while True:

        choice = input("Choose an action:\n1. Connect to a user\n2. List active users\nEnter your choice (1 or 2): ")

        if choice == "1": 
            peer_connect = input("Which user would you like to connect to?\nEnter their username: ")
            peer_info = query_peer(SERVER_IP, SERVER_PORT, peer_connect)
            if peer_info:
                peer_ip, peer_port = peer_info[0], peer_info[1]
                message = input("Enter your message: ")
                send_message_to_peer(peer_ip, peer_port, message)
            else:
                print("\nUser does not exist.\n")
            
        elif choice == "2":
            list_users = get_users(SERVER_IP, SERVER_PORT)
            if list_users:
                print('\n', list(list_users.keys()), '\n')
            else:
                print("Failed to retrieve information about the active users.")
        
if __name__ == '__main__':
    main()
