import socket
import ssl
import json

def load_database():
    try:
        with open('database.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
def save_database(database):
    with open('database.json', 'w') as file:
        json.dump(database, file)

def process_request(request):
    command, *args = request.split()
    if command == 'GET':
        # Obtém o valor associado à chave especificada pelo cliente
        key = args[0]
        value = database.get(key, f'A chave "{key}" não existe')
        return value
    
    elif command == 'SET':
        key, value = args
        database[key] = value
        save_database(database)
        return 'OK'
    else:
        return 'Comando inválido'

# Configurações do servidor
HOST = 'localhost'
PORT = 8888
CERTFILE = 'cert.pem'  # Certificado do servidor
KEYFILE = 'key.pem'    # Chave privada do servidor

# Carrega o banco de dados a partir do arquivo
database = load_database()

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configura o socket para aceitar conexões seguras
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

# Associa o socket ao host e porta especificados
server_socket.bind((HOST, PORT))

# Inicia a escuta por conexões
server_socket.listen(1)
print('Aguardando conexões...')

# Aceita uma nova conexão
client_socket, client_address = server_socket.accept()
print('Conexão estabelecida com', client_address)

# Configura a conexão para usar TLS
secure_socket = context.wrap_socket(client_socket, server_side=True)

while True:
    # Recebe a requisição do cliente
    request = secure_socket.recv(1024).decode()

    # Processa a requisição
    response = process_request(request)

    # Envia a resposta ao cliente
    secure_socket.sendall(response.encode())

# Encerra a conexão com o cliente
secure_socket.shutdown(socket.SHUT_RDWR)
secure_socket.close()