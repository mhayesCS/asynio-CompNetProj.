import asyncio

async def connect_to_server(ip, port):
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        return reader, writer
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None, None

async def send_message(writer, message):
    try:
        writer.write(message.encode())
        await writer.drain()
    except Exception as e:
        print(f"Error sending message to server: {e}")

async def receive_response(reader):
    try:
        response = await reader.read(1024)
        return response.decode().strip()
    except Exception as e:
        print(f"Error receiving response from server: {e}")
        return None

async def main():
    try:
        reader, writer = await connect_to_server('127.0.0.1', 12000)
        if reader and writer:
            while True:
                message = input("Enter message to send (type 'exit' to quit): ")
                await send_message(writer, message)
                response = await receive_response(reader)
                if response:
                    print(f"Received response from server: {response}")
                if message.lower() == 'exit':
                    break
            writer.close()
            await writer.wait_closed()
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    asyncio.run(main())
