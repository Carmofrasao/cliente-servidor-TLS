import cmd
import ssl
import socket

class KeyValueStoreShell(cmd.Cmd):
    intro = "Bem-vindo ao shell do Key-Value Store. Digite 'help' para listar os comandos disponíveis."
    prompt = "(KVS) "

    def __init__(self, HOST='localhost', PORT=8888):
        super().__init__()
        # self.kvs = KeyValueStore("database.pkl")
        # Configurações do cliente
        self.HOST = HOST
        self.PORT = PORT

    def _send_query(self, query):
        # Cria um socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Configura o socket para usar TLS
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations('cert.pem')

        # Estabelece a conexão segura com o servidor
        secure_socket = context.wrap_socket(client_socket, server_hostname=self.HOST)
        secure_socket.connect((self.HOST, self.PORT))
        
        # Envia a requisição ao servidor
        secure_socket.sendall(query.encode())

        # Recebe a resposta do servidor
        response = secure_socket.recv(1024).decode()

        # Encerra a conexão com o servidor
        secure_socket.shutdown(socket.SHUT_RDWR)
        secure_socket.close()

        return response

    def do_create(self, arg):
        """Cria um novo par chave-valor. Sintaxe: create <chave> <valor>"""
        args = arg.split()
        if len(args) != 2:
            print("Comando inválido. Uso: create <chave> <valor>")
            return
        # chave, valor = args
        # self.kvs.create(eval(chave), eval(valor))
        self._send_query(arg)

    def do_read(self, arg):
        """Lê o valor de uma chave. Sintaxe: read <chave>"""
        chave = arg.strip()
        if not chave:
            print("Comando inválido. Uso: read <chave>")
            return
        # valor = self.kvs.read(eval(chave))
        valor = self._send_query(arg)
        print(valor)

    def do_update(self, arg):
        """Atualiza o valor de uma chave existente. Sintaxe: update <chave> <valor>"""
        args = arg.split()
        if len(args) != 2:
            print("Comando inválido. Uso: update <chave> <valor>")
            return
        # chave, valor = args
        # self.kvs.update(eval(chave), eval(valor))
        self._send_query(arg)

    def do_delete(self, arg):
        """Exclui um par chave-valor. Sintaxe: delete <chave>"""
        args = arg.split()
        if len(args) != 1:
            print("Comando inválido. Uso: delete <chave>")
            return
        # chave = args[0]
        # self.kvs.delete(eval(chave))
        self._send_query(arg)


    def do_keys(self, arg):
        """Obtém todas as chaves do Key-Value Store. Sintaxe: keys"""
        # chaves = self.kvs.get_all_keys()
        chaves = self._send_query(arg)

        print(chaves)

    def do_values(self, arg):
        """Obtém todos os valores do Key-Value Store. Sintaxe: values"""
        # valores = self.kvs.get_all_values()
        valores = self._send_query(arg)

        print(valores)

    def do_show(self, arg):
        """Mostra toda a Key-Value Store. Sintaxe: show"""
        print(arg)
        data = self._send_query(arg)
        print(data)

    def do_exit(self, arg):
        """Sai do shell. Sintaxe: exit"""
        return True

if __name__ == "__main__":
    KeyValueStoreShell().cmdloop()
