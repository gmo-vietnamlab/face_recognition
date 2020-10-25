from __future__ import division
from datetime import datetime
import cv2
import numpy as np
import pandas as pd
import insightface
import face_recognition
import faiss
import pickle


def init_faiss_index(model='face_recognition', dim=128):
    with open('encodings/thcs_quangtrung_encodings.dat', 'rb') as f:
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


class FaceRecognizeDemo(object):
    def __init__(self, source):
        self.image = None
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_FPS, 14)

    def get_frame_without_predict(self):
        try:
            ret, self.image = self.cap.read()
            ret, jpeg = cv2.imencode('.jpg', self.image)
            return jpeg.tobytes()
        except Exception:
            return


class Recognize(object):
    def __init__(self):
        self.image = None
        self.fa = insightface.app.FaceAnalysis()
        self.fa.prepare(ctx_id=-1)
        self.set_faiss_index()

    def set_faiss_index(self):
        self.name_list, self.faiss_index = init_faiss_index('arcface', 512)

    def recognize_image(self, image):
        rgb_frame = image[:, :, ::-1]
        f_locations = face_recognition.face_locations(rgb_frame, model="hog")
        name = 'Unknown'
        print('in predict')

        if len(f_locations) > 0:
            print('found face')
            face = self.fa.get(image)
            face_encoding = face[0].normed_embedding

            similarity, id = self.faiss_index.search(np.ascontiguousarray([face_encoding]), 1)
            if 1 - similarity < 0.6:
                # only accept distance < 0.6
                name = self.name_list[id[0][0]]

        return name