from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import ContextTypes, CallbackQueryHandler
from sql_environment.sql_main import Sql_Base
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class EventDispatchher():
    def __init__(self, application):
        self.application = application
        self.event_registor = {}
        self.dispatcher = CallbackQueryHandler(self.button)
        self.application.add_handler(self.dispatcher)

    def add_event(self, key, callback):
        self.event_registor[key] = callback

    def on_dispatcher(self):
        self.application.add_handler(self.dispatcher)

    def off_dispatcher(self):
        self.application.remove_handler(self.dispatcher)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        print(query.data)
        key = query.data
        if key in self.event_registor.keys():
            await self.event_registor[key](query, context)
