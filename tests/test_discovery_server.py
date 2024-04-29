import pytest
import socket
import threading
import json
import time
from discovery_server import start_server, inactivity_checker

# Define test parameters
HOST = '127.0.0.1'
PORT = 12345

@pytest.fixture(scope='module')
def start_discovery_server():
    # Start the discovery server in a separate thread
    thread = threading.Thread(target=start_server, args=(HOST, PORT))
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Wait for server to start
    yield
    # Clean up after tests
    # You can add cleanup code here if necessary

def test_register_peer(start_discovery_server):
    # Test registering a peer with the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        message = {
            'type': 'register',
            'peer_id': 'test_peer',
            'ip_address': '192.168.0.1',
            'port': 54321,
            'timestamp': time.time()
        }
        sock.sendall(json.dumps(message).encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
        assert response == ''  # Assuming the server does not send a response upon successful registration

# Add more test cases as needed

