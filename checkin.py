from __future__ import division
from checkin_api.checkin_api import CheckinAPI
from model.face_rec_arcface import FaceRecognizer
from datetime import datetime
from dateutil import tz
import cv2
import time
import sys
import os
import uuid


class CheckIn(object):
    def __init__(self, input_source, face_recognizer):
        self.checkin_api = CheckinAPI()
        self.face_recognizer = face_recognizer
        self.image = None
        self.predict_name = ['Unknown']
        self.cap = cv2.VideoCapture(input_source)
        self.cap.set(cv2.CAP_PROP_FPS, 10)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        self.in_predict = True
        self.time_zone = tz.tzlocal()
        self.checked = []
        self.today_dir = 'checkin_result/{}'.format(datetime.now().strftime('%Y%m%d'))

    def run_camera(self):
        try:
            ret, self.image = self.cap.read()
            self.predict_name()
            # copy image then add text to that copy
            image = self.image.copy()
            cv2.rectangle(image, (0, 0), (260, 50), (255, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_TRIPLEX
            cv2.putText(image, self.predict_name[0], (10, 30), font, 1.3, (0, 128, 0), 1)

            # Display the resulting image
            # cv2.imshow('Video', image)

        except Exception as e:
            print('Got exception when capture video!¥n', e)
            pass

    def predict_name(self):
        print('run predict')
        # continue
        # time.sleep(1)
        if self.image is None:
            return
        found_front_face, self.predict_name[0] = self.face_recognizer.recognize_image(self.image)
        if found_front_face:
            self.do_check_in(self.predict_name[0])

    def do_check_in(self, name):
        if name != 'Unknown' and name not in self.checked:
            self.checked.append(name)
            cv2.imwrite('{}/known/{}.jpg'.format(self.today_dir, uuid.uuid4()))
            now = datetime.now(self.time_zone)
            checkin_time = now.isoformat(timespec='seconds')
            self.checkin_api.call_api(name, checkin_time)
        else:
            # save unknown person image for analysis
            cv2.imwrite('{}/unknown/{}.jpg'.format(self.today_dir, uuid.uuid4()))


if __name__ == "__main__":
    checkIn = CheckIn(input_source=-1, face_recognizer=FaceRecognizer())

    # make check in result dir:
    if not os.path.isdir(checkIn.today_dir):
        os.mkdir(checkIn.today_dir)
        os.mkdir(checkIn.today_dir + '/known')
        os.mkdir(checkIn.today_dir + '/unknown')

    start = time.time()
    while checkIn.cap.isOpened():
        if time.time() - start > 30:
            sys.exit()
        checkIn.run_camera()
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    checkIn.cap.release()
    cv2.destroyAllWindows()
