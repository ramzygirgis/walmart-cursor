import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_path_to_wd = os.path.abspath(working_directory)
    path_to_target = os.path.normpath(os.path.join(abs_path_to_wd, file_path))
    try:
        if not os.path.commonpath([abs_path_to_wd, path_to_target]) == abs_path_to_wd:
            return f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory'
        if os.path.isdir(path_to_target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(path_to_target)
        os.makedirs(parent_dir, exist_ok = True)
        with open(path_to_target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given string to the file at the specific filepath, relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath to the desired file, relative to the working directory",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "String containing the text that we would like to write to the specified file",
            ),
        },
    ),
)