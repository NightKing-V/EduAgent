import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Import and run the Streamlit app
    from ui.streamlit_app import *
    
    # This file can be run with: streamlit run main.py