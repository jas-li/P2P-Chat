from ipaddress import ip_address
import socket
import threading
import json
import time

# Global dictionary to store active peers {peer_id: (ip_address, timestamp)}
registry = {}

def handle_peer(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
        message = json.loads(data)
        # Process registration or keep-alive
        if message['type'] in ['register', 'keep_alive']:
            registry[message['peer_id']] = (message['ip_address'], message['timestamp'])
        elif message['type'] == 'query':
            response = registry.get(message['query_id'], None)
            client_socket.send(json.dumps(response).encode('utf-8'))
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Starting Discovery Server on {}:{}".format(host, port))

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_peer, args=(client_socket,))
        thread.start()

def inactivity_checker(interval=30):
    def run_checker():
        while True:
            current_time = time.time()
            inactive_peers = []
            for peer_id, (ip_address, timestamp) in registry.items():
                if current_time - timestamp > 60:
                    inactive_peers.append(peer_id)

            for peer_id in inactive_peers:
                del registry[peer_id]
            time.sleep(interval)
    
    thread = threading.Thread(target=run_checker) # creates a different thread
    thread.daemon = True  
    thread.start()


if __name__ == '__main__':
    start_server()
    

