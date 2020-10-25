from keras.preprocessing import image
import os
import uuid
import cv2
import argparse

"""
example usage:   
    python3 data_augmentation.py -d test_augmentation -t 2
"""


def face_augment(data_dir, time=5):
    """
    :param data_dir: the origin folder contain all dataset in which each subfolder save all images of same person/
    :param time: how many images will be generate for each origin image.
    :return: new images will be stored in the same folder as origin image.
    """

    datagen = image.ImageDataGenerator(
        rotation_range=30,  # (degree) randomly rotate image
        width_shift_range=0.05,  # (fraction of total width) randomly translate image horizontally
        height_shift_range=0.05,  # same above
        shear_range=0.05,  # shearing
        zoom_range=0.05,  # zo  oming inside image
        horizontal_flip=True,  # flip image horizontally
        brightness_range=[0.6, 1.4],
        fill_mode='nearest'  # filling in newly created pixels
    )

    for folder_name in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue
        file_names = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]
        for img_path in file_names:
            print(img_path)
            img = image.load_img(img_path, target_size=(128, 128))
            x = image.img_to_array(img)
            x = x.reshape((1,) + x.shape)
            i = 0
            for batch in datagen.flow(x, batch_size=1):
                f = str(uuid.uuid4())
                cv2.imwrite(folder_path + '/' + f + ".jpg", batch[0][:, :, ::-1])
                i += 1
                if i == time:
                    break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_dir', help='data directory', required=True)
    parser.add_argument('-t', '--time', help='how many image to be generated', required=False)
    args = parser.parse_args()
    face_augment(args.data_dir, int(args.time))
