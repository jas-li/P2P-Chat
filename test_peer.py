import socket
import json
import time

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

def query_peer(server_ip, server_port):
    query_message = json.dumps({
        'type': 'query',
        'peer_id': 'my_peer123',  # This could be used by the server for logging or authentication.
        'query_id': 'testpeer'  # The ID of the peer we're asking about.
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

def send_keep_alive(server_ip, server_port, peer_id):
    message = json.dumps({
        'type': 'keep_alive',
        'peer_id': peer_id,
        'timestamp': time.time()
    })

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))
        sock.sendall(message.encode('utf-8'))

def main():
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 12345
    PEER_IP = '192.168.1.2'
    PEER_PORT = 54321  
    username = input("Please enter a username: ")

    register_with_server(SERVER_IP, SERVER_PORT, username, PEER_IP, PEER_PORT)
    print(f"User {username} registered with the discovery server at {SERVER_IP}:{SERVER_PORT}")

    while True:
        send_keep_alive(SERVER_IP, SERVER_PORT, username)
        choice = input("Choose an action:\n1. Connect to a user\n2. List active users\nEnter your choice (1 or 2): ")

        if choice == "1": 
            peer_connect = input("Which user would you like to connect to?\nEnter their username: ")
            
        elif choice == "2":
            list_users = get_users(SERVER_IP, SERVER_PORT)
            if list_users:
                print(list(list_users.keys()))
            else:
                print("Failed to retrieve information about the active users.")
        
if __name__ == '__main__':
    main()
