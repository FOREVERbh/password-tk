import random
import string
import pyperclip
import tkinter as tk
from tkinter import messagebox, ttk


def password_tkk():
    root = tk.Tk()
    root.title("安全密码生成器")
    root.geometry("450x450")
    root.config(bg="#f8f9fa")  # 更舒适的背景色
    root.resizable(False, False)

    # 主框架（使用grid布局更精确控制组件位置）
    main_frame = tk.Frame(root, bg="#f8f9fa")
    main_frame.pack(pady=40, padx=30)

    # 1. 密码长度设置区域
    length_frame = tk.Frame(main_frame, bg="#f8f9fa")
    length_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

    label_length = tk.Label(
        length_frame, text="密码长度：",
        font=("Microsoft YaHei", 12),
        bg="#f8f9fa"
    )
    label_length.pack(side="left", padx=5)

    entry_length = tk.Entry(
        length_frame,
        font=("Microsoft YaHei", 12),
        width=10,
        bd=2, relief="solid",
        justify="center"  # 输入内容居中显示
    )
    entry_length.insert(0, 12)
    entry_length.pack(side="left", padx=5)

    # 长度范围提示
    label_range = tk.Label(
        length_frame, text="(4-32位)",
        font=("Microsoft YaHei", 10),
        bg="#f8f9fa",
        fg="#6c757d"
    )
    label_range.pack(side="left", padx=5)

    # 2. 密码复杂度选项（新增更多自定义选项）
    complexity_frame = tk.Frame(main_frame, bg="#f8f9fa")
    complexity_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")

    # 复选框变量
    var_lower = tk.IntVar(value=1)  # 小写字母（默认勾选）
    var_upper = tk.IntVar(value=1)  # 大写字母（默认勾选）
    var_digit = tk.IntVar(value=1)  # 数字（默认勾选）
    var_punct = tk.IntVar(value=1)  # 特殊符号（默认勾选）

    # 复选框布局（两列显示）
    checkbox_lower = tk.Checkbutton(
        complexity_frame, text="包含小写字母(a-z)",
        font=("Microsoft YaHei", 11),
        bg="#f8f9fa",
        selectcolor="#f8f9fa",
        variable=var_lower
    )
    checkbox_lower.grid(row=0, column=0, sticky="w", padx=5, pady=3)

    checkbox_upper = tk.Checkbutton(
        complexity_frame, text="包含大写字母(A-Z)",
        font=("Microsoft YaHei", 11),
        bg="#f8f9fa",
        selectcolor="#f8f9fa",
        variable=var_upper
    )
    checkbox_upper.grid(row=0, column=1, sticky="w", padx=5, pady=3)

    checkbox_digit = tk.Checkbutton(
        complexity_frame, text="包含数字(0-9)",
        font=("Microsoft YaHei", 11),
        bg="#f8f9fa",
        selectcolor="#f8f9fa",
        variable=var_digit
    )
    checkbox_digit.grid(row=1, column=0, sticky="w", padx=5, pady=3)

    checkbox_punct = tk.Checkbutton(
        complexity_frame, text="包含特殊符号(!@#$等)",
        font=("Microsoft YaHei", 11),
        bg="#f8f9fa",
        selectcolor="#f8f9fa",
        variable=var_punct
    )
    checkbox_punct.grid(row=1, column=1, sticky="w", padx=5, pady=3)

    # 3. 密码显示区域（优化显示样式）
    label_psw_title = tk.Label(
        root, text="生成的密码：",
        font=("Microsoft YaHei", 12),
        bg="#f8f9fa"
    )
    label_psw_title.pack(pady=(10, 5))

    # 密码显示标签（使用边框和背景色突出显示）
    psw_display = tk.Label(
        root,
        font=("Consolas", 13, "bold"),  # 等宽字体，更适合显示密码
        text="点击下方按钮生成密码",
        bg="white",
        fg="#2d3436",
        wraplength=380,
        padx=20,
        pady=15,
        relief="solid",
        bd=1,
        width=35
    )
    psw_display.pack(pady=5)

    def generate_password():
        # 1. 处理密码长度
        try:
            length = int(entry_length.get().strip())
            # 强制长度范围
            if length < 4:
                length = 4
                messagebox.showinfo("提示", "密码长度不能小于4位，已自动调整为4位！")
            elif length > 32:
                length = 32
                messagebox.showinfo("提示", "密码长度最大支持32位，已自动调整为32位！")
        except ValueError:
            length = 12
            messagebox.showwarning("警告", "请输入有效的数字！已默认生成12位密码。")

        # 2. 构建字符池（根据复选框选择）
        chars = ""
        if var_lower.get() == 1:
            chars += string.ascii_lowercase
        if var_upper.get() == 1:
            chars += string.ascii_uppercase
        if var_digit.get() == 1:
            chars += string.digits
        if var_punct.get() == 1:
            # 过滤掉一些容易引起冲突的特殊符号
            safe_punct = '!@#$%^&*()_+-=[]{}|;:,.?~`'
            chars += safe_punct

        # 3. 检查是否至少选择了一种字符类型
        if not chars:
            messagebox.showerror("错误", "请至少选择一种字符类型！")
            return

        # 4. 生成密码（确保满足所选的字符类型要求）
        def create_valid_password():
            password_list = random.choices(chars, k=length)
            # 检查是否包含所选的所有字符类型
            conditions = []
            if var_lower.get() == 1:
                conditions.append(any(c in string.ascii_lowercase for c in password_list))
            if var_upper.get() == 1:
                conditions.append(any(c in string.ascii_uppercase for c in password_list))
            if var_digit.get() == 1:
                conditions.append(any(c in string.digits for c in password_list))
            if var_punct.get() == 1:
                conditions.append(any(c in safe_punct for c in password_list))
            return password_list if all(conditions) else create_valid_password()

        # 生成最终密码
        password_list = create_valid_password()
        final_pwd = ''.join(password_list)

        # 5. 更新显示并复制到剪贴板
        psw_display.config(text=final_pwd)
        pyperclip.copy(final_pwd)

        # 显示成功提示（使用更友好的提示语）
        messagebox.showinfo("操作成功", f"密码已生成并复制到剪贴板！\n密码长度：{length}位")

    # 4. 生成按钮（优化样式和交互）
    button_generate = tk.Button(
        root, text="生成安全密码",
        font=("Microsoft YaHei", 13, "bold"),
        bg="#28a745",
        fg="white",
        bd=0,
        relief="flat",
        padx=30,
        pady=8,
        cursor="hand2",
        command=generate_password,
        activebackground="#218838"  # 点击时背景色变化
    )
    button_generate.pack(pady=20)

    # 5. 底部提示信息
    tip_label = tk.Label(
        root, text="密码包含大小写字母、数字和特殊符号，安全性更高",
        font=("Microsoft YaHei", 10),
        bg="#f8f9fa",
        fg="#6c757d"
    )
    tip_label.pack(side="bottom", pady=10)

    root.mainloop()


# 运行程序
if __name__ == "__main__":
    password_tkk()