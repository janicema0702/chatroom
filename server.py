import PySimpleGUI as sg # gui 
import socket #main communication
import threading #concurrent thread

HOST = '192.168.1.133' # example: "127.0.0.1"
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] 

# keep listening to the active client
def listen_for_messages(client, username):
    
    while 1: #always true
        response = client.recv(2048).decode('utf-8')
        if response != "":
            final_msg = username + ": " + response
            send_messages_to_all(final_msg)
        else:
            print ("the message send fromm client {username} is empty")


# function to send message to a single client (private msg)
def send_message_to_client(client, message):
    client.sendall(message.encode('utf-8'))

# sending messages (all connected  will recceive message)
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)


# function ot handle client
def client_handler(client):
    
    # server will llisten fro client message that contains the username
    while 1:

        username = client.recv(2048).decode('utf-8') # 2048 = max size of the message
        if username != "":
            active_clients.append((username, client))
            break
        else:
            print("Client username is empty")

    threading.Thread(target = listen_for_messages, args = (client, username)).start()

# main function
def main():
    # creating the socket class object
    # AF_INET: IPv4 addresses
    # SOCK_STREAM: TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print (f"Running the server on {HOST} {PORT}")
    except:
        print (f"Unable to bind to host {HOST} and port {PORT}")

    # set server limit
    server.listen(LISTENER_LIMIT)

    #keep listening to client connection
    while 1:
        client, address = server.accept() #listen to client connections and give the two values
        print(f"Successfully connected to client {address[0]} {address[1]} ")

        threading.Thread(target = client_handler, args = (client, )).start() #blank in args is important


if __name__ == '__main__':
    main()
