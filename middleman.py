import socket
import ssl

# Configurações do cliente
HOST = 'localhost'
PORT = 8888

# Cria um socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(True)
while True:
    print(sock.accept())
