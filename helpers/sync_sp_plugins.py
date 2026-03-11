"""
Sync Helper Script for Substance Painter plugins.

This script copies your Python plugin files from this repository directly into
Substance Painter's plugin folder. It flattens the folder structure so Painter
can discover and run the plugins correctly.

LEARNING NOTE: This is a great example of a practical utility script! 
It uses some of Python's most powerful standard libraries:
- `pathlib`: The modern way to handle file paths (instead of joining strings).
- `shutil`: For high-level file operations (like copying and deleting).
- `json`: For saving and loading configuration data.
"""
import os
import sys
import json
import shutil
import platform
from pathlib import Path

# We save the path to Painter's folder in a JSON file so we only have to ask you once.
CONFIG_FILE_NAME = "sp_path.json"

def get_sp_plugins_dir(repo_root):
    """
    Finds the Substance Painter plugins directory.
    1. Checks if we saved a custom path earlier.
    2. Tries to auto-discover it based on your OS.
    3. Asks you to type it in if both fail.
    """
    # A Path object makes it easy to construct file paths with the '/' operator
    config_path = repo_root / "helpers" / CONFIG_FILE_NAME
    
    # 1. Check saved config
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                data = json.load(f)
                saved_path = Path(data.get("plugins_path", ""))
                if saved_path.exists():
                    return saved_path
        except Exception as e:
            print(f"Warning: Could not read {CONFIG_FILE_NAME}: {e}")

    # 2. Auto-discover common paths
    system = platform.system()
    home = Path.home()  # Usually C:\Users\Username on Windows
    
    # Construct the default path Adobe uses for Painter
    if system == "Windows":
        auto_path = home / "Documents" / "Adobe" / "Adobe Substance 3D Painter" / "python" / "plugins"
    elif system == "Darwin": # macOS
        auto_path = home / "Documents" / "Adobe" / "Adobe Substance 3D Painter" / "python" / "plugins"
    else: # Linux
        auto_path = home / "Documents" / "Adobe" / "Adobe Substance 3D Painter" / "python" / "plugins"

    # .exists() checks if the folder actually exists on your hard drive
    if auto_path.exists():
        return auto_path

    # 3. Prompt user if auto-discovery fails
    print(f"\nCould not automatically find the Substance Painter plugins folder.")
    print(f"Looked in: {auto_path}")
    print("Please enter the full path to your Substance Painter 'python/plugins' folder.")
    print(r"Example: C:\Users\Name\Documents\Adobe\Adobe Substance 3D Painter\python\plugins")
    
    # Loop until the user provides a valid path
    while True:
        user_input = input("\nPath: ").strip()
        # Remove quotes if the user pasted a path wrapped in them
        user_input = user_input.strip('"').strip("'")
        
        if not user_input:
            print("Canceled.")
            sys.exit(1)
            
        custom_path = Path(user_input)
        if custom_path.exists() and custom_path.is_dir():
            # Save it for next time to make life easier!
            try:
                # Ensure the helpers folder exists
                config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(config_path, "w") as f:
                    json.dump({"plugins_path": str(custom_path)}, f, indent=4)
                print(f"Saved custom path to {CONFIG_FILE_NAME}!")
                return custom_path
            except Exception as e:
                print(f"Warning: Could not save path to {CONFIG_FILE_NAME}: {e}")
                return custom_path
        else:
            print(f"Error: Folder does not exist: {custom_path}")
            print("Please try again or press Enter to cancel.")

def find_plugin_roots(repo_root):
    """
    Finds the main root folders that contain our plugin code.
    This lets the script support 'LabExercises', 'LabSolutions', and 'prep'.
    """
    roots = []
    candidate_names = ["LabExercises", "LabSolutions", "prep"]
    
    for name in candidate_names:
        folder = repo_root / name
        if folder.exists() and folder.is_dir():
            roots.append(folder)
            
    return roots

def sync_plugins():
    """Main execution function."""
    # __file__ is the path to this script. .parent goes up one folder (to repo root).
    repo_root = Path(__file__).resolve().parent.parent
    
    sp_dir = get_sp_plugins_dir(repo_root)
    if not sp_dir:
        return
        
    folders = find_plugin_roots(repo_root)
    
    if not folders:
        print("No plugin root folders found (e.g. 'LabExercises', 'prep', etc).")
        return
        
    # Give the user a menu to choose from
    print("\nAvailable Roots to Sync From:\n")
    for i, folder in enumerate(folders):
        print(f"  [{i+1}] {folder.name}")
        
    print(f"\n  [0] CANCEL")
    
    # Get the user's choice safely
    while True:
        try:
            choice_str = input("\nEnter the number of the root folder to sync: ").strip()
            if not choice_str:
                continue
            choice = int(choice_str)
            if choice == 0:
                print("Canceled.")
                return
            if 1 <= choice <= len(folders):
                break
            print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a number.")
            
    source_dir = folders[choice - 1]
    
    # Step A: Clean the destination folder entirely.
    # We do this so deleted scripts in our repo don't stay alive in Painter as "ghost" plugins.
    print(f"\nClearing old files from Painter plugins folder: {sp_dir}")
    for item in sp_dir.iterdir():
        # Only delete Python files to avoid breaking anything else
        if item.is_file() and item.name.endswith(".py"):
            item.unlink() # Deletes the file
            
    print(f"Syncing from: {source_dir.name}")
    print("-" * 40)
    
    # Step B: Find and copy the new code
    count = 0
    # .rglob() searches recursively through all subfolders for files matching the pattern
    for py_file in source_dir.rglob("*.py"):
        if py_file.is_file():
            
            # NOTE: We only want to sync code from Week 5 and Week 6!
            # Ignore anything from week 4 by checking the folder path as a string
            if "05_SP_" not in str(py_file) and "06_SP_" not in str(py_file):
                continue
            
            # shutil.copy2 copies the file AND preserves its metadata (like modify time)
            # The destination combines the Painter directory and the file's name, 'flattening' the structure
            dest_file = sp_dir / py_file.name
            shutil.copy2(py_file, dest_file)
            print(f"  Copied: {py_file.name}")
            count += 1
            
    print("-" * 40)
    print(f"Success! {count} Python files synced.")
    print("In Substance Painter, go to: Python -> Reload Plugins Folder")

# Standard Python trick: This ensures the code only runs if the script is executed directly
# (e.g. `python sync_sp_plugins.py`), not if someone imports it from another file.
if __name__ == "__main__":
    sync_plugins()
