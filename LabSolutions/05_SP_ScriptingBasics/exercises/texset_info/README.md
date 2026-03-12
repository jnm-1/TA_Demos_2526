# Exercise: Texture Set Info Panel

**Goal:** Build a dock widget that displays the current texture set's name, resolution, and number of channels.

## What you'll practice
- Reading project state with `substance_painter.textureset`
- Building a simple PySide6 UI inside Substance Painter
- Navigating the Python API documentation

## Requirements
- A dock widget with at least 3 labels showing: name, resolution, channels
- A "Refresh" button that updates the info
- **Bonus:** Auto-update when switching texture sets (look at `substance_painter.event`)

## Getting started
- Copy the structure from the hello world demo — you need `start_plugin()` and `close_plugin()`
- Check the docs: **Python > Documentation** inside Painter → find the `textureset` module
- To get the currently selected texture set: `ts.get_active_stack()` returns the active stack, then `.material()` gives you its `TextureSet`
