#!/usr/bin/env bash

SERVERLEDGE_CLI="${1:-../../../serverledge/bin/serverledge-cli}"

"$SERVERLEDGE_CLI" create --update --function sa_retrieve \
    --memory 256 \
    --runtime custom \
    --custom_image matnar/sa-retrieve \
    --input "minio_endpoint:Text" \
    --input "minio_access_key:Text" \
    --input "minio_secret_key:Text" \
    --input "data_url:Text" \
    --input "local_dir:Text" \
    --input "object_name:Text" \
    --output "status:Text" \
    --output "local_download:Bool" \
    --output "uploaded:Bool" \
    --output "object_name:Text"


"$SERVERLEDGE_CLI" create --update --function sa_extract \
    --memory 256 \
    --runtime custom \
    --custom_image matnar/sa-extract \
    --input "minio_endpoint:Text" \
    --input "minio_access_key:Text" \
    --input "minio_secret_key:Text" \
    --input "tgz_input_object_name:Text" \
    --input "subset:Float" \
    --input "local_dataset_file:Text" \
    --input "local_output_dir:Text" \
    --input "output_train_object_name:Text" \
    --input "output_test_object_name:Text" \
    --output "status:Text" \
    --output "train_object_name:Text" \
    --output "test_object_name:Text"



"$SERVERLEDGE_CLI" create --update --function sa_train \
    --memory 1024 \
    --runtime custom \
    --custom_image matnar/sa-train \
    --input "minio_endpoint:Text" \
    --input "minio_access_key:Text" \
    --input "minio_secret_key:Text" \
    --input "subset:Float" \
    --input "max_features:Int" \
    --input "train_object_data:Text" \
    --input "local_train_file:Text" \
    --input "local_model_file:Text" \
    --input "local_vectorizer_file:Text" \
    --input "output_model_object:Text" \
    --input "output_vectorizer_object:Text" \
    --input "reuse_trained_model:Bool"
    --output "status:Text" \
    --output "model_object_name:Text" \
    --output "vectorizer_object_name:Text" \



"$SERVERLEDGE_CLI" create --update --function sa_evaluate \
    --memory 512 \
    --runtime custom \
    --custom_image matnar/sa-evaluate \
    --input "minio_endpoint:Text" \
    --input "minio_access_key:Text" \
    --input "minio_secret_key:Text" \
    --input "test_object_data:Text" \
    --input "local_test_file:Text" \
    --input "subset:Float" \
    --input "local_model_file:Text" \
    --input "local_vectorizer_file:Text" \
    --input "input_model_object:Text" \
    --input "input_vectorizer_object:Text" \
    --output "status:Text" \
    --output "accuracy:Float"

## TODO: How to support environment variables? 
