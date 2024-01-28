import cv2
import numpy as np
import asyncio
import websockets
import json
from fer import FER

from daily import daily
from time import sleep

# Emotion detector from fer
emotion_detector = FER(mtcnn=True)
 


def calculate_happiness_score_fer(frame):
    # Calculate happiness score for frame using neural network
    # use cv2 to detect face, using haar cascade

    # 0.0: sad
    # 0.5: neutral
    # 1.0: happy

    # pretrained models need to be already on the server
    face_cascadeClassifier = cv2.CascadeClassifier('pretrainedModels/haarcascade_face.xml')

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = face_cascadeClassifier.detectMultiScale(gray, 1.3, 5)

    max_happiness_score = 0.0

    # iterate over faces, resize and preprocess them, then predict happiness score
    for (x, y, w, h) in faces:
        # use only the face region of interest
        roi_gray = gray[y:y+h, x:x+w]
        roi = frame[y:y+h, x:x+w]
        result = emotion_detector.detect_emotions(roi)
        if(len(result) == 0):
            continue
        print("RESULT:")
        print(result)
        emotions = result[0]["emotions"]
        happiness_score = emotions["happy"]
        if happiness_score > max_happiness_score:
            max_happiness_score = happiness_score

    return max_happiness_score


# global variables
iterations_participant1 = 0
iterations_participant2 = 0

# initialize the dailyco client
daily.Daily.init()

# create the client
client = daily.CallClient()

# join the dailyco meeting 
client.join("https://makemelaugh.daily.co/O8EvAKGhOPHpYuqfBHog")
print("Joined meeting")


# get the participant id of the current users
participants = client.participants()
dict_keys = participants.keys()
# remove "local" from the list
dict_keys = list(dict_keys)
dict_keys.remove("local")

if(len(dict_keys) > 4 or len(dict_keys) < 2):
    print("ERROR: There should be 2 (or more?) participants in the call")
    exit(1)
# get the first participant id
PARTICIPANT_ID1 = dict_keys[0]
# get the second participant id
PARTICIPANT_ID2 = dict_keys[1]

print(f"Participant id 1: {PARTICIPANT_ID1}")
print(f"Participant id 2: {PARTICIPANT_ID2}")

# set global variable for current happiness scores for each participant
global happiness_score_participant1
global happiness_score_participant2

# async calls
# called after every frame is received
def on_video_frame(participant_id, video_frame):
    #print(f"NEW FRAME FROM {participant_id}")
    # print(f"NEW FRAME FROM {participant_id}")
    if participant_id == PARTICIPANT_ID1:
        global iterations_participant1
        if iterations_participant1 % 30 == 0:
            print(f"NEW FRAME FROM {participant_id}")
            # convert the video frame to a numpy array
            npframebuffer = video_frame.buffer
            frame_width = video_frame.width
            frame_height = video_frame.height
            frame_colorFormat = video_frame.color_format
            frame = np.frombuffer(npframebuffer, dtype=np.uint8).reshape(frame_height, frame_width, 4) # RGBA
            # convert the frame from RGBA to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

            # show the frame in a window for 1 second
            
            

            # # calculate happiness score for participant 1
            global happiness_score_participant1
            happiness_score_participant1 = calculate_happiness_score_fer(frame)
            print(f"Happiness score: {happiness_score_participant1}")

        iterations_participant1 += 1
    elif participant_id == PARTICIPANT_ID2:
        global iterations_participant2
        if iterations_participant2 % 30 == 0:
            print(f"NEW FRAME FROM {participant_id}")
            # convert the video frame to a numpy array
            npframebuffer = video_frame.buffer
            frame_width = video_frame.width
            frame_height = video_frame.height
            frame_colorFormat = video_frame.color_format
            frame = np.frombuffer(npframebuffer, dtype=np.uint8).reshape(frame_height, frame_width, 4) # RGBA

            # convert the frame from RGBA to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)


            # # calculate happiness score
            global happiness_score_participant2
            happiness_score_participant2 = calculate_happiness_score_fer(frame)
            print(f"Happiness score: {happiness_score_participant2}")

        iterations_participant2 += 1


client.set_video_renderer(PARTICIPANT_ID1, on_video_frame)
client.set_video_renderer(PARTICIPANT_ID2, on_video_frame)

timeSeconds = 0

# start_server = websockets.serve(send_happiness_score, "localhost", 6789)
async def send_happiness_scores(websocket, path):
    while True:
        data = {0: happiness_score_participant1*10, 1: happiness_score_participant2*10}
        await websocket.send(json.dumps(data))
        await asyncio.sleep(1)  # Send data every second


start_server = websockets.serve(send_happiness_scores, "localhost", 6789)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# while True:
#     sleep(1)

    # after 10 seconds, leave the call and rejoin it
    # timeSeconds += 1
    # if timeSeconds == 10:
    #     print("Leaving call")
    #     client.leave()
    #     print("Rejoining call")
    #     client.join("https://makemelaugh.daily.co/O8EvAKGhOPHpYuqfBHog")
    #     print("reJoined meeting")
    #     # set the video renderer for the new participants
    #     client.set_video_renderer(PARTICIPANT_ID1, on_video_frame)
    #     client.set_video_renderer(PARTICIPANT_ID2, on_video_frame)
    #     timeSeconds = 0


# close the client
client.leave()