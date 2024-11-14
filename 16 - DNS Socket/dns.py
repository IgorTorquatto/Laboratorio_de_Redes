import socket

# Matriz com os nomes e endereços IP fictícios
dns_table = {
    "alice": "192.168.4.20",
    "bob": "192.168.4.21",
    "charlie": "192.168.4.22",
}

# Configurações do servidor DNS
server_ip = "192.168.4.13"  # IP da máquina do servidor DNS
server_port = 1234  # Porta de escuta do servidor DNS

# Cria o socket UDP
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
