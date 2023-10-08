from telegram import Update, ReplyKeyboardMarkup
from config import TOKEN, USER_NAME, LOGIN, START_REG

from telegram.ext import Updater, CommandHandler, \
    MessageHandler, CallbackContext, ConversationHandler, filters
from telegram.ext import Application, ContextTypes, CallbackQueryHandler
from sql_environment.sql_main import Sql_Base
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .telebot_first_exam import TeleBotExam
from .telegramm_config import KEY_BOARDS_BUTTONS
from .lesson_flow import TeleBotLesson
from .dictionary_flow import TeleBotTranslate
from .button_event_dispatcher import EventDispatchher


class Telebot():
    def __init__(self, db:Sql_Base):
        self.data_base = db
        self.application = Application.builder().token(TOKEN).build()
        self.request_data = {}


        self.registration_conversation = ConversationHandler(
            entry_points=[CommandHandler("start", self.start_base_line)],
            states={
                USER_NAME: [MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    self.get_name)],
                LOGIN: [MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    self.get_login)],
            },
            fallbacks=[],
        )

        self.menu_echo = MessageHandler(filters.TEXT & ~filters.COMMAND, self.menu_buttons)

        self.event_dispatcher = EventDispatchher(application=self.application)
        self.event_dispatcher.add_event("start_test", self._start_exam)
        self.event_dispatcher.add_event("start_from_begin", self._start_learning)
        self.event_dispatcher.add_event("start_from_continue", self._start_learning)

        self.telebot_exam = TeleBotExam(application=self.application,
                                        db=self.data_base,
                                        event_dispatcher=self.event_dispatcher)
        self.lesson_flow = TeleBotLesson(self.application, self.data_base, self.menu_echo, self.event_dispatcher)

        self.translator = TeleBotTranslate(application=self.application,
                                           db=self.data_base,
                                           menu_echo=self.menu_echo)

        # self.application.add_handler(CommandHandler("start", self.start_base_line))
        self.application.add_handler(self.registration_conversation)
        self.application.add_handler(self.menu_echo)

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    ### Registration methods
    async def user_name(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Пожалуйста, введите ваше полное имя:")
        return USER_NAME

    async def get_name(self, update: Update, context: CallbackContext) -> int:
        self.request_data["user_name"] = update.message.text
        print(self.request_data["user_name"])
        await update.message.reply_text(f"Привет, {self.request_data['user_name']}, приятно познакомиться!")
        await update.message.reply_text("Пожалуйста, введите ваш логин:")
        return LOGIN

    async def get_login(self, update: Update, context: CallbackContext) -> int:
        login = update.message.text
        user_id = update.message.from_user.id
        if not self.data_base.check_login(login):
            self.request_data["login"] = login
            self.request_data["tg_id"] = user_id
            self.request_data["progress"] = 1

            self.data_base.add_user(self.request_data)

            self.request_data = {}

            reply_markup = InlineKeyboardMarkup(KEY_BOARDS_BUTTONS["after_registration"])

            await update.message.reply_text("Регистрация прошла успешно. \n Теперь давайте продолжим:",
                                            reply_markup=reply_markup)

            return ConversationHandler.END
        else:
            await update.message.reply_text("Такой логин уже существует")
            await update.message.reply_text("Пожалуйста, введите ваш логин:")
            return LOGIN

    async def _start_learning(self, update: Update, context: CallbackContext):
        reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
        await update.message.reply_text(f"Начнём сначала! \n Начните учиться", reply_markup=reply_markup)

    async def _start_exam(self, update: Update, context: CallbackContext):
        await self.telebot_exam.start_test(update, context)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        print(query.data)

        if query.data == 'start_test':
            await self.telebot_exam.start_test(query, context)
        elif query.data == 'start_from_begin':
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await query.message.reply_text(f"Начнём сначала! \n Начните учиться", reply_markup=reply_markup)
        elif query.data == 'start_from_continue':
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await query.message.reply_text(f"Продолжим! \n Начните учиться", reply_markup=reply_markup)

    async def start_base_line(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        is_usr = self.data_base.check_telegram_id(user_id)
        with open("./data/img/learn-english-.jpg", "rb") as image_file:
            if not is_usr:
                caption="""
                    **Добро пожаловать**\nВы готовы начать путешествие в мир английского языка
                """
                await update.message.reply_photo(photo=image_file, caption=caption, parse_mode='MarkdownV2')
                return await self.user_name(update, context)
            else:

                reply_markup = InlineKeyboardMarkup(KEY_BOARDS_BUTTONS["do_you_want_to_continue"])
                await update.message.reply_text("Вы уже зарегистрированный пользоватль \n Желаете ли продолжить",
                                                reply_markup=reply_markup)


    async def menu_buttons (self, update: Update, context: CallbackContext) -> None:
        received_text = update.message.text
        if received_text == "Начать Урок":

            await self.lesson_flow.show_lessons(update, context)
        elif received_text == "Игры":
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["games"], one_time_keyboard=True)
            await update.message.reply_text("Игры", reply_markup=reply_markup)
        elif received_text == "Настройки":
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["settings"], one_time_keyboard=True)
            await update.message.reply_text("Настройки", reply_markup=reply_markup)
        elif received_text == "Назад":
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await update.message.reply_text(f"Продолжим! \n Начните учиться", reply_markup=reply_markup)
        elif received_text == "Уроки":
            await self.lesson_flow.show_menu_lessons(update, context)
        elif received_text == "Словарь":
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await update.message.reply_text(f"Comming soon", reply_markup=reply_markup)
            #await self.translator.start_dictionary(update, context)
        elif received_text == "Написание":
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await update.message.reply_text(f"Comming soon", reply_markup=reply_markup)
        elif received_text == "Слова-Карточки":
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await update.message.reply_text(f"Comming soon", reply_markup=reply_markup)
        elif received_text == "Фразы":
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await update.message.reply_text(f"Comming soon", reply_markup=reply_markup)



