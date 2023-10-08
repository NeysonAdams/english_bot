from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import text, MetaData
from .models import Base, Users, TestData, Articles, HomeWork, HMQuery, Test_type, Lesson, Words
from .test_examples import TEST_QUESTION, LESSONS, WORDS
from config import TEST_MODE

class Sql_Base():
    def __init__(self):
        self.database_url = "sqlite:///main_data_base.db"
        print(self.database_url)
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)

        if TEST_MODE:
            try:
                self._drop_tables()
            except:
                pass

        Base.metadata.create_all(self.engine)

        if TEST_MODE:
            self._put_test_questions()
            self._put_test_lessons()
            self._put_home_work_test_data()
            self._put_words()

    def _put_words(self):
        words = WORDS
        session = self.Session()
        for word in words:
            new_word = Words(
                english=word["english"],
                russian=word["russian"],
                uzbek=word["uzbek"]
            )
            session.add(new_word)
            session.commit()
        session.close()

    def _put_home_work_test_data(self):
        homwworks = LESSONS["homework"]
        session = self.Session()
        for hm in homwworks:
            new_lesson = HomeWork(
                lesson_id=hm["lesson_id"],
                name=hm["name"],
                caption=hm["caption"]
            )
            session.add(new_lesson)
            session.commit()
        session.close()

    def _put_test_lessons(self):
        lessons = LESSONS["lessons"]
        session = self.Session()
        for les in lessons:
            new_lesson = Lesson(
                lessonDif=les["lessonDif"],
                name=les["name"],
                video_url=les["video_url"],
                homework=les["homework"],
                articles=les["articles"]
            )
            session.add(new_lesson)
            session.commit()

        session.close()


    def _put_test_questions(self):
        questions= TEST_QUESTION["questions"]
        session = self.Session()
        for quest in questions:
            new_question = TestData(
                question=quest["question"],
                var1=quest["var1"],
                var2=quest["var2"],
                var3=quest["var3"],
                var4=quest["var4"],
                right_var=quest["right_var"],
                var_dif=quest["var_dif"]
            )
            session.add(new_question)
            session.commit()

        session.close()


    def _drop_tables(self):
        for table in Base.metadata.tables:
            table_to_drop = Base.metadata.tables[table]
            table_to_drop.drop(self.engine)

    def _check_tables(self):
        session = self.Session()

        result = session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';"))

        for row in result:
            print(row[0])

        session.close()

    def check_telegram_id(self, tg_id):
        session = self.Session()
        current_tg_id = session.query(Users).filter_by(tg_id=tg_id).first()
        session.close()
        if current_tg_id:
            return True
        else:
            return False

    def check_login(self, login):
        session = self.Session()
        login = session.query(Users).filter_by(login=login).first()
        session.close()

        if login:
            return True
        else:
            return False



    def add_user(self, request):
        user_name = request["user_name"]
        tg_id = request["tg_id"]
        login = request["login"]
        progress = request["progress"]

        session = self.Session()

        new_user = Users(tg_id=tg_id,
                         name=user_name,
                         login=login,
                         progress=progress,
                         current_lesson=0)
        session.add(new_user)
        session.commit()

        session.close()

    def get_test_questions(self):
        session = self.Session()

        beginner = session.query(TestData).filter_by(var_dif=1).order_by(func.random()).limit(3).all()
        elementary = session.query(TestData).filter_by(var_dif=2).order_by(func.random()).limit(3).all()
        preint = session.query(TestData).filter_by(var_dif=3).order_by(func.random()).limit(3).all()
        inter = session.query(TestData).filter_by(var_dif=4).order_by(func.random()).limit(3).all()
        preadv = session.query(TestData).filter_by(var_dif=5).order_by(func.random()).limit(3).all()
        advan = session.query(TestData).filter_by(var_dif=6).order_by(func.random()).limit(3).all()

        session.close()

        questions = []
        for i in beginner:
            questions.append(i.serialize)
        for i in elementary:
            questions.append(i.serialize)
        for i in preint:
            questions.append(i.serialize)
        for i in inter:
            questions.append(i.serialize)
        for i in preadv:
            questions.append(i.serialize)
        for i in advan:
            questions.append(i.serialize)

        return questions

    def update_user(self, tg_id,
                    name = None,
                    login = None,
                    progress = None,
                    current_lesson = None
    ):
        session = self.Session()
        user = session.query(Users).filter_by(tg_id=tg_id).first()
        if name:
            user.name = name
        if login:
            user.login = login
        if progress:
            user.progress = progress
        if current_lesson:
            user.current_lesson = current_lesson

        session.commit()
        session.close()

    def get_user(self, tg_id):
        session = self.Session()
        user = session.query(Users).filter_by(tg_id=tg_id).first()
        session.close()
        return user

    def get_lessons(self, tg_id):
        session = self.Session()
        user = session.query(Users).filter_by(tg_id=tg_id).first()
        lessons = session.query(Lesson).filter_by(lessonDif=user.progress).all()
        session.close()
        return lessons, user

    def get_current_lesson(self, tg_id) -> Lesson:
        lessons, user = self.get_lessons(tg_id)
        s = user.current_lesson
        lst = [int(x) for x in s.split(',')]
        current_lesson = lessons[0]
        for lesson in lessons:
            is_pased = True
            for x in lst:
                if lesson.id == x:
                    is_pased = False
                    break

            if is_pased:
                current_lesson = lesson
                break
        session = self.Session()
        if user.current_lesson == "":
            user.current_lesson = str(current_lesson.id)
        else:
            user.current_lesson = f"{user.current_lesson},{current_lesson.id}"
        session.commit()
        session.close()
        print("lesson geted by name")
        return current_lesson

    def get_lesson_by_name(self, name) -> Lesson:
        session = self.Session()
        lesson = session.query(Lesson).filter_by(name=name).first()
        session.close()
        return lesson

    def get_home_work(self, lesson_id):
        session = self.Session()
        homework = session.query(HomeWork).filter_by(lesson_id=lesson_id).all()
        session.close()
        return homework

    def get_translate(self, c_word):
        session = self.Session()
        ru_word = session.query(Words).filter_by(russian=c_word).first()
        uz_word = session.query(Words).filter_by(uzbek=c_word).first()
        en_word = session.query(Words).filter_by(english=c_word).first()
        session.close()

        if ru_word :
            return "ru", ru_word.english
        if uz_word:
            return "uz", uz_word.english
        if en_word:
            return "en", (en_word.russian, en_word.uzbek)

        return "None", "No word in dictionary"









