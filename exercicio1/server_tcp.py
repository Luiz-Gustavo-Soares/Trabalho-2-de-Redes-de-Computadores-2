# Grupo: Luiz Gustavo Soares, Italo Felipe Santos Rocha

import socket
import threading
from datetime import datetime


def atender_cliente(conn, endereco):
    """Atende a uma conexão de cliente TCP individual em uma thread dedicada.

    Recebe mensagens do cliente, valida seu conteúdo, imprime os dados no console 
    com carimbo de data/hora e envia uma resposta de confirmação.

    Args:
        conn (socket.socket): Objeto socket da conexão estabelecida com o cliente.
        endereco (tuple): Tupla contendo o endereço IP (str) e a porta (int) do cliente.

    Raises:
        ConnectionResetError: Se a conexão for encerrada abruptamente pelo cliente.
    """

    ip, porta = endereco

    print(f"[{datetime.now():%d/%m/%Y %H:%M:%S}] "
          f"Cliente conectado: {ip}:{porta}")

    try:
        with conn:
            while True:
                dados = conn.recv(1024)

                # Cliente encerrou a conexão
                if not dados:
                    break

                mensagem = dados.decode("utf-8").strip()

                # Validação de mensagem vazia
                if not mensagem:
                    conn.sendall("Mensagem vazia".encode("utf-8"))
                    continue

                print(f"[{datetime.now():%d/%m/%Y %H:%M:%S}] "
                      f"{ip}:{porta} -> {mensagem}")

                conn.sendall("Mensagem recebida".encode("utf-8"))

    except ConnectionResetError:
        print(f"Conexão perdida com {ip}:{porta}")

    finally:
        print(f"Cliente desconectado: {ip}:{porta}")


def iniciar_servidor(porta):
    """Inicializa o servidor TCP, aguarda conexões e gerencia threads para cada cliente.

    Configura o socket do servidor, associa-o ao endereço IP '0.0.0.0' na porta 
    especificada e entra em um loop infinito aceitando novas conexões de clientes,
    iniciando uma nova thread para cada atendimento.

    Args:
        porta (int): Número da porta em que o servidor irá escutar as conexões.
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(("0.0.0.0", porta))
        servidor.listen()

        print(f"Servidor TCP iniciado na porta {porta}")
        print("Aguardando conexões...")

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
        description='Server TCP.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de execucao do servidor', default=5000)

    args = parser.parse_args()

    iniciar_servidor(args.port)
