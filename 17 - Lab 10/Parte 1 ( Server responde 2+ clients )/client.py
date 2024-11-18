import socket

def client_program():
    host = 'localhost'  # Host do servidor (use 'localhost' ou o IP do servidor)
    port = 1234         # Porta usada pelo servidor

    # Cria o socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta ao servidor
        client_socket.connect((host, port))
        print("Conectado ao servidor.")

        while True:
            # Envia uma mensagem ao servidor
            message = input("Digite a mensagem para o servidor (ou 'sair' para encerrar): ")
            if message.lower() == 'sair':
                break

            client_socket.sendall(message.encode('utf-8'))  # Envia a mensagem ao servidor
            data = client_socket.recv(1024).decode('utf-8')  # Recebe a resposta do servidor
            print("Resposta do servidor:", data)

    except Exception as e:
        print(f"Erro na conexão: {e}")

    finally:
        # Fecha o socket do cliente
        client_socket.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    client_program()
