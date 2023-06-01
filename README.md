# Cliente Servidor TLS

## Certificados

Execute o seguinte comando em seu terminal para gerar novos certificados:

    openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem -subj "/C=BR/ST=Parana/L=Curitiba/O=Organization/CN=localhost"

Mudar CN para usar em dois computadores, para gerar novos certificados, C, ST, L e O devem estar iguais na linha a cima!

## Uso

- Para usar o sistema normalmente, basta executar em ordem:

```shell
python3 server.py
python3 client.py
```

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

# Testes:

## Autenticação

Executando o cliente com a opção `client.py --noauth` podemos ver que utilizar um certificado desconhecido pelo servidor não permite a comunicação do cliente com o servidor.

```shell
python server.py
python client.py --noauth
```

## Sigilo

Para visualizar as mensagens abertas e cifradas basta executar ou o cliente ou o servicor com a opção `--show`

```shell
python server.py --show
python client.py --show
```

## Integridade

Para alterar um byte da mensagem e verificar que uma mensagem alterada não é descriptografada corretamente, execute:

```shell
python server.py
python client.py --edit
```

Executando o cliente com `--edit` é possível editar um byte (escolha um endereço maior que 10).

- Já o server pode receber `--show` ou `--edit` opcionalmente, apenas para ver as mensagens trafegando.
