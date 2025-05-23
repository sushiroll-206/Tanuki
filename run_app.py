# run_app.py
# Simple Python script to launch the Streamlit Resume Matcher app

import subprocess
import sys
import os

def run_streamlit():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(project_dir, "app.py")

    if not os.path.exists(app_path):
        print("app.py not found. Please make sure you're in the correct directory.")
        sys.exit(1)

    print("Launching Streamlit app...")
    subprocess.run(["streamlit", "run", app_path])

if __name__ == "__main__":
    run_streamlit()
