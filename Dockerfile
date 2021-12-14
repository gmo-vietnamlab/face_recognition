FROM ubuntu:20.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget gcc g++ cmake  && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y cron

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

COPY . /usr/src/app

RUN conda create -n face python=3.7

RUN apt-get update

RUN apt-get install cron

RUN activate face

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN /root/miniconda3/envs/face/bin/pip install install --upgrade pip setuptools wheel

RUN /root/miniconda3/envs/face/bin/pip install numpy==1.21.2

RUN /root/miniconda3/envs/face/bin/pip install Cython==0.29.24

RUN /root/miniconda3/envs/face/bin/pip install opencv-python==4.4.0.42

RUN /root/miniconda3/envs/face/bin/pip install faiss-cpu==1.7.1.post2

RUN /root/miniconda3/envs/face/bin/pip install fastapi==0.70.0

RUN /root/miniconda3/envs/face/bin/pip install --no-cache-dir -r requirements.txt

CMD /root/miniconda3/envs/face/bin/python train_and_get_api.py

EXPOSE 8000
