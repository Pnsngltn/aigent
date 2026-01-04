
import os
import sys
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT 
from functions.get_file_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content, 
        schema_run_python_file,
        schema_write_file,
    ]
)

def main(*args):
    verbose = False
    model_name = "gemini-2.0-flash-001"
    #if not sys.argv[1:]:
        #print("Usage: uv run main.py <prompt>")
        #sys.exit(1)
    args = sys.argv[1:]
    if "--verbose" in args:
        args.remove("--verbose")
        verbose = True
    user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum." # " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()

