import socket
import ssl

# Configurações do cliente
HOST = 'localhost'
PORT = 8888

while True:
    # Cria um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Configura o socket para usar TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('cert.pem')

    # Estabelece a conexão segura com o servidor
    secure_socket = context.wrap_socket(client_socket, server_hostname=HOST)
    secure_socket.connect((HOST, PORT))
    
    # Solicita uma ação ao usuário
    action = input('Digite "GET chave" para obter um valor ou "SET chave valor" para definir um valor: ')

    # Envia a requisição ao servidor
    secure_socket.sendall(action.encode())

    # Recebe a resposta do servidor
    response = secure_socket.recv(1024).decode()

    # Imprime a resposta
    print('Resposta do servidor:', response)

    # Encerra a conexão com o servidor
    secure_socket.shutdown(socket.SHUT_RDWR)
    secure_socket.close()