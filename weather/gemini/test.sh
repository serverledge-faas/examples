
CLI=$HOME/Dev/serverledge/bin/serverledge-cli

$CLI create -u -f gemini --memory 500 --runtime custom --custom_image geminifunc \
	--input "gemini_api_key:Text" --input "prompt:Text" \
	--output "response:Text"

$CLI invoke -f gemini --params_file input.json --ret_output
