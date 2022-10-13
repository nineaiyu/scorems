#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : scorems
# filename : models
# author : ly_13
# date : 2022/10/13

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "userinfo"
    username = Column(String(30), primary_key=True, comment='用户名或学号，唯一')
    password = Column(String(30), comment='密码')

    def __repr__(self):
        return f"User(username={self.username!r})"


class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), comment='姓名')
    username = Column(String(30), comment='学号')
    # semester = Column(String(30), comment='学期')
    chinese = Column(Integer, comment='语文')
    math = Column(Integer, comment='数学')
    english = Column(Integer, comment='英语')
    politics = Column(Integer, comment='政治')
    score = Column(Integer, comment='总成绩')
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )

    def __repr__(self):
        return f"Score(username={self.username!r},nickname={self.nickname!r})"


engine = create_engine("sqlite+pysqlite:///./db_file", echo=True, future=True)


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def check_db():
    try:
        session.query(User).first()
    except Exception as e:
        init_db()


if __name__ == '__main__':
    init_db()
