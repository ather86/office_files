import os
import subprocess

venv_scripts = r"C:\Users\athek\OneDrive\Documents\my_streamlit_app\user_story_tool\py311env\Scripts"

# Add venv Scripts folder to PATH
os.environ["PATH"] = venv_scripts + os.pathsep + os.environ["PATH"]

# Absolute path to app.py
app_path = r"C:\Users\athek\OneDrive\Documents\my_streamlit_app\user_story_tool\app.py"

try:
    subprocess.run(["streamlit", "run", app_path], check=True)
except Exception as e:
    print("Error running the Streamlit app:", e)

input("Press Enter to exit...")
