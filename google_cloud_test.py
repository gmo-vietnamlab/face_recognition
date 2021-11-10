import os
from re import L
from google.cloud import storage
from google.cloud.client import Client
from google.cloud.storage import blob, bucket


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/thanh/.config/gcloud/authen.json'

storage_client = storage.Client()

vars(bucket)

#Access to a bucket
my_bucket = storage_client.get_bucket('rem_recommend_dev')


employee_name = input()
path = '/home/thanh/'
test_path = path + employee_name + '/'
os.mkdir(test_path)


#download files:
prefix = 'rem_recommend_dev/model/'
blobs = my_bucket.list_blobs(prefix=prefix)

storage_client = storage.Client()
blobs = my_bucket.list_blobs()  # Get list of files
for blob in blobs:
    filename = blob.name.replace('/', '_') 
    blob.download_to_filename(test_path + filename)
