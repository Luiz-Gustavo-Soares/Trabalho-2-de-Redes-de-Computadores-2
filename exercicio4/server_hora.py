
import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"

# Contador compartilhado entre as threads
total_atendimentos = 0

lock = threading.Lock()


def atender_cliente(conn, endereco):
    """
    Atende ao cliente, recebendo uma solicitação e enviando a hora atual.

    Args:
        conn (socket.socket): O socket de conexão com o cliente.
        endereco (tuple): O endereço do cliente no formato (ip, porta).
    """
    global total_atendimentos

    ip, porta = endereco

    try:
        with conn:
            solicitacao = conn.recv(1024)

            if not solicitacao:
                return

            # Incrementa o contador de forma thread-safe
            with lock:
                total_atendimentos += 1
                contador = total_atendimentos

            agora = datetime.now()

            hora = agora.strftime("%H:%M:%S")
            data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")

            conn.sendall(hora.encode("utf-8"))

            print(
                f"[{data_hora}] "
                f"Cliente: {ip}:{porta} | "
                f"Atendimento: {contador} | "
                f"Hora enviada: {hora}"
            )

    except (ConnectionError, OSError) as erro:
        print(f"Erro ao atender {ip}:{porta}: {erro}")


def iniciar_servidor(port):
    """
    Inicia o servidor de hora, escutando na porta especificada e atendendo clientes.

    Args:
        port (int): A porta na qual o servidor deve escutar.
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST, port))
        servidor.listen()

        print(f"Servidor de hora iniciado na porta {port}")

        while True:
            conn, endereco = servidor.accept()

            thread = threading.Thread(
                target=atender_cliente,
                args=(conn, endereco)
            )

            thread.start()

    except KeyboardInterrupt:
        print("\nServidor encerrado.")

    finally:
        servidor.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Hora TCP Server.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de execucao do servidor', default=7000)

    args = parser.parse_args()

    iniciar_servidor(args.port)
