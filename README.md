# Xiong Xiong Lock Screen Challenge

A fun fake "virus" lock screen for Windows that teaches children how to use keyboard shortcuts and system operations.

## Features

- Full-screen "virus" interface with scary red theme, blinking warnings, fake progress bar
- Press **F1** for hints on how to "crack" the virus
- Three difficulty levels: Easy / Medium / Hard
- Congratulations screen when successfully closed

## Quick Start

Make sure Python 3 is installed, then double-click one of the batch files:

| File | Difficulty | Description |
|------|-----------|-------------|
| `start_easy.bat` | Easy | Windowed mode, close button visible |
| `start_medium.bat` | Medium | Fullscreen, Alt+F4 and Win+D work |
| `start_hard.bat` | Hard | Fullscreen + topmost, most close methods blocked |

Or run from command line:

```bash
python lock_screen.py --level easy
python lock_screen.py --level medium
python lock_screen.py --level hard
```

## How to "Crack" It

Press **F1** in-game for hints. Methods include:

1. `Alt + F4` - Close window
2. `Win + D` - Show desktop
3. `Alt + Tab` - Switch to another window
4. `Ctrl + Alt + Del` - Open security options
5. `Ctrl + Shift + Esc` - Open Task Manager directly
6. `Win` key - Open Start menu

Hard mode secret exit: `Ctrl + Shift + Q`
