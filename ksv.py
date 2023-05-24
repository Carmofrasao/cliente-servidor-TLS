import cmd
from crud import KeyValueStore

class KeyValueStoreShell(cmd.Cmd):
    intro = "Bem-vindo ao shell do Key-Value Store. Digite 'help' para listar os comandos disponíveis."
    prompt = "(KVS) "

    def __init__(self):
        super().__init__()
        self.kvs = KeyValueStore("database.pkl")

    def do_create(self, arg):
        """Cria um novo par chave-valor. Sintaxe: create <chave> <valor>"""
        args = arg.split()
        if len(args) != 2:
            print("Comando inválido. Uso: create <chave> <valor>")
            return
        chave, valor = args
        self.kvs.create(eval(chave), eval(valor))

    def do_read(self, arg):
        """Lê o valor de uma chave. Sintaxe: read <chave>"""
        chave = arg.strip()
        if not chave:
            print("Comando inválido. Uso: read <chave>")
            return
        valor = self.kvs.read(eval(chave))
        print(valor)

    def do_update(self, arg):
        """Atualiza o valor de uma chave existente. Sintaxe: update <chave> <valor>"""
        args = arg.split()
        if len(args) != 2:
            print("Comando inválido. Uso: update <chave> <valor>")
            return
        chave, valor = args
        self.kvs.update(eval(chave), eval(valor))

    def do_delete(self, arg):
        """Exclui um par chave-valor. Sintaxe: delete <chave>"""
        args = arg.split()
        if len(args) != 1:
            print("Comando inválido. Uso: delete <chave>")
            return
        chave = args[0]
        self.kvs.delete(eval(chave))

    def do_keys(self, arg):
        """Obtém todas as chaves do Key-Value Store. Sintaxe: keys"""
        chaves = self.kvs.get_all_keys()
        print(chaves)

    def do_values(self, arg):
        """Obtém todos os valores do Key-Value Store. Sintaxe: values"""
        valores = self.kvs.get_all_values()
        print(valores)

    def do_show(self, arg):
        """Mostra toda a Key-Value Store. Sintaxe: show"""
        print(self.kvs.data)

    def do_exit(self, arg):
        """Sai do shell. Sintaxe: exit"""
        return True

if __name__ == "__main__":
    KeyValueStoreShell().cmdloop()
