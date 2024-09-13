import socket
import threading
from colored_print import log

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

clients = []
client_id_counter = 0

def handle_client(conn, addr, client_id):
    print(f"[NEW CONNECTION] {addr} (ID: {client_id}) connected.")
    connected = True
    while connected:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"[MESSAGE FROM {addr} (ID: {client_id})] {message}")
                broadcast(message, conn)
            else:
                connected = False
        except ConnectionResetError:
            connected = False

    conn.close()
    
    # Remove the client by finding its dictionary in the clients list
    for client in clients:
        if client['conn'] == conn:
            clients.remove(client)
            break
    print(f"[DISCONNECTED] {addr} (ID: {client_id}) disconnected.")

def broadcast(message, current_conn):
    for client in clients:
        print(client)
        if client["conn"] != current_conn:
            try:
                client['conn'].send(message.encode('utf-8'))
            except:
                clients.remove(client)

def start():
    global client_id_counter
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        client_id_counter += 1
        client_id = client_id_counter
        clients.append({
            'id': client_id,
            'conn': conn
        })
        
        log.success("CLIENTS: ")
        log.success(clients)
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

if __name__ == "__main__":
    server.listen()
    print("[STARTING] Server is starting...")
    start()
