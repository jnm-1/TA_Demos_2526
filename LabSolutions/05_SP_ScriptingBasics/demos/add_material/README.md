# Demo: Add Smart Material

**What we'll build:** A plugin with a text input and button that searches the shelf for a smart material and adds it to the current layer stack.

## What you'll learn
- `substance_painter.resource.search()` — finding assets in the shelf
- `substance_painter.layerstack.insert_smart_material()` — modifying the layer stack from code
- `ts.get_active_stack()` — getting the currently active texture set's stack
- Combining `QLineEdit` (text input) with a button for user interaction
- Input validation — checking for empty fields and open projects before acting
