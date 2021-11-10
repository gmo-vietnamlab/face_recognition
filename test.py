from os import sendfile
from model.face_rec_arcface import FaceRecognizer
import cv2


user_id = "LeBinhThanh"
img = cv2.imread('test_abc.png')

class CheckIn(object):
    def __init__(self, img, face_recognizer):
        self.face_recognizer = face_recognizer
        self.img = img
        self.predicted_name = ['Unknown']
        self.in_predict = True
        self.checked_name = []

    def predict_name(self, user_id):
        if self.img is None:
            return
        found_front_face, self.predicted_name[0] = self.face_recognizer.recognize_image(self.img)
        if found_front_face:
            self.predicted_name[0] == user_id
            return True
        else: 
            return False

if __name__ == "__main__":
    value = CheckIn(img,face_recognizer=FaceRecognizer()).predict_name(user_id)
    checkIn = CheckIn(face_recognizer=FaceRecognizer(img))
    checkIn.predicted_name()
