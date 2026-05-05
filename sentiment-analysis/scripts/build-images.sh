#!/bin/bash

cd ../src
docker build --build-arg HANDLER_ENV="retrieve" -t matnar/sa-retrieve .      
docker build --build-arg HANDLER_ENV="extract" -t matnar/sa-extract .      
docker build --build-arg HANDLER_ENV="train" -t matnar/sa-train .      
docker build --build-arg HANDLER_ENV="evaluate" -t matnar/sa-evaluate .      
