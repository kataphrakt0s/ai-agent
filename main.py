import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose = False

    # Get all arguments except the script name, up to --verbose if present
    args = sys.argv[1:]
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")
    user_prompt = " ".join(args)

    if len(args) == 0:
        print("Error: No contents provided. Please provide a prompt as a command line argument.")
        sys.exit(1)

    # Initialize messages with combined prompt
    system_context = """You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory."""

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Add available functions to the messages
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    
    # Main conversation loop
    max_iterations = 20
    for iteration in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions])
            )

            if not response.candidates:
                print("No response received from the model")
                return

            for candidate in response.candidates:
                if not candidate.content:
                    continue

                messages.append(candidate.content)

                # Process each part of the response
                if hasattr(candidate.content, 'parts') and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Handle function calls
                        if hasattr(part, 'function_call') and part.function_call:
                            function_call_result = call_function(part.function_call, verbose)
                            messages.append(function_call_result)
                        
                        # Handle text responses - this is the final response
                        elif hasattr(part, 'text') and not any(
                            hasattr(p, 'function_call') for p in candidate.content.parts
                        ):
                            print("\nFinal response:")
                            print(part.text)
                            return

        except Exception as e:
            print(f"Error: {str(e)}")
            return

    print("Maximum iterations reached without final response")

if __name__ == "__main__":
    main()
