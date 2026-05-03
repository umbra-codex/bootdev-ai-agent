import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("api key wasn't found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = genai.Client(api_key=api_key)

def generate_content(messages):
    return client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt
    ),
)

def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        response = generate_content(messages)

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        if not response.function_calls:
            print(f"Response:\n{response.text}")
            return
        
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if not function_call_result.parts:
                raise Exception("call_function returned a Content object with no parts")
            
            if function_call_result.parts[0].function_response is None:
                raise Exception("function_response is None")
            
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("function_response.response is None")
            
            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_results))
    
    print("Error: max iterations reached without a final response")
    sys.exit(1)

if __name__ == "__main__":
    main()