from socket import *
import time
import datetime

sock = socket(AF_INET, SOCK_DGRAM)

client_address = ('', 50000)
sock.settimeout(1)

RTTmin = RTTmax = RTTmean = 0
qtdPings = 10
pingsPerderdidos = 0
somaRTTs = 0

for a in range(0, qtdPings):
    
    message = 'Ping ' + str(a) + ' - ' + str(time.localtime().tm_hour)
    tempo_envio = time.time_ns()
    sock.sendto(message.encode(), ("", 50000))

    try:
        data = sock.recv(1024)
        tempo_recebido = time.time_ns()
        RTTsec = (tempo_recebido - tempo_envio) / 1000000000
        somaRTTs += RTTsec
        print("Servidor retornou a mensagem: ", data.decode(), '\nRTT: ', RTTsec , ' s')
        if a == 0:
            RTTmin = RTTmax = RTTsec

        if RTTsec < RTTmin:
            RTTmin = RTTsec

        if RTTsec > RTTmax:
            RTTmax
    except: 
        RTTmax = 1
        pingsPerderdidos += 1
        somaRTTs += 1
        print("Request time out")

    print("-" * 20)

porcentagem = (pingsPerderdidos * 100) / qtdPings

print("RTTmax: ", RTTmax)
print("RTTmin: ", RTTmin)
print("RTTmédio: ", somaRTTs / qtdPings)
print("Perda de pacotes: ", porcentagem, "%")