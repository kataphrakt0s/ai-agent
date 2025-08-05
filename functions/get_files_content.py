import os
from functions.config import FILE_CONTENT_CHAR_LIMIT

def get_file_content(working_directory, file_path):
    try:
        # Construct the full path to the file
        full_path = os.path.join(working_directory, file_path)

        # Check if the file is outside the working directory
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory) + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the path is a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read and return the content of the file, truncating if necessary
        with open(full_path, 'r') as file:
            content = file.read(FILE_CONTENT_CHAR_LIMIT + 1)
        if len(content) > 10000:
            content = content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'
        
        return content

    except PermissionError:
        return f'Error: Permission denied accessing "{file_path}"'
    except OSError as e:
        return f'Error: {str(e)}'