import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the 'content' passed into the function into a file specified file path. Creates it, if it doesn't already exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written into the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_work = os.path.abspath(working_directory)
    abs_file = os.path.abspath(full_path)

    # Make sure "file_path" is inside "working_directory"
    if os.path.commonpath([abs_work, abs_file]) != abs_work:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # If file_path doesn't exist, create it
    try:
        with open(full_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Failed to write to "{file_path}": {e}'

