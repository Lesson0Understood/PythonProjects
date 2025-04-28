import re
import os

def sanitize_filename(name):
    """Removes characters invalid for filenames."""
    if not name:
        return "Unnamed_Channel"
    # Remove invalid characters specific to Windows/Unix systems
    sanitized = re.sub(r'[\\/*?:"<>|]', "", name)

    # Replace sequences of whitespace with a single underscore
    sanitized = re.sub(r'\s+', '_', sanitized).strip('_')

    # Remove leading/trailing dots or spaces (often problematic)
    sanitized = sanitized.strip('. ')

    # Limit length to avoid issues with maximum path lengths (optional)
    sanitized = sanitized[:150]
    return sanitized if sanitized else "Unnamed_Channel" # Ensure not empty

def ensure_dir_exists(directory_path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Created directory: '{directory_path}'")
        except OSError as e:
            print(f"Error creating directory '{directory_path}': {e}")