import os

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

