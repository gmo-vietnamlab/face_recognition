import os
from google.cloud import storage
from google.cloud.client import Client
from google.cloud.storage import blob, bucket
from save_face_encoding import arcface_save_encodings, augment_images


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/thanh/.config/gcloud/authen.json'
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/usr/src/app/.config/gcloud/authen.json'
storage_client = storage.Client()
vars(bucket)

#Access to a bucket
my_bucket = storage_client.get_bucket('rem_recommend_dev')


#Thay lai dia chi url gsc va url src code
#Tham khao https://cloud.google.com/storage/docs/gsutil/commands/rsync
os.system(command="gsutil -m cp -r gs://rem_recommend_dev/micro-erp-data/employee_data /home/thanh/erp/face_recognition/data")
#os.system(command='gsutil -m cp -r gs://rem_recommend_dev/micro-erp-data/employee_data /usr/src/app/data')


#os.system(command='python save_face_encoding.py')
#os.system(command='/root/miniconda3/envs/face/bin/python save_face_encoding.py')
