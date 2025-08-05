import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    # Print function call with simpler format
    print(f" - Calling function: {function_name}")

    # Define mapping of function names to actual functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    # Check if function exists in our map
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )

    # Add working_directory to args and call the function
    function_args["working_directory"] = "./calculator"
    function_result = function_map[function_name](**function_args)

    # Return the result wrapped in Content
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )