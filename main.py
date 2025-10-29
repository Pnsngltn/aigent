import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main(*args):
    verbose = False
    model = "gemini-2.0-flash-001"
    if not sys.argv[1:]:
        print("Usage: uv run main.py <prompt>")
        sys.exit(1)
    args = sys.argv[1:]
    if "--verbose" in args:
        args.remove("--verbose")
        verbose = True
    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(model=model, contents=messages)

    print(response.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()


