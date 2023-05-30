import cmd
import ssl
import socket
from crud import KeyValueStore as kvs
import pyshark

class KeyValueStoreShell(cmd.Cmd):
    intro = "Bem-vindo ao shell do Key-Value Store. Digite 'help' para listar os comandos disponíveis."
    prompt = "(KVS) "

    def __init__(self, Host='localhost', Port=8888):
        super().__init__()
        self.HOST = Host
        self.PORT = Port
        # Configurações do cliente
        self.secure_socket = self._connect(Host, Port)

    def _connect(self, HOST, PORT):
        # Cria um socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Configura o socket para usar TLS
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations('certificado/cert.pem')

        # Estabelece a conexão segura com o servidor
        secure_socket = context.wrap_socket(client_socket, server_hostname=HOST)
        secure_socket.connect((HOST, PORT))
        
        return secure_socket

    def _send_query(self, query):
        # Envia a requisição ao servidor
        self.secure_socket.sendall(query.encode())

        iface_name = 'lo'

        capture = pyshark.LiveCapture(
            interface=iface_name,
        )

        if query != 'exit':
            # Scan (basicamente wireshark)
            capture.sniff(timeout=0.5)

            # Iterando sobre os pacotes interceptados
            for packet in capture:
                # Só imprime se for um pacote com tls
                if packet.highest_layer == 'TLS':
                    # Encontrando os dados no pacote
                    string = packet.tls.app_data.replace(':', '')
                    
                    print('\nMensagem enviada original')
                    print(f'Cifrada : {string}\n')
                    
                    # Só precisamos do primeiro pacote TLS
                    break

        # Recebe a resposta do servidor
        return self.secure_socket.recv(1024).decode()

    def _warn(self, msg):
        if(msg == "None" or msg == None):
            print("Ok")
        else:
            print(msg)

    def do_create(self, arg):
        """Cria um novo par chave-valor. Sintaxe: create <chave> <valor>"""
        args = arg.split()
        if len(args) != 2:
            print("Comando inválido. Uso: create <chave> <valor>")
            return
        chave, valor = args
        # self.kvs.create(eval(chave), eval(valor))
        resp = self._send_query(f"{kvs.create.__name__} {chave} {valor}")
        self._warn(resp)

    def do_read(self, arg):
        """Lê o valor de uma chave. Sintaxe: read <chave>"""
        chave = arg.strip()
        if not chave:
            print("Comando inválido. Uso: read <chave>")
            return
        # valor = self.kvs.read(eval(chave))
        valor = self._send_query(f'{kvs.read.__name__} {chave}')
        print(valor)

    def do_update(self, arg):
        """Atualiza o valor de uma chave existente. Sintaxe: update <chave> <valor>"""
        args = arg.split()
        if len(args) != 2:
            print("Comando inválido. Uso: update <chave> <valor>")
            return
        chave, valor = args
        # self.kvs.update(eval(chave), eval(valor))
        resp = self._send_query(f'{kvs.update.__name__} {chave} {valor}')
        self._warn(resp)

    def do_delete(self, arg):
        """Exclui um par chave-valor. Sintaxe: delete <chave>"""
        args = arg.split()
        if len(args) != 1:
            print("Comando inválido. Uso: delete <chave>")
            return
        chave = args[0]
        # self.kvs.delete(eval(chave))
        resp = self._send_query(f'{kvs.delete.__name__} {chave}')
        self._warn(resp)


    def do_keys(self, arg):
        """Obtém todas as chaves do Key-Value Store. Sintaxe: keys"""
        # chaves = self.kvs.get_all_keys()
        chaves = self._send_query(kvs.get_all_keys.__name__)
        print(chaves)

    def do_values(self, arg):
        """Obtém todos os valores do Key-Value Store. Sintaxe: values"""
        # valores = self.kvs.get_all_values()
        valores = self._send_query(kvs.get_all_values.__name__)
        print(valores)

    def do_show(self, arg):
        """Mostra toda a Key-Value Store. Sintaxe: show"""
        data = self._send_query(kvs.show.__name__)
        print(data)

    def do_help(self, arg):
        """Mostra comandos disponíveis e como usá-los."""
        command_names = [cmd_name[3:] for cmd_name in dir(self) if cmd_name.startswith('do_')]
        command_usage = [getattr(self, f"do_{cmd_name}").__doc__ for cmd_name in command_names]
        
        print("\nComandos disponíveis:")
        for name, usage in zip(command_names, command_usage):
            print(f"  {name}{' '*(10-len(name))}: {usage}")
        print()

    def do_exit(self, arg):
        """Sai do shell. Sintaxe: exit"""
        self._send_query('exit')
        return True

if __name__ == "__main__":
    KeyValueStoreShell().cmdloop()
