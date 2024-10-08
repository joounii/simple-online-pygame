import socket
import threading
import json
from colored_print import log

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

clients = []
client_id_counter = 0

# commands the server can handle.
def command_almost_all(data, current_conn):
    message = data["message"]
    for client in clients:
        print(client)
        # finde what player sent the message and add it to the message
        if client["conn"] != current_conn:
            if current_conn == clients[0]["conn"]:
                data_message = "1;" + message
            elif current_conn == clients[1]["conn"]:
                data_message = "2;" + message
            else:
                data_message = "3;" + message
                
            try:
                log.success(data_message)
                client['conn'].send(data_message.encode('utf-8'))
            except:
                clients.remove(client)
                
# code for the server

def handle_client(conn, addr, client_id):
    print(f"[NEW CONNECTION] {addr} (ID: {client_id}) connected.")
    connected = True
    while connected:
        try:
            message = json.loads(conn.recv(1024).decode('utf-8'))
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

def broadcast(data, current_conn):
    if data["command"] == "almost_all":
        command_almost_all(data, current_conn)
    
    

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
