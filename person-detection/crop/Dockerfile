#FROM grussorusso/serverledge-python310 
FROM python:3.13.8-bookworm
RUN pip3 install pillow numpy minio
#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY executor.py /
COPY function.py /

WORKDIR /
CMD python executor.py
