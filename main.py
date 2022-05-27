import asyncio
import aiofiles
import datetime


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


if __name__ == '__main__':
    address, port = "minechat.dvmn.org", 5000
    history_file_path = "./history.log"
    asyncio.run(main(address, port, history_file_path))
