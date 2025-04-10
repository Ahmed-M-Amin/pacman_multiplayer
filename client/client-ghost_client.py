#!/usr/bin/env python3
import socket
import json
import threading
import sys

HOST = '127.0.0.1'  # Change to server's IP address
PORT = 5555

def receive_updates(sock):
    """Listen for game state updates from the server."""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            try:
                state = json.loads(data.decode())
                print("Game State Update:")
                print(state)
            except Exception as e:
                print("Error decoding state update:", e)
        except Exception as e:
            print("Error receiving data:", e)
            break

def send_moves(sock):
    """Send move commands for Ghost player using input."""
    print("Enter move commands for a Ghost (UP, DOWN, LEFT, RIGHT). Type 'exit' to quit.")
    while True:
        move = input("Your move: ").strip().upper()
        if move == 'EXIT':
            break
        command = {
            'role': 'ghost',
            'direction': move
        }
        sock.sendall(json.dumps(command).encode())

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print("Could not connect to server:", e)
        sys.exit(1)
    
    threading.Thread(target=receive_updates, args=(sock,), daemon=True).start()
    send_moves(sock)
    sock.close()
    print("Disconnected.")

if __name__ == '__main__':
    main()
