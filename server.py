import socket
from  threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None

CLIENTS = {}


# Boilerplate Code
def handleClient(player_socket,player_name):
    global CLIENTS

    # Sending Initial message
    playerType =CLIENTS[player_name]["player_type"]
    if(playerType== 'player1'):
        CLIENTS[player_name]['turn'] = True
        player_socket.send(str({'player_type' : CLIENTS[player_name]["player_type"] , 'turn': CLIENTS[player_name]['turn'], 'player_name' : player_name }).encode())
    else:
        CLIENTS[player_name]['turn'] = False
        player_socket.send(str({'player_type' : CLIENTS[player_name]["player_type"] , 'turn': CLIENTS[player_name]['turn'], 'player_name' : player_name }).encode())

    while True:
        try:
            message = player_socket.recv(2048)
            if(message):
                for cName in CLIENTS:
                    cSocket = CLIENTS[cName]["player_socket"]
                    cSocket.send(message)
        except:
            pass



def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()

        player_name = player_socket.recv(1024).decode().strip()

        if(len(CLIENTS.keys()) == 0):
            CLIENTS[player_name] = {'player_type' : 'player1'}
        else:
            CLIENTS[player_name] = {'player_type' : 'player2'}


        CLIENTS[player_name]["player_socket"] = player_socket
        CLIENTS[player_name]["address"] = addr
        CLIENTS[player_name]["player_name"] = player_name
        CLIENTS[player_name]["turn"] = False

        print(f"Connection established with {player_name} : {addr}")


        # ------------ Boilerplate  Code Start
        thread = Thread(target = handleClient, args=(player_socket,player_name,))
        thread.start()
        # ------------ Boilerplate  Code End




def setup():
    print("\n")
    print("\t\t\t\t\t\t*** LUDO LADDER ***")


    global SERVER
    global PORT
    global IP_ADDRESS

    IP_ADDRESS = '127.0.0.1'
    PORT = 6000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")


    acceptConnections()


setup()
