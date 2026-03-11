import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    abs_path_to_wd = os.path.abspath(working_directory)
    path_to_target = os.path.normpath(os.path.join(abs_path_to_wd, file_path))

    if not os.path.commonpath([abs_path_to_wd, path_to_target]) == abs_path_to_wd:
        return f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory'
    if not os.path.isfile(path_to_target):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if len(file_path) < 3 or file_path[-3:] != '.py':
        return f'Error: "{file_path}" is not a Python file'
    try:
        command = ["python", path_to_target]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd = abs_path_to_wd, capture_output=True, timeout=30, text=True)
        s = ''
        if result.returncode != 0:
            s += f'Process exited with code {result.returncode}. '
        if not result.stdout and not result.stderr:
            s += 'No output produced. '
        elif not result.stdout:
            s += f'STDERR: {result.stderr}'
        elif not result.stderr:
            s += f'STDOUT: {result.stdout}'
        else:
            s += f'STDOUT: {result.stdout}. STDERR: {result.stderr}'
        return s
    except Exception as e:
        return f'Error: executing Python file: {e}'