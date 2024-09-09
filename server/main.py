import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"[MESSAGE FROM {addr}] {message}")
                broadcast(message, conn)
            else:
                connected = False
        except ConnectionResetError:
            connected = False

    conn.close()
    clients.remove(conn)
    print(f"[DISCONNECTED] {addr} disconnected.")

def broadcast(message, current_conn):
    for client in clients:
        print(client)
        if client != current_conn:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

if __name__ == "__main__":
    server.listen()
    print("[STARTING] Server is starting...")
    start()
