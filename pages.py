#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : scorems
# filename : pages
# author : ly_13
# date : 2022/10/13
import string
from tkinter import StringVar, Label, Entry, font, W, E, Button, messagebox, Menu
from tkinter.ttk import Frame

from models import session, User
from views import AddFrame, DeleteFrame, EditFrame, SearchFrame, CountFrame, ScoreFrame


class LoginPage(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master
        self.root.geometry('%dx%d' % (480, 320))
        self.username = StringVar(value='')
        self.password = StringVar(value='')
        self.init_page()

    def init_page(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page, text="学生成绩管理系统", font=("宋体", 20)).grid(row=0, pady=40, stick=W)
        Label(self.page, text='账户:', font=font.Font(size=12)).grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, stick=E)
        Label(self.page, text='密码:', font=font.Font(size=12)).grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, stick=E)
        Button(self.page, text='登录', command=self.login, font=font.Font(size=12)).grid(row=3, stick=W, pady=30)
        Button(self.page, text='注册', command=self.register, font=font.Font(size=12)).grid(row=3, stick=E, pady=30)

    def check_info(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        if len(username) == 0 or len(password) == 0:
            messagebox.showinfo(title='错误', message='账号密码不能为空')
            return
        if set(username) - set(string.digits + string.ascii_lowercase):
            messagebox.showinfo(title='错误', message=f'账号只能为 {string.digits + string.ascii_lowercase}')
            return
        if set(password) - set(string.digits + string.ascii_letters):
            messagebox.showinfo(title='错误', message=f'密码只能为 {string.digits + string.ascii_letters}')
            return

        return username, password

    def login(self):
        username, password = self.check_info()
        res = session.query(User).filter(User.username == username, User.password == password).first()
        if res:
            self.page.destroy()
            MainPage(self.root)
        else:
            messagebox.showinfo(title='错误', message='账号或密码错误！')

    def register(self):
        username, password = self.check_info()
        res = session.query(User).filter(User.username == username).first()
        if res:
            messagebox.showinfo(title='结果', message="已存在该用户信息！")
            return

        session.add(User(username=username, password=password))
        session.commit()
        messagebox.showinfo(title='提示', message=f"用户 {username} 注册成功")


class MainPage(object):
    def __init__(self, master=None):
        self.root = master
        self.add_page = AddFrame(self.root)
        self.del_page = DeleteFrame(self.root)
        self.edit_page = EditFrame(self.root)
        self.search_page = SearchFrame(self.root)
        self.count_page = CountFrame(self.root)
        self.score_page = ScoreFrame(self.root)
        self.root.geometry('%dx%d' % (600, 400))
        self.init_page()

    def init_page(self):
        self.add_page.pack()  # 默认显示数据录入界面
        menubar = Menu(self.root)
        menubar.add_command(label='添加', command=self.change_page())
        menubar.add_command(label='删除', command=self.change_page('del_page'))
        menubar.add_command(label='修改', command=self.change_page('edit_page'))
        menubar.add_command(label='查找', command=self.change_page('search_page'))
        menubar.add_command(label='成绩排行', command=self.change_page('score_page'))
        menubar.add_command(label='班级统计', command=self.change_page('count_page'))
        self.root['menu'] = menubar  # 设置菜单栏

    def change_page(self, active='add_page'):
        def change():
            getattr(self, active).pack()
            pages = ['add_page', 'del_page', 'edit_page', 'search_page', 'count_page', 'score_page']
            for page in set(pages) - {active}:
                getattr(self, page).pack_forget()

        return change
