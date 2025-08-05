import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Get absolute paths
        full_path = os.path.join(working_directory, file_path)
        abs_working = os.path.abspath(working_directory)
        abs_file = os.path.abspath(full_path)

        # Check if file is outside working directory
        if not abs_file.startswith(abs_working + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        # Check if file is a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Prepare command
        cmd = ['python', os.path.basename(file_path)] + args

        # Run the process
        completed_process = subprocess.run(
            cmd,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(full_path)
        )

        # Prepare output
        output_parts = []
        
        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
        
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
            
        if not output_parts:
            return "No output produced."
            
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"