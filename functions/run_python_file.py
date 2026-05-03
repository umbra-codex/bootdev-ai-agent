import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
  name="run_python_file",
  description="Executes a Python file at the given path relative to the working directory and returns its stdout and stderr output",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Path to the Python file to execute, relative to the working directory",
      ),
      "args": types.Schema(
        type=types.Type.ARRAY,
        description="Optional list of command-line arguments to pass to the Python file",
        items=types.Schema(type=types.Type.STRING)
      ),
    },
    required=["file_path"],
  )
)

def run_python_file(working_directory, file_path, args=None):
  working_dir_abs = os.path.abspath(working_directory)
  target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

  if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(target_file):
    return f'Error: "{file_path}" does not exist or is not a regular file'
  
  if not file_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file'
  
  try:
    command = ["python", target_file]
    if args:
      command.extend(args)
    
    result = subprocess.run(
      command,
      cwd=working_dir_abs,
      capture_output=True,
      text=True,
      timeout=30,
    )

    output = []
    if result.returncode != 0:
      output.append(f"Process exited with code {result.returncode}")
    if not result.stdout and not result.stderr:
      output.append("No output produced")
    else:
      if result.stdout:
        output.append(f"STDOUT:\n{result.stdout}")
      if result.stderr:
        output.append(f"STDERR:\n{result.stderr}")
    return "\n".join(output)
  
  except Exception as ex:
    return f"Error: executing Python file: {ex}"