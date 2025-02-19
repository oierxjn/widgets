import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import ttk

import logging
import argparse
import threading

# 默认值设置
def_max_length = 0
def_prefix = ""

# 日志配置函数，在出现错误时调用
def configure_logging():
    logging.basicConfig(filename='rename_errors.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def collect_all_files(directory):
    all_files = []
    if not os.path.exists(directory):
        result_text.insert(tk.END, f"指定的目录 {directory} 不存在。\n")
        return all_files
    # 获取当前目录下的所有文件和子目录，并按名称排序
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            all_files.append(item_path)
    return all_files


def rename_files(all_files, max_length=def_max_length, prefix=def_prefix, match_prefix="", file_extensions=[],
                 match_chars="", remove_chars="", progress_callback=None):
    total_files = len(all_files)
    processed_files = 0
    for file_path in all_files:
        result_text.insert(tk.END, f"正在重命名第 {processed_files + 1} 个文件，共 {total_files} 个文件\n")
        filename = os.path.basename(file_path)
        # 匹配文件规则
        if file_extensions and not any(filename.endswith(ext) for ext in file_extensions):
            continue
        if match_prefix and not any(filename.startswith(p) for p in match_prefix.split(',')):
            continue
        if match_chars and not any(char in filename for char in match_chars.split(',')):
            continue

        name, ext = os.path.splitext(filename)
        # 最大文件名长度限制
        if max_length and len(name) > max_length:
            name = name[:max_length]

        # 重命名删除字符规则
        if remove_chars:
            for char in remove_chars.split(','):
                name = name.replace(char, "")

        new_filename = prefix + name + ext
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
        index = 1
        if os.path.basename(new_file_path) == os.path.basename(file_path):
            continue
        while os.path.exists(new_file_path):
            new_filename = f"{prefix}{name}_{index}{ext}"
            new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
            index += 1
        try:
            os.rename(file_path, new_file_path)
            result_text.insert(tk.END, f"已将 {file_path} 重命名为 {new_file_path}\n")
            if auto_scroll_var.get():
                result_text.see(tk.END)
        except Exception as e:
            # 出现错误时配置日志记录
            configure_logging()
            result_text.insert(tk.END, f"重命名 {file_path} 时出错: {e}\n")
            logging.error(f"重命名 {file_path} 时出错: {e}")
            if auto_scroll_var.get():
                result_text.see(tk.END)
        processed_files += 1
        if progress_callback:
            progress_callback(processed_files / total_files * 100)

    result_text.insert(tk.END, "完成重命名。\n")
    if auto_scroll_var.get():
        result_text.see(tk.END)
    messagebox.showinfo("提示", "重命名已完成！")


def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        if not os.path.exists(directory):
            result_text.insert(tk.END, f"选择的目录 {directory} 不存在，请重新选择。\n")
            return
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)


def start_rename(root):
    directory = directory_entry.get()
    if not os.path.exists(directory):
        result_text.insert(tk.END, f"指定的目录 {directory} 不存在，请检查输入。\n")
        return
    max_length_str = max_length_entry.get()
    if max_length_str and not max_length_str.isdigit():
        result_text.insert(tk.END, "最大文件名长度必须为整数，请重新输入。\n")
        return
    max_length = int(max_length_str) if max_length_str.isdigit() else 0
    file_extensions = file_extensions_entry.get().split(',')
    file_extensions = [ext.strip() for ext in file_extensions if ext.strip()]
    match_prefix = match_prefix_entry.get()
    match_chars = match_chars_entry.get()
    remove_chars = remove_chars_entry.get()

    def update_progress(progress):
        progress_bar['value'] = progress
        root.update_idletasks()

    def rename_thread():
        all_files = collect_all_files(directory)
        rename_files(all_files, max_length, prefix=prefix_entry.get(), match_prefix=match_prefix,
                     file_extensions=file_extensions, match_chars=match_chars,
                     remove_chars=remove_chars, progress_callback=update_progress)

    thread = threading.Thread(target=rename_thread)
    thread.start()


class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


