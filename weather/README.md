## Description

The workflow takes latitude and longitude as input, retrieves weather forecast
data using an open API and asks Gemini to prepare a brief summary.

## Usage 

Create custom images for functions:

    docker build -t geminifunc gemini/
    docker build -t weatherfunc weather/

Create functions and workflow (assuming `CLI` env. variable contains the path of
Serverledge CLI executable):

    $CLI create -u -f resize --memory 500 --runtime custom --custom_image resizefunc \
        --input "img:Text" --output "img:Text"

    $CLI create -u -f yoloFunc --memory 900 --runtime custom --custom_image yolofunc \
        --input "img:Text" --output "Img:Text" --output "Detections:ArrayText" --output "Count:Int"

    $CLI create -u -f cropFunc --memory 500 --runtime custom --custom_image cropfunc \
        --input "Img:Text" --input "Detections:ArrayText" --input "Count:Int" \
            --output "Objects:ArrayText" 

    $CLI create-workflow -s workflow.json -f weatherForecast

Invoke the workflow with an example input:

    $CLI invoke-workflow -f weatherForecast -j weather/input.json > output.txt

