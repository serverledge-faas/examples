from google import genai


def handler (params, context):
    try:
        api_key = params["gemini_api_key"]
        prompt = params["prompt"]
    except:
        # TODO: error
        return {}

    client = genai.Client(api_key=api_key)

    gemini_response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    print(gemini_response.text)

    response = {}
    response["response"] = gemini_response.text

    return response
