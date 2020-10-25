from __future__ import division
from datetime import datetime
import cv2
import numpy as np
import pandas as pd
import pickle
import threading
import time
import json
import requests
import datetime


class CheckIn(object):
    def __init__(self, source):
        self.image = None
        self.p_name = ['Unknown']
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_FPS, 10)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        self.in_predict = True

    def run_check_in(self):
        try:
            ret, self.image = self.cap.read()

            # copy image then add text to that copy
            image = self.image.copy()
            cv2.rectangle(image, (0, 0), (260, 50), (255, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_TRIPLEX
            cv2.putText(image, self.p_name[0], (10, 30), font, 1.3, (0, 128, 0), 1)

            # Display the resulting image
            cv2.imshow('Video', image)

        except Exception:
            pass

    def predict_name(self):

        while self.in_predict:
            time.sleep(1)
            if self.image is None:
                continue
            print('send request: ', self.image.shape)
            _, img_encoded = cv2.imencode('.jpg', self.image)

            rp = requests.get(url='http://localhost:5000/predict_frame',
                              headers={
                                  'Content-Type': 'image/jpeg',
                                  'User-Agent': 'test'
                              },
                              data=img_encoded.tostring())

            self.p_name[0] = rp.json()['name']


if __name__ == "__main__":
    checkIn = CheckIn(source=0)

    predict_thread = threading.Thread(target=checkIn.predict_name)
    predict_thread.start()

    while checkIn.cap.isOpened():
        checkIn.run_check_in()
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    checkIn.cap.release()
    # rec.writer.release()
    cv2.destroyAllWindows()
    predict_thread.join()
    del predict_thread
