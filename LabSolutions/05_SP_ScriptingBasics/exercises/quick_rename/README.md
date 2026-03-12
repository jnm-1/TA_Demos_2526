# Exercise: Quick Rename

**Goal:** Build a dock widget that adds a user-defined prefix to all layer names in the current stack.

## What you'll practice
- Using `substance_painter.layerstack` to iterate and modify layers
- Combining a `QLineEdit` input with a button action
- Finding the right API functions by reading the documentation

## Requirements
- A text field for the prefix (e.g. `arm_`)
- A button that renames all layers by prepending the prefix
- Don't double-prefix layers that already have it
- Show a status message with how many layers were renamed

## Getting started
- Start from the hello world demo structure
- You'll need: `ts.get_active_stack()` to get the current stack
- Check the `layerstack` docs for functions to list layers and get/set names
