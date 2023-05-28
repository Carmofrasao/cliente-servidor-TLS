import ssl
import socket
from crud import KeyValueStore
import pyshark

# Configurações do servidor
HOST = 'localhost'
PORT = 8888

iface_name = 'lo'
filter_string = 'port 8888'


capture = pyshark.LiveCapture(
    interface=iface_name,
)

# Carrega o banco de dados a partir do arquivo
database = KeyValueStore('database.pkl')

def process_request(request):
    args = request.split()
    comm = args[0]
    
    if comm not in dir(KeyValueStore):
        return f"'{comm}' não foi interpretado pelo server" 

    foo = getattr(database, comm)

    try:
        resp = str(foo(*args[1:]))
    except Exception as e:
        resp = f'Não entendi o comando - "{request}"\nErro: {str(e)}'

    return resp


# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configura o socket para aceitar conexões seguras
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='certificado/cert.pem', keyfile='certificado/key.pem')

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
    capture.sniff(timeout=5)
    for packet in capture:
        print('-------------------------------------------------')
        print(packet)
        print('-------------------------------------------------')
    # Recebe a requisição do cliente
    ciphered = secure_socket.recv(1024)
    request = ciphered.decode()

    # print('cifrado: ', ciphered)
    print('claro  : ', request)
    
    if request == 'exit': break

    # Processa a requisição
    response = process_request(request)

    # Envia a resposta ao cliente
    secure_socket.sendall(response.encode())

# Encerra a conexão com o cliente
secure_socket.shutdown(socket.SHUT_RDWR)
secure_socket.close()