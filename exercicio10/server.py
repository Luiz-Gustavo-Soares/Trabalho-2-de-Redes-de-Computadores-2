# Grupo: Luiz Gustavo Soares, Italo Felipe Santos Rocha

import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

HOST = "0.0.0.0"

clientes = {}


async def transmitir(mensagem, remetente=None):
    """
    Transmite uma mensagem para todos os clientes conectados, exceto o remetente.

    Args:
        mensagem (str): A mensagem a ser transmitida.
        remetente (WebSocketServerProtocol, optional): A conexão do cliente remetente 
            que deve ser excluída da transmissão. O padrão é None.
    """
    conexoes = list(clientes.keys())

    tarefas = [
        cliente.send(mensagem)
        for cliente in conexoes
        if cliente != remetente
    ]

    # Envia para todos simultaneamente
    resultados = await asyncio.gather(
        *tarefas,
        return_exceptions=True
    )

    # Identifica conexões que falharam
    for cliente, resultado in zip(
        [c for c in conexoes if c != remetente],
        resultados
    ):
        if isinstance(resultado, Exception):
            try:
                await cliente.close()
            except Exception:
                pass


async def atender_cliente(websocket):
    """
    Gerencia o ciclo de vida da conexão de um cliente individual no chat.

    Lida com o registro do nickname, recebimento e repasse de mensagens, 
    além de tratar desconexões e limpeza de estado.

    Args:
        websocket (WebSocketServerProtocol): A conexão WebSocket do cliente.
    """
    nickname = None

    try:
        # Primeira mensagem recebida é o nickname
        nickname = await websocket.recv()
        nickname = nickname.strip()

        if not nickname:
            await websocket.close(
                reason="Nickname inválido"
            )
            return

        clientes[websocket] = nickname

        print(f"{nickname} entrou no chat.")

        await transmitir(
            f"*** {nickname} entrou no chat ***",
            websocket
        )

        async for mensagem in websocket:
            mensagem = mensagem.strip()

            if not mensagem:
                continue

            print(f"[{nickname}]: {mensagem}")

            await transmitir(
                f"[{nickname}]: {mensagem}",
                websocket
            )

    except ConnectionClosed:
        print(f"Conexão perdida: {nickname}")

    finally:
        if nickname and clientes.pop(websocket, None):
            print(f"{nickname} saiu do chat.")

            await transmitir(
                f"*** {nickname} saiu do chat ***"
            )


async def iniciar_servidor(port):
    """
    Inicializa e mantém em execução o servidor WebSocket na porta especificada.

    Args:
        port (int): O número da porta onde o servidor escutará as conexões.

    """
    print(f"Servidor WebSocket iniciado na porta {port}")

    async with serve(
        atender_cliente,
        HOST,
        port
    ):
        await asyncio.Future()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Websocket Server.'
    )

    parser.add_argument('-p', '--port', type=int, help='porta de execucao do servidor', default=8765)

    args = parser.parse_args()

    try:
        asyncio.run(iniciar_servidor(args.port))

    except KeyboardInterrupt:
        print("\nServidor encerrado.")
