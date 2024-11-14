import socket

# Configurações do cliente DNS
server_ip = "192.168.4.13"  # IP do servidor DNS
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
