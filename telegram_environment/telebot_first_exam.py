from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import ContextTypes, CallbackQueryHandler
from sql_environment.sql_main import Sql_Base
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .telegramm_config import KEY_BOARDS_BUTTONS

class TeleBotExam():
    def __init__(self, application, db:Sql_Base, event_dispatcher):
        self.data_base = db
        self.application = application

        self.event_dispatcher = event_dispatcher
        self.questions = self.data_base.get_test_questions()
        self.length = len(self.questions)
        self.id = 0
        self.points = 0

    async def build_question(self, update):
        if self.id >= self.length:
            self.event_dispatcher.on_dispatcher()
            self.application.remove_handler(self.test_handler)
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await update.message.reply_text(f"Тест окончен! \n Начните учиться", reply_markup=reply_markup)
            return
        caption = self.questions[self.id]["question"]
        buttons = [
            [InlineKeyboardButton(self.questions[self.id]["var1"], callback_data=1)],
            [InlineKeyboardButton(self.questions[self.id]["var2"], callback_data=2)],
            [InlineKeyboardButton(self.questions[self.id]["var3"], callback_data=3)],
            [InlineKeyboardButton(self.questions[self.id]["var4"], callback_data=4)]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text(caption, reply_markup=reply_markup)

    async def test_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == self.questions[self.id]["right_var"]:
            self.points = self.points + 1

        self.id = self.id + 1

        await self.build_question(query)

    async def start_test(self, update, context: CallbackContext):
        self.test_handler = CallbackQueryHandler(self.test_button)
        self.event_dispatcher.off_dispatcher()
        self.application.add_handler(self.test_handler)

        await self.build_question(update)