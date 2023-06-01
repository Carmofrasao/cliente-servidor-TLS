# Autores
# Eduardo Gobbo W.V.G. 
# Anderson Aparecido do Carmo Frasão
# Ultima alteração 31/05/2023 - 22h56m

# Testes:
# 1. Autenticação   - comentar a linha de `context.wrap_socket` em Server.create_socket
# 2. Sigilo         - executando server ou client basta executar com `--show`
# 3. Integridade    - executando client com `--edit` é possível editar um byte (endereço maior que 10)
#                     podemos ver que o server tem erro ao descriptografar a mensagem.  

CERT_FILE='certificado/cert.pem'
PKEY_FILE='certificado/key.pem'

PORT=8888
HOST='localhost'
HOSTNAME = HOST

LOOPBACK_ADDR = (HOST, PORT)
SERVER_ADDRESS = (HOST, PORT)