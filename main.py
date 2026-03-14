import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt
from config import model_name
from config import MAX_ITERATIONS


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    done = False

    for _ in range(MAX_ITERATIONS):
        if done:
            continue
        response, function_responses = generate_content(client, messages, args.verbose)

        for candidate in response.candidates:
            new_message = candidate.content
            messages.append(new_message)

        if not response.function_calls:
            print(response.text)
            break # exit the loop

        messages.append(types.Content(role="user", parts=function_responses))

        if _ == MAX_ITERATIONS - 1:
            print(f'Model has hit the maximum number of iterations ({MAX_ITERATIONS} iterations)')
            sys.exit(1)



def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if not response.function_calls:
        # print("Response:")
        # print(response.text)
        return response, None
    
    function_results = []

    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if function_call_result.parts == []:
            raise Exception("Error: function_call_result.parts is empty")
        if not function_call_result.parts[0].function_response:
            raise Exception('Error: function_call_result.parts[0].function_response is None')
        if not function_call_result.parts[0].function_response.response:
            raise Exception('Error: function_call_result.parts[0].function_response.response is None')
        
        function_results.append(function_call_result.parts[0])

        # if verbose:
        #     print(f"-> {function_call_result.parts[0].function_response.response}")

    return response, function_results

if __name__ == "__main__":
    main()
