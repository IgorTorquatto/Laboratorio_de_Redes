import random
from socket import *

# Cria o socket UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Define o endereço e a porta do socket
serverSocket.bind(('', 50000))

while True:

    # Gera números randômicos entre 0 to 10
    rand = random.randint(0, 10)

    # Recebe o pacote e o endereço do cliente
    message, address = serverSocket.recvfrom(1024)

    # Coloca a mensagem em maíusculo
    message = message.upper()

    # Se o número rand é menor que 4, consideramos o pacote perdido.
    if rand < 4:
        continue
    
    #Caso contrário, o servidor responde
    serverSocket.sendto(message, address)