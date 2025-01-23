### 文件重命名工具帮助文档

#### 工具概述
此工具的作用是按照给定规则对指定目录下的文件进行重命名。用户可指定最大文件名长度、重命名前缀、需匹配的文件名前缀以及文件后缀等规则。

#### 使用方法
该工具支持图形界面（GUI）和命令行参数两种使用方式。

##### 命令行使用方式
在命令行执行 Python 脚本时，可运用如下命令行参数：
```bash
python FileRenameTool.py <directory> [--max_length <max_length>] [--prefix <prefix>] [--match_prefix <match_prefix>] [--file_extensions <file_extensions>]
```

##### 参数表格
| 参数名 | 是否必选 | 描述 | 默认值 | 示例 |
| ---- | ---- | ---- | ---- | ---- |
| `<directory>` | 是 | 要重命名文件所在的目录路径 | 无 | `/path/to/directory` |
| `--max_length <max_length>` | 否 | 最大文件名长度。若文件名长度超出该值，会对文件名进行截断 | 0（不限制文件名长度） | `10` |
| `--prefix <prefix>` | 否 | 重命名时添加的前缀 | 空字符串（不添加前缀） | `new_` |
| `--match_prefix <match_prefix>` | 否 | 用于匹配文件名的前缀，仅文件名以此前缀开头的文件会被重命名 | 空字符串（不进行前缀匹配） | `old_` |
| `--file_extensions <file_extensions>` | 否 | 指定的文件后缀，多个后缀用逗号分隔，只有指定后缀的文件会被重命名 | 空字符串（不限制文件后缀） | `.txt,.jpg` |

##### 示例
- 重命名指定目录下所有文件，不限制文件名长度，不添加前缀：
```bash
python FileRenameTool.py /path/to/directory
```
- 重命名指定目录下所有 `.txt` 文件，最大文件名长度为 10，添加前缀 `new_`：
```bash
python FileRenameTool.py /path/to/directory --max_length 10 --prefix new_ --file_extensions .txt
```
- 重命名指定目录下所有以 `old_` 开头的文件，不限制文件名长度，不添加前缀：
```bash
python FileRenameTool.py /path/to/directory --match_prefix old_
```

##### 注意事项
- 在命令行使用工具时，若输入的参数格式有误，工具会给出错误提示。
- 重命名过程中若出现错误，错误信息会被记录在 `rename_errors.log` 文件里。 