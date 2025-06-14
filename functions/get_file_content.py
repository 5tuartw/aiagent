import os
from google.genai import types

def get_file_content(working_directory, file_path):
    #2. If the file_path is outide the working_directory, return a string with an error:
    #   f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        abs_working_directory = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: could not find absolute path of working_directory "{working_directory}": {e}'

    target_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not target_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    #3. If the file_path is not a file, again, return an error string:
    #   f'Error: File not found or is not a regular file: "{file_path}"'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    #4. Read the file and return its contents as as string
    #   If the file is longer than 10000 characters, truncate it to 10000 characters and append this message to the end:
    #   [...File "{file_path}" truncated at 10000 characters]
    try:
        file = open(target_file_path, "r", encoding="utf-8")
    except Exception as e:
        return f'Error: unable to open file "{file_path}": {e}'
    
    content = file.read()
    if len(content) > 10000:
        content += content[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
    print(len(content))
    return content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a file truncated to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to retrieve content from, relative to the working directory",
            ),
        },
    ),
)