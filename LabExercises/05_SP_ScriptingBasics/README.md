# 05 - Substance Painter: Scripting Basics

## Setup: Syncing Your Code to Substance Painter

Substance Painter only loads plugins from its own folder. To easily test your code inside PyCharm while Painter runs it, we use a synchronization script.

### Step 1: Run the Sync Script
1. Open a terminal in PyCharm (or regular command prompt).
2. Run the helper script located in the repository root:
   ```bash
   python helpers/sync_sp_plugins.py
   ```
3. Type the number corresponding to the `LabExercises` folder.
4. *First time only:* If the script cannot automatically find your Substance Painter folder, it will ask you to paste the path to it. It saves this path so you only have to do it once.

### Step 2: Reload Plugins
1. Open Substance Painter.
2. Go to **Python → Reload Plugins Folder**.
3. Your plugins will now appear in the menu.

**Tip:** Every time you write new code or make changes, just run the sync script again and click Reload Plugins.

### How it works
The `SUBSTANCE_PAINTER_PLUGINS_PATH` environment variable tells Painter to search an additional folder for plugins. You edit in PyCharm, Painter sees the changes after a reload.

