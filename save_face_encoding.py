import os
import glob
import face_recognition
import numpy as np
import pickle
import cv2
import insightface
from face_save import FaceSave
import shutil
import argparse


def crop_face(image, crop_locations):
    scale = 0.075
    height = crop_locations[2] - crop_locations[0]
    width = crop_locations[1] - crop_locations[3]

    top = crop_locations[0] - (height * scale)
    right = crop_locations[1] + (width * scale)
    bottom = crop_locations[2] + (height * scale)
    left = crop_locations[3] - (width * scale)

    fixed_cropped_location = np.round([top, right, bottom, left]).astype(int)
    # fixed_cropped_location = crop_locations
    cropped_image = image[fixed_cropped_location[0]:fixed_cropped_location[2],
                    fixed_cropped_location[3]:fixed_cropped_location[1], :].copy()
    cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    return cropped_image


def augment_images(capture_directory, output_directory):
    train_face_save = FaceSave(output_directory)
    all_people = os.listdir(capture_directory)
    print(all_people)
    for person in all_people:
        list_capture_images = glob.glob(os.path.join(capture_directory, person) + '/*.png')
        list_capture_images.extend(glob.glob(os.path.join(capture_directory, person) + '/*.JPG'))

        for capture_image in list_capture_images:
            image = face_recognition.load_image_file(capture_image)
            face_locations = face_recognition.face_locations(image, model="hog")
            if len(face_locations) > 0:
                try:
                    # cropped_image = crop_face(image, face_locations[0])
                    # if cropped_image is not None and (cropped_image.size > 0):
                    train_face_save.save_known_image(image, person, 150)
                except Exception:
                    print('failed: ', capture_image)
                    os.remove(capture_image)
            else:
                print('cannot get face model using hog {}'.format(capture_image))
                continue


def arcface_save_encodings(image_dir):
    fa = insightface.app.FaceAnalysis()
    fa.prepare(ctx_id=-1)

    all_encoding = {}
    all_people = os.listdir(image_dir)
    for person in all_people:
        list_encoding = []
        person_imagepaths = glob.glob(os.path.join(image_dir, person) + '/*.jpg')
        person_imagepaths.extend(glob.glob(os.path.join(image_dir, person) + '/*.png'))
        for imagepath in person_imagepaths:
            print('image path: {}'.format(imagepath))
            face_image = cv2.imread(imagepath)
            if len(face_recognition.face_locations(face_image, model="hog")) > 0:
                face = fa.get(face_image)
                print('fa face: ', face)
                try:
                    face_encoding = face[0].normed_embedding
                    print('get encoding {} '.format(face_encoding))
                    # print("Encode for image %s" % imagepath)
                    list_encoding.append({imagepath: face_encoding})
                except:
                    print("Failed to encode image %s" % imagepath)
            else:
                # remove image that dlib cannot detect
                print("remove image that dlib cannot detect %s" % imagepath)
                os.remove(imagepath)
                continue

        all_encoding[str(person)] = list_encoding
    return all_encoding


def save_encoding_main(overwrite=False):
    directory = 'data/employee_data'
    train_directory = 'data/train_images'
    encoding_file_name = 'data/encodings/vnlab_HN_encodings.dat'

    # remove data in train directory
    if os.path.isdir(train_directory):
        shutil.rmtree(train_directory)
    os.mkdir(train_directory)

    # print("Crop faces and augment images")
    augment_images(directory, train_directory)

    # get and save encodings
    encodings = arcface_save_encodings(train_directory)

    if not overwrite:
        with open(encoding_file_name, 'rb') as f:
            old_encodings = pickle.load(f)
        encodings = {**old_encodings, **encodings}

    with open(encoding_file_name, 'wb') as f:
        pickle.dump(encodings, f)

    # remove data in employee_data
    # if os.path.isdir(directory):
        # shutil.rmtree(directory)
    # os.mkdir(directory)


if __name__ == "__main__":
    save_encoding_main(overwrite=True)
