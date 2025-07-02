import tempfile
import os

def save_uploaded_file_temporarily(uploaded_file) -> str:
    """
    Saves a Streamlit-uploaded file to a temporary path.
    
    Args:
        uploaded_file: Streamlit UploadedFile (e.g., PDF)
    
    Returns:
        str: Path to the saved temporary file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name  # Return the file path


def cleanup_temp_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"Failed to delete temp file: {e}")
