import face_recognition
import numpy as np
import cv2, queue, threading, time
import requests, os, re
import sys


# bufferless VideoCapture
class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


def validateFace(face_locations):
    closer_validation_value = 230
    face_closer_track = False
    if (len(face_locations) == 1):
        #  print(face_locations[0])
        x, y, w, h = face_locations[0]
        cam_width = w - x
        if (cam_width >= closer_validation_value):
            face_closer_track = True
    return face_closer_track


# Select the webcam of the computer
# video_capture = VideoCapture('https://stream-eu1-charlie.dropcam.com:443/nexus_aac/b85a6ec812c045cd921f4164e8e7ecc0/playlist.m3u8?public=GqJifk6U25')
video_capture = VideoCapture("/dev/video2")

# video_capture.set(5,1)

# * -------------------- USERS -------------------- *
known_face_encodings = []
known_face_names = []
known_faces_filenames = []

for (dirpath, dirnames, filenames) in os.walk('assets/img/users/'):
    known_faces_filenames.extend(filenames)
    break

for filename in known_faces_filenames:
    face = face_recognition.load_image_file('assets/img/users/' + filename)
    known_face_names.append(filename[:-4])
    known_face_encodings.append(face_recognition.face_encodings(face)[0])
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
key = cv2.waitKey(1)
closer_validation_value = 230
status_update = False
while True:
    # for i in range(5):
    #     video_capture.grab()
    # Grab a single frame of video
    frame = video_capture.read()
    windowWidth = frame.shape[1]
    windowHeight = frame.shape[0]

    # # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # print(sys.exc_info())
    # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    # frame = small_frame[:, :, ::-1]

    # Process every frame only one time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        ##### For Closer Attendance to validate if person is closer to camera
        face_closer_track = validateFace(face_locations)

        # Initialize an array for the name of the detected users
        face_names = []

        # * ---------- Initialyse JSON to EXPORT --------- *
        json_to_export = {}

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings,
                                                     face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:

                name = known_face_names[best_match_index]
                if status_update:
                    # * ---------- SAVE data to send to the API -------- *

                    json_to_export['name'] = name

                    json_to_export['date'] = f"{time.strftime('%Y-%m-%d')}"
                    json_to_export[
                        'date_time'] = f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
                    #json_to_export['picture_array'] = frame.tolist()

                    # * ---------- SEND data to API --------- *
                    r = requests.post(url='http://127.0.0.1:5000/receive_data',
                                      json=json_to_export)
                    print("Status: ", r.status_code)
                    status_update = False
                    time.sleep(5)

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        # top *= 4
        # right *= 4
        # bottom *= 4
        # left *= 4

        # Draw a box around the face
        if (face_closer_track):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 120, 11), 4)
        else:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0,
        #            (255, 255, 255), 1)
        #cv2.putText(frame, name, (left, bottom), font, 1.0, (255, 255, 255), 1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(frame, (0, windowHeight - 30),
                      (windowWidth, windowHeight), (4, 44, 80, 255), -2)
        cv2.putText(frame, name, (5, windowHeight - 10), font, 1,
                    (0, 255, 255), 2, cv2.LINE_4)

    # Display the resulting image
    cv2.imshow('Video', frame)
    if face_closer_track:
        status_update = True

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
