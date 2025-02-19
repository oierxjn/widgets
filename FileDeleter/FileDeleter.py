import os
import argparse
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
import logging
import threading

# 定义警告信息
WARNING_MSG = "删除操作不可逆，请在使用前确保你要删除的文件是你真正需要删除的，以免造成数据丢失。"

# 功能标签的解释信息
LABEL_TOOLTIPS = {
    "文件前缀:": "输入文件的前缀，多个前缀用竖线 | 分隔，符合这些前缀的文件将参与筛选",
    "文件后缀:": "输入文件的后缀，多个后缀用竖线 | 分隔，符合这些后缀的文件将参与筛选",
    "匹配字符:": "输入文件内容中要匹配的字符，多个字符用竖线 | 分隔，文件内容包含这些字符的文件将参与筛选"
}


def count_files_to_delete(directory, prefixes, suffixes, contents):
    """
    统计需要删除的文件数量
    :param directory: 要搜索的目录
    :param prefixes: 匹配的文件前缀列表
    :param suffixes: 匹配的文件后缀列表
    :param contents: 匹配的文件内容关键字列表
    :return: 需要删除的文件数量
    """
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            should_delete = True
            if prefixes:
                should_delete = any(file.startswith(prefix) for prefix in prefixes) and should_delete
            if suffixes:
                should_delete = any(file.endswith(suffix) for suffix in suffixes) and should_delete
            if contents:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        should_delete = any(content in file_content for content in contents) and should_delete
                except Exception:
                    should_delete = False
            if should_delete:
                count += 1
    return count


def delete_files(directory, prefixes, suffixes, contents, output_text, progress_bar):
    """
    根据匹配规则删除文件
    :param directory: 要搜索的目录
    :param prefixes: 匹配的文件前缀列表
    :param suffixes: 匹配的文件后缀列表
    :param contents: 匹配的文件内容关键字列表
    :param output_text: 用于输出信息的文本框
    :param progress_bar: 进度条
    """
    if not os.path.exists(directory):
        error_msg = f"指定的目录 {directory} 不存在。"
        output_text.insert(tk.END, f"错误: {error_msg}\n")
        raise FileNotFoundError(error_msg)
    if not os.path.isdir(directory):
        error_msg = f"{directory} 不是一个有效的目录。"
        output_text.insert(tk.END, f"错误: {error_msg}\n")
        raise NotADirectoryError(error_msg)

    total_files = count_files_to_delete(directory, prefixes, suffixes, contents)
    deleted_files = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            should_delete = True
            if prefixes:
                should_delete = any(file.startswith(prefix) for prefix in prefixes) and should_delete
            if suffixes:
                should_delete = any(file.endswith(suffix) for suffix in suffixes) and should_delete
            if contents:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        should_delete = any(content in file_content for content in contents) and should_delete
                except Exception:
                    should_delete = False

            if should_delete:
                try:
                    os.remove(file_path)
                    output_text.insert(tk.END, f"Deleted: {file_path}\n")
                    deleted_files += 1
                    progress = (deleted_files / total_files) * 100
                    progress_bar['value'] = progress
                    output_text.update_idletasks()
                except PermissionError:
                    error_msg = f"没有权限删除文件 {file_path}。"
                    output_text.insert(tk.END, error_msg + "\n")
                    raise PermissionError(error_msg)
                except Exception as e:
                    error_msg = f"删除文件 {file_path} 时出现未知错误: {e}"
                    output_text.insert(tk.END, error_msg + "\n")
                    raise Exception(error_msg)


def arg_mode():
    """
    参数调用模式
    """
    print(WARNING_MSG)
    parser = argparse.ArgumentParser(description='根据不同规则删除文件')
    parser.add_argument('directory', help='要搜索的目录')
    parser.add_argument('--prefix', help='匹配的文件前缀，多个用竖线 | 分隔')
    parser.add_argument('--suffix', help='匹配的文件后缀，多个用竖线 | 分隔')
    parser.add_argument('--content', help='匹配文件中的字符，多个用竖线 | 分隔')
    args = parser.parse_args()

    # 模拟文本框和进度条输出
    class MockOutput:
        def insert(self, _, text):
            print(text.strip())

    class MockProgressBar:
        def __init__(self):
            self.value = 0

        def __setitem__(self, key, value):
            if key == 'value':
                self.value = value
                # 使用 ANSI 转义序列覆盖之前的输出
                print(f"\rProgress: {self.value:.2f}%", end='', flush=True)

    prefixes = [prefix.strip() for prefix in (args.prefix or "").split('|') if prefix.strip()]
    suffixes = [suffix.strip() for suffix in (args.suffix or "").split('|') if suffix.strip()]
    contents = [content.strip() for content in (args.content or "").split('|') if content.strip()]

    if not prefixes and not suffixes and not contents:
        print("未指定任何匹配规则，请使用 --prefix、--suffix 或 --content 参数指定匹配规则。")
        return

    try:
        delete_files(args.directory, prefixes, suffixes, contents, MockOutput(), MockProgressBar())
        print()  # 换行，避免下一次输出与进度条重叠
    except (FileNotFoundError, NotADirectoryError, PermissionError, Exception) as e:
        # 配置日志记录
        logging.basicConfig(filename='error.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(str(e))
        print(f"错误: {e}")


def gui_mode():
    """
    GUI 工作模式
    """

    def select_directory():
        directory = filedialog.askdirectory()
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

    def execute_deletion():
        directory = directory_entry.get()
        prefixes = [prefix.strip() for prefix in (prefix_entry.get() or "").split('|') if prefix.strip()]
        suffixes = [suffix.strip() for suffix in (suffix_entry.get() or "").split('|') if suffix.strip()]
        contents = [content.strip() for content in (content_entry.get() or "").split('|') if content.strip()]

        if not prefixes and not suffixes and not contents:
            messagebox.showwarning("警告", "未指定任何匹配规则，请在输入框中输入匹配关键字。")
            return

        def deletion_thread():
            try:
                progress_bar['value'] = 0
                delete_files(directory, prefixes, suffixes, contents, output_text, progress_bar)
                output_text.insert(tk.END, "文件删除操作已完成。\n")
                if auto_scroll_var.get():
                    output_text.see(tk.END)
            except (FileNotFoundError, NotADirectoryError, PermissionError, Exception) as e:
                # 配置日志记录
                logging.basicConfig(filename='error.log', level=logging.ERROR,
                                    format='%(asctime)s - %(levelname)s - %(message)s')
                logging.error(str(e))
                output_text.insert(tk.END, f"错误: {e}\n")
                if auto_scroll_var.get():
                    output_text.see(tk.END)

        thread = threading.Thread(target=deletion_thread)
        thread.start()

    def show_tooltip(event):
        widget = event.widget
        text = widget.cget("text")
        if text in LABEL_TOOLTIPS:
            tooltip = tk.Toplevel(root)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 20}+{event.y_root + 20}")
            label = tk.Label(tooltip, text=LABEL_TOOLTIPS[text], background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
            widget.tooltip = tooltip

    def hide_tooltip(event):
        widget = event.widget
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            del widget.tooltip

    root = tk.Tk()
    root.title("文件删除工具")

    # 提示信息
    warning_label = tk.Label(root, text=WARNING_MSG, fg="red")
    warning_label.pack()

    # 目录选择
    directory_label = tk.Label(root, text="选择目录:")
    directory_label.pack()
    directory_entry = tk.Entry(root, width=50)
    directory_entry.pack()
    select_button = tk.Button(root, text="选择目录", command=select_directory)
    select_button.pack()

    # 修改此处的提示文本
    hint_label = tk.Label(root, text="多个关键字请用竖线 | 分隔。关键字为空时不启用对应规则")
    hint_label.pack()

    # 匹配文件前缀
    prefix_frame = tk.Frame(root)
    prefix_frame.pack()
    prefix_label = tk.Label(prefix_frame, text="文件前缀:")
    prefix_label.pack(side=tk.LEFT)
    prefix_label.bind("<Enter>", show_tooltip)
    prefix_label.bind("<Leave>", hide_tooltip)
    prefix_entry = tk.Entry(prefix_frame, width=30)
    prefix_entry.pack(side=tk.LEFT)

    # 匹配文件后缀
    suffix_frame = tk.Frame(root)
    suffix_frame.pack()
    suffix_label = tk.Label(suffix_frame, text="文件后缀:")
    suffix_label.pack(side=tk.LEFT)
    suffix_label.bind("<Enter>", show_tooltip)
    suffix_label.bind("<Leave>", hide_tooltip)
    suffix_entry = tk.Entry(suffix_frame, width=30)
    suffix_entry.pack(side=tk.LEFT)

    # 匹配文件中的字符
    content_frame = tk.Frame(root)
    content_frame.pack()
    content_label = tk.Label(content_frame, text="匹配字符:")
    content_label.pack(side=tk.LEFT)
    content_label.bind("<Enter>", show_tooltip)
    content_label.bind("<Leave>", hide_tooltip)
    content_entry = tk.Entry(content_frame, width=30)
    content_entry.pack(side=tk.LEFT)

    # 自动滚动复选框
    auto_scroll_var = tk.IntVar(value=1)  # 默认勾选
    auto_scroll_checkbox = tk.Checkbutton(root, text="文本框自动滚动", variable=auto_scroll_var)
    auto_scroll_checkbox.pack()

    # 删除按钮
    delete_button = tk.Button(root, text="删除文件", command=execute_deletion)
    delete_button.pack()

    # 进度条
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack()

    # 输出文本框
    output_text = scrolledtext.ScrolledText(root, width=60, height=10)
    output_text.pack()

    root.mainloop()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        arg_mode()
    else:
        gui_mode()
