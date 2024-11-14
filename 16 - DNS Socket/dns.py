import socket

'''Código do Servidor

O servidor recebe uma string e envia um endereço IP correspondente

Para implementar o servidor:

Como o servidor precisa saber previamente os nomes e endereços IP utilizei o dicionário do python
O dicionário servirá como nossa "matriz" onde cada chave é o nome e cada valor o endereço IP correspondente, todos fictícios

Utilizei variáveis para especificar o IP e a porta em que o servidor está rodando
O cliente precisará saber essas informações para se conectar ao servidor

Criei um socket utilizando a biblioteca 'socket' do python 
AF_INET -> especifica que estamos utilizando o protocolo IPV4
SOCK_DGRAM -> especifica o uso do protocolo  de transporte UDP

O protocolo de transporte é UDP porque é uma simples consulta rápida DNS então é o ideal

Utilizei o método bind para associar o socket criado ao endereço IP e número de porta especificados
Dessa forma o servidor começa a escutar por mensagens recebidas na porta 1234

While True para manter o servidor em execução
sock.recvfrom(1024) -> escuta por mensagens UDP com tamanho máximo de 1024 bytes e retornando dois valores
data = a mensagem recebida em bytes
client_address: um tupla com o endereço IP e a porta do cliente que enviou a mensagem


name -> A mensagem data é decodificada (decode("utf-8"))
para transformar os bytes em uma string, e strip() remove espaços extras ao redor, caso existam.

dns_table.get(name, "Nome não encontrado") -> verifica se o nome solicitado (name) está presente no dicionário dns_table. 
Se o nome for encontrado, a função get retorna o IP correspondente; caso contrário, retorna "Nome não encontrado"

sock.sendto(ip_address.encode("utf-8"), client_address) -> envia a resposta para o cliente.
A resposta é codificada em bytes e enviada de volta ao endereço do cliente (client_address).

O print  final exibe uma mensagem de log no servidor, indicando o nome solicitado,
o endereço do cliente e a resposta enviada.

'''

dns_table = {
    "alice": "192.168.4.20",
    "bob": "192.168.4.21",
    "charlie": "192.168.4.22",
}

server_ip = "127.0.0.1"  # IP da máquina do servidor DNS
server_port = 1234  # Porta de escuta do servidor DNS

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip, server_port))
print(f"Servidor DNS rodando em {server_ip}:{server_port}")

while True:
    # Recebe o nome do cliente (destinatário)
    data, client_address = sock.recvfrom(1024)
    name = data.decode("utf-8").strip()

    # Procura o IP correspondente na tabela
    ip_address = dns_table.get(name, "Nome não encontrado")

    # Envia o IP de volta ao cliente
    sock.sendto(ip_address.encode("utf-8"), client_address)
    print(f"Solicitação para {name} de {client_address} -> Resposta: {ip_address}")
