# run_app.py
import os
import subprocess
import sys
import venv
from pathlib import Path

VENV_DIR = Path("venv")
REQUIREMENTS_FILE = Path("requirements.txt")


def in_virtualenv():
    return sys.prefix != sys.base_prefix


def create_virtualenv():
    print("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)


def install_dependencies():
    print("Installing dependencies from requirements.txt...")
    pip_path = VENV_DIR / "bin" / "pip" if os.name != 'nt' else VENV_DIR / "Scripts" / "pip.exe"
    subprocess.check_call([str(pip_path), "install", "-r", str(REQUIREMENTS_FILE)])


def run_streamlit_app():
    streamlit_path = VENV_DIR / "bin" / "streamlit" if os.name != 'nt' else VENV_DIR / "Scripts" / "streamlit.exe"
    subprocess.check_call([str(streamlit_path), "run", "app.py"])


if __name__ == "__main__":
    # Check if we're in the virtual environment already
    if not in_virtualenv():
        print("Not in a virtual environment.")

        if not VENV_DIR.exists():
            create_virtualenv()

        install_dependencies()

        # Re-run the script in the new virtual environment
        python_path = VENV_DIR / "bin" / "python" if os.name != 'nt' else VENV_DIR / "Scripts" / "python.exe"
        print("Re-running script inside virtual environment...")
        subprocess.check_call([str(python_path), __file__])
        sys.exit(0)

    else:
        print("Virtual environment detected.")
        run_streamlit_app()
