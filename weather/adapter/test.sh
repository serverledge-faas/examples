
CLI=$HOME/Dev/serverledge/bin/serverledge-cli

$CLI create -u -f adapter --memory 200 --runtime python310 --handler function.handler --src function.py  \
	--input "gemini_api_key:Text" \
	--input "current_temperature:Float" --input "daily_rain_sum:ArrayFloat" \
	--input "daily_max_temp:ArrayFloat" --input "daily_min_temp:ArrayFloat" \
	--output "prompt:Text" --output "gemini_api_key:Text"

$CLI invoke -f adapter --params_file input.json --ret_output
