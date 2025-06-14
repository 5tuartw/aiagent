import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    #2. If the directory argument is outside the working_directory, return a string with an error:
    #   f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        abs_working_directory = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: could not find absolute path of working_directory "{working_directory}": {e}'

    target_directory = abs_working_directory

    if directory:
        target_directory = os.path.abspath(os.path.join(abs_working_directory, directory))

    #print(abs_working_directory)
    #print(abs_directory_path)

        if not target_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    #3. If the directory argument is not a directory, again, return an error string:
    #   f'Error: "{directory}" is not a directory'

    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    #4. Build and return a string representing the contents of the directory. It should use this format:
    #   - README.md: file_size=1032 bytes, is_dir=False
    #   - src: file_size=128 bytes, is_dir=True
    #   - package.json: file_size=1234 bytes, is_dir=False

    contents_list = os.listdir(target_directory)
    contents_info = []

    for item in contents_list:
        info = item
        item_path = os.path.join(target_directory, item)
        try:
            info += ": file_size=" + str(os.path.getsize(item_path)) + " bytes, "
            if os.path.isdir(item_path):
                info += "is_dir=True"
            else:
                info += "is_dir=False"
            contents_info.append(info)
        except Exception as e:
            return f'Error: could not get file size or file/directory status of item {item}: {e}'
    
    return "\n".join(contents_info)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)