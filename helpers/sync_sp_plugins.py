import os
import sys
import json
import shutil
import platform
from pathlib import Path

# The JSON file to save custom paths
CONFIG_FILE_NAME = "sp_path.json"

def get_sp_plugins_dir(repo_root):
    """
    Find the Substance Painter plugins directory.
    Checks config file first, then auto-discovers based on OS,
    and finally prompts the user if not found.
    """
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

    # 2. Auto-discover
    system = platform.system()
    home = Path.home()
    
    if system == "Windows":
        auto_path = home / "Documents" / "Adobe" / "Adobe Substance 3D Painter" / "python" / "plugins"
    elif system == "Darwin": # macOS
        auto_path = home / "Documents" / "Adobe" / "Adobe Substance 3D Painter" / "python" / "plugins"
    else: # Linux
        auto_path = home / "Documents" / "Adobe" / "Adobe Substance 3D Painter" / "python" / "plugins"

    if auto_path.exists():
        return auto_path

    # 3. Prompt user if auto-discovery fails
    print(f"\nCould not automatically find the Substance Painter plugins folder.")
    print(f"Looked in: {auto_path}")
    print("Please enter the full path to your Substance Painter 'python/plugins' folder.")
    print(r"Example: C:\Users\Name\Documents\Adobe\Adobe Substance 3D Painter\python\plugins")
    
    while True:
        user_input = input("\nPath: ").strip()
        # Remove quotes if pasted
        user_input = user_input.strip('"').strip("'")
        
        if not user_input:
            print("Canceled.")
            sys.exit(1)
            
        custom_path = Path(user_input)
        if custom_path.exists() and custom_path.is_dir():
            # Save it for next time
            try:
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
    """Find main root folders that contain plugin code."""
    roots = []
    # Common root folders that might exist
    candidate_names = ["LabExercises", "LabSolutions", "prep"]
    
    for name in candidate_names:
        folder = repo_root / name
        if folder.exists() and folder.is_dir():
            roots.append(folder)
            
    # Also add the repo root itself as a fallback if needed, but usually these 3 cover it
    return roots

def sync_plugins():
    repo_root = Path(__file__).resolve().parent.parent
    
    sp_dir = get_sp_plugins_dir(repo_root)
    if not sp_dir:
        return
        
    folders = find_plugin_roots(repo_root)
    
    if not folders:
        print("No plugin root folders found (e.g. 'LabExercises', 'prep', etc).")
        return
        
    print("\nAvailable Roots to Sync From:\n")
    for i, folder in enumerate(folders):
        print(f"  [{i+1}] {folder.name}")
        
    print(f"\n  [0] CANCEL")
    
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
    
    # First, Clean the destination plugins folder to avoid conflicts
    print(f"\nClearing old files from Painter plugins folder: {sp_dir}")
    for item in sp_dir.iterdir():
        if item.is_file() and item.name.endswith(".py"):
            item.unlink()
            
    print(f"Syncing from: {source_dir.name}")
    print("-" * 40)
    
    count = 0
    # Recursively find all .py files in the chosen root
    for py_file in source_dir.rglob("*.py"):
        if py_file.is_file():
            shutil.copy2(py_file, sp_dir / py_file.name)
            print(f"  Copied: {py_file.name}")
            count += 1
            
    print("-" * 40)
    print(f"Success! {count} Python files synced.")
    print("In Substance Painter, go to: Python -> Reload Plugins Folder")

if __name__ == "__main__":
    sync_plugins()
