import scapy.all as scapy
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def scan(ip):
    print(f"[+] Scanning {ip}....")
    arp_request = scapy.ARP(pdst=ip)  # cria uma requisição ARP para a rede especificada pelo ip.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # cria um pacote de broadcast Ethernet para que todos os dispositivos na rede recebam a requisição.
    arp_request_broadcast = broadcast/arp_request  # combina os pacotes ARP e de broadcast.
    
    print("[+] Sending ARP request...")
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    client_list = []

    if answered_list:
        print(f"[+] Received {len(answered_list)} responses")
    else:
        print("[+] No responses received")

    # coleta os endereços IP e MAC das respostas e os armazena em uma lista de dicionários nesse loop:
    for packet in answered_list:
        client_dict = {"ip": packet[1].psrc, "mac": packet[1].hwsrc}
        client_list.append(client_dict)
    
    if client_list:
        print("[+] Clients found:")
        for client in client_list:
            print(f"IP: {client['ip']}, MAC: {client['mac']}")
    else:
        print("[+] No clients found")

    print(client_list)

# Função para permitir ao usuário parar o script
def user_stop(timer):
    input("Press Enter to stop the scan...\n")
    timer.cancel()
    print("Scan stopped.")

# Defina o intervalo de rede a ser escaneado
subnet = "10.0.84.0/24"  # Mude para o intervalo da sua rede

# Inicie o scanner com um intervalo de 1 segundo
timer = RepeatTimer(1.0, scan, [subnet])
timer.start()

# Permitir ao usuário decidir quando parar o script
user_stop(timer)
