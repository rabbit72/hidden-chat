import asyncio


async def listen_hidden_chat(address: str, port: int):
    reader, writer = await asyncio.open_connection(address, port)
    while True:
        message = await reader.readline()
        print(message.decode().rstrip())


if __name__ == '__main__':
    address, port = "minechat.dvmn.org", 5000
    asyncio.run(listen_hidden_chat(address, port))
