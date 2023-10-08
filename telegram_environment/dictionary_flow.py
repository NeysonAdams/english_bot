from telegram import Update, ReplyKeyboardMarkup, InputFile, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, filters
from telegram.ext import ContextTypes, CallbackQueryHandler
from sql_environment.sql_main import Sql_Base
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .telegramm_config import KEY_BOARDS_BUTTONS

class TeleBotTranslate():
    def __init__(self, application, db:Sql_Base, menu_echo):
        self.data_base = db
        self.application = application
        self.trans = MessageHandler(filters.TEXT & ~filters.COMMAND, self.translate)

        self.button_handler = CallbackQueryHandler(self.button)
        self.menu_echo = menu_echo



    async def start_dictionary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.application.add_handler(self.trans)
        self.application.add_handler(self.button_handler)
        self.application.remove_handler(self.menu_echo)

        await update.message.reply_text(f"Словарь! \n", reply_markup=ReplyKeyboardRemove())
        reply_markup = InlineKeyboardMarkup(KEY_BOARDS_BUTTONS["dict_exit"])

        await update.message.reply_text(" Введите слово получите пеевод",
                                        reply_markup=reply_markup)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        if query.data == 'dict_exit':
            self.application.remove_handler(self.trans)
            self.application.remove_handler(self.button_handler)
            self.application.add_handler(self.menu_echo)
            reply_markup = ReplyKeyboardMarkup(KEY_BOARDS_BUTTONS["main_menu"], one_time_keyboard=True)
            await update.message.reply_text(f"Начнём сначала! \n Начните учиться", reply_markup=reply_markup)

    async def translate(self, update: Update, context: CallbackContext) -> None:
        user_input = update.message.text.lower()
        ind , w_translate  = self.data_base.get_translate(user_input)

        if ind == "en":
            w_translate = w_translate[0]

        reply_markup = InlineKeyboardMarkup(KEY_BOARDS_BUTTONS["dict_exit"])
        await update.message.reply_text(w_translate,
                                        reply_markup=reply_markup)