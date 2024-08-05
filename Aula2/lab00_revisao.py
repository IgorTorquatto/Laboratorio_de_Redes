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

    print(answered_list)

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
