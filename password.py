import random
import string
import pyperclip
import tkinter as tk
from tkinter import messagebox


def password_tkk():
    root = tk.Tk()
    root.title("安全密码生成器")
    root.geometry("400x400")
    root.config(bg="#f0f0f0")
    root.resizable(False, False)  # 禁止窗口缩放，保持界面整洁

    # 主框架（统一管理组件间距）
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(pady=30)

    # 1. 密码长度标签
    label_length = tk.Label(
        main_frame, text="密码长度",
        font=("Arial", 12),
        bg="#f0f0f0"
    )
    label_length.pack(side="left", padx=5)

    # 2. 密码长度输入框
    entry_length = tk.Entry(
        main_frame,
        font=("Arial", 12),
        width=14,
        bd=2, relief="solid"  # 添加边框，更美观
    )
    entry_length.insert(0, 12)  # 默认值12
    entry_length.pack(side="left", padx=5)

    # 3. 包含特殊符号复选框
    var_punct = tk.IntVar(value=1)  # 默认勾选
    checkbox_punct = tk.Checkbutton(
        main_frame, text="包含特殊符号",
        font=("Arial", 12),
        bg="#f0f0f0",
        selectcolor="#f0f0f0",  # 勾选时背景色一致
        variable=var_punct
    )
    checkbox_punct.pack(side="left", padx=5)

    # 4. 密码显示标签（增加样式，更醒目）
    label_psw = tk.Label(
        root,
        font=("Arial", 12, "bold"),  # 加粗字体
        text="",
        bg="#f0f0f0",
        fg="#e74c3c",  # 红色文字，突出密码
        wraplength=350  # 密码过长时自动换行
    )
    label_psw.pack(pady=30)

    def generate_password():
        # 处理密码长度
        try:
            length = int(entry_length.get().strip())
            # 强制长度在4-32之间（太短不安全，太长不实用）
            if length < 4:
                length = 12
            elif length > 32:
                length = 32
                messagebox.showinfo("提示", "密码长度最大支持32位，已自动调整！")
        except:
            length = 12
            messagebox.showwarning("警告", "输入无效，默认生成12位密码！")

        # 构建字符池
        chars = string.ascii_letters + string.digits  # 大小写字母+数字（必选）
        if var_punct.get() == 1:
            chars += string.punctuation  # 勾选则添加特殊符号

        # 生成密码
        password_list = random.choices(chars, k=length)

        # 确保密码复杂度：包含大小写字母+数字
        has_lower = any(c in string.ascii_lowercase for c in password_list)
        has_upper = any(c in string.ascii_uppercase for c in password_list)
        has_digit = any(c in string.digits for c in password_list)

        # 不满足复杂度则重新生成
        while not (has_lower and has_upper and has_digit):
            password_list = random.choices(chars, k=length)
            has_lower = any(c in string.ascii_lowercase for c in password_list)
            has_upper = any(c in string.ascii_uppercase for c in password_list)
            has_digit = any(c in string.digits for c in password_list)

        final_pwd = ''.join(password_list)
        label_psw.config(text=f"生成密码: {final_pwd}")

        # 自动复制到剪贴板（增加用户体验）
        pyperclip.copy(final_pwd)
        messagebox.showinfo("成功", "密码已生成并复制到剪贴板！")

    # 5. 生成按钮（优化样式）
    button_generate = tk.Button(
        root, text="生成密码",
        font=("Arial", 12),
        bg="#4CAF50",  # 绿色背景
        fg="white",  # 白色文字
        bd=0, relief="flat",
        padx=20, pady=5,
        cursor="hand2",  # 鼠标悬浮时显示手型
        command=generate_password
    )
    button_generate.pack(pady=10)

    root.mainloop()


# 运行程序
password_tkk()