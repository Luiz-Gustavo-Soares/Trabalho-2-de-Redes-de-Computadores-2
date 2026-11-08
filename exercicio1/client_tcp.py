
import socket


def iniciar_cliente(host, porta):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((host, porta))
        print(f"Conectado ao servidor {host}:{porta}")

        with cliente:
            while True:
                mensagem = input("Digite uma mensagem (ou 'sair'): ")

                if mensagem.strip().lower() == "sair":
                    print("Encerrando conexão...")
                    break

                # Validação de mensagem vazia
                if not mensagem.strip():
                    print("Erro: a mensagem não pode ser vazia.")
                    continue

                cliente.sendall(mensagem.encode("utf-8"))

                resposta = cliente.recv(1024).decode("utf-8")
                print(f"Servidor: {resposta}")

    except ConnectionRefusedError:
        print("Erro: servidor indisponível ou conexão recusada.")

    except ConnectionError:
        print("Erro: conexão com o servidor foi perdida.")

    finally:
        print("Cliente encerrado.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Cliente TCP.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de cenecao no servidor', default=5000)
    parser.add_argument('-s', '--host', type=str, help='host de cenecao no servidor', default='127.0.0.1')

    args = parser.parse_args()

    iniciar_cliente(args.host, args.port)
