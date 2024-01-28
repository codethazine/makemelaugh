import asyncio
import websockets
import json
import random
from daily import Daily, CallClient

Daily.init()
client = CallClient()

async def send_random_data(websocket, path):
    while True:
        data = {"id1": round(random.random(), 3), "id2": round(random.random(), 3)}
        await websocket.send(json.dumps(data))
        await asyncio.sleep(1)  # Send data every second

start_server = websockets.serve(send_random_data, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
