# Demo: One-Click Bake

**What we'll build:** A plugin with a single button that triggers a full bake of all texture sets.

## What you'll learn
- `substance_painter.baking` module — automating bake operations
- `baking.bake_async()` — triggers baking for a texture set
- Event-driven completion: listening for `BakingProcessEnded` to know when it's done
- Defensive UI: disabling the button during baking to prevent double-clicks (same pattern from the LiDAR downloader!)
