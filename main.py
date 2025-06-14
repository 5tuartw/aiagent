import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)



#available_functions_map = {
#    "get_files_info": get_files_info
#}

if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
else:
    sys.exit(1)

verbose = False
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose = True

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

max_iterations = 20
iterations = 0
final_response = None
response = None

while iterations < max_iterations:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    messages.append(response.candidates[0].content)

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, verbose)
            messages.append(function_call_result)
        iterations += 1
    else:
        print(response.text)
        break

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