def create_gui():
    global directory_entry, max_length_entry, prefix_entry, match_prefix_entry, file_extensions_entry, match_chars_entry
    global result_text, progress_bar, remove_chars_entry, auto_scroll_var
    root = tk.Tk()
    root.title("文件重命名工具")

    # 使用框架来布局描述和输入框
    frame = tk.Frame(root)
    frame.pack(pady=5)

    # 目录路径标签
    directory_label = tk.Label(frame, text="目录路径:")
    directory_label.grid(row=0, column=0, padx=5, pady=2)
    ToolTip(directory_label, "选择要重命名文件所在的目录")
    # 目录路径输入框
    directory_entry = tk.Entry(frame, width=60)
    directory_entry.grid(row=0, column=1, padx=5, pady=2, columnspan=2)

    # 选择目录按钮
    select_button = tk.Button(frame, text="选择目录", command=select_directory)
    select_button.grid(row=0, column=3, padx=5, pady=2)

    # 最大文件名长度部分
    max_length_label = tk.Label(frame, text="最大文件名长度:")
    max_length_label.grid(row=1, column=0, padx=5, pady=2)
    ToolTip(max_length_label, "设置文件名的最大长度，超出部分将被截断，输入 0 表示不限制")
    max_length_entry = tk.Entry(frame, width=10)
    max_length_entry.grid(row=1, column=1, padx=5, pady=2)

    # 重命名前缀部分
    prefix_label = tk.Label(frame, text="重命名前缀:")
    prefix_label.grid(row=2, column=0, padx=5, pady=2)
    ToolTip(prefix_label, "输入要添加到文件名前面的前缀内容")
    prefix_entry = tk.Entry(frame, width=60)
    prefix_entry.insert(0, def_prefix)
    prefix_entry.grid(row=2, column=1, padx=5, pady=2, columnspan=3)

    # 重命名删除字符部分
    remove_chars_label = tk.Label(frame, text="重命名删除字符:")
    remove_chars_label.grid(row=3, column=0, padx=5, pady=2)
    ToolTip(remove_chars_label, "输入要从文件名中删除的字符，多个字符用逗号分隔")
    remove_chars_entry = tk.Entry(frame, width=60)
    remove_chars_entry.grid(row=3, column=1, padx=5, pady=2, columnspan=3)

    # 匹配的文件名前缀部分
    match_prefix_label = tk.Label(frame, text="匹配的文件名前缀:")
    match_prefix_label.grid(row=4, column=0, padx=5, pady=2)
    ToolTip(match_prefix_label, "输入要匹配的文件名前缀，多个前缀用逗号分隔，只有匹配的文件才会被重命名")
    match_prefix_entry = tk.Entry(frame, width=60)
    match_prefix_entry.grid(row=4, column=1, padx=5, pady=2, columnspan=3)

    # 匹配文件后缀部分
    file_extensions_label = tk.Label(frame, text="匹配文件后缀:")
    file_extensions_label.grid(row=5, column=0, padx=5, pady=2)
    ToolTip(file_extensions_label, "输入要匹配的文件后缀，多个后缀用逗号分隔，只有匹配的文件才会被重命名")
    file_extensions_entry = tk.Entry(frame, width=60)
    file_extensions_entry.grid(row=5, column=1, padx=5, pady=2, columnspan=3)

    # 匹配重命名文件字符部分
    match_chars_label = tk.Label(frame, text="匹配重命名文件字符:")
    match_chars_label.grid(row=6, column=0, padx=5, pady=2)
    ToolTip(match_chars_label, "输入要匹配的文件名中的字符，多个字符用逗号分隔，只有包含这些字符的文件才会被重命名")
    match_chars_entry = tk.Entry(frame, width=60)
    match_chars_entry.grid(row=6, column=1, padx=5, pady=2, columnspan=3)

    # 提示文本
    tk.Label(frame, text="多关键字用逗号分隔，关键字为空则不启用对应规则", fg="gray").grid(row=7, column=0, columnspan=4, pady=2)

    # 自动滚动复选框
    auto_scroll_var = tk.IntVar()
    auto_scroll_var.set(1)  # 默认勾选
    auto_scroll_checkbox = tk.Checkbutton(frame, text="文本框自动滚动到最底部", variable=auto_scroll_var)
    auto_scroll_checkbox.grid(row=8, column=0, columnspan=4, pady=2)

    # 开始重命名按钮
    start_button = tk.Button(frame, text="开始重命名", command=lambda: start_rename(root))
    start_button.grid(row=9, column=0, columnspan=4, pady=10)

    # 进度条
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress_bar.grid(row=10, column=0, columnspan=4, pady=5)

    # 结果显示文本框
    result_text = scrolledtext.ScrolledText(frame, width=80, height=10)
    result_text.grid(row=11, column=0, columnspan=4, pady=5)

    root.mainloop()


def run_with_args():
    parser = argparse.ArgumentParser(description='文件重命名工具')
    parser.add_argument('directory', type=str, help='要重命名文件的目录')
    parser.add_argument('--max_length', type=int, default=def_max_length, help='最大文件名长度')
    parser.add_argument('--prefix', type=str, default=def_prefix, help='重命名前缀')
    parser.add_argument('--match_prefix', type=str, default="", help='匹配的文件名前缀')
    parser.add_argument('--file_extensions', type=str, default="", help='匹配文件后缀')
    parser.add_argument('--match_chars', type=str, default="", help='匹配重命名文件字符')
    parser.add_argument('--remove_chars', type=str, default="", help='重命名删除字符')
    args = parser.parse_args()
    file_extensions = args.file_extensions.split(',') if args.file_extensions else []
    file_extensions = [ext.strip() for ext in file_extensions if ext.strip()]
    # 创建一个假的结果文本框，用于日志显示
    global result_text
    result_text = scrolledtext.ScrolledText()

    def dummy_progress_callback(progress):
        pass

    all_files = collect_all_files(args.directory)
    rename_files(all_files, args.max_length, args.prefix, args.match_prefix, file_extensions,
                 args.match_chars, args.remove_chars, dummy_progress_callback)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_with_args()
    else:
        create_gui()
