#!/bin/sh

CLI=$HOME/Dev/serverledge/bin/serverledge-cli

$CLI create -u -f weather --memory 500 --runtime custom --custom_image weatherfunc \
     --input "gemini_api_key:Text" --input "latitude:Float" --input "longitude:Float"\
	--output "gemini_api_key:Text" \
	--output "current_temperature:Float" --output "daily_rain_sum:ArrayFloat" \
	--output "daily_max_temp:ArrayFloat" --output "daily_min_temp:ArrayFloat" 

$CLI create -u -f adapter --memory 200 --runtime python310 --handler function.handler --src adapter/function.py  \
	--input "gemini_api_key:Text" \
	--input "current_temperature:Float" --input "daily_rain_sum:ArrayFloat" \
	--input "daily_max_temp:ArrayFloat" --input "daily_min_temp:ArrayFloat" \
	--output "prompt:Text" --output "gemini_api_key:Text"

$CLI create -u -f gemini --memory 500 --runtime custom --custom_image geminifunc \
	--input "gemini_api_key:Text" --input "prompt:Text" \
	--output "response:Text"

$CLI create-workflow -s workflow.json -f weatherForecast
sleep 1
$CLI invoke-workflow -f weatherForecast -j weather-api/input.json | tee output.txt

