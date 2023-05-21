# Cliente Servidor TLS

Caso ocorra o seguinte erro:

    ValueError: Cannot set verify_mode to CERT_NONE when check_hostname is enabled

Execute o seguinte comando em seu terminal:

    openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem -subj "/C=BR/ST=Parana/L=Curitiba/O=Organization/CN=localhost"

Mudar CN para usar em dois computadores, para gerar novos certificados, C, ST, L e O devem estar iguais na linha a cima e em `certificado.py`!

* Para usar o sistema, execute:

    `python3 server.py`

    `python3 client.py`

    * O cliente tem acesso a base de dados do server, para usar:

        * Buscar um item da base:
        
            GET id

        * Incluir item:

            SET id contudo