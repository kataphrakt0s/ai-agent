import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    try:
        # Construct the full path to the file
        full_path = os.path.join(working_directory, file_path)

        # Check if the file would be outside the working directory
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory) + os.sep):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Create the file if it does not exist
        if not os.path.exists(full_path):
            open(full_path, 'a').close()

        # Write the content to the file
        with open(full_path, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except PermissionError:
        return f'Error: Permission denied accessing "{file_path}"'
    except OSError as e:
        return f'Error: {str(e)}'