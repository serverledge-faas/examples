
CLI=$HOME/Dev/serverledge/bin/serverledge-cli

$CLI create -u -f formatter --memory 200 --runtime python310 --handler function.handler --src function.py  \
	--input "current_temperature:Float" --input "daily_rain_sum:ArrayFloat" \
	--input "daily_max_temp:ArrayFloat" --input "daily_min_temp:ArrayFloat" \
	--output "response:Text" 

$CLI invoke -f formatter --params_file input.json --ret_output
