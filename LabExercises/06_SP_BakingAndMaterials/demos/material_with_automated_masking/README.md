# Demo: Material with Automated Masking

**What we'll build:** A plugin that applies a Smart Material and then adds a Smart Mask to it — showing the full pattern of material + mask automation via Python.

## What you'll learn
- `layer.add_mask()` — adding a mask slot to a layer programmatically
- `insert_smart_mask()` — inserting a Smart Mask into the mask stack
- `InsertPosition.inside_node()` with `NodeStack.Mask` — targeting the mask stack
- The pattern: insert material → add mask → insert mask effect
