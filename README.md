Running 

```cd check_in_face_rec```

Go to parent folder
```cd ..```

Get link of parent folder
```readlink -f``` 

Post above link in below 
```export PYTHONPATH="${PYTHONPATH}:{folder_here}```

Register user for training:
```/usr/bin/python3.6 -m ./check_in_face_rec/register_webcam_images```

Run webcam
```/usr/bin/python3.6 -m ./check_in_face_rec/face_rec_from_webcam```
