# Grupo: Luiz Gustavo Soares, Italo Felipe Santos Rocha

import socket
import threading




def receber_mensagens(arquivo):
    """Recebe e imprime mensagens do servidor.

    Args:
        arquivo (file): O arquivo usado para receber mensagens do servidor.

    Raises:
        ConnectionError: Se ocorrer um erro de conexão com o servidor.
        OSError: Se ocorrer um erro de sistema operacional durante a comunicação.
    """
    try:
        for mensagem in arquivo:
            print(mensagem.strip())

    except (ConnectionError, OSError):
        print("Conexão com o servidor perdida.")


def iniciar_cliente(host, port):
    """Inicia o cliente do chat e se conecta ao servidor.

    Args:
        host (str): O endereço IP do servidor.
        port (int): A porta do servidor.

    Raises:
        ConnectionRefusedError: Se o servidor não aceitar a conexão.
        ConnectionError: Se ocorrer um erro de conexão com o servidor.
        OSError: Se ocorrer um erro de sistema operacional durante a comunicação.
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((host, port))

        nickname = input("Digite seu nickname: ").strip()

        if not nickname or "\n" in nickname:
            print("Nickname inválido.")
            return

        cliente.sendall((nickname + "\n").encode("utf-8"))

        arquivo = cliente.makefile("r", encoding="utf-8")

        # Thread responsável por receber mensagens
        thread = threading.Thread(
            target=receber_mensagens,
            args=(arquivo,),
            daemon=True
        )

        thread.start()

        print("Conectado ao chat!")
        print("Digite 'sair' para desconectar.")

        while True:
            mensagem = input()

            cliente.sendall(
                (mensagem + "\n").encode("utf-8")
            )

            if mensagem.strip().lower() == "sair":
                break

    except ConnectionRefusedError:
        print("Servidor indisponível.")

    except (ConnectionError, OSError):
        print("Erro de comunicação com o servidor.")

    finally:
        cliente.close()
        print("Conexão encerrada.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Chat TCP Cliente.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de cenecao no servidor', default=6000)
    parser.add_argument('-s', '--host', type=str, help='host de cenecao no servidor', default='127.0.0.1')

    args = parser.parse_args()

    iniciar_cliente(args.host, args.port)
