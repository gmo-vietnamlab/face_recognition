from __future__ import division
import cv2
import numpy as np
import uuid
import insightface
import face_recognition


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.


from numpy.linalg import norm


def cosine_distance(emb1, emb2):
    sim = np.dot(emb1, emb2)/(norm(emb1)*norm(emb2))
    return 1-sim


# Get a reference to webcam #0 (the default one)
def save_result(face_locations, face_names, frame, scale):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= round(1/scale)
        right *= round(1/scale)
        bottom *= round(1/scale)
        left *= round(1/scale)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # save the resulting image
        print('save image')
        cv2.imwrite('check_in_thcs_quangtrung/output_images/{}_{}.png'.format(name, str(uuid.uuid4())), frame)


def run_image(scale=1):
    fa = insightface.app.FaceAnalysis()
    fa.prepare(ctx_id=-1)
    knn_model = load('check_in_face_rec/saved_model/knn_thcs_quangtrung.joblib')

    # hanle a single image
    image_path = '/Users/phamvanhau/source_project/python/check_in_face_rec/known_capture_dataset/bang/IMG_0519.JPG'
    face_image = cv2.imread(image_path)
    print(face_image.shape)
    face = fa.get(face_image)
    face_locations = face_recognition.face_locations(face_image, model="hog")[0]
    face_encoding = face[0].normed_embedding

    face_name = knn_model.predict([face_encoding])

    print(face_name, face_locations)

    save_result([face_locations], face_name, face_image, scale=scale)


if __name__ == "__main__":
    run_image()