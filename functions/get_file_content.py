import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
  name="get_file_content",
  description="Reads and returns the content of a file at the given path relative to the working directory, truncated at the maximum character limit",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Path to the file to read, relative to the working directory"
      )
    }
  )
)

def get_file_content(working_directory, file_path):
  working_dir_abs = os.path.abspath(working_directory)
  target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

  if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(target_file):
    return f'Error: File not found or is not a regular file: "{file_path}"'

  with open(target_file, "r") as f:
    try:
      file_content_string = f.read(MAX_CHARS)
      if f.read(1):
        file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    except OSError as ex:
      return f'Error: {ex}'

  return file_content_string
