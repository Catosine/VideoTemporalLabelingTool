# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-25

### Added
- Python 3.12 LTS compatibility
- Type hints throughout the codebase
- Modern project structure with `src/` layout
- `pyproject.toml` for modern Python packaging
- `.gitignore` with comprehensive rules
- Multi-language README support (English, Chinese, Japanese)
- Entry point `vtlt` command for easy execution
- Support for additional video formats (.mov, .mkv)
- Development dependencies (pytest, black, ruff, mypy)

### Changed
- Updated wxPython from 4.0.7.post2 to 4.2.0+
- Updated pandas from 0.25.3 to 2.0.0+
- Updated opencv-python from 4.2.0.32 to 4.9.0+
- Migrated from `.format()` to f-strings throughout
- Improved docstrings with Google style
- Refactored code to use `pathlib.Path` instead of `os.path`
- Renamed internal variables to snake_case for consistency
- Updated minimum Python version to 3.9

### Removed
- Support for Python < 3.9
- Deprecated `depricated` directory contents

### Fixed
- Proper handling of empty video lists
- Frame boundary checks to prevent overflow
- Resource path resolution for packaged installation
- Exception handling in main entry point

## [1.1.0] - 2020-07-13

### Added
- Initial release
- Basic video temporal labeling functionality
- wxPython GUI interface
- CSV export for labels
- Support for .avi, .mp4, .wav formats
- FPS selection menu (5, 10, 15, 20, 30)

[2.0.0]: https://github.com/jokebear-bot/VideoTemporalLabelingTool/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/jokebear-bot/VideoTemporalLabelingTool/releases/tag/v1.1.0
