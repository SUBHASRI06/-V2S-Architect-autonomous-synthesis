import os
import shutil
import re

def save_generated_code(filename, code):
    """Saves files and cleans up AI formatting."""
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Clean the filename and handle any sub-paths
    clean_filename = filename.strip()
    clean_filename = re.sub(r'---.*?$', '', clean_filename, flags=re.MULTILINE).strip()
    
    file_path = os.path.join(output_dir, clean_filename)
    
    # 2. Create subfolders if necessary
    subfolder = os.path.dirname(file_path)
    if subfolder and not os.path.exists(subfolder):
        os.makedirs(subfolder, exist_ok=True)
    
    # 3. Strip AI markdown backticks (e.g., ```verilog)
    clean_code = re.sub(r'```[a-z]*\n', '', code)
    clean_code = clean_code.replace('```', '')
    
    # 4. Save as raw text
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(clean_code.strip())
    
    return file_path, clean_filename

def create_project_zip():
    """Builds the final ZIP package."""
    output_dir = "outputs"
    zip_name = "v2s_package"
    
    if os.path.exists(f"{zip_name}.zip"):
        os.remove(f"{zip_name}.zip")
        
    if os.path.exists(output_dir) and any(os.scandir(output_dir)):
        shutil.make_archive(zip_name, 'zip', output_dir)
        return f"{zip_name}.zip"
    return None