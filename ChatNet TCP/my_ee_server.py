import socket
import threading
import time
from colorama import Fore, Style
from e2ee_logic import *


clients={}          # {username : [client_socket , its pubic_key]


def send_message(message, sender_socket=None):
    for username in clients.keys():
        client_socket=clients[username][0]
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                del clients[username]

def manage_client(client_socket):
    current_chat=None
    try:

        username = client_socket.recv(1024).decode('utf-8')
        if username in clients:
            client_socket.send(f"User already exists , try some other Username ".encode("utf-8"))
            time.sleep(0.2)
            client_socket.close()
            return
        public_key= client_socket.recv(4096)
        clients[username]=[client_socket , public_key]
        print(f"{username} has connected.")
        client_socket.send("You are now connected.".encode('utf-8'))
        send_message(message=f'{username} has joined.'.encode('utf-8'),sender_socket=client_socket)
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            if data.startswith(b'/quit'):
                break
            elif data.startswith(b'/list'):
                connected_users = ", ".join(clients.keys())
                client_socket.send(f"Connected users: {connected_users}".encode('utf-8'))

            elif data.startswith(b'##keys'):
                receiver= data.decode('utf-8').split()[1]
                if receiver in clients.keys():
                    current_chat=receiver
                    client_socket.send(clients[receiver][1])

            else:
                try:
                    clients[current_chat][0].send(data)
                except Exception as e:
                    send_message(message=data ,sender_socket=client_socket )
                    print(data)


    finally:
        send_message(message=f"{username} has left the server".encode('utf-8') , sender_socket=client_socket)
        clients[username][0].close()
        del clients[username]
        print(f"{username} has left the server")


def start_server():
    HOST = '127.0.0.1'
    PORT=12233
    server_socket=socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server_socket.bind((HOST , PORT))
    server_socket.listen(5)
    print(f"server running on host :{HOST} , port : {PORT}")

    while True:
        client_socket, address = server_socket.accept()
        print(f" User connected on - - {address[0]} : {address[1]}")
        client_thread = threading.Thread(target=manage_client, args=(client_socket,))
        client_thread.start()


if __name__=='__main__':
    start_server()
