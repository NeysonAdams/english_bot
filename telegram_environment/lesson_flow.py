from telegram import Update, ReplyKeyboardMarkup, InputFile, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from sql_environment.sql_main import Sql_Base
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .telegramm_config import KEY_BOARDS_BUTTONS

class TeleBotLesson():
    def __init__(self, application, db:Sql_Base, menu_echo, event_dispatcher):
        self.data_base = db
        self.application = application
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.add_event("start_home_work", self.start_home_work)
        self.event_dispatcher.add_event("finish_lesson", self._finish_lesson)
        self.menu_echo = menu_echo
        self.l_menu = MessageHandler(filters.TEXT & ~filters.COMMAND, self.lesson_menu)

    async def _finish_lesson(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
        await update.message.reply_text(f"Продолжим!", reply_markup=reply_markup)

    async def start_home_work(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        home_work = self.current_homework
        caption = f"**{home_work[self.hw_id].name}**\n{home_work[self.hw_id].caption}"
        if (self.hw_id+1) < len(home_work):
            self.hw_id = self.hw_id+1
            reply_markup = InlineKeyboardMarkup(KEY_BOARDS_BUTTONS["home_work"])
        else:
            reply_markup = InlineKeyboardMarkup(KEY_BOARDS_BUTTONS["finish_lesson"])

        await update.message.reply_text(caption, parse_mode='MarkdownV2', reply_markup=reply_markup)



    async def show_lessons(self, update, context, by_name=None):
        print(by_name)
        if by_name:
            self.current_lesson = self.data_base.get_lesson_by_name(by_name)
        else:
            user_id = update.message.from_user.id
            self.current_lesson= self.data_base.get_current_lesson(user_id)
        self.current_homework = self.data_base.get_home_work(self.current_lesson.id)
        self.hw_id =0

        await update.message.reply_text(self.current_lesson.name, reply_markup=ReplyKeyboardRemove())
        reply_markup = InlineKeyboardMarkup(KEY_BOARDS_BUTTONS["home_work"])

        with open(self.current_lesson.video_url, 'rb') as video_file:
            try:
                await context.bot.send_video(chat_id=update.message.chat_id,
                                         video=InputFile(video_file),
                                         caption="Закончили просмотор переходите к домашнему заданию",
                                         reply_markup=reply_markup
                                         )
            except Exception as e:
                print(e)


    async def show_menu_lessons(self, update, context, page=0):
        self.page = page
        if page == 0:
            self.application.remove_handler(self.menu_echo)
            self.application.add_handler(self.l_menu)
        user_id = update.message.from_user.id
        lessons, _ = self.data_base.get_lessons(user_id)
        keys = []
        i = 0
        print(len(lessons))
        for lesson in lessons:
            if i>= page*3 and i<(page+1)*3:
                keys.append([lesson.name])
            i = i+1

        move_arrow= ["<",">"]
        if page == 0:
            move_arrow = [">"]
        elif page*3> len(lessons):
            move_arrow = ["<"]

        keys.append(move_arrow)
        keys.append(["Назад"])

        reply_markup = ReplyKeyboardMarkup(keys)
        await update.message.reply_text("Уроки",
                                        reply_markup=reply_markup)

    async def lesson_menu(self, update: Update, context: CallbackContext) -> None:
        received_text = update.message.text

        if received_text == "Назад":
            self.application.add_handler(self.menu_echo)
            self.application.remove_handler(self.l_menu)
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await update.message.reply_text(f"Продолжим! \n Начните учиться", reply_markup=reply_markup)
        elif received_text == ">":
            self.page = self.page+1
            await self.show_menu_lessons(update, context, self.page)
        elif received_text == "<":
            self.page = self.page - 1
            await self.show_menu_lessons(update, context, self.page)
        else:
            self.application.add_handler(self.menu_echo)
            self.application.remove_handler(self.l_menu)
            await self.show_lessons(update, context, received_text)

