# Autores
# Eduardo Gobbo W.V.G. 
# Anderson Aparecido do Carmo Frasão
# Ultima alteração 31/05/2023 - 22h56m

# Testes:
# 1. Autenticação   - comentar a linha de `context.wrap_socket` em Server.create_socket
# 2. Sigilo         - executando server ou client basta executar com `--show`
# 3. Integridade    - executando client com `--edit` é possível editar um byte (endereço maior que 10)
#                     podemos ver que o server tem erro ao descriptografar a mensagem.  

from ssl import SSLContext, PROTOCOL_TLS_CLIENT
from socket import create_connection
import sys

from config import HOSTNAME, SERVER_ADDRESS, CERT_FILE
from key_value_store import KeyValueStoreShell
from inspectable import InspectableSocket

class Client:
    def __init__(self):
        context = SSLContext(PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(CERT_FILE)
        self.context = context
        self.hostname = HOSTNAME

    def create_simple_socket(self):
        return create_connection(SERVER_ADDRESS)

    def create_socket(self):
        socket = self.create_simple_socket()
        return self.context.wrap_socket(socket, server_hostname=self.hostname)

    def run(self):
        # herdar e implementar interação com o server aqui
        pass


class ClientKVS(Client):
    def run(self):
        KeyValueStoreShell(self.create_socket()).cmdloop()


class ClientAtacavel(ClientKVS):
    def __init__(self, allow_editing=False):
        super().__init__()
        self.allow_editing = allow_editing
        self.show_ciphered = show_ciphered

    def create_socket(self):
        socket = self.create_simple_socket()
        socket = InspectableSocket(
            socket,
            self.context,
            allow_editing=self.allow_editing,
            server_hostname=self.hostname,
        )
        socket.do_handshake()
        return socket


if __name__ == "__main__":
    allow_editing = "--edit" in sys.argv
    show_ciphered = "--show" in sys.argv

    if(allow_editing or show_ciphered):
        ClientAtacavel(allow_editing=allow_editing).run()
    else:
        ClientKVS().run()

