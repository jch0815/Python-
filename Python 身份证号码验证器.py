import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime

class IDCardValidator:
    def __init__(self, root):
        self.root = root
        self.root.title("身份证号码验证器")
        self.root.geometry("400x250")
        
        # 设置窗口图标（需要准备一个.ico文件）
        try:
            self.root.iconbitmap("id_card.ico")
        except:
            pass
        
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        tk.Label(self.root, text="身份证号码验证器", font=("Arial", 16)).pack(pady=10)
        
        # 输入框
        tk.Label(self.root, text="请输入18位身份证号码:").pack()
        self.id_entry = tk.Entry(self.root, width=25, font=("Arial", 12))
        self.id_entry.pack(pady=5)
        
        # 验证按钮
        tk.Button(self.root, text="验证", command=self.validate_id, width=10, height=1).pack(pady=10)
        
        # 结果显示
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=10)
        
        # 详细信息
        self.detail_label = tk.Label(self.root, text="", font=("Arial", 10), wraplength=380, justify="left")
        self.detail_label.pack()
    
    def validate_id(self):
        id_number = self.id_entry.get().strip()
        
        # 基本格式检查
        if not re.match(r'^\d{17}[\dXx]$', id_number):
            self.show_result("错误", "身份证号码格式不正确！", "red")
            return
        
        # 提取各部分信息
        try:
            # 地区码（前6位）
            area_code = id_number[:6]
            
            # 出生日期（7-14位）
            birth_date_str = id_number[6:14]
            birth_date = datetime.strptime(birth_date_str, "%Y%m%d")
            
            # 顺序码（15-17位）
            sequence_code = id_number[14:17]
            
            # 校验码（第18位）
            check_code = id_number[17].upper()
        except ValueError:
            self.show_result("错误", "身份证号码包含无效日期！", "red")
            return
        
        # 校验码验证
        if check_code != self.calculate_check_code(id_number[:17]):
            self.show_result("错误", "身份证号码校验码不正确！", "red")
            return
        
        # 性别判断（顺序码第3位，奇数为男，偶数为女）
        gender = "男" if int(sequence_code[-1]) % 2 else "女"
        
        # 年龄计算
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # 显示结果
        details = f"""
        地区码: {area_code}
        出生日期: {birth_date.strftime("%Y年%m月%d日")}
        年龄: {age}岁
        性别: {gender}
        顺序码: {sequence_code}
        校验码: {check_code}
        """
        self.show_result("有效", "身份证号码有效！", "green", details)
    
    def calculate_check_code(self, id_17):
        """计算身份证校验码"""
        # 权重系数
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 校验码对应关系
        check_codes = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 
                      5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
        
        total = 0
        for i in range(17):
            total += int(id_17[i]) * weights[i]
        
        return check_codes[total % 11]
    
    def show_result(self, title, message, color, details=""):
        self.result_label.config(text=message, fg=color)
        self.detail_label.config(text=details)
        if color == "red":
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = IDCardValidator(root)
    root.mainloop()