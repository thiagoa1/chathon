import socket

import threading
#import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


class ChatUser:

    def __init__(self, conn, name=None):
        self.conn = conn
        self.name = name

    def getConn(self):
        return self.conn

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name


userList = []


def findUserInList(conn):
    for user in userList:
        if user.getConn() == conn:
            return user
    return None


def findUserByName(name):
    for user in userList:
        if user.getName() == name:
            return user
    return None


def dealClient(conn, addr):
    with conn:
        print('Conectado à', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break

            strData = data.decode()
            strDataSplit = strData.split(":", 1)
            protocol = strDataSplit[0]

            if protocol == "login":
                [_, userName] = strData.split(":", 1)
                user = findUserInList(conn)
                if user == None:
                    userList.append(ChatUser(conn, userName))
                else:
                    user.setName(userName)
                print('Usuário ', userName, ' logou')

            elif protocol == "message":
                [_, toName, message] = strData.split(":", 2)

                user = findUserInList(conn)
                toUser = findUserByName(toName)

                if toUser == None:
                    user.getConn().sendall(("[Servidor] Usuário " +
                                  toName + " não foi encontrado").encode())
                else:
                    toUser.getConn().sendall(
                        ("["+user.getName() + "] " + message).encode())
            elif protocol == "list":
                userNameList = [user.getName() for user in userList]
                userNameString = ', '.join(userNameList)
                #userListString = map(lambda user : user.getName(), userList).join(', ')
                user.getConn().sendall((userNameString).encode())

            else:
                user.getConn().sendall(
                    ("[Servidor] Mensagem não suportada: " + strData).encode())


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Servidor Iniciado")
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            userList.append(ChatUser(conn))
            t = threading.Thread(target=dealClient, args=(conn, addr,))
            t.start()
