import socket
import threading
import sys

# Função para lidar com cada conexão (cliente)
def clientthread(conn):
    try:
        # Recebe dados do cliente (a requisição HTTP)
        data = conn.recv(1024).decode()

        if not data:
            return  # Se não houver dados, encerra a conexão

        # Exibe a requisição recebida (apenas para debug)
        print("Requisição recebida:")
        print(data)

        # Verifica se o navegador está requisitando "/hello"
        if "GET /hello " in data:
            # Resposta HTTP válida com "hello world"
            response = (
                "HTTP/1.1 200 OK\r\n"  # Status da resposta
                "Content-Type: text/plain\r\n"  # Tipo do conteúdo
                "Content-Length: 11\r\n"  # Tamanho do corpo da mensagem
                "\r\n"  # Separador entre cabeçalho e corpo
                "hello world"  # Corpo da resposta
            )
        else:
            # Resposta para outros caminhos (404 Not Found)
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "404 Not Found"
            )

        # Envia a resposta ao cliente
        conn.sendall(response.encode())
    except Exception as e:
        print(f"Erro ao processar a conexão: {e}")
    finally:
        # Fecha a conexão
        conn.close()

host = ''
port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Garante que o socket será destruído (pode ser reusado) após uma interrupção da execução
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to local host and port
try:
    s.bind((host, port))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

s.listen(1)

print(f"Servidor rodando em http://localhost:{port}/")

# Continua recebendo conexões
while True:
    # Aceita conexões
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # Cria nova thread para uma nova conexão.
    threading.Thread(target=clientthread, args=(conn,)).start()
