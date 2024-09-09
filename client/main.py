import socket
import threading
import pygame
import sys
from pong import game

# Server address configuration
HOST = '127.0.0.1'  # Same as the server address
PORT = 12345        # Same port as the server

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[RECEIVED] {message}")
            else:
                break
        except:
            print("[ERROR] Connection to the server lost.")
            break

def send_messages(client_socket):
    while True:
        message = input("")
        client_socket.send(message.encode('utf-8'))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
send_thread = threading.Thread(target=send_messages, args=(client_socket,))
game_client = threading.Thread(target=game, args=(client_socket,))

receive_thread.start()
send_thread.start()
game_client.start()

receive_thread.join()
send_thread.join()
game_client.join()

