import scapy.all as scapy
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def scan(ip):
    print(f"[+] Scanning {ip}....")
    arp_request = ARP(pdst=ip) # cria uma requisição ARP para a rede especificada pelo ip.
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff") # cria um pacote de broadcast Ethernet para que todos os dispositivos na rede recebam a requisição.
    arp_request_broadcast = broadcast/arp_request # (combina os pacotes ARP e de broadcast.)
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]  # envia o pacote e recebe as respostas.

    client_list = []

    # coleta os endereços IP e MAC das respostas e os armazena em uma lista de dicionários nesse loop:
    for packet in answered_list:
        client_dict = {"ip": packet[1].psrc, "mac": packet[1].hwsrc}
        client_list.append(client_dict)
    print(client_list)

# Função para permitir ao usuário parar o script
def user_stop(timer):
    input("Press Enter to stop the scan...\n")
    timer.cancel()
    print("Scan stopped.")


subnet = "10.0.84.0/24"  

# Inicie o scanner com um intervalo de 1 segundo
timer = RepeatTimer(1.0, scan, [subnet])
timer.start()

# Permitir ao usuário decidir quando parar o script
user_stop(timer)
