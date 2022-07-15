import socket
import threading

HOST = '172.17.133.52'
PORT = 1234

def listen_to_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != "":
            username = message.split(": ") [0]
            content = message.split(": ") [1]
            print(f"[{username}] {content}")
        else:
            print("Message received from client is empty")

def send_message_to_server(client):

    while 1:
        message = input("Message: ")
        if message != "":
            client.sendall(message.encode())
        else:
            print("Empty message")
            

def communicate_to_server(client):
    username = input("Enter username: ")
    if username != "":
        client.sendall(username.encode()) #sends username to server and start the server listen thread
    else:
        print ("Username cannot be empty")
        exit(0)

    threading.Thread(target = listen_to_server, args = (client,)).start()
    
    send_message_to_server(client)

# main function
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connect to the server
    try:
        client.connect((HOST,PORT))
        print(f"successfully connected")
    except:
        print (f"Unable to bind to host {HOST} and port {PORT}")

    communicate_to_server(client)


if __name__ == '__main__':
    main()
