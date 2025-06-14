import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):

    split_file_name = file_path.split(".")
    if not split_file_name[len(split_file_name)-1] == "py":
        return f'Error: File "{file_path}" does not have .py extension'
    
    try:
        abs_working_directory = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: could not find absolute path of working_directory "{working_directory}": {e}'

    target_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not target_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file_path):
        return f'Error: File "{file_path}" not found.'

    output_lines = []
    try:
        result = subprocess.run(["python3", target_file_path], cwd=working_directory, capture_output=True, timeout=30, text=True)
        if result.stdout == None or result.stderr == None:
            return 'No output produced.'
        output_lines.append(result.stdout)
        output_lines.append(result.stderr)
        if not result.returncode == 0:
            output_lines.append(f'Process exited with code X')
    except Exception as e:
        return f"Error: executing Python file: {e}"

    return "\n".join(output_lines)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a named python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run",
            ),
        },
    ),
)
