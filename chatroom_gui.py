from operator import truediv
import PySimpleGUI as sg # gui 
import socket #main communication
import threading #concurrent thread

these_name_list = sg.theme_list()
sg.theme('DarkTeal6')

layout = [
        [sg.Text("                                          "),
        sg.Text("Chatroom",justification='center', font=("Helvetica", 20)) ], 
        [sg.Text("Host"), sg.Input("", key = '-HOST-', do_not_clear = False, size =(13, 1)), 
        sg.Text("Port"), sg.Input("", key = '-PORT-', do_not_clear = False ,size =(5, 1)),
        sg.Text(" "),
        sg.Button('Connect', font=("Helvetica", 7 )),
        sg.Text(" "),
        sg.Text("Disconnected", font=("Helvetica", 12), key = "-CONNECTION-")], 
        [sg.Text("Username"), sg.Input("", key = '-USERNAME INPUT-', do_not_clear = False ,size =(22, 5)),
        sg.Text(" "),
        sg.Button('Enter', font=("Helvetica", 7 ))],
        [sg.Listbox(values = [],  
        enable_events = True, size = (40,20), font=("Helvetica", 15), key = "-OUTPUT-")],
        [sg.Text("Message"), sg.Input("", key = '-MESSAGE INPUT-', do_not_clear = False, size =(45, 5), ), 
        sg.Button('Send', font=("Helvetica", 7 ), bind_return_key = True)]
]


window = sg.Window("Chatroom", layout, size=(400, 500), return_keyboard_events = True)
outputlist =[]

#Client functions

def listen_to_server(client):
    while True:    
        message = client.recv(2048).decode('utf-8')
        if message != "":
            username = message.split(": ") [0]
            content = message.split(": ") [1]
            outputlist.append(str("[" + username + "] " + content))
            window["-OUTPUT-"].update(outputlist)

        else:
            outputlist.append("Message received from client is empty")
            window["-OUTPUT-"].update(outputlist)  
        



while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "Connect":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #connect to the server
        try:
                HOST = str([values['-HOST-']][0])
                PORT = int([values['-PORT-']][0])
                client.connect((HOST,PORT))
                print(f"successfully connected")
                window["-CONNECTION-"].update("Connected",font=("Helvetica", 12))
                window["-USERNAME INPUT-"].update("Enter username ")
                
        except:
                print (f"Unable to bind to host {HOST} and port {PORT}")
                window["-CONNECTION-"].update("[ERROR]",font=("Helvetica", 12))  
        

    elif event == "Enter":
        username = (str(values['-USERNAME INPUT-'])) 
        client.sendall((username).encode()) #sends username to server and start the server listen thread
        outputlist.append("Welcome " + username + "!")
        window["-OUTPUT-"].update(outputlist)
        #window["-OUTPUT-"].Widget.selection_set(outputlist[-1])  
        threading.Thread(target = listen_to_server, args = (client, )).start()

    elif event == "Send":  
        #while 1:
                message = (str(values['-MESSAGE INPUT-']))
                client.sendall(message.encode()) 
                window["-MESSAGE INPUT-"].update("")  

    #elif event == "-OUTPUT-":



window.close()