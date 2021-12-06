import base64
from fastapi import FastAPI, Request
from model.face_rec_arcface import FaceRecognizer
import cv2


class CheckIn(object):
    def __init__(self, face_recognizer=FaceRecognizer()):
        self.face_recognizer = face_recognizer
        self.predicted_name = ['Unknown']

    def verify(self, user_id, img):
        if img is None:
            return False
        found_front_face, self.predicted_name[0] = self.face_recognizer.recognize_image(img)
        if found_front_face:
            if self.predicted_name[0] == user_id:
                return True
            else: 
                 return False
        return False


app = FastAPI()
CHECKIN_IMAGE_NAME = 'employee.png'

@app.get('/api/checkin')
async def json(request: Request):
    json_type = await request.json()
    image_encode = json_type['image_encode']
    user_id = json_type['user_id']

    bytes_code = bytes(image_encode, 'utf-8')
    image_decode = base64.decodebytes(bytes_code)
    image = open(CHECKIN_IMAGE_NAME,'wb')
    image.write(image_decode)
    
    checkInModel = CheckIn()
    img = cv2.imread(CHECKIN_IMAGE_NAME)
    verified = checkInModel.verify(user_id, img)
    return {'verified': verified}

