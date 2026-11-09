# Grupo: Luiz Gustavo Soares, Italo Felipe Santos Rocha, Tayna Lino de Carvalho

import socket

MAX_UDP_PAYLOAD = 65507
TIMEOUT = 5


def iniciar_cliente(host, porta):
    """Inicia o cliente UDP para envio de mensagens e recepção de ecos.

    O cliente conecta-se ao host e porta especificados via UDP, permitindo que o
    usuário envie mensagens interativamente. Possui validação de tamanho de payload,
    timeout configurado para respostas e tratamento de encerramento.

    Args:
        host (str): O endereço IP ou nome de host do servidor UDP.
        porta (int): A porta de rede em que o servidor está escutando.

    Raises:
        OSError: Se houver falha crítica na criação ou comunicação do socket.
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Aguarda no máximo 5 segundos pela resposta
    cliente.settimeout(TIMEOUT)

    try:
        while True:
            mensagem = input("Digite uma mensagem (ou 'sair'): ")

            if mensagem.strip().lower() == "sair":
                print("Cliente encerrado.")
                break

            if not mensagem.strip():
                print("Erro: mensagem vazia.")
                continue

            dados = mensagem.encode("utf-8")

            # Validação do tamanho máximo
            if len(dados) > MAX_UDP_PAYLOAD:
                print("Erro: mensagem excede o limite UDP.")
                continue

            cliente.sendto(dados, (host, porta))

            try:
                resposta, endereco = cliente.recvfrom(
                    MAX_UDP_PAYLOAD
                )

                print(f"Echo recebido: {resposta.decode('utf-8')}")

            except socket.timeout:
                print("Erro: servidor não respondeu dentro do prazo.")

    except OSError as erro:
        print(f"Erro de comunicação: {erro}")

    finally:
        cliente.close()
        print("Socket fechado.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Cliente UDP.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de cenecao no servidor', default=6000)
    parser.add_argument('-s', '--host', type=str, help='host de cenecao no servidor', default='127.0.0.1')

    args = parser.parse_args()

    iniciar_cliente(args.host, args.port)
