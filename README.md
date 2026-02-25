# Video Temporal Labeling Tool

A desktop application for temporal video data labeling. It records temporal labels for videos and stores the corresponding start and end frame indices.

![UI](./src/vtlt/resource/main.jpg)

## Requirements

- Python >= 3.9 (Python 3.12 recommended)
- wxPython >= 4.2.0
- pandas >= 2.0.0
- opencv-python >= 4.9.0
- numpy >= 1.24.0

## Installation

```bash
# Clone the repository
git clone https://github.com/jokebear-bot/VideoTemporalLabelingTool.git

# Navigate to the directory
cd VideoTemporalLabelingTool

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

## Usage

### Run as module
```bash
python -m vtlt
```

### Run directly
```bash
python src/vtlt/app.py
```

## Features

- 🎥 Video frame extraction and display
- 🏷️ Temporal labeling with start/end frame selection
- 📊 CSV export for annotations
- 🖥️ Cross-platform desktop GUI (Windows, macOS, Linux)
- ⌨️ **Keyboard shortcuts** for efficient navigation (see below)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `←` (Left Arrow) | Previous frame (-1) |
| `→` (Right Arrow) | Next frame (+1) |
| `Shift + ←` | Previous N frames (-FPI) |
| `Shift + →` | Next N frames (+FPI) |
| `S` | Select start frame |
| `E` | Select end frame |
| `Ctrl + S` | Save label |

## Project Structure

```
VideoTemporalLabelingTool/
├── src/vtlt/           # Main package
│   ├── __init__.py
│   ├── __main__.py     # Entry point
│   ├── app.py          # GUI application
│   ├── service.py      # Business logic
│   └── resource/       # Static resources
├── pyproject.toml      # Project configuration
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

## License

This project is licensed under the MIT License.
