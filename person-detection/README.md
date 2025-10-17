## Description

The workflow takes a (base64-encoded) image, resizes it and uses YOLOv8 to
detect people. If any person is detected, the corresponding region of the image
is saved to a minIO bucket.

## Usage 

Start minIO:

    bash start-minio.sh

Create custom images for functions:

    docker build -t yolofunc yolo/
    docker build -t cropfunc crop/
    docker build -t resizefunc resize/

Create functions and workflow (assuming `CLI` env. variable contains the path of
Serverledge CLI executable):

    $CLI create -u -f resize --memory 500 --runtime custom --custom_image resizefunc \
        --input "img:Text" --output "img:Text"

    $CLI create -u -f yoloFunc --memory 900 --runtime custom --custom_image yolofunc \
        --input "img:Text" --output "Img:Text" --output "Detections:ArrayText" --output "Count:Int"

    $CLI create -u -f cropFunc --memory 500 --runtime custom --custom_image cropfunc \
        --input "Img:Text" --input "Detections:ArrayText" --input "Count:Int" \
            --output "Objects:ArrayText" 

    $CLI create-workflow -s workflow.json -f detection

Invoke the workflow with an example input:

    $CLI invoke-workflow -f detection -j resize/input.json > output.txt

