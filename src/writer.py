import argparse
import asyncio


def send_message(writer, message: str):
    writer.write(message.encode())


async def main(address, port, user):
    message = "----------- Я СНОВА ТЕСТИРУЮ ЧАТИК.---------------"
    reader, writer = await asyncio.open_connection(address, port)

    send_message(writer, user + "\n")
    send_message(writer, message + "\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--host", type=str, default="minechat.dvmn.org")
    parser.add_argument("--port", type=int, default=5050)
    parser.add_argument(
        "--user", type=str, default="929521e0-e034-11ec-8c47-0242ac110002"
    )

    args = parser.parse_args()
    asyncio.run(main(args.host, args.port, args.user))
