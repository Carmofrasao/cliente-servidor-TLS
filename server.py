import socket
import ssl
import json
from crud import KeyValueStore

def process_request(request):
    args = request.split()

    comm = args[0]
    if comm not in dir(KeyValueStore):
        return f"'{comm}' não foi interpretado pelo server" 

    foo = getattr(database, comm)
    try:
        resp = str(foo(*args[1:]))
    except Exception as e:
        resp = f'Error while evaluating - {request} :\n{str(e)}'

    return resp

# Configurações do servidor
HOST = 'localhost'
PORT = 8888
CERTFILE = 'cert.pem'  # Certificado do servidor
KEYFILE = 'key.pem'    # Chave privada do servidor

# Carrega o banco de dados a partir do arquivo
database = KeyValueStore('database.pkl')

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