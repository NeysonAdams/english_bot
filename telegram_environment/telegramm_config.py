from telegram import InlineKeyboardButton

KEY_BOARDS_BUTTONS = {
    "after_registration": [
            [InlineKeyboardButton("Пройти тестирование", callback_data="start_test")],
            [InlineKeyboardButton("Начать с начального уровня", callback_data="start_from_begin")]
    ],
    "do_you_want_to_continue": [
            [
                InlineKeyboardButton("Да", callback_data="start_from_continue"),
                InlineKeyboardButton("Нет", callback_data="start_from_begin"),
            ]
        ],
    "main_menu": [
        ["Начать Урок"],
        ["Уроки"],
        ["Игры"],
        ["Настройки"]
    ],

    "games": [
        ["Написание"],
        ["Слова-Карточки"],
        ["Фразы"],
        ["Назад"]
    ],

    "settings": [
        ["RU", "UZ", "EN"],
        ["Назад"]
    ],

    "home_work": [
            [InlineKeyboardButton("Домашнее задание", callback_data="start_home_work")]
    ],
    "finish_lesson": [
            [InlineKeyboardButton("Завершить урок", callback_data="finish_lesson")]
    ],
    "dict_exit": [
        [InlineKeyboardButton("Выйти", callback_data="dict_exit")]
    ]

}