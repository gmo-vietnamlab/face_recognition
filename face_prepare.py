import face_recognition
import glob
import os


class FacePrepare(object):

    @staticmethod
    def get_images(directory):
        image_files = []
        for file in glob.glob(os.path.join(directory, "*")):
            image_files.append(file)
        return image_files

    def get_info(self, directory):
        image_files = self.get_images(directory)
        images = []
        encodings = []
        labels = []
        for index, image_file in enumerate(image_files):
            image = face_recognition.load_image_file(image_file)
            images.append(image)
            encoding = face_recognition.face_encodings(image)[0]
            encodings.append(encoding)
            file_name = os.path.basename(image_file)
            label = os.path.splitext(file_name)[0]
            labels.append(label)
        return images, encodings, labels

