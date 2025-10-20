# Sentiment Analysis Workflow

This serverless workflow is inspired by the application presented in the [HEFTless paper](https://doi.org/10.1109/CLUSTER59578.2024.00032).
It uses the [Amazon Review Dataset](https://s3.amazonaws.com/fast-ai-nlp/amazon_review_polarity_csv.tgz) to train and test a sentiment analysis application. 

This is an opinionated implementation of the Sentiment Analysis application, we designed to test Serverledge functionality 
while using realistic workloads. 

## Workflow Description 

> The workflow definition differs from the application design presented in [HEFTless paper](https://doi.org/10.1109/CLUSTER59578.2024.00032)
> since our framework does not currently support fork/join constructs. 

The Sentiment Analysis (SA) workflow combines function tasks and choice tasks. 
SA consists of the following tasks:
* RetrieveState (`sa_retrieve`): Retrieves the dataset;
* ExtractState (`sa_extract`): Preprocess the dataset;
* ChoiceState: Choose whether to train and test either a low or a high accuracy model;
  If the input parameter `max_features` is below 10000, the low-accuracy model will be used in the remainder of the workflow;
* LATrainState (`sa_train`): The training task of the low-accuracy sentiment analysis model;
* LAEvaluateFinalState (`sa_evaluate`): The final task of the low-accuracy sentiment analysis model;
* HATrainState (`sa_train`): The training task of the high-accuracy sentiment analysis model;
* HAEvaluateFinalState (`sa_evaluate`): The final task of the high-accuracy sentiment analysis model. 
  

    +----------+    +---------+    +--------+      +---------+    +------------+
    | Retrieve | -> | Extract | -> | Choice | -+-> | HATrain | -> | HAEvaluate |  
    +----------+    +---------+    +--------+  |   +---------+    +------------+
                                               |   +---------+    +------------+
                                               +-> | LATrain | -> | LAEvaluate |
                                               |   +---------+    +------------+
                                               |   +---------+
                                               +-> |  Fail   |
                                                   +---------+

## Requirements 

This SA workflow retrieves a dataset from AWS, stores it on [MinIO](https://github.com/minio/minio), and runs machine learning tasks on it. 

To run MinIO using docker containers, run: 

    docker run -p 9000:9000 -p 9001:9001 \                                   
        -e "MINIO_ROOT_USER=minio" \
        -e "MINIO_ROOT_PASSWORD=minio123" \
        quay.io/minio/minio server /data --console-address ":9001"

## Build the Sentiment Analysis Tasks

This SA workflow comes with a `Dockerfile`, which simplifies the application deployment. 
The Dockerfile enables building the container image of the different tasks, through an environment variable `HANDLER_ENV`.
 * HANDLER_ENV="retrieve": to build the image for the retriever `sa-sentiment-analysis-retrieve`;
 * HANDLER_ENV="extract": to build the image for the extractor `sa-sentiment-analysis-extract`; 
 * HANDLER_ENV="train": to build the image for the training tasks `sa-sentiment-analysis-train`;
 * HANDLER_ENV="evaluate": to build the image for the evaluation tasks `sa-sentiment-analysis-evaluate`.


To build the container, run the following command:

    cd ./src
    docker build --build-arg HANDLER_ENV="retrieve" -t sa-sentiment-analysis-retrieve .      
    docker build --build-arg HANDLER_ENV="extract" -t sa-sentiment-analysis-extract .      
    docker build --build-arg HANDLER_ENV="train" -t sa-sentiment-analysis-train .      
    docker build --build-arg HANDLER_ENV="evaluate" -t sa-sentiment-analysis-evaluate .      

## Launch the Server 
The SA workflow creates an HTTP Server that executes different functions according to the received REST call. 
By default, the server listens to `8080`.
The server needs `MinIO` as object storage to save intermediary data.

### API of the Retrieve Task
POST localhost:8080/invoke

    {
        "Params" : {
            "data_url": "https://s3.amazonaws.com/fast-ai-nlp/amazon_review_polarity_csv.tgz", 
            "local_dir": "./amazon_review_polarity_csv.tgz", 
            "object_name": "raw/amazon_review_polarity_csv.tgz"
        }
    }


### API of the Extract Task

POST localhost:8080/invoke

    {
        "Params" : {
            "tgz_input_object_name": "data/test.csv",
            "subset" : 0.002,
            "local_dataset_file": "./amazon_review_polarity_csv.tgz", 
            "local_output_dir": "./data", 
            "output_train_object_name": "data/train.csv",
            "output_test_object_name": "data/test.csv"
        }
    }


### API of the Train Task

POST localhost:8080/invoke

    {
      "Params" : {
          "subset": 0.001, 
          "max_features": 2, 
          "train_object_data": "data/train.csv", 
          "local_train_file": "train.csv", 
          "local_model_file": "sentiment_model.pkl", 
          "local_vectorizer_file": "tfidf_vectorizer.pkl",
          "output_model_object": "model/sentiment_model.pkl", 
          "output_vectorizer_object": "model/tfidf_vectorizer.pkl" 
      }
    }

### API of the Evaluate Task

POST localhost:8080/invoke

    {
        "Params" : {
            "test_object_data": "data/test.csv", 
            "local_test_file": "test.csv", 
            "subset": 0.0002, 
            "local_model_file": "sentiment_model.pkl", 
            "local_vectorizer_file": "tfidf_vectorizer.pkl", 
            "input_model_object": "model/sentiment_model.pkl", 
            "input_vectorizer_object": "model/tfidf_vectorizer.pkl"
        }
    }


### Setting MinIO Parameters
Each docker image enables the customization of the MinIO connection string. 
We can set information for connecting to MinIO using environment variables.

    MINIO_ENDPOINT="172.17.0.1:9000"
    MINIO_ACCESS_KEY=minio
    MINIO_SECRET_KEY=minio123
    MINIO_BUCKET=serverledge
    MINIO_SECURE=false

