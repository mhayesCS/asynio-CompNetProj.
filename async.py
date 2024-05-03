import asyncio

class P2PServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.peers = []

    async def handle_client(self, reader, writer):
        peer_addr = writer.get_extra_info('peername')
        print(f"New connection from peer: {peer_addr}")
        self.peers.append((reader, writer))
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                message = data.decode().strip()
                print(f"Received from {peer_addr}: {message}")
                response = f"Acknowledged your message: {message}"  # Acknowledgment message
                await self.route_message(response, writer)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            print(f"Closing connection with peer: {peer_addr}")
            self.peers.remove((reader, writer))
            writer.close()
            await writer.wait_closed()

    async def route_message(self, message, sender_writer):
        for reader, writer in self.peers:
            if writer != sender_writer:
                await self.send_message(writer, message)

    async def send_message(self, writer, message):
        try:
            writer.write(message.encode())
            await writer.drain()
        except Exception as e:
            print(f"Error sending message to peer: {e}")

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.ip, self.port)
        print(f"Server started on {self.ip}:{self.port}")
        async with server:
            await server.serve_forever()

async def main():
    server = P2PServer('127.0.0.1', 12000)
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())
