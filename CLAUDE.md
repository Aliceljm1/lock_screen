# CLAUDE: Xiong Xiong Lock Screen Challenge

## Project Overview

A single-file Python/tkinter application that displays a fake virus lock screen. 
Children learn Windows keyboard shortcuts by figuring out how to close it.

## Tech Stack

- Python 3 (any version with tkinter)
- tkinter (built-in GUI library, no external dependencies)
- argparse (built-in CLI argument parser)

## Directory Structure

```
lock_screen/
├── lock_screen.py      # Main application (single file, all logic here)
├── start_easy.bat      # Launcher: easy mode
├── start_medium.bat    # Launcher: medium mode
├── start_hard.bat      # Launcher: hard mode
├── requirements.txt    # Dependencies (none - stdlib only)
├── .gitignore
├── README.md
└── CLAUDE.md           # This file
```

## Core Module: lock_screen.py

- Entry point: `main()` function at bottom
- Single class: `LockScreen` handles everything
- Key sections (marked with comment headers):
  - **Window Setup**: `_setup_easy/medium/hard()` - configure window per difficulty
  - **UI Construction**: `_create_ui()` - build the virus-themed interface
  - **Key Bindings**: `_bind_keys()` - F1 for hints, Escape, secret combos
  - **Hint Dialog**: `_show_hints()` - Toplevel window with shortcut list
  - **Close Handlers**: `_on_close()`, `_on_hard_close_attempt()`, `_secret_exit()`
  - **Congratulations**: `_show_congratulations()` - transforms UI to victory screen
  - **Animations**: 5 animation loops (warning blink, challenge pulse, progress bar, hex code, F1 hint blink)

## Data Flow

```
main() -> argparse -> LockScreen(level) -> _setup_window() -> _create_ui() -> _bind_keys() -> _start_animations() -> mainloop()
                                                                                    |
                                                                              F1 -> _show_hints()
                                                                              close -> _show_congratulations()
```

## Difficulty Levels

| Level | Window Mode | Alt+F4 | Topmost | Secret Exit |
|-------|------------|--------|---------|-------------|
| easy | Windowed 900x700 | Works | No | N/A |
| medium | Fullscreen | Works | No | N/A |
| hard | Fullscreen | Blocked | Yes | Ctrl+Shift+Q |

## Common Modification Scenarios

| I want to... | Modify... |
|-------------|-----------|
| Change challenge text | `_create_ui()` -> `challenge_label` text |
| Add/remove hint items | `_show_hints()` -> `hints` list |
| Change visual colors | Class constants at top (`RED`, `DARK_BG`, etc.) |
| Add new difficulty level | Add `_setup_xxx()`, update argparse choices |
| Change animation speed | `self.root.after(ms, ...)` values in `_animate_*()` |
| Add new fake status messages | `FAKE_STATUSES` list |
| Change congratulations message | `_show_congratulations()` method |
| Add sound effects | Import `winsound`, call in relevant methods |

## Launch Commands

```bash
# Development
python lock_screen.py --level easy

# Via batch files (double-click)
start_easy.bat / start_medium.bat / start_hard.bat
```
