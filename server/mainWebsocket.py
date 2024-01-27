# Server elaborating frames  received from websocket and returning a score from 0 to 1 to clients
# client send a frame to server
# server return an happiness score to client
# client send a frame every second
# repeat until client close connection

import cv2
import numpy as np
import websockets
import asyncio
from fer import FER

# Emotion detector from fer
emotion_detector = FER() 
 

def calculate_happiness_score_cascade(frame):
    # TODO: Calculate happiness score for frame
    # use cv2 to detect face and smile, using haar cascade

    # 0.0: sad
    # 1.0: happy

    # pretrained models need to be already on the server
    face_cascadeClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    smile_cascadeClassifier = cv2.CascadeClassifier('haarcascade_smile.xml')

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = face_cascadeClassifier.detectMultiScale(gray, 1.3, 5)

    # for each face, detect smile
    for (x, y, w, h) in faces:
        # draw region of interest around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # detect smile
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        smiles = smile_cascadeClassifier.detectMultiScale(roi_gray, 1.8, 20)

        # if smile detected, return 1.0
        if len(smiles) > 0:
            return 1.0
    
    # if no smile detected, return 0.0
    return 0.0



def calculate_happiness_score_fer(frame):
    # Calculate happiness score for frame using neural network
    # use cv2 to detect face, using haar cascade

    # 0.0: sad
    # 0.5: neutral
    # 1.0: happy

    # pretrained models need to be already on the server
    face_cascadeClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = face_cascadeClassifier.detectMultiScale(gray, 1.3, 5)

    max_happiness_score = 0.0

    # iterate over faces, resize and preprocess them, then predict happiness score
    for (x, y, w, h) in faces:
        # use only the face region of interest
        roi_gray = gray[y:y+h, x:x+w]
        result = emotion_detector.detect_emotions(roi_gray)
        emotions = result[0]["emotions"]
        happiness_score = emotions["happy"]
        if happiness_score > max_happiness_score:
            max_happiness_score = happiness_score

    return max_happiness_score

async def handle_client(websocket, path):
    print("New client connected")
    try:
        while True:
            # receive frame from client
            frame = await websocket.recv()
            print("Frame received")

            # convert frame from string to numpy array
            frame = np.frombuffer(frame, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # calculate happiness score
            # happiness_score = calculate_happiness_score_cascade(frame)
            happiness_score = calculate_happiness_score_fer(frame)
            print("Happiness score: ", happiness_score)

            # send happiness score to client
            await websocket.send(str(happiness_score))
            print("Happiness score sent")
    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected")


async def main():
    print("Starting server")
    # WebSocket server
    server = await websockets.serve(handle_client, "127.0.0.1", 8765)
    print("Server started")

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())