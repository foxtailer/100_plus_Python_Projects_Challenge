import asyncio
import websockets
import json

async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)

        text = data["text"]

        # modify message
        response = {
            "text": f'Echo from server: "{text}"'
        }

        await websocket.send(json.dumps(response))


async def main():
    async with websockets.serve(handler, "localhost", 3000):
        print("Server running on ws://localhost:3000")
        await asyncio.Future()  # run forever


asyncio.run(main())
