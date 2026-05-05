#!/bin/sh

CLI=$HOME/Dev/serverledge/bin/serverledge-cli

$CLI create -u -f resize --memory 900 --runtime custom --custom_image grussorusso/resizefunc \
     --input "img:Text" --output "img:Text"

$CLI create -u -f mobilenet --memory 900 --runtime custom --custom_image grussorusso/mobilenetssd \
     --input "img:Text" --output "Img:Text" --output "Detections:ArrayText" --output "Count:Int"

$CLI create -u -f cropFunc --memory 900 --runtime custom --custom_image grussorusso/cropfunc \
	--input "Img:Text" --input "Detections:ArrayText" --input "Count:Int" \
        --output "Objects:ArrayText" 

$CLI create-workflow -s workflow.json -f detection
sleep 1
$CLI invoke-workflow -f detection -j resize/input.json > output.txt

