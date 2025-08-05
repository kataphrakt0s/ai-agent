import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # Treat "." as the current working directory
        if directory == ".":
            full_path = os.path.abspath(working_directory)
        else:
            full_path = os.path.join(working_directory, directory)

        # Return error if the directory is outside the working directory
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory) + os.sep) and os.path.abspath(full_path) != os.path.abspath(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Return error if the path is not a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        # Get contents and build formatted string
        contents = []
        for item in os.listdir(full_path):
            try:
                item_path = os.path.join(full_path, item)
                is_dir = os.path.isdir(item_path)
                size = 0 if is_dir else os.path.getsize(item_path)
                contents.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            except PermissionError:
                contents.append(f"- {item}: Error: Permission denied")
            except OSError as e:
                contents.append(f"- {item}: Error: {str(e)}")
        
        return "\n".join(sorted(contents))
    
    except PermissionError:
        return f'Error: Permission denied accessing "{directory}"'
    except OSError as e:
        return f'Error: {str(e)}'


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