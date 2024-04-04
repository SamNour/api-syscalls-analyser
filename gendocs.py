import os
import subprocess

# Get a list of all Python files in the current directory
python_files = [f for f in os.listdir(".") if f.endswith(".py")]

# Run the pdoc command on each Python file
for file in python_files:
    subprocess.run(
        ["python3", "-m", "pdoc", "-d", "google", "-o", "./documentation", file]
    )
