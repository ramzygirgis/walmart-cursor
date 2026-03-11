import os

def get_files_info(working_directory, directory = '.'):
    '''
    directory is rel. path to file from working_directory. the LLM agent will be able to select the directory it wants to scan,
    but we choose working_directory, limiting the scope of files and directories the agent can view.
    '''
    abs_path_to_wd = os.path.abspath(working_directory)
    path_to_target = os.path.normpath(os.path.join(abs_path_to_wd, directory))
    is_target_valid = os.path.commonpath([abs_path_to_wd, path_to_target]) == abs_path_to_wd
    if not is_target_valid:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path_to_target):
        return f'Error: "{directory}" is not a directory'
    str = ''
    try:
        for item in os.listdir(path_to_target):
                path_to_item = os.path.join(path_to_target, item)
                if os.path.isfile(path_to_item):
                    str += f'- {item}: file_size={os.path.getsize(path_to_item)} bytes, is_dir=False\n'
                else:
                    str += f'- {item}: file_size={os.path.getsize(path_to_item)} bytes, is_dir=True\n'
        return str
    except Exception as e:
         return f'Error: {e}'
        