import asyncio
import websockets
import json
import random
from daily import Daily, CallClient

Daily.init()
client = CallClient()
min_value = 0.1
max_value = 10
room_id = "249k9f9jjjf3f3f3f"

async def send_random_data(websocket, path):
    while True:
        data = {0: round(random.uniform(min_value, max_value), 3), 1: round(random.uniform(min_value, max_value), 3),
                "room_id": room_id}
        await websocket.send(json.dumps(data))
        await asyncio.sleep(1)  # Send data every second

start_server = websockets.serve(send_random_data, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
