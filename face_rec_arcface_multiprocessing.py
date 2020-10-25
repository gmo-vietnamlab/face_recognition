from __future__ import division
from datetime import datetime
import cv2
import numpy as np
import pandas as pd
import insightface
import face_recognition
import faiss
import pickle
import threading
from multiprocessing import Process, Value
import ctypes
import time
import datetime


def init_faiss_index(model='face_recognition', dim=128):
    with open('encodings/thcs_quangtrung_augment.dat', 'rb') as f:
        all_face_encodings = pickle.load(f)

    pandas_dict = {}

    pandas_dict['label'] = []

    pandas_dict['image'] = []

    pandas_dict['vector'] = []

    for person, encodings in all_face_encodings.items():

        for encoding in encodings:
            pandas_dict['label'].append(person)

            pandas_dict['image'].append(str(list(encoding.keys())[0]))

            pandas_dict['vector'].append(list(encoding.values())[0])
    df_all = pd.DataFrame.from_dict(pandas_dict)

    list_vector = ['vector_' + str(i) for i in range(0, dim)]
    df_all[list_vector] = pd.DataFrame(df_all.vector.values.tolist(), index=df_all.index)

    if model == 'arcface':
        quantizer = faiss.IndexFlatIP(dim)
        index = faiss.IndexIVFFlat(quantizer, dim, 100, faiss.METRIC_INNER_PRODUCT)

        train_vectors = np.ascontiguousarray(df_all[list_vector].astype('float32'))
        faiss.normalize_L2(train_vectors)
    else:
        index = faiss.IndexFlatL2(128)
        train_vectors = np.ascontiguousarray(df_all[list_vector].astype('float32'))

    index.train(train_vectors)
    index.add(train_vectors)

    return df_all['label'], index


PREDICTED_NAME = Value(ctypes.c_int, 0)


class Recognize(object):
    def __init__(self, source):
        self.image = None
        self.fa = insightface.app.FaceAnalysis()
        self.fa.prepare(ctx_id=-1)
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_FPS, 14)
        self.name_list, self.faiss_index = init_faiss_index('arcface', 512)
        cap_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        cap_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # self.writer = cv2.VideoWriter('demo_{}.avi'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")),
        #                               cv2.VideoWriter_fourcc(*'XVID'), 20.0, (cap_width, cap_height))
        self.in_predict = True

    def get_frame_with_predict(self):
        try:
            ret, self.image = self.cap.read()
            print(type(self.image))
            image = self.image.copy()
            cv2.rectangle(image, (0, 0), (260, 50), (255, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_TRIPLEX
            cv2.putText(image, str(PREDICTED_NAME.value), (10, 30), font, 1.3, (0, 128, 0), 1)

            # Display the resulting image
            cv2.imshow('Video', image)

            # Save frame
            # self.writer.write(image)

            # ret, jpeg = cv2.imencode('.jpg', image)
            # return jpeg.tobytes()
        except Exception:
            pass

    def predict_name(self, process_variable):
        print('xxx predict name')
        while self.in_predict:
            print('in predict 1')
            time.sleep(0.6)
            if self.image is None:
                print('none')
                continue
            image = self.image.copy()
            rgb_frame = image[:, :, ::-1]
            f_locations = face_recognition.face_locations(rgb_frame, model="hog")
            name = 'Unknown'
            print('in predict 2')
            if len(f_locations) > 0:
                print('found face')
                face = self.fa.get(image)
                face_encoding = face[0].normed_embedding

                similarity, id = self.faiss_index.search(np.ascontiguousarray([face_encoding]), 1)
                if 1 - similarity < 0.6:
                    # only accept distance < 0.6
                    name = self.name_list[id[0][0]]

            process_variable.value += 1


if __name__ == "__main__":
    rec = Recognize(source="video_data/test/video_thcs_quangtrung.mp4")
    # rec = Recognize(source=0)

    predict_process = Process(target=rec.predict_name, args=(PREDICTED_NAME,))
    predict_process.start()

    while rec.cap.isOpened():
        rec.get_frame_with_predict()
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    rec.cap.release()
    # rec.writer.release()
    cv2.destroyAllWindows()
    predict_process.join()
    del predict_process
