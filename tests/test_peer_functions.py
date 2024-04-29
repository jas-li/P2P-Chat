import pytest
from unittest.mock import patch
import socket
import json
import time

from peer1.test_peer1 import (
    register_with_server,
    query_peer,
    get_users,
    send_keep_alive,
    start_keep_alive_scheduler,
    start_peer_server,
    run_peer_server,
    send_message_to_peer,
    initialize_db,
    log_message
)

# Mocking server connection
@pytest.fixture
def mock_socket():
    with patch('socket.socket') as mock_socket:
        yield mock_socket.return_value

# Test initialize_db function
def test_initialize_db():
    # Setup
    db_path = 'test.db'

    # Mock database connection
    with patch('sqlite3.connect') as mock_connect:
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Action
        initialize_db(db_path)

        # Assertions
        mock_connect.assert_called_once_with(db_path)
        mock_cursor.execute.assert_called_once_with(
            '''CREATE TABLE IF NOT EXISTS messages
                      (id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, message TEXT, timestamp REAL)'''
        )
        mock_connect.return_value.commit.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

