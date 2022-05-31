import argparse
import asyncio
import logging


def create_logger() -> logging.Logger:
    logger = logging.getLogger("sender")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


logger = create_logger()


def send_message(writer, message: str):
    logger.debug(message.rstrip())
    encoded_message = message.encode()
    writer.write(encoded_message)


async def read_message(reader) -> str:
    message = await reader.readline()
    decoded_message = message.decode()
    logger.debug(decoded_message.rstrip())
    return decoded_message


async def main(address, port, user):
    message = "----------- Я СНОВА ТЕСТИРУЮ ЧАТИК.---------------"
    reader, writer = await asyncio.open_connection(address, port)
    await read_message(reader)
    send_message(writer, user + "\n")
    await read_message(reader)
    await read_message(reader)
    send_message(writer, message + "\n\n")
    await read_message(reader)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--host", type=str, default="minechat.dvmn.org")
    parser.add_argument("--port", type=int, default=5050)
    parser.add_argument(
        "--user", type=str, default="929521e0-e034-11ec-8c47-0242ac110002"
    )

    args = parser.parse_args()
    asyncio.run(main(args.host, args.port, args.user))
