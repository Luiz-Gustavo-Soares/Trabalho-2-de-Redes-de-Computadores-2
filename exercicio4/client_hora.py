
import socket


def solicitar_hora(host, port):
    """
    Solicita a hora atual do servidor e a exibe na tela.

    Args:
        host (str): O endereço IP do servidor.
        port (int): A porta do servidor.

    Raises:
        ConnectionRefusedError: Se o servidor estiver indisponível.
        ConnectionError: Se ocorrer um erro de conexão.
        OSError: Se ocorrer um erro de sistema operacional.
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((host, port))

        cliente.sendall("HORA".encode("utf-8"))

        resposta = cliente.recv(1024).decode("utf-8")

        if resposta:
            print(f"Hora atual do servidor: {resposta}")
        else:
            print("Servidor encerrou a conexão sem responder.")

    except ConnectionRefusedError:
        print("Erro: servidor indisponível.")

    except (ConnectionError, OSError) as erro:
        print(f"Erro de comunicação: {erro}")

    finally:
        cliente.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Hora TCP Cliente.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de cenecao no servidor', default=7000)
    parser.add_argument('-s', '--host', type=str, help='host de cenecao no servidor', default='127.0.0.1')

    args = parser.parse_args()

    solicitar_hora(args.host, args.port)

