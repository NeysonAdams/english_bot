from sql_environment.sql_main import Sql_Base
from telegram_environment.telebot_main import Telebot


if __name__ == '__main__':
    bd = Sql_Base()
    telebot = Telebot(bd)

