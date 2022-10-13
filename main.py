# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import Tk

from models import check_db
from pages import LoginPage

if __name__ == '__main__':
    check_db()
    root = Tk()
    root.title('学生成绩管理系统')
    LoginPage(root)
    root.mainloop()
