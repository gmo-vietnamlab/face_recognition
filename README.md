# Download src code:

```git checkout test_api```

```git clone```

```cd /face_recognition```

# Docker build:

Docker build images:

```docker build -t face_recognition .```
  
Docker run container

```docker run -p 8000 face_recognition```

# Add images for new employee

```cd /face_recognition```

Create new employee folder and add to

```data/emplyee_data/new_employee```

# Change port and host in Dockerfile if set machine to server:
edit train_and_get_api.py file and Dockerfile. Exp:

```os.system(command='/root/miniconda3/envs/face/bin/uvicorn get_api:app --host 192.168.1.123 --port 12345 --reload')```

```EXPOSE 12345```

```docker run -p 8000 face_recognition ```


