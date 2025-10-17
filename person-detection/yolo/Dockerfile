#FROM grussorusso/serverledge-python310 
FROM python:3.13.8-bookworm
RUN pip3 install ultralytics pillow numpy
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY yolov8n.pt /
COPY executor.py /
COPY function.py /

WORKDIR /
CMD python executor.py
