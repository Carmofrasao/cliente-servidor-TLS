# Cliente Servidor TLS

Caso ocorra o seguinte erro:

    ValueError: Cannot set verify_mode to CERT_NONE when check_hostname is enabled

Execute o seguinte comando em seu terminal:

    openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem -subj "/C=BR/ST=Parana/L=Curitiba/O=Organization/CN=localhost"

Mudar CN para usar em dois computadores, para gerar novos certificados, C, ST, L e O devem estar iguais na linha a cima e em `certificado.py`!

- Para usar o sistema, execute em ordem:

```shell
python3 server.py
python3 client.py
```

# Uso

- O cliente tem acesso a base de dados do server, para usar:

```
Comandos disponíveis:
  create    : Cria um novo par chave-valor. Sintaxe: create <chave> <valor>
  delete    : Exclui um par chave-valor. Sintaxe: delete <chave>
  exit      : Sai do shell. Sintaxe: exit
  help      : Mostra comandos disponíveis e como usá-los.
  keys      : Obtém todas as chaves do Key-Value Store. Sintaxe: keys
  read      : Lê o valor de uma chave. Sintaxe: read <chave>
  show      : Mostra toda a Key-Value Store. Sintaxe: show
  update    : Atualiza o valor de uma chave existente. Sintaxe: update <chave> <valor>
  values    : Obtém todos os valores do Key-Value Store. Sintaxe: values
```
