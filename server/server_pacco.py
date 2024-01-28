import asyncio
import websockets
import json

async def time(websocket, path):
    while True:
        data = {"id1": 0.1, "id2": 0.3}
        await websocket.send(json.dumps(data))
        await asyncio.sleep(1)  # Send data every second

start_server = websockets.serve(time, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
