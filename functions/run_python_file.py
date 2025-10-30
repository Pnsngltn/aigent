import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_work = os.path.abspath(working_directory)
    abs_file = os.path.abspath(full_path)

    # Check if file is inside working_directory
    if os.path.commonpath([abs_work, abs_file]) != abs_work:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check file_path exists
    if not os.path.exists(full_path): 
        return f'Error: File "{file_path}" not found.'

    # Check if file ends with '.py'
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    command = ["python3", file_path, *args]


    try:

        completed_process = subprocess.run(
                command, capture_output=True, cwd=abs_work, text=True, timeout=30
                )

        output = []

        if completed_process.stdout.strip():
            output.append(f"STDOUT:\n{completed_process.stdout.strip()}")

        if completed_process.stderr.strip():
            output.append(f"STDERR:\n{completed_process.stderr.strip()}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        if not output:
            return "No output produced."

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out"

    except Exception as e:
        return f"Error: executing Python file: {e}"




