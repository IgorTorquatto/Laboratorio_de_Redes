from socket import *
import time

# Configurações de socket e servidor
sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(1)  # Definindo tempo limite de 1 segundo

# Variáveis para cálculo de estatísticas
RTTmin = None
RTTmax = 0
qtdPings = 10
pingsPerdidos = 0
somaRTTs = 0
pingsComRTT = 0  # Contador para pings com RTT válido

# Loop para enviar 10 pings
for a in range(1, qtdPings + 1):
    message = f'Ping {a} - {time.strftime("%H:%M:%S")}'
    tempo_envio = time.time_ns()  # Tempo de envio em nanosegundos
    sock.sendto(message.encode(), ("127.0.0.1", 50000))

    try:
        # Recebe resposta do servidor
        data, server = sock.recvfrom(1024)
        tempo_recebido = time.time_ns()
        RTTsec = (tempo_recebido - tempo_envio) / 1_000_000_000  # Converte RTT para segundos

        # Apenas registra RTTs válidos
        somaRTTs += RTTsec
        pingsComRTT += 1
        print(f"Servidor retornou a mensagem: {data.decode()}\nRTT: {RTTsec:.3f} s")

        # Atualizar RTTmin e RTTmax com RTT válido
        RTTmin = RTTsec if RTTmin is None else min(RTTmin, RTTsec)
        RTTmax = max(RTTmax, RTTsec)

    except timeout:
        # Trata o tempo limite de resposta
        pingsPerdidos += 1
        print("Request time out")

    print("-" * 20)

# Cálculo da média de RTT usando apenas pings com RTT válidos
RTTmedio = somaRTTs / pingsComRTT if pingsComRTT > 0 else 0
porcentagem_perda = (pingsPerdidos * 100) / qtdPings

# Exibição dos resultados finais
print("RTT máximo:", RTTmax)
print("RTT mínimo:", RTTmin if RTTmin is not None else "Nenhum RTT válido")
print("RTT médio:", RTTmedio)
print("Perda de pacotes:", porcentagem_perda, "%")
