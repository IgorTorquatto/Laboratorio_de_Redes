import socket

'''
Código do Cliente DNS

O cliente DNS solicita um endereço IP ao servidor DNS enviando um nome
e recebe a resposta com o IP correspondente. Depois, envia uma mensagem
para o destinatário no IP e porta recebidos.

Para implementar o cliente:

O cliente utiliza o IP e a porta do servidor para se conectar.
Essas variáveis especificam onde o servidor DNS está rodando.
O IP foi definido como "127.0.0.1" para rodar localmente.

O cliente solicita ao usuário que digite o nome do destinatário.
Esse nome será enviado ao servidor DNS para consulta.

Criei um socket utilizando a biblioteca 'socket' do python
AF_INET -> especifica que estamos utilizando o protocolo IPV4
SOCK_DGRAM -> especifica o uso do protocolo de transporte UDP

sock.sendto(name.encode("utf-8"), (server_ip, server_port)) ->
envia o nome do destinatário para o servidor DNS.
A função encode transforma a string em bytes, como necessário para envio.

Após enviar o nome, o cliente aguarda a resposta do servidor DNS.
sock.recvfrom(1024) -> recebe a resposta do servidor com tamanho máximo de 1024 bytes.
A resposta inclui o endereço IP correspondente ou uma mensagem de erro.

Se o IP retornado pelo servidor for "Nome não encontrado", o cliente informa ao usuário
que o nome solicitado não foi encontrado.

Caso contrário, o cliente exibe o IP correspondente na tela.
Após isso, ele prepara e envia uma mensagem ao destinatário no IP e porta especificados.

destination_port = 60500 -> porta onde o destinatário está escutando

A mensagem é definida como uma string para simular uma comunicação com o destinatário.
sock.sendto(message.encode("utf-8"), (ip_address, destination_port)) ->
envia a mensagem para o destinatário usando o IP e porta.

No final, sock.close() encerra o socket após o envio da mensagem.

Esse cliente DNS simula uma interação básica onde ele consulta o servidor DNS
por um IP e envia uma mensagem ao destinatário depois de obter a resposta.
'''


# Configurações do cliente DNS
server_ip = "127.0.0.1"  # IP do servidor DNS
server_port = 1234  # Porta do servidor DNS

# Nome do destinatário para obter o IP
name = input("Digite o nome do destinatário: ")

# Cria o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia o nome do destinatário para o servidor DNS
sock.sendto(name.encode("utf-8"), (server_ip, server_port))

# Recebe o IP correspondente do servidor DNS
ip_address, _ = sock.recvfrom(1024)
ip_address = ip_address.decode("utf-8")

if ip_address == "Nome não encontrado":
    print("O nome solicitado não foi encontrado no servidor DNS.")
else:
    print(f"Endereço IP de {name}: {ip_address}")

    # Configurações para enviar a mensagem ao destinatário
    destination_port = 60500  # Porta onde o destinatário está escutando
    message = "Olá, estou enviando uma mensagem via cliente DNS!"

    # Envia a mensagem para o destinatário
    sock.sendto(message.encode("utf-8"), (ip_address, destination_port))
    print(f"Mensagem enviada para {name} ({ip_address}:{destination_port})")

sock.close()
