# FileDeleter - File Deletion Tool

## 1. Introduction
FileDeleter is a practical Python program that provides two operation modes: command - line arguments and Graphical User Interface (GUI). It helps users delete files in a specified directory according to specific rules. Users can filter files based on file prefixes, suffixes, and characters within the file content. Only files that meet all selected rules simultaneously will be deleted.

## 2. Features
- **Multi - rule Matching**: Supports matching based on file prefixes, suffixes, and characters in the file content. Multiple rules work simultaneously, and only files that meet all rules will be deleted.
 - **Multi - keyword Support**: Each matching rule allows the input of multiple keywords, separated by the vertical bar `|`.
 - **Progress Display**: During the file deletion process, a progress bar will be used to display the operation progress in real - time, allowing users to understand the completion status of the operation.
 - **Error Logging**: All error messages that occur during the operation are recorded in the `error.log` file, which is convenient for subsequent problem - solving.
 - **Dual - mode Operation**: Provides both command - line and GUI operation modes, allowing users to choose flexibly according to their needs.

## 3. Installation and Running
### Installation
Ensure that you have installed a Python environment (Python 3.6 or above is recommended). This tool only depends on the Python standard library and does not require the installation of additional dependencies.

### Running
Save the script as a `.py` file (for example, `FileDeleter.py`), and then choose the following ways to run it according to your needs:
#### Command - line Mode
Enter the following command in the command line:
```bash
python FileDeleter.py [Directory Path] [Optional Parameters]
```
For example:
```bash
python FileDeleter.py /path/to/directory --prefix abc|def --suffix.txt|.log --content hello|world
```
#### GUI Mode
Run the script directly without providing any command - line parameters:
```bash
python FileDeleter.py
```
The script will pop up a graphical user interface, and users can operate through this interface.

## 4. Command - line Parameter Explanation
| Parameter | Explanation | Example |
| ---- | ---- | ---- |
| `[Directory Path]` | Required parameter, specifying the directory to be searched. | `/path/to/directory` |
| `--prefix` | Optional parameter, specifying the file prefixes to match. Multiple prefixes are separated by the vertical bar `|`. | `--prefix abc|def` |
| `--suffix` | Optional parameter, specifying the file suffixes to match. Multiple suffixes are separated by the vertical bar `|`. | `--suffix.txt|.log` |
| `--content` | Optional parameter, specifying the characters in the file content to match. Multiple characters are separated by the vertical bar `|`. | `--content hello|world` |

## 5. GUI Interface Operation Instructions
1. **Select Directory**: Click the "Select Directory" button, and a file selection dialog box will pop up. Users can select the directory to be searched in it. After the selection is completed, the directory path will be displayed in the input box.
2. **Enter Matching Keywords**:
   - **File Prefix**: Enter the file prefixes to match in the "File Prefix" input box. Multiple prefixes are separated by the vertical bar `|`. If the input is empty, the file prefix matching rule will not be enabled.
   - **File Suffix**: Enter the file suffixes to match in the "File Suffix" input box. Multiple suffixes are separated by the vertical bar `|`. If the input is empty, the file suffix matching rule will not be enabled.
   - **Matching Characters**: Enter the characters in the file content to match in the "Matching Characters" input box. Multiple characters are separated by the vertical bar `|`. If the input is empty, the file content matching rule will not be enabled.
3. **Prompt Information**: A warning message "The deletion operation is irreversible. Please ensure that the files you want to delete are truly the ones you need to delete before using it to avoid data loss." will be displayed at the top of the interface to remind users to operate with caution. Above the input box area, there is a prompt "Multiple keywords should be separated by the vertical bar `|`. When the keyword is empty, the corresponding rule will not be enabled." to guide users to enter keywords correctly.
4. **Execute Deletion Operation**: Click the "Delete Files" button. The script will search and delete files that meet all the rules simultaneously in the specified directory according to the matching rules entered by the user. During the deletion process, the progress bar will display the operation progress in real - time. After the operation is completed, corresponding information will be displayed in the text box below.

## 6. Precautions
1. **Data Security**: The deletion operation is irreversible. Please carefully confirm the files to be deleted before using it to avoid data loss.
2. **File Encoding**: When matching file content, the script assumes that the file is saved in UTF - 8 encoding. If the file uses other encodings, it may cause matching failures or errors.
3. **Permission Issues**: Ensure that you have sufficient permissions to delete files in the specified directory. If you do not have permissions, corresponding error prompts will be displayed in the output information and recorded in the `error.log` file.

## 7. Error Handling and Logging
### Error Handling
The script will handle various possible errors during execution, such as the specified directory does not exist, is not a valid directory, or there is no permission to delete files. When an error occurs, corresponding error messages will be displayed in the command line or the output text box of the GUI interface.

### Logging
All error messages are recorded in the `error.log` file. The format of the log file is `%(asctime)s - %(levelname)s - %(message)s`, which is convenient for users to view and analyze problems later. 