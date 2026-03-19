# Exercise: Color ID Masking

**Goal:** Build a plugin that applies a Smart Material, but masks it using a **Color Selection** effect so it only appears where a specific color is painted in the baked ID map.

## What you'll practice
- Adding a mask to a layer (`add_mask`)
- Inserting a **Color Selection** effect into the mask stack
- Setting the target color via `get_parameters()` / `set_parameters()`
- Reading the Substance Painter Python API docs independently

## Requirements
- A `QComboBox` to pick a Smart Material (e.g. Iron Raw, Leather, Wood Pine)
- A `QComboBox` to pick a target color: Red, Green, or Blue
- A button that:
  1. Inserts the selected Smart Material
  2. Adds a **black** mask to it (why black and not white?)
  3. Inserts a Color Selection effect into the mask
  4. Configures it to match the selected color

## Hints
- You already know `insert_smart_material`, `add_mask`, and `InsertPosition.inside_node` from the demo
- Search the docs for a function that inserts a "color selection" effect
- The effect has `get_parameters()` and `set_parameters()` methods
- Look at the `colors` field — it takes a list of `Color` objects
- Check `substance_painter.colormanagement` for how to create a `Color`

