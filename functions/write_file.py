import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: could not find absolute path of working_directory "{working_directory}": {e}'

    target_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not target_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    dir_path = os.path.dirname(target_file_path)

    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except Exception as e:
            return f'Error: Unable to create path "{target_file_path}": {e}'

    try:
        with open(target_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: Unable to write to "{file_path}": {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write provided content to a file. If the file does not exist it creates it, otherwise it overwrites the existing content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
    ),
)