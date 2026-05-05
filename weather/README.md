## Description

The workflow takes latitude and longitude as input, retrieves weather forecast
data using an open API and asks Gemini to prepare a brief summary.


< weather > ---> < choice > ----> < adapter > ---> < gemini >
                               \--- < formatter > 

## Usage 

Create custom images for functions:

    docker build -t geminifunc gemini/
    docker build -t weatherfunc weather/

Create functions and workflow (assuming `CLI` env. variable contains the path of
Serverledge CLI executable):

    $CLI create -u -f weather --memory 500 --runtime custom --custom_image weatherfunc \
        --input "gemini_api_key:Text" --input "latitude:Float" --input "longitude:Float"\
        --input "ai_report:Bool" \
        --output "gemini_api_key:Text" \
        --output "ai_report:Bool" \
        --output "current_temperature:Float" --output "daily_rain_sum:ArrayFloat" \
        --output "daily_max_temp:ArrayFloat" --output "daily_min_temp:ArrayFloat" 

    $CLI create -u -f formatter --memory 128 --runtime python310 --handler function.handler --src formatter/function.py  \
        --input "current_temperature:Float" --input "daily_rain_sum:ArrayFloat" \
        --input "daily_max_temp:ArrayFloat" --input "daily_min_temp:ArrayFloat" \
        --output "response:Text"

    $CLI create -u -f adapter --memory 200 --runtime python310 --handler function.handler --src adapter/function.py  \
        --input "gemini_api_key:Text" \
        --input "current_temperature:Float" --input "daily_rain_sum:ArrayFloat" \
        --input "daily_max_temp:ArrayFloat" --input "daily_min_temp:ArrayFloat" \
        --output "prompt:Text" --output "gemini_api_key:Text"

    $CLI create -u -f gemini --memory 500 --runtime custom --custom_image geminifunc \
        --input "gemini_api_key:Text" --input "prompt:Text" \
        --output "response:Text"

    $CLI create-workflow -s workflow.json -f weatherForecast

Invoke the workflow with an example input:

    $CLI invoke-workflow -f weatherForecast -j weather/input.json > output.txt

