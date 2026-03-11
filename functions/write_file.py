import os

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