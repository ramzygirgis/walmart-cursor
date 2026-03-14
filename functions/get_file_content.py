import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_path_to_wd = os.path.abspath(working_directory)
    path_to_target_dir = os.path.normpath(os.path.join(abs_path_to_wd, file_path))
    try:
        if not os.path.commonpath([abs_path_to_wd, path_to_target_dir]) == abs_path_to_wd:
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(path_to_target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(path_to_target_dir, "r") as f:
            file_contents = f.read(MAX_CHARS)
            if f.read(1):
                file_contents += f'[... File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_contents
    
    except Exception as e:
        return f'Error: {e}'
    
schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description="Lists the contents of a specified file in the working directory, providing a string of the file's contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath to the desired file, relative to the working directory",
            ),
        },
    ),
)