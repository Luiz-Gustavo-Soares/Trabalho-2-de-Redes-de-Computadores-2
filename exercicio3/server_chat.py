# Grupo: Luiz Gustavo Soares, Italo Felipe Santos Rocha, Tayna Lino de Carvalho

import socket
import threading

HOST = "0.0.0.0"

clientes = {}
lock = threading.Lock()


def transmitir(mensagem, remetente=None):
    """Transmite uma mensagem para todos os clientes conectados, exceto o remetente.

    Args:
        mensagem (str): A mensagem a ser transmitida.
        remetente (socket.socket, optional): O socket do cliente remetente que 
            não deve receber a mensagem de volta. O padrão é None.
    """
    dados = (mensagem + "\n").encode("utf-8")

    with lock:
        desconectados = []

        for cliente in clientes:
            if cliente != remetente:
                try:
                    cliente.sendall(dados)
                except OSError:
                    desconectados.append(cliente)

        for cliente in desconectados:
            clientes.pop(cliente, None)


def atender_cliente(conn, endereco):
    """Gerencia a conexão individual de um cliente no chat.

    Lê o apelido inicial, processa as mensagens recebidas, gerencia a saída 
    do chat e garante a limpeza dos recursos ao desconectar.

    Args:
        conn (socket.socket): O objeto socket da conexão do cliente.
        endereco (tuple): O endereço IP e porta do cliente (host, port).
    """
    arquivo = conn.makefile("r", encoding="utf-8")

    try:
        # Primeira mensagem do cliente é o nickname
        nickname = arquivo.readline().strip()

        if not nickname:
            return

        with lock:
            clientes[conn] = nickname

        print(f"{nickname} conectado: {endereco}")

        transmitir(f"*** {nickname} entrou no chat ***", conn)

        for linha in arquivo:
            mensagem = linha.strip()

            if not mensagem:
                continue

            if mensagem.lower() == "sair":
                break

            print(f"[{nickname}]: {mensagem}")

            transmitir(f"[{nickname}]: {mensagem}", conn)

    except (ConnectionError, OSError):
        pass

    finally:
        with lock:
            nickname = clientes.pop(conn, None)

        arquivo.close()
        conn.close()

        if nickname:
            print(f"{nickname} desconectado")
            transmitir(f"*** {nickname} saiu do chat ***")


def iniciar_servidor(port):
    """Inicia um servidor de chat que escuta em uma porta específica.

    Args:
        port (int): A porta em que o servidor deve escutar.

    Raises:
        KeyboardInterrupt: Se o servidor for encerrado manualmente pelo usuário.
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((HOST, port))
    servidor.listen()

    print(f"Servidor de chat iniciado na porta {port}")

    try:
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
        description='Chat TCP Server.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de execucao do servidor', default=6000)

    args = parser.parse_args()

    iniciar_servidor(args.port)
