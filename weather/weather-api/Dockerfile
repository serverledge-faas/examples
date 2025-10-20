#FROM grussorusso/serverledge-python310 
FROM python:3.13.8-alpine

RUN pip install openmeteo-requests requests-cache retry-requests numpy pandas

COPY executor.py /
COPY function.py /

WORKDIR /
CMD python executor.py
