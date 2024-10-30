from socket import *
import time

# Configurações do socket e endereço do servidor
sock = socket(AF_INET, SOCK_DGRAM)
server_address = ('127.0.0.1', 50000)
sock.settimeout(1)  # Tempo limite de 1 segundo

# Variáveis de estatísticas
RTTmin = float('inf')
RTTmax = 0
somaRTTs = 0
qtdPings = 10
pingsPerdidos = 0

# Envio de 10 pings
for seq in range(1, qtdPings + 1):
    # Formata a mensagem de acordo com o requisito
    envio_hora = time.strftime("%H:%M:%S", time.localtime())
    message = f'Ping {seq} - {envio_hora}'
    tempo_envio = time.time() #marca o tempo de envio do ping  em segundos

    # Envia a mensagem para o servidor
    sock.sendto(message.encode(), server_address)
    try:
        # Recebe a resposta do servidor e calcula o RTT
        data, _ = sock.recvfrom(1024)
        tempo_recebido = time.time() #captura o tempo de recebimento do ping
        RTTsec = tempo_recebido - tempo_envio
        somaRTTs += RTTsec

        # Imprime a resposta e o RTT calculado
        print(f"Servidor retornou a mensagem: {data.decode()}\nRTT: {RTTsec:.6f} s")

        # Atualiza RTTmin e RTTmax
        RTTmin = min(RTTmin, RTTsec)
        RTTmax = max(RTTmax, RTTsec)
    except timeout:
        # Se o tempo limite for excedido, considera o ping como perdido
        pingsPerdidos += 1
        print("Request time out")

    print("-" * 20)

# Estatísticas finais
if qtdPings - pingsPerdidos > 0:
    RTTmedio = somaRTTs / (qtdPings - pingsPerdidos)
else:
    RTTmedio = 0
perda_percentual = (pingsPerdidos / qtdPings) * 100 #porcentagem da perda ( pings perdidos em 10)

print(f"RTT máximo: {RTTmax:.6f}")
print(f"RTT mínimo: {RTTmin:.6f}")
print(f"RTT médio: {RTTmedio:.6f}")
print(f"Perda de pacotes: {perda_percentual:.1f}%")
