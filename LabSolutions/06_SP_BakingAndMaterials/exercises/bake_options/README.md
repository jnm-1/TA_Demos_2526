# Exercise: Bake with HP/LP Setup

**Goal:** Extend the bake demo to let the user configure the high-poly mesh and baking options before baking.

## What you'll practice
- Using `QComboBox` for dropdown selection
- Using `QCheckBox` for toggle options
- Working with `BakingParameters` to configure baking settings
- Using `QFileDialog` to browse for a file
- Combining UI input with baking operations

## Requirements
1. A **file picker** (button + label) to select the high-poly mesh file (`.fbx`, `.obj`, etc.)
2. A **checkbox** to toggle "Use Low Poly as High Poly" (skips the HP file entirely — useful for AO-only bakes)
3. A **resolution dropdown** with options: 512, 1024, 2048, 4096 (secondary feature)
4. A **bake button** that:
   - Sets the high-poly mesh path on the baking parameters
   - OR sets "use low as high" if checked
   - Respects the selected resolution
   - Disables during baking (defensive UI!)
5. A **status label** that updates when baking completes

## Getting started
- `BakingParameters.from_texture_set(texture_set)` → gets the baking params for a texture set
- `.common()` → returns a dict of common parameter Properties (keys like `'HipolyMesh'`, `'OutputSize'`, `'UseLowPolyAsHighPoly'`)
- `BakingParameters.set({...})` → sets parameters in batch
- `QFileDialog.getOpenFileName()` → opens a file browser, returns a tuple `(path, filter)`
- `QCheckBox` → use `.isChecked()` to read the toggle state
- Use `QUrl.fromLocalFile(path).toString()` to format file paths for the baking API
- Print `common.keys()` in the Python console to discover all available parameter names!
