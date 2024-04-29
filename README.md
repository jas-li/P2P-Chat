# Peer-to-Peer Messaging System

This project implements a peer-to-peer messaging system where users can register themselves with a central discovery server and communicate with each other directly. It consists of two main components:

1. **Peer Implementation**: This is the client-side implementation responsible for registering with the server, querying for active peers, sending and receiving messages, and maintaining a local SQLite database for message logging.

2. **Discovery Server**: This is the central server responsible for managing peer registrations, responding to queries about active peers, and removing inactive peers from the registry.

## Peer Implementation

### Dependencies
- Python 3.x

### Usage
1. **Run the Discovery Server**: Start the discovery server by running `python discovery_server.py`.
2. **Run the Peer Client**: Start the peer client by running `python peer_client.py`.
3. **Register**: Enter a username to register with the discovery server.
4. **Connect to a User**: Choose to connect to another registered user by their username and start messaging.
5. **List Active Users**: View a list of active users currently registered with the discovery server.

## Discovery Server

### Dependencies
- Python 3.x

### Usage
1. **Start the Server**: Run `python discovery_server.py` to start the discovery server.
2. **Inactivity Checker**: The server automatically removes inactive peers from the registry after a set interval.

## Additional Notes
- Messages are logged locally in an SQLite database for each peer.
- Both the peer client and the discovery server should be running simultaneously for the system to function properly.
