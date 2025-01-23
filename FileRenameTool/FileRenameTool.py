import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
import logging
import argparse

# 配置日志
logging.basicConfig(filename='rename_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 默认值设置
def_max_length=0
def_prefix=""

def rename_files(directory, max_length=def_max_length, prefix=def_prefix, match_prefix="", file_extensions=[]):
    # 检查指定的目录是否存在
    if not os.path.exists(directory):
        result_text.insert(tk.END, f"指定的目录 {directory} 不存在。\n")
        return
    # 使用 os.walk 递归遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 如果指定了文件后缀，检查当前文件后缀是否符合要求
            if file_extensions and not any(filename.endswith(ext) for ext in file_extensions):
                continue
            # 检查文件名是否以前缀开头
            if match_prefix and not filename.startswith(match_prefix):
                continue
            # 拼接文件的完整路径
            old_file_path = os.path.join(root, filename)
            # 获取文件名和扩展名
            name, ext = os.path.splitext(filename)
            # 如果文件名长度超过最大长度，进行截断
            if max_length and len(name) > max_length:
                name = name[:max_length]
            # 构建新的文件名
            new_filename = prefix + name + ext
            # 拼接新文件的完整路径
            new_file_path = os.path.join(root, new_filename)
            index = 1
            
            # 检查新文件名是否和原文件名相同
            if os.path.basename(new_file_path) == os.path.basename(old_file_path):
                continue
            # 检查新文件名是否已存在，如果存在则添加序号
            while os.path.exists(new_file_path):
                new_filename = f"{prefix}{name}_{index}{ext}"
                new_file_path = os.path.join(root, new_filename)
                index += 1
            
            try:
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                result_text.insert(tk.END, f"已将 {old_file_path} 重命名为 {new_file_path}\n")
            except Exception as e:
                result_text.insert(tk.END, f"重命名 {old_file_path} 时出错: {e}\n")
                # 记录错误日志
                logging.error(f"重命名 {old_file_path} 时出错: {e}")

def select_directory():
    # 打开文件夹选择对话框
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def start_rename():
    directory = directory_entry.get()
    try:
        max_length = int(max_length_entry.get())
    except ValueError:
        result_text.insert(tk.END, "请输入有效的最大文件名长度（整数）。\n")
        return
    # 获取用户输入的文件后缀
    file_extensions = file_extensions_entry.get().split(',')
    file_extensions = [ext.strip() for ext in file_extensions if ext.strip()]
    # 获取用户输入的匹配前缀
    match_prefix = match_prefix_entry.get()
    rename_files(directory, max_length, prefix=prefix_entry.get(), match_prefix=match_prefix, file_extensions=file_extensions)

def run_with_args():
    parser = argparse.ArgumentParser(description='文件重命名工具')
    parser.add_argument('directory', type=str, help='要重命名文件的目录')
    parser.add_argument('--max_length', type=int, default=def_max_length, help='最大文件名长度')
    parser.add_argument('--prefix', type=str, default=def_prefix, help='重命名前缀')
    parser.add_argument('--match_prefix', type=str, default="", help='匹配的文件名前缀')
    parser.add_argument('--file_extensions', type=str, default="", help='指定文件后缀，逗号分隔')
    args = parser.parse_args()
    file_extensions = args.file_extensions.split(',') if args.file_extensions else []
    file_extensions = [ext.strip() for ext in file_extensions if ext.strip()]
    # 创建一个假的结果文本框，用于日志显示
    global result_text
    result_text = scrolledtext.ScrolledText()
    rename_files(args.directory, args.max_length, args.prefix, args.match_prefix, file_extensions)



if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_with_args()
    else:
        # 创建主窗口
        root = tk.Tk()
        root.title("文件重命名工具")

        # 创建选择目录的按钮
        select_button = tk.Button(root, text="选择目录", command=select_directory)
        select_button.pack(pady=10)

        # 创建输入目录路径的文本框
        directory_entry = tk.Entry(root, width=50)
        directory_entry.pack(pady=5)

        # 创建输入最大文件名长度的标签和文本框
        max_length_label = tk.Label(root, text="最大文件名长度:")
        max_length_label.pack(pady=5)
        max_length_entry = tk.Entry(root, width=10)
#         max_length_entry.insert(0, str(def_max_length))
        max_length_entry.pack(pady=5)

        # 创建输入前缀的标签和文本框
        prefix_label = tk.Label(root, text="重命名前缀:")
        prefix_label.pack(pady=5)
        prefix_entry = tk.Entry(root, width=20)
        prefix_entry.insert(0, def_prefix)
        prefix_entry.pack(pady=5)

        # 创建输入匹配前缀的标签和文本框
        match_prefix_label = tk.Label(root, text="匹配的文件名前缀:")
        match_prefix_label.pack(pady=5)
        match_prefix_entry = tk.Entry(root, width=20)
        match_prefix_entry.pack(pady=5)

        # 创建输入文件后缀的标签和文本框
        file_extensions_label = tk.Label(root, text="指定文件后缀 (逗号分隔):")
        file_extensions_label.pack(pady=5)
        file_extensions_entry = tk.Entry(root, width=30)
        file_extensions_entry.pack(pady=5)

        # 创建开始重命名的按钮
        start_button = tk.Button(root, text="开始重命名", command=start_rename)
        start_button.pack(pady=20)

        # 创建显示结果的文本框
        result_text = scrolledtext.ScrolledText(root, width=80, height=10)
        result_text.pack(pady=10)

        # 运行主循环
        root.mainloop()