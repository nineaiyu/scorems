#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : scorems
# filename : views
# author : ly_13
# date : 2022/10/13
import datetime
from tkinter import StringVar, Label, Entry, font, W, E, Button, messagebox, IntVar, ttk, Scrollbar
from tkinter.ttk import Frame

import matplotlib.pyplot as plt
import xlwt

from models import session, Score

columns = {
    'index': '排名',
    'username': '学号',
    'nickname': '姓名',
    'chinese': '语文',
    'math': '数学',
    'english': '英语',
    'politics': '政治',
    'score': '总分'
}


class AddFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.username = StringVar()
        self.nickname = StringVar()
        self.chinese = IntVar()
        self.math = IntVar()
        self.english = IntVar()
        self.politics = IntVar()
        self.show()

    def check(self):
        data = {
            'username': self.username.get().strip(),
            'nickname': self.nickname.get().strip(),
        }
        try:
            data['chinese'] = self.chinese.get()
            data['math'] = self.math.get()
            data['english'] = self.english.get()
            data['politics'] = self.politics.get()
            data['score'] = sum([data['chinese'], data['math'], data['english'], data['politics']])
        except Exception as e:
            print(e)
            messagebox.showinfo(title='结果', message="输入有误，请检查")
            return {}
        if data['username'] and data['nickname']:
            return data
        return {}

    def click(self):
        data = self.check()
        if data:
            res = session.query(Score).filter(Score.username == data.get('username')).first()
            if res:
                messagebox.showinfo(title='结果', message="已存在该学生科目信息！")
                return
            session.add(Score(**data))
            session.commit()
            messagebox.showinfo(title='结果', message="成绩信息添加成功！")
        else:
            messagebox.showinfo(title='提示', message="输入有误，请检查")

    def username_input(self):
        Label(self, text='学号: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)

    def show(self):
        Label(self).grid(row=0, stick=W, pady=10)

        self.username_input()

        index = 2
        for key, label in columns.items():
            if key in ['index', 'username', 'score']: continue
            Label(self, text=f'{label}: ').grid(row=index, stick=W, pady=10)
            Entry(self, textvariable=getattr(self, key)).grid(row=index, column=1, stick=E)
            index += 1

        Button(self, text='录入', command=self.click).grid(row=7, column=1, stick=E, pady=10)


class EditFrame(AddFrame):
    def __init__(self, master=None):
        super().__init__(master)

    def click(self):
        data = self.check()
        if data:
            res = session.query(Score).filter(Score.username == data['username'])
            if res and res.first():
                del data['username']
                res.update(data)
                session.commit()
                messagebox.showinfo(title='结果', message="成绩信息修改成功！")
            else:
                messagebox.showinfo(title='结果', message="查询信息不存在！")
                return
        else:
            messagebox.showinfo(title='提示', message="输入有误，请检查")

    def username_input(self):
        Label(self, text='学号: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)
        Button(self, text='查询', font=font.Font(size=12), command=self.search).grid(row=1, stick=E, column=2, pady=10)

    def search(self):
        username = self.username.get().strip()
        if username:
            res = session.query(Score).filter(Score.username == username).first()
            if res:
                for key in columns.keys():
                    if key in ['index', 'score', 'math']:
                        continue
                    print(key, getattr(res, key))
                    getattr(self, key).set(getattr(res, key))
            else:
                messagebox.showinfo(title='提示', message="查询信息不存在")
        else:
            messagebox.showinfo(title='提示', message="输入项为空")


class DeleteFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master
        self.username = StringVar()
        self.nickname = StringVar()
        self.show()

    def do_action(self, res):
        res.delete()
        session.commit()
        messagebox.showinfo(title='提示', message="删除成功")

    def click(self):
        username = self.username.get().strip()
        nickname = self.nickname.get().strip()
        if username or nickname:
            res = session.query(Score)
            if username:
                res = res.filter(Score.username == username)
            if nickname:
                res = res.filter(Score.nickname == nickname)
            if res and res.first():
                self.do_action(res)
                return
            else:
                messagebox.showinfo(title='提示', message="查询信息不存在")
        else:
            messagebox.showinfo(title='提示', message="输入项为空")

    def show_button(self):
        Button(self, text='删除', command=self.click).grid(row=6, column=1, stick=E, pady=10)

    def show(self):
        Label(self).grid(row=0, stick=W, pady=10)

        Label(self, text='学号: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)

        Label(self, text='姓名: ').grid(row=2, stick=W, pady=10)
        Entry(self, textvariable=self.nickname).grid(row=2, column=1, stick=E)
        self.show_button()


class SearchFrame(DeleteFrame):
    def __init__(self, master=None):
        super().__init__(master)

    def do_action(self, res):
        message = ''
        for key, value in columns.items():
            if key == 'index':
                continue
            message += f'{value}:{getattr(res.first(), key, "")}\n'
        messagebox.showinfo(title='结果',
                            message=message)

    def show_button(self):
        Button(self, text='查找', command=self.click).grid(row=6, column=1, stick=E, pady=10)


class ScoreFrame(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.ysb = None
        self.tree = None
        Label(self, text="成绩排行榜", font=("宋体", 20)).pack(pady=10)
        Button(self, text='导出成绩', command=write_easy_excel).pack(pady=10)

    def pack_forget(self) -> None:
        super().pack_forget()
        if self.tree:
            self.tree.destroy()
        if self.ysb:
            self.ysb.destroy()

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.tree = ttk.Treeview(self, show='headings', columns=list(columns.keys()))
        xsb = Scrollbar(self, orient="horizontal", command=self.tree.xview())  # x滚动条
        self.ysb = Scrollbar(self, orient="vertical", command=self.tree.yview())  # y滚动条
        self.tree.configure(yscrollcommand=self.ysb.set, xscrollcommand=xsb.set)  # y滚动条关联
        self.ysb.pack(side="right", fill="y")
        result = session.query(Score).order_by(Score.score.desc()).all()
        for column, label in columns.items():
            width = 40
            if column in ['username', 'nickname']:
                width = 80
            self.tree.column(column, width=width)
            self.tree.heading(column, text=label)
        index = 1
        for res in result:
            res.index = index
            self.tree.insert("", index, values=[getattr(res, x) for x in columns.keys()])
            index += 1
        self.tree.pack(pady=30)


class CountFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master
        self.result = session.query(Score).all()
        self.show()

    def pack(self):
        super().pack()
        self.result = session.query(Score).all()

    def show(self):
        Label(self, text="查看表格", font=("宋体", 20)).grid(row=0, pady=40, stick=W)
        Button(self, text='学生总成绩', font=font.Font(size=12), command=self.sum_score).grid(row=2, stick=W, pady=10)
        Button(self, text='各科平均分', font=font.Font(size=12), command=self.avg_score).grid(row=3, stick=W, pady=10)
        Button(self, text='各科最高分', font=font.Font(size=12), command=self.best_score).grid(row=4, stick=W, pady=10)
        Button(self, text='各科最低分', font=font.Font(size=12), command=self.bad_score).grid(row=5, stick=W, pady=10)

    def sum_score(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        if len(self.result) == 0:
            messagebox.showinfo(title='提示', message="暂无数据，请先录入成绩")
            return
        name = [res.nickname for res in self.result]
        students_scores = [res.score for res in self.result]

        plt.title('学生总成绩分布图')
        plt.xlabel('姓名')
        plt.ylabel('总分')
        plt.bar(name, students_scores)
        plt.show()

    def avg_score(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        if len(self.result) == 0:
            messagebox.showinfo(title='提示', message="暂无数据，请先录入成绩")
            return
        chinese_avg = sum([res.chinese for res in self.result]) / len(self.result)
        math_avg = sum([res.chinese for res in self.result]) / len(self.result)
        english_avg = sum([res.english for res in self.result]) / len(self.result)
        politics_avg = sum([res.politics for res in self.result]) / len(self.result)

        plt.title('每门课程平均分展示图')
        plt.xlabel('课程名')
        plt.ylabel('平均分')
        plt.bar('语文', chinese_avg)
        plt.bar('数学', math_avg)
        plt.bar('英语', english_avg)
        plt.bar('政治', politics_avg)
        plt.show()

    def best_score(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        if len(self.result) == 0:
            messagebox.showinfo(title='提示', message="暂无数据，请先录入成绩")
            return
        chinese_max = max([res.chinese for res in self.result])
        math_max = max([res.chinese for res in self.result])
        english_max = max([res.english for res in self.result])
        politics_max = max([res.politics for res in self.result])

        plt.title('每门课程最高分展示图')
        plt.xlabel('课程名')
        plt.ylabel('最高分')
        plt.bar('语文', chinese_max)
        plt.bar('数学', math_max)
        plt.bar('英语', english_max)
        plt.bar('政治', politics_max)
        plt.show()

    def bad_score(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        if len(self.result) == 0:
            messagebox.showinfo(title='提示', message="暂无数据，请先录入成绩")
            return
        chinese_min = min([res.chinese for res in self.result])
        math_min = min([res.chinese for res in self.result])
        english_min = min([res.english for res in self.result])
        politics_min = min([res.politics for res in self.result])

        plt.title('每门课程最低分展示图')
        plt.xlabel('课程名')
        plt.ylabel('最低分')
        plt.bar('语文', chinese_min)
        plt.bar('数学', math_min)
        plt.bar('英语', english_min)
        plt.bar('政治', politics_min)
        plt.show()


def write_easy_excel():
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('student_info')
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style = xlwt.XFStyle()
    style.alignment = alignment

    head = list(columns.keys())

    for h in range(len(head)):
        sheet.write(0, h, head[h], style)

    result = session.query(Score).order_by(Score.score.desc()).all()
    index = 1
    for res in result:
        res.index = index
        row = 0
        for key in columns.keys():
            sheet.write(index, row, getattr(res, key), style)
            row += 1
        index += 1

    # 保存表格，并命名
    n_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
    workbook.save(f'{n_time}.student_info.xls')
