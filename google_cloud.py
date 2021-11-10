import os
from re import split
from google.cloud import storage
from google.cloud.client import Client
from google.cloud.storage import blob, bucket
from save_face_encoding import save_encoding_main
from crontab import CronTab
import datetime


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/thanh/.config/gcloud/authen.json'
storage_client = storage.Client()
vars(bucket)

#rsync data multiprocessing
#gsutil -m rsync -d -r (local address) gs://mybucket/data

#Access to a bucket
my_bucket = storage_client.get_bucket('rem_recommend_dev')



gcs_image_path = 'micro-erp-data/employee_data'
employees = my_bucket.list_blobs(prefix=gcs_image_path)
employees_set = set()

for blob in employees:
    employee_fullname = os.path.dirname(blob.name)
    employee_fullname = employee_fullname.split(gcs_image_path +'/')[1]
    employees_set.add(employee_fullname)
print(employees_set)

local_path = 'data/employee_data2'
for employee in employees_set:
    employee_local_path = os.path.join(local_path, employee)
    if not os.path.exists(employee_local_path):
        x = os.mkdir(employee_local_path)

print(x)

storage_client = storage.Client()
blobs = employee_local_path.list_blobs()  # Get list of files
for blob in blobs:
    filename = blob.name.replace('/', '_') 
    blob.download_to_filename(employee_local_path)

save_encoding_main(overwrite=True)

