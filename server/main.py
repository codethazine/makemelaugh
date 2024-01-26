# TODO: Add server elaborating happiness frames and returning score 0-1 to clients
# client send a frame to server
# server return an happiness score to client
# client send a frame every second
# repeat until client close connection

import socket
import sys
import cv2
import pickle
import numpy as np
import threading
import time  # Added for timeout functionality

def calculate_happiness_score(frame):
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
        # draw rectangle around face
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

# use a neural network to detect happiness and get a score from 0 to 1
def calculate_happiness_score2(frame):
    # detect face, use neural network to detect happiness
    face_cascadeClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = face_cascadeClassifier.detectMultiScale(gray, 1.3, 5)

    # for each face, detect smile
    for (x, y, w, h) in faces:
        # draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # detect smile
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # TODO: use neural network to detect happiness

        # if smile detected, return 1.0
        if len(smiles) > 0:
            return 1.0
    

def handle_client(connection):
    try:
        # Set a timeout for the connection (1 second in this case)
        connection.settimeout(1.0)

        while True:
            # Receive frame from client
            frame_data = b''
            while True:
                packet = connection.recv(4096)
                if not packet:
                    break
                frame_data += packet

            if not frame_data:
                break  # No more data, exit loop

            # Deserialize frame data
            frame = pickle.loads(frame_data)

            # Calculate happiness score for the frame
            happiness_score = calculate_happiness_score(frame)

            # Send happiness score back to client
            connection.sendall(str(happiness_score).encode())

    except socket.timeout:
        print("Connection timed out")
        connection.close()

    except Exception as e:
        print("Error:", e)

    finally:
        # Clean up the connection
        connection.close()


def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5) # 5 is the maximum number of queued connections

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        print('connection from', client_address)

        # Start a new thread to handle the connection
        client_handler = threading.Thread(target=handle_client, args=(connection,))
        client_handler.start()

if __name__ == "__main__":
    main()