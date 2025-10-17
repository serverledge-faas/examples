#FROM grussorusso/serverledge-python310 
FROM python:3.13.8-bookworm
RUN pip3 install pillow numpy minio
#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

ENV MINIO_ENDPOINT="172.17.0.1:9000"
ENV MINIO_ACCESS_KEY=minio
ENV MINIO_SECRET_KEY=minio123
ENV MINIO_BUCKET=serverledge
ENV MINIO_SECURE=false

COPY executor.py /
COPY function.py /
COPY minioclient.py /

WORKDIR /
CMD python executor.py
