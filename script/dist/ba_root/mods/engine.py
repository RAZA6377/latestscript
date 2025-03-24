import os
import shutil
from setuptools import setup
from Cython.Build import cythonize

# Define folder paths
py_folder = "pyfiles"
so_folder = "sofiles"

# Create folders if they don't exist
os.makedirs(py_folder, exist_ok=True)
os.makedirs(so_folder, exist_ok=True)

# Get all .py files in pyfiles folder
py_files = [f for f in os.listdir(py_folder) if f.endswith(".py")]

# Process each Python file
for py_file in py_files:
    py_path = os.path.join(py_folder, py_file)
    
    # Generate .so file using Cython
    setup(
        ext_modules=cythonize(py_path),
        script_args=["build_ext", "--inplace"]
    )
    
    # Find the generated .so file
    base_name = py_file.replace(".py", "")
    for file in os.listdir():
        if file.startswith(base_name) and file.endswith(".so"):
            so_path = os.path.join(so_folder, file)
            shutil.move(file, so_path)
            print(f"Converted: {py_file} → {file} (moved to {so_folder}/)")

print("✅ All .py files have been converted to .so files and moved to sofiles/")