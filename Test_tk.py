import tkinter as tk
import random

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("动态更新列表")
        self.test = Test('第一个','第二个')
        self.label = tk.Label(root, text="", font=("Arial", 16))
        self.label.pack(pady=20)
        self.multi = tk.Entry(root)
        self.multi.pack(pady=20)
        self.multi.bind('<Return>', self.submit)

        self.update_button = tk.Button(root, text="更新列表", command=self.update_list)
        self.update_button.pack(pady=10)

        self.shun_but = tk.Button(root, text='顺', command=self.test.shun)
        self.shun_but.pack(pady=10)
        self.ni_but = tk.Button(root, text='逆', command=self.test.ni)
        self.ni_but.pack(pady=10)

        self.my_list = []  # 初始化列表
        self.update_ui()  # 初始更新界面

    def update_list(self):
        # 模拟更新列表，随机添加一个新元素
        new_element = random.randint(1, 100)
        self.my_list.append(new_element)
        self.update_ui()
    def submit(self, event):
        self.my_list.append(2 * int(self.multi.get()))
        self.multi.delete(0, tk.END)

    def update_ui(self):
        # 更新界面显示的文本
        self.label.config(text=str(self.my_list))
        # 每500毫秒更新一次
        self.root.after(500, self.update_ui)

class Test:
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def shun(self):
        print(f'{str(self.a)+str(self.b)}')
    def ni(self):
        print(f'{str(self.b)+str(self.a)}')
    def get_input(self):
        ans = input('乘二')
        return ans


root = tk.Tk()
running = App(root)
root.mainloop()