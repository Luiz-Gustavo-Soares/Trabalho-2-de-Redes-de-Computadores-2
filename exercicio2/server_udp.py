# Grupo: Luiz Gustavo Soares, Italo Felipe Santos Rocha

import socket
from datetime import datetime

MAX_UDP_PAYLOAD = 65507


def iniciar_servidor(porta):
    """Inicia um servidor UDP que escuta em uma porta específica.

    O servidor aguarda por mensagens recebidas de clientes, exibe as informações
    de data/hora, IP, porta e o conteúdo da mensagem no console, e realiza um
    'echo' (envia de volta a mesma mensagem recebida) para o cliente.

    Args:
        porta (int): O número da porta em que o servidor irá escutar as conexões UDP.

    Raises:
        KeyboardInterrupt: Quando o usuário interrompe a execução com Ctrl+C.
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        servidor.bind(("0.0.0.0", porta))

        print(f"Servidor UDP iniciado na porta {porta}")
        print("Aguardando mensagens...")

        while True:
            dados, endereco = servidor.recvfrom(MAX_UDP_PAYLOAD)

            ip, porta_cliente = endereco
            mensagem = dados.decode("utf-8", errors="replace")

            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            print(
                f"[{data_hora}] {ip}:{porta_cliente} -> {mensagem}"
            )

            # Envia a mesma mensagem recebida
            servidor.sendto(dados, endereco)

    except KeyboardInterrupt:
        print("\nServidor encerrado.")

    finally:
        servidor.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Server TCP.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de execucao do servidor', default=6000)

    args = parser.parse_args()

    iniciar_servidor(args.port)
