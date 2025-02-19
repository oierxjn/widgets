# File Renaming Tool

## Introduction
This is a powerful file renaming tool that supports both graphical user interface (GUI) and command - line usage modes. Users can set various renaming rules according to their needs, such as setting the maximum file name length, adding prefixes, matching specific prefixes or suffixes, matching specific characters, and deleting specific characters.

## Features
1. **Multiple Renaming Rules**: It supports setting multiple renaming rules, including the maximum file name length, adding prefixes, matching file name prefixes, matching file extensions, matching specific characters, and deleting specific characters.
2. **Recursive Processing**: It can recursively traverse the specified directory and its sub - directories to rename all files within them.
3. **Progress Display**: In GUI mode, a progress bar is provided to show the renaming progress, making it convenient for users to track the operation status.
4. **Error Logging**: Errors that occur during the renaming process are recorded in the `rename_errors.log` file, which helps users troubleshoot issues.
5. **Auto - Scroll**: In GUI mode, users can choose whether to enable the auto - scroll function for the result text box, making it easier to view the latest renaming information.

## Installation and Usage

### Installation
This tool is written in Python and does not require additional installation. Just make sure you have Python 3.x installed on your system.

### GUI Mode
Run the `FileRenameTool.py` file directly without any parameters, and the program will automatically open the graphical user interface:
```bash
python FileRenameTool.py
```
In the GUI interface, you can follow these steps:
1. **Select Directory**: Click the "Select Directory" button to choose the directory where the files to be renamed are located.
2. **Set Renaming Rules**: Enter the maximum file name length, renaming prefix, matching file name prefix, matching file extensions, matching characters for renaming files, and characters to be removed from file names in the corresponding input boxes. Separate multiple keywords with commas. If a keyword is empty, the corresponding rule will not be enabled.
3. **Auto - Scroll Setting**: Check the "Automatically scroll the text box to the bottom" checkbox. The result text box will automatically scroll to the bottom when new information is added.
4. **Start Renaming**: Click the "Start Renaming" button. The program will start renaming files according to the rules you set, and the current progress will be displayed in the progress bar.

### Command - Line Mode
Run the `FileRenameTool.py` file in the command line and pass the corresponding parameters:
```bash
python FileRenameTool.py <directory> [--max_length <max_length>] [--prefix <prefix>] [--match_prefix <match_prefix>] [--file_extensions <file_extensions>] [--match_chars <match_chars>] [--remove_chars <remove_chars>]
```

| Parameter | Required | Description | Default Value |
| --- | --- | --- | --- |
| `<directory>` | Yes | Specify the directory containing the files to be renamed | None |
| `--max_length` | No | Set the maximum file name length. Enter 0 to indicate no limit | 0 |
| `--prefix` | No | Set the renaming prefix, which will be added to the front of the file name | Empty string |
| `--match_prefix` | No | Specify the prefixes to match in file names. Separate multiple prefixes with commas. Only files with matching prefixes will be renamed | Empty string |
| `--file_extensions` | No | Specify the file extensions to match. Separate multiple extensions with commas. Only files with matching extensions will be renamed | Empty string |
| `--match_chars` | No | Specify the characters to match in file names. Separate multiple characters with commas. Only files containing these characters will be renamed | Empty string |
| `--remove_chars` | No | Specify the characters to be removed from file names. Separate multiple characters with commas | Empty string |

### Example
Here is an example of using the command - line mode to add the `new_` prefix to all files with the `.txt` extension in the `C:\test` directory and limit the file name length to 10:
```bash
python FileRenameTool.py C:\test --max_length 10 --prefix new_ --file_extensions .txt
```

## Notes
1. When using the command - line mode, make sure the input parameters are in the correct format; otherwise, the program may malfunction.
2. The renaming operation is irreversible. Please back up important files before the operation to avoid data loss.
3. If an error occurs during the renaming process, the program will record the error information in the `rename_errors.log` file. You can view this file to understand the specific error cause.

## Contribution
If you find any issues or have suggestions for improvement, please feel free to submit an Issue or a Pull Request.