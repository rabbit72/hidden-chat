import argparse
import asyncio
import datetime

import aiofiles


async def main(address, port, history_file_path):
    async with aiofiles.open(history_file_path, mode="a") as log_file:
        reader, writer = await asyncio.open_connection(address, port)
        while True:
            encoded_message: bytes = await reader.readline()
            message = encoded_message.decode()

            now = datetime.datetime.now()
            datetime_string = now.strftime("%d.%m.%y %H:%M")
            formatted_message = f"[{datetime_string}] {message}"

            await log_file.write(formatted_message)
            print(formatted_message, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--host", type=str, default="minechat.dvmn.org")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--history", type=str, default="./history.log")

    args = parser.parse_args()
    asyncio.run(main(args.host, args.port, args.history))
