#!/bin/bash

cd ../src
docker build --build-arg HANDLER_ENV="retrieve" -t sa-retrieve .      
docker build --build-arg HANDLER_ENV="extract" -t sa-extract .      
docker build --build-arg HANDLER_ENV="train" -t sa-train .      
docker build --build-arg HANDLER_ENV="evaluate" -t sa-evaluate .      
