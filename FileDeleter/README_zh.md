# 文件删除工具使用说明
[英文(English)](https://github.com/oierxjn/widgets/blob/main/FileDeleter/README.md)
## 一、工具简介
文件删除工具是一款实用的Python程序，它支持通过命令行参数和图形用户界面（GUI）两种方式运行，帮助用户根据特定规则删除指定目录下的文件。用户可以依据文件的前缀、后缀以及文件内容中的字符来筛选文件，且只有同时满足所有选定规则的文件才会被删除。

## 二、功能特性
- **多规则匹配**：支持根据文件前缀、后缀和文件内容中的字符进行匹配，多个规则同时生效，只有同时满足所有规则的文件才会被删除。
- **多关键字支持**：每个匹配规则都允许输入多个关键字，关键字之间使用竖线 `|` 分隔。
- **进度显示**：在删除文件过程中，会通过进度条实时展示操作进度，让用户了解操作的完成情况。
- **错误日志记录**：所有操作过程中出现的错误信息都会被记录到 `error.log` 文件中，方便后续问题排查。
- **双操作模式**：提供命令行和GUI两种操作模式，用户可根据自身需求灵活选择。

## 三、安装与运行
### 安装
确保你的系统已经安装了Python环境（建议使用Python 3.6及以上版本）。本工具仅依赖Python标准库，无需额外安装其他依赖。

### 运行
将脚本保存为一个 `.py` 文件（例如 `file_deleter.py`），然后根据需求选择以下方式运行：
#### 命令行模式
在命令行中输入以下命令：
```bash
python file_deleter.py [目录路径] [可选参数]
```
例如：
```bash
python file_deleter.py /path/to/directory --prefix abc|def --suffix.txt|.log --content hello|world
```
#### GUI 模式
直接运行脚本，不提供任何命令行参数：
```bash
python file_deleter.py
```
脚本会弹出一个图形用户界面，用户可以通过该界面进行操作。

## 四、命令行参数说明
| 参数 | 说明 | 示例 |
| ---- | ---- | ---- |
| `[目录路径]` | 必需参数，指定要搜索的目录。 | `/path/to/directory` |
| `--prefix` | 可选参数，指定要匹配的文件前缀，多个前缀用竖线 `|` 分隔。 | `--prefix abc|def` |
| `--suffix` | 可选参数，指定要匹配的文件后缀，多个后缀用竖线 `|` 分隔。 | `--suffix.txt|.log` |
| `--content` | 可选参数，指定要匹配的文件内容中的字符，多个字符用竖线 `|` 分隔。 | `--content hello|world` |

## 五、GUI 界面操作说明
1. **选择目录**：点击“选择目录”按钮，会弹出一个文件选择对话框，用户可以在其中选择要搜索的目录。选择完成后，目录路径会显示在输入框中。
2. **输入匹配关键字**：
   - **文件前缀**：在“文件前缀”输入框中输入要匹配的文件前缀，多个前缀用竖线 `|` 分隔。若输入为空，则不启用文件前缀匹配规则。
   - **文件后缀**：在“文件后缀”输入框中输入要匹配的文件后缀，多个后缀用竖线 `|` 分隔。若输入为空，则不启用文件后缀匹配规则。
   - **匹配字符**：在“匹配字符”输入框中输入要匹配的文件内容中的字符，多个字符用竖线 `|` 分隔。若输入为空，则不启用文件内容匹配规则。
3. **提示信息**：界面上方会显示“删除操作不可逆，请在使用前确保你要删除的文件是你真正需要删除的，以免造成数据丢失。”的警告信息，提醒用户谨慎操作。在输入框区域上方，有“多个关键字请用竖线 | 分隔。关键字为空时不启用对应规则”的提示，指导用户正确输入关键字。
4. **执行删除操作**：点击“删除文件”按钮，脚本会根据用户输入的匹配规则，在指定目录下搜索并删除同时满足所有规则的文件。删除过程中，进度条会实时显示操作进度，操作完成后，会在下方的文本框中显示相应的信息。

## 六、注意事项
1. **数据安全**：删除操作不可逆，请在使用前仔细确认要删除的文件，以免造成数据丢失。
2. **文件编码**：在匹配文件内容时，脚本假设文件是以UTF - 8编码保存的。如果文件使用其他编码，可能会导致匹配失败或出现错误。
3. **权限问题**：确保你有足够的权限删除指定目录下的文件。如果没有权限，会在输出信息中显示相应的错误提示，并记录到 `error.log` 文件中。

## 七、错误处理与日志记录
### 错误处理
脚本在执行过程中会对各种可能出现的错误进行处理，例如指定的目录不存在、不是有效的目录、没有权限删除文件等。遇到错误时，会在命令行或GUI界面的输出文本框中显示相应的错误信息。

### 日志记录
所有错误信息都会记录到 `error.log` 文件中，日志文件的格式为 `%(asctime)s - %(levelname)s - %(message)s`，方便用户后续查看和分析问题。 
