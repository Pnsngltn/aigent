import os
from google.genai import types
from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file inside the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING, 
                description="The path of the file we want to read contents from. This is a required argument.", 
            ), 
        },
    ), 
)

def get_file_content(working_directory, file_path):
    # 2: Make sure 'file_path' is inside 'working_directory'
    full_path = os.path.join(working_directory, file_path)
    abs_work = os.path.abspath(working_directory)
    abs_file = os.path.abspath(full_path)
    if os.path.commonpath([abs_work, abs_file]) != abs_work:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        # 3: If file path is not a file
        if not os.path.isfile(abs_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # 4: Read the file and return the content as a string
        with open(abs_file, "r") as f:
            file_content = f.read(MAX_CHARS)
            check = f.read(1)
            if check:
                return f'{file_content}[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content

    except Exception as e:
        return f'Error: Cannot read file "{file_path}": {e}'
