import socket
import threading

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

running = False

def inputLoop(sock):
    global running
    while running:
        toNameOrList = input('Digite para quem enviar, ou escreva #lista para ver a lista de usuários ou #sair para fechar o cliente: \n')
        print(toNameOrList)
        print(toNameOrList.startswith('#lista'))
        if toNameOrList.startswith('#lista'):
            sock.sendall(("list:").encode())
        elif toNameOrList.startswith('#sair'):
            running = False
        else:
            read = input('Digite a mensagem para enviar: \n')
            sock.sendall(("message:" + toNameOrList + ":" + read).encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.settimeout(1.0)
        
        global running
        running = True
        print('Conectado ao servidor')

        userName = input('Digite o seu nome de usuário: \n')
        sock.sendall(("login:" + userName).encode())

        t = threading.Thread(target=inputLoop, args=(sock,))
        t.start()
        while running:
            try:
                data = sock.recv(1024).decode()
                print(repr(data))
            except socket.timeout:
                continue

if __name__ == "__main__":
    main()