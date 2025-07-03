import tempfile
import os

def save_uploaded_file_temporarily(uploaded_file, chat_id) -> str:
    os.makedirs(f"app/data/{chat_id}", exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=f"app/data/{chat_id}", delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


def cleanup_temp_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"Failed to delete temp file: {e}")
