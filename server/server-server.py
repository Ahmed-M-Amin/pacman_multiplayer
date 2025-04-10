#!/usr/bin/env python3
import socket
import threading
import json
import time

from game_logic import update_game_state, get_current_state
from security import validate_input

HOST = '0.0.0.0'
PORT = 5555

clients = []  # List of active client sockets
client_lock = threading.Lock()

def handle_client(conn, addr):
    """Handle incoming data from a single client."""
    print(f"Client connected: {addr}")
    try:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break  # Disconnect if no data
                # ... rest of the existing code ...
            except socket.error:
                print(f"Socket error for client {addr}")
                break
            except Exception as e:
                print(f"Exception in handling client {addr}: {e}")
                break
    finally:
        with client_lock:
            if conn in clients:  # Check if client is still in list
                clients.remove(conn)
        conn.close()
        print(f"Client disconnected: {addr}")

def broadcast_state(state):
    """Sends the updated game state to all connected clients."""
    message = json.dumps(state).encode()
    with client_lock:
        for client in clients:
            try:
                client.sendall(message)
            except Exception as e:
                print(f"Error broadcasting to a client: {e}")

def handle_client(conn, addr):
    """Handle incoming data from a single client."""
    print(f"Client connected: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break  # Disconnect if no data
            try:
                move_command = json.loads(data.decode())
            except json.JSONDecodeError:
                print("Received invalid JSON")
                continue

            # Validate input
            if not validate_input(move_command):
                print("Invalid command received; ignoring.")
                continue

            # Update game state based on the move command
            update_game_state(move_command)
            
            # Get the updated game state
            state = get_current_state()
            broadcast_state(state)
        except Exception as e:
            print(f"Exception in handling client {addr}: {e}")
            break

    with client_lock:
        clients.remove(conn)
    conn.close()
    print(f"Client disconnected: {addr}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        with client_lock:
            clients.append(conn)
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()

if __name__ == '__main__':
    start_server()
