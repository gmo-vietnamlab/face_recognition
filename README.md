Running 

```cd /PATH/TO/face_recognition```

Add path 
```export PYTHONPATH="${PYTHONPATH}:`pwd````

Start virtualenv
```source face_rec_venv/bin/activate```

Run checkin
```python checkin.py```

Note: check file job/run_checkin.sh for more detail

Prepare encoding file
```python save_face_encoding.py```

Docker build images:

  ```docker images -t face_recognition .```

#change port and host in Dockerfile if set machine to server 
#Exp: ```CMD ["/root/miniconda3/envs/face/bin/uvicorn", "get_api:app", "--reload", "--host", "192.168.1.123", "--port", "12345"]```
      ```EXPOSE 12345```

Docker run container

```docker run -p 8000 face-recognition```
