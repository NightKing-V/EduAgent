import os
import sys
from ui.app import EduAgentApp

# Make sure Python can find other app modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


# Application entry point
if __name__ == "__main__":
    app = EduAgentApp()
    app.run()