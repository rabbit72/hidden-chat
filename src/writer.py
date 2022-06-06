import argparse
import asyncio
import json
import logging

import aiofiles

USER_TOKEN_FILE = "./.secret"


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

EMPTY_STRING = ""


async def load_user_token(target: str) -> str:
    try:
        async with aiofiles.open(target, mode="r") as f:
            secret = await f.read()
            if not secret:
                return EMPTY_STRING
            return json.loads(secret)["account_hash"]
    except FileNotFoundError:
        return EMPTY_STRING


async def register_new_user(address, port, user_name: str) -> dict:
    reader, writer = await asyncio.open_connection(address, port)
    await read_message(reader)
    send_message(writer, "\n")
    await read_message(reader)
    send_message(writer, user_name + "\n")
    user_data = json.loads(await read_message(reader))
    writer.close()
    if not user_data:
        print("Error during registration")
        exit()
    return user_data


async def save_user_token(target: str, user_secret: dict):
    async with aiofiles.open(target, mode="w") as f:
        await f.write(json.dumps(user_secret) + "\n")


async def authenticate(reader, writer, user_token: str) -> bool:
    success_authentication_message = (
        "Welcome to chat! Post your message below. End it with an empty line."
    )
    await read_message(reader)
    send_message(writer, user_token + "\n")
    user_data = json.loads(await read_message(reader))
    if not user_data:
        return False
    greeting = await read_message(reader)
    return success_authentication_message in greeting


def send_message(writer, message: str):
    logger.debug(message.rstrip())
    encoded_message = message.encode()
    writer.write(encoded_message)


async def read_message(reader) -> str:
    message = await reader.readline()
    decoded_message = message.decode()
    logger.debug(decoded_message.rstrip())
    return decoded_message


async def main(address: str, port: int, new_user_name: str):
    if new_user_name:
        user_secret = await register_new_user(address, port, new_user_name)
        await save_user_token(USER_TOKEN_FILE, user_secret)

    user_token = await load_user_token(USER_TOKEN_FILE)
    if not user_token:
        print("Нет токена. Зарегистрируйте заново с --register {user}")
        exit()

    message = "----------- Я СНОВА ТЕСТИРУЮ ЧАТИК.---------------"
    reader, writer = await asyncio.open_connection(address, port)
    if await authenticate(reader, writer, user_token):
        send_message(writer, message + "\n\n")
        await read_message(reader)
    else:
        print(
            f"Неизвестный токен. "
            f"Проверьте его или зарегистрируйте заново: {user_token}"
        )
        exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--host", type=str, default="minechat.dvmn.org")
    parser.add_argument("--port", type=int, default=5050)
    parser.add_argument("--register", type=str)

    args = parser.parse_args()
    asyncio.run(main(args.host, args.port, args.register))
