import scapy.all as scapy
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def scan(ip):
    print(f"[+] Scanning {ip}....")
    arp_request = scapy.ARP(pdst=ip) 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast = broadcast/arp_request 
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=1)[0] 
    client_list = []

    for packet in answered_list:
        client_dict = {"ip": packet[1].psrc, "mac": packet[1].hwsrc}
        client_list.append(client_dict)
    print(client_list)

def user_stop(timer):
    input("Press Enter to stop the scan...\n")
    timer.cancel()
    print("Scan stopped.")

subnet = "192.168.0.0/24"  

timer = RepeatTimer(1.0, scan, [subnet])
timer.start()

# Permitir ao usuário decidir quando parar o script
user_stop(timer)

#linha 11 : Cria um pacote ARP passando o ip da rede
#linha 12:  Cria um pacote Ethernet que será enviado para o endereço de broadcast (todos os dispositivos na rede)
#linha 13: Combina os pacotes ARP e Ethernet em um único pacote

#linha 14: SRP -> send and receive packets . Diz que o pacote combinado será enviado, espera o tempo do timeout, em segundos, por respostas antes de considerar que não há mais respostas
#verbose = 1 indica que será impresso informações sobre o que está acontecendo, '0' desativa essas mensagens
#O método srp retorna uma tupla contendo duas listas: (answered_list, unanswered_list) [0] no final da chamada srp seleciona apenas a primeira lista, que é a answered_list.

#linha 17 ( FOR ): Para cada resposta recebida, extrai o IP e o MAC do dispositivo e adiciona à lista de clientes.
#Então para cada resposta é criado um dicionário com chaves ip e mac dos dispositivos da rede e cada dicionário é adicionado na lista client_list
# cada elemento de answered_list é uma tupla de dois elementos packet[1] refere-se ao segundo elemento da tupla, que é o pacote recebido
#psrc se refere ao endereço IP da máquina que respondeu e o hwsrc é o endereço MAC da máquina que respondeu

#linha 20: É impresso a lista de clientes