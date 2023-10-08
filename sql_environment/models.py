from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

class Test_type(Enum):
    ALL = 0,
    BIGINER = 1,
    ELEMENTERY = 2,
    PREINTERMEDIA = 3,
    INTERMEDIA = 4,
    PREADVANCED = 5,
    ADVANCED = 6

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    tg_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False)
    progress = Column(Integer)
    current_lesson = Column(String)

class TestData(Base):
    __tablename__ = 'test_data'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    question = Column(String, nullable=False)
    var1 = Column(String, nullable=False)
    var2 = Column(String, nullable=False)
    var3 = Column(String, nullable=False)
    var4 = Column(String, nullable=False)
    right_var = Column(Integer, nullable=False)
    var_dif = Column(Integer, nullable=False)

    @property
    def serialize(self):
        return {
            "question": self.question,
            "var1": self.var1,
            "var2": self.var2,
            "var3": self.var3,
            "var4": self.var4,
            "right_var": self.right_var,
            "var_dif": self.var_dif
        }

class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    lessonDif = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    video_url = Column(String)
    homework = Column(String)
    articles = Column(String)

    @property
    def serialize(self):
        return {
            "lessonDif": self.lessonDif,
            "name": self.name,
            "video_url": self.video_url,
            "homework": self.homework,
            "articles": self.articles
        }

class Articles(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    lesson_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String)

    @property
    def serialize(self):
        return {
            "name": self.name,
            "url": self.url,
        }

class HomeWork(Base):
    __tablename__ = 'homeWork'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    lesson_id = Column(Integer, nullable=False)
    name = Column(String)
    caption = Column(String, nullable=False)

    @property
    def serialize(self):
        return {
            "name": self.name,
            "caption": self.caption
        }

class HMQuery(Base):
    __tablename__ = 'homeWorkQuery'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    hm_id = Column(Integer, nullable=False)
    caption = Column(String, nullable=False)

class Words(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    english = Column(String)
    russian = Column(String)
    uzbek = Column(String)


