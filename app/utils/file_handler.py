import tempfile
import os

def save_uploaded_file_temporarily(uploaded_file, chat_id) -> str:
    os.makedirs(f"app/data/{chat_id}", exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=f"app/data/{chat_id}", delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name

def cleanup_temp_file(path: str):
    """
    Deletes the specified temp file and attempts to clean up its parent folder if needed.
    """
    try:
        # Delete the file
        if os.path.exists(path):
            os.remove(path)
            print(f"✅ Deleted file: {path}")
        else:
            print(f"⚠️ File already deleted or not found: {path}")

        # Attempt to delete the parent folder if it's empty
        parent_dir = os.path.dirname(path)
        if os.path.exists(parent_dir) and not os.listdir(parent_dir):
            os.rmdir(parent_dir)
            print(f"🧹 Cleaned up empty temp directory: {parent_dir}")

    except Exception as e:
        print(f"❌ Failed to clean up: {e}")

