# Grupo: Luiz Gustavo Soares, Italo Felipe Santos Rocha

import asyncio
import websockets
from websockets.exceptions import ConnectionClosed



async def receber_mensagens(websocket):
    """Recebe e exibe mensagens enviadas pelo servidor via WebSocket.

    Fica escutando continuamente por novas mensagens na conexão e as imprime
    no console. Encerra a execução caso a conexão seja fechada.

    Args:
        websocket (websockets.client.WebSocketClientProtocol): A conexão
            ativa com o servidor WebSocket.

    Raises:
        ConnectionClosed: Se a conexão com o servidor for encerrada inesperadamente.
    """
    try:
        async for mensagem in websocket:
            print(mensagem)

    except ConnectionClosed:
        print("Conexão com o servidor encerrada.")


async def iniciar_cliente(host, port):
    """Inicializa o cliente de chat WebSocket, lidando com entrada e envio de mensagens.

    Solicita um nickname ao usuário, estabelece a conexão com o servidor,
    envia o nickname inicial e gerencia simultaneamente o envio de mensagens
    digitadas pelo usuário e o recebimento de mensagens do chat.

    Args:
        host (str): O endereço IP ou hostname do servidor WebSocket.
        port (int): A porta em que o servidor WebSocket está escutando.
    """
    uri = f"ws://{host}:{port}"

    nickname = input("Digite seu nickname: ").strip()

    if not nickname:
        print("Nickname inválido.")
        return

    try:
        async with websockets.connect(uri) as websocket:

            await websocket.send(nickname)

            print("Conectado ao chat!")
            print("Digite 'sair' para desconectar.")

            # Cria uma tarefa para receber mensagens
            tarefa_recebimento = asyncio.create_task(
                receber_mensagens(websocket)
            )

            try:
                while True:
                    mensagem = await asyncio.to_thread(input)

                    if mensagem.strip().lower() == "sair":
                        break

                    if not mensagem.strip():
                        continue

                    await websocket.send(mensagem)

            finally:
                await websocket.close()

                tarefa_recebimento.cancel()

                await asyncio.gather(
                    tarefa_recebimento,
                    return_exceptions=True
                )

    except ConnectionRefusedError:
        print("Servidor indisponível.")

    except ConnectionClosed:
        print("Conexão encerrada pelo servidor.")

    except OSError as erro:
        print(f"Erro de comunicação: {erro}")

    finally:
        print("Cliente encerrado.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Websocket Cliente.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de cenecao no servidor', default=8765)
    parser.add_argument('-s', '--host', type=str, help='host de cenecao no servidor', default='127.0.0.1')

    args = parser.parse_args()

    asyncio.run(iniciar_cliente(args.host, args.port))
