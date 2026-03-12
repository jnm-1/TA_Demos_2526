# Demo: Hello World Plugin

**What we'll build:** A minimal Substance Painter plugin — one button that logs a message.

## What you'll learn
- The plugin lifecycle: `start_plugin()` and `close_plugin()`
- Why you don't need `QApplication` or `if __name__ == "__main__"` inside a host app
- `substance_painter.ui.add_dock_widget()` — registering UI with Painter
- `substance_painter.logging` — printing to Painter's log
- `button.clicked.connect()` — same signal/slot pattern as the standalone Python app
