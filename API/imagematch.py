import face_recognition
import numpy as np
import cv2, queue, threading, time
import requests, os, re, sys


class validate_profile:
    known_faces_filenames = []
    referenceImage = ""

    def __init__(self, name):
        for (dirpath, dirnames, filenames) in os.walk('assets/img/users/'):
            self.known_faces_filenames.extend(filenames)
        self.referenceImage = name
        print(self.referenceImage)

    def matchImage(self):
        capturedImage = face_recognition.load_image_file(
            f"assets/img/{self.referenceImage}")
        print(capturedImage)
        captured_locations = face_recognition.face_locations(capturedImage)

        capturedImage_encoding = face_recognition.face_encodings(
            capturedImage, captured_locations)[0]
        for match_face in self.known_faces_filenames:
            print(match_face)
            matchImage = face_recognition.load_image_file(
                f"assets/img/users/{match_face}")
            matchImage_locations = face_recognition.face_locations(matchImage)
            matchImage_encoding = face_recognition.face_encodings(
                matchImage, matchImage_locations)[0]

            #matches = face_recognition.compare_faces(capturedImage_encoding,
            #                                         matchImage_encoding)
            matches = face_recognition.compare_faces([capturedImage_encoding],
                                                     matchImage_encoding)
            print(matches)
            face_distances = face_recognition.face_distance(
                [capturedImage_encoding], matchImage_encoding)
            print(face_distances)
            best_match_index = np.argmin(face_distances)
            print(best_match_index)


v_profile = validate_profile("o1.jpg")
v_profile.matchImage()
