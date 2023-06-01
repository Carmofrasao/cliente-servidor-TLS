import cmd
import pickle
import functools


def evaluate_arguments(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        args = [eval(arg) for arg in args]
        kwargs = {key: eval(value) if isinstance(value, str) else value for key, value in kwargs.items()}
        return str(func(self, *args, **kwargs))
    return wrapper


class KeyValueStore:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def _push_data(self, data:dict):
        with open(self.filename, 'wb') as file:
            for key, value in data.items():
                self.create(key, value)
            self._save_data()

    @evaluate_arguments
    def create(self, key, value):
        """Adiciona `key` : `value` ao BD se `key` nao existe."""
        if key in self.data:
            return f"Chave {key} Já existe!"
        self.data[key] = value
        self._save_data()

    @evaluate_arguments
    def read(self, key):
        """Retorna um dict com todos os pares `{key: value}`"""
        if key not in self.data: 
            return f"Chave {key} não exite."
        return self.data.get(key)

    @evaluate_arguments
    def update(self, key, value):
        """Atualiza `key` com `value` no BD se `key` existe."""
        if key not in self.data:
            return f"Chave {key} não exite."
        self.data[key] = value
        self._save_data()

    def show(self):
        return self.data

    @evaluate_arguments
    def delete(self, key):
        """Deleta o par `{key: value}` se `key` existe."""
        if key not in self.data:
            return f"Chave {key} não existe."
        del self.data[key]
        self._save_data()

    def get_all_keys(self):
        """Retorna uma lista com todas as chaves do BD."""

        return list(self.data.keys())

    def get_all_values(self):
        """Retorna uma lista com todos os valores do DB."""
        return list(self.data.values())


# shorthand for class bellow
#define kvs KeyValueStore
kvs = KeyValueStore

class KeyValueStoreShell(cmd.Cmd):
    intro = "Bem-vindo ao shell do Key-Value Store. Digite 'help' para listar os comandos disponíveis."
    prompt = "(KVS) "

    # Configurações do cliente
    def __init__(self, socket):
        super().__init__()
        
        # um socket configurado para enviar e receber packets
        self.secure_socket = socket

    def _send_query(self, query):
        # Envia a requisição ao servidor
        self.secure_socket.send(query.encode())

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
