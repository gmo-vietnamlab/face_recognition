from model.face_rec_arcface import FaceRecognizer, FaceRecognizeDemo
from save_face_encoding import save_encoding_main
from flask import Flask, render_template, Response, jsonify, request
import time
import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import cv2

app = Flask(__name__)

ENABLE_CHECK_IN = False
CHECK_IN_FILE = ''
CHECK_IN_DATA = None

recognizer = FaceRecognizer()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enable_check_in', methods=['POST'])
def ENABLE_CHECK_IN():
    try:
        global ENABLE_CHECK_IN, CHECK_IN_FILE, CHECK_IN_DATA

        # enable check in
        ENABLE_CHECK_IN = True

        # create empty file
        CHECK_IN_FILE = 'checkin_result/file_diem_danh_{}.csv'.format(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        Path(CHECK_IN_FILE).touch()

        # create empty pandas dataframe
        CHECK_IN_DATA = pd.DataFrame({}, columns=['Ten_hoc_sinh', 'Thoi_gian_diem_danh'])
        return '', 204
    except:
        return 'Error!', 500


@app.route('/disable_check_in', methods=['POST'])
def disable_check_in():
    try:
        print('here 1')
        global ENABLE_CHECK_IN, CHECK_IN_DATA, CHECK_IN_FILE
        ENABLE_CHECK_IN = False
        print('here 2', CHECK_IN_DATA, CHECK_IN_FILE)
        CHECK_IN_DATA.to_csv(CHECK_IN_FILE)
        return '', 204
    except Exception as e:
        print(e)
        return 'Error!', 500


@app.route('/predict_frame', methods=['GET'])
def predict_frame():
    try:
        nparr = np.fromstring(request.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print('decoded shape: ', img.shape)
        predicted_name = recognizer.recognize_image(img)
        print('predicted name ', predicted_name)
        do_check_in(predicted_name, datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        return jsonify({'name': predicted_name})
    except:
        return 'Error!', 500


def do_check_in(name, check_in_time):
    try:
        global ENABLE_CHECK_IN, CHECK_IN_DATA
        if ENABLE_CHECK_IN and name != 'Unknown' and name not in CHECK_IN_DATA[
            'Ten_hoc_sinh'].values:
            CHECK_IN_DATA.loc[len(CHECK_IN_DATA)] = [name, check_in_time]
            print(CHECK_IN_DATA)
        return '', 204
    except:
        return 'Error!', 500


@app.route('/diem_danh')
def diem_danh():
    return render_template('checkin.html')


@app.route('/add_new_person')
def add_new_person():
    try:
        return render_template('add_data.html')
    except:
        return 'Error!', 500


@app.route('/add_new_person_encodings', methods=['POST'])
def add_new_person_encodings():
    try:
        save_encoding_main(overwrite=False)
        recognizer.set_faiss_index()
        return '', 204
    except:
        return 'Error!', 500


@app.route('/checkin_result')
def checkin_result():
    return render_template('checkin_result.html')


@app.route('/demo')
def demo():
    return render_template('demo.html')


def gen_demo(camera):
    while True:
        time.sleep(0.02)
        frame = camera.get_frame_without_predict()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_demo')
def video_demo():
    try:
        v_demo = FaceRecognizeDemo(source="video_data/test/demo_20200913_163633.avi")
        return Response(gen_demo(v_demo),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        return 'Error!', 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port="5000")
