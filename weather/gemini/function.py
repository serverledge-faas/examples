from google import genai


def handler (params, context):
    try:
        api_key = params["gemini_api_key"]
        prompt = params["prompt"]
    except:
        # TODO: error
        return {}

    client = genai.Client(api_key=api_key)

    LITE="gemini-3.1-flash-lite-preview"
    GEMMA="gemma-3-27b-it"
    FLASH="gemini-2.5-flash"

    gemini_response = client.models.generate_content(
        model=GEMMA, contents=prompt
    )
    print(gemini_response.text)

    response = {}
    response["response"] = gemini_response.text

    return response
