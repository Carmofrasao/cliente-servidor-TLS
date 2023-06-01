# Autores
# Eduardo Gobbo W.V.G. 
# Anderson Aparecido do Carmo Frasão
# Ultima alteração 31/05/2023 - 22h56m

# Testes:
# 1. Autenticação   - comentar a linha de `context.wrap_socket` em Server.create_socket
# 2. Sigilo         - executando server ou client basta executar com `--show`
# 3. Integridade    - executando client com `--edit` é possível editar um byte (endereço maior que 10)
#                     podemos ver que o server tem erro ao descriptografar a mensagem.  

from socket import create_server, SHUT_RDWR
import ssl
import sys

from config import PORT, CERT_FILE, PKEY_FILE
from inspectable import InspectableListenerSocket
from key_value_store import KeyValueStore


class Server:
    def __init__(self):
        self.listener_socket = None
        self.client_socket = None
        self.client_address = None

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(CERT_FILE, PKEY_FILE)
        self.context = context

    def run(self):
        self.listener_socket = self.create_socket()
        print('Aguardando conexões...')

        try:
            self.client_socket, self.client_address = self.listener_socket.accept()
            print('Conexão estabelecida com', self.client_address)
            
            self.handle_client()
        except ssl.SSLEOFError:
            # When a handshake is unexpectedly closed, we ignore
            print("Client didn't finish handshake")

        self.listener_socket.close()

    def create_simple_socket(self):
        return create_server(("", PORT))

    def create_socket(self):
        socket = self.create_simple_socket()
        return self.context.wrap_socket(socket, server_side=True)

    def handle_client(self):
        # herdar classe e implementar lógica nesta função
        # self.client_socket.send(msg.encode())
        # self.client_socket.recv(1024).decode()
        pass



class ServerKVS(Server):
    def __init__(self):
        super().__init__()

        self.database = KeyValueStore('database.pkl')

    def handle_client(self):
        while True:
            
            # Recebe a requisição do cliente
            request = self.client_socket.recv(1024).decode()
            
            if request == 'exit': break

            # Processa a requisição
            response = self.process_request(request)

            # Envia a resposta ao cliente
            self.client_socket.send(response.encode())

        # Encerra a conexão com o cliente
        self.listener_socket.shutdown(SHUT_RDWR)
        self.listener_socket.close()

    def process_request(self, request):
        args = request.split()
        comm = args[0]
        
        if comm not in dir(KeyValueStore):
            return f"'{comm}' não foi interpretado pelo server" 

        foo = getattr(self.database, comm)

        try:
            resp = str(foo(*args[1:]))
        except Exception as e:
            resp = f'Não entendi o comando - "{request}"\nErro: {str(e)}'

        return resp


class ServerAtacavel(ServerKVS):
    def create_socket(self):
        socket = self.create_simple_socket()
        return InspectableListenerSocket(socket, self.context, server_side=True)


if __name__ == '__main__':
    allow_editing = "--edit" or "--show" in sys.argv

    if(allow_editing):
        ServerAtacavel().run()
    else:
        ServerKVS().run()