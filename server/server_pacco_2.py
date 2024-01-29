from daily import Daily, CallClient
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env file
# Accessing the ROOM_ID
room_id = os.getenv('ROOM_ID', 'O8EvAKGhOPHpYuqfBHog')  # 'default_value' is a fallback if ROOM_ID is not set


Daily.init()
client = CallClient()

client.join(f"https://makemelaugh.daily.co/{room_id}")
# client.set_video_renderer(PARTICIPANT_ID, on_video_frame)