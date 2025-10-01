import socket
from colorama import Fore, Back, Style, init
import time
from e2ee_logic import *
import threading

init(autoreset=True) #For the colarma package
HOST='127.0.0.1'
PORT=12233
private_key=None
received_public_keys = []
sent_public_keys={}
# An event to signal when a requested key has been received.
key_received_event = threading.Event()
send_username_event= threading.Event()

def receive_thread(server_socket):
    while True:
        try:
            message = server_socket.recv(4096)
            if not message:
                print("[!] Disconnected from server.")
                break

            elif message.startswith(b'-----BEGIN PUBLIC KEY-----'):
                received_public_keys.append(message)
                key_received_event.set()
                continue

            else:
                try:
                    decrypted_text= decrypt_text(message, private_key=private_key).decode('utf-8')
                    Name , text = decrypted_text[1:].split(maxsplit=1)
                    words=text.split()
                    sender=words[-1]
                    words.pop()
                    print(Fore.RED+ f"[PRIVATE]{sender} : {' '.join(words)}")
                except Exception as e:
                    print(message.decode('utf-8'))

        except Exception as e:
            print(f"An error occurred: {e}")
            break
    server_socket.close()
            





def send_thread(server_socket):
    while True:
        message_ = input("")
        message= message_ + f' {Username}'
        message2 =f'{Username} : {message_}'
        if message.startswith('@'):
            username, text = message.split(sep=' ', maxsplit=1)
            username = username[1:]
            server_socket.send(f'##keys {username}'.encode('utf-8'))
            key_received_event.clear()
            event_was_set = key_received_event.wait(timeout=5.0)
            if event_was_set:
                server_socket.send(encrypt_text(message , bytes_to_public_key(received_public_keys[-1])))
        elif message_.startswith('/'):
            server_socket.send(message_.encode('utf-8'))
        else:
            server_socket.send(message2.encode('utf-8'))


def get_user_name():
    while True:
        username = input("Choose your username: ")
        if ' ' in username:
            print("Username cannot have white spaces")
            continue
        if username:
            return username
        print("Username cannot be empty.")


def run_client():
    global Username
    Username = get_user_name()
    server_socket=socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    try:
        server_socket.connect((HOST,PORT))
        server_socket.send(Username.encode('utf-8'))
    except Exception as e:
        print(f'OOPS ! {e}')
    global private_key
    public_key,private_key = generate_public_private_key()
    public_key_bytes=public_key_to_bytes(public_key)
    server_socket.send(public_key_bytes)

    time.sleep(0.1)
    sending_thread = threading.Thread( target=send_thread , args=(server_socket,) ,daemon=False)
    receiving_thread=threading.Thread(target= receive_thread , args=(server_socket,) , daemon=False)

    sending_thread.start()
    receiving_thread.start()

if __name__=='__main__':
    run_client()







