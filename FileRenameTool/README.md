# File Renaming Tool

## Overview
This tool is designed to rename files in a specified directory according to certain rules. You can specify the maximum file name length, the prefix for renaming, the prefix for matching file names, and file extensions to filter files.

## Usage

### 1. Command - Line Mode
You can use the following command - line arguments when running the Python script:
```bash
python FileRenameTool.py <directory> [--max_length <max_length>] [--prefix <prefix>] [--match_prefix <match_prefix>] [--file_extensions <file_extensions>]
```

### Parameter Table
| Parameter Name | Required | Description | Default Value | Example |
| ---- | ---- | ---- | ---- | ---- |
| `<directory>` | Yes | The path of the directory where the files to be renamed are located. | None | `/path/to/directory` |
| `--max_length <max_length>` | No | The maximum length of the file name. If the file name length exceeds this value, the file name will be truncated. | 0 (No limit on file name length) | `10` |
| `--prefix <prefix>` | No | The prefix to be added during file renaming. | Empty string (No prefix added) | `new_` |
| `--match_prefix <match_prefix>` | No | The prefix used to match file names. Only files whose names start with this prefix will be renamed. | Empty string (No prefix matching) | `old_` |
| `--file_extensions <file_extensions>` | No | Specified file extensions, separated by commas. Only files with the specified extensions will be renamed. | Empty string (No limit on file extensions) | `.txt,.jpg` |

### Examples
- Rename all files in the specified directory without limiting the file name length and without adding a prefix:
```bash
python FileRenameTool.py /path/to/directory
```
- Rename all `.txt` files in the specified directory, with a maximum file name length of 10 and adding the prefix `new_`:
```bash
python FileRenameTool.py /path/to/directory --max_length 10 --prefix new_ --file_extensions .txt
```
- Rename all files starting with `old_` in the specified directory, without limiting the file name length and without adding a prefix:
```bash
python FileRenameTool.py /path/to/directory --match_prefix old_
```

### Notes
- If you enter incorrect parameter formats when using the tool in command - line mode, the tool will prompt an error message.
- If an error occurs during the renaming process, the error information will be recorded in the `rename_errors.log` file.

### 2. GUI Mode
If you do not provide any command - line arguments, the tool will start in GUI mode. You can interact with the graphical interface to select the directory, set parameters, and start the renaming process. 