import db

import logging
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram import types, Bot, Dispatcher
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio


TOKEN = "BOT_TOKEN"  # Astra Bot Token (From BotFather)
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)


# Configure logging
logging.basicConfig(level=logging.INFO)


class FSM(StatesGroup):
    Introduction = State()
    Learning = State()


@dp.message(Command(commands=["start"]))
async def start(message: types.Message, state: FSMContext) -> None:
    # Регистрация пользователя в базе данных
    registered = await db.register(message.chat.id, message.from_user.username, str(message.from_user.first_name) + ' ' + str(message.from_user.last_name))
    if registered:  # Если пользователь зарегистрирован
        await state.set_state(FSM.Introduction)  # Состояние
        photo = FSInputFile("./Pictures/Banners/Баннер1.png")
        inb = KeyboardButton(text='Вперёд!')
        inkb = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, one_time_keyboard=True, keyboard=[[inb], ])
        info = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Совет ✎', callback_data="info")], ])
        await message.answer("*Привет! 👋*\nЭто бот, который поможет тебе освоить операционную систему Astra Linux.", reply_markup=info)
        await asyncio.sleep(2)
        await message.answer_photo(photo, "*Наша главная цель* — помочь тебе научиться работать с Astra Linux и использовать её возможности в полной мере 😎", reply_markup=inkb)


@dp.callback_query(lambda call: call.data == "info", FSM.Introduction)
async def info(callback_query: types.CallbackQuery):
    await callback_query.answer(text="Для ответа используй кнопки внизу клавиатуры 🔽", show_alert=True)


@dp.message(lambda message: 'Вперёд!' in message.text, FSM.Introduction)
async def lets_go(message: types.message):
    await message.answer("Отлично! Давай я расскажу тебе, как устроен бот и что тебя ждет в этом курсе:", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(2)
    photo = FSInputFile("./Pictures/Banners/Баннер2.png")
    inb = KeyboardButton(text='А как работает WebApp?')
    inkb = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, one_time_keyboard=True, keyboard=[[inb], ])
    await message.answer_photo(photo, "Курс состоит из двух частей — *теоретической и практической* 🧑‍💻", reply_markup=inkb)


@dp.message(lambda message: 'А как работает WebApp?' in message.text, FSM.Introduction)
async def move_on(message: types.message):
    ReplyKeyboardRemove()
    inb = InlineKeyboardButton(text='Вводный модуль 📝', web_app=WebAppInfo(url='https://astralinuxedu.tilda.ws/intro'))
    inkb = InlineKeyboardMarkup(inline_keyboard=[[inb], ])
    await message.answer("Очень просто!\nТы можешь уже сейчас сделать свой первый шаг к обучению, прочитав наш вводный модуль 😉", reply_markup=inkb)
    await asyncio.sleep(2)
    inb = KeyboardButton(text='А что дальше?')
    inkb = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, one_time_keyboard=True, keyboard=[[inb], ])
    await message.answer("Именно в таких специальных окнах будет находиться весь необходимый материал 👍", reply_markup=inkb)


@dp.message(lambda message: 'А что дальше?' in message.text, FSM.Introduction)
async def whats_next(message: types.message):
    photo = FSInputFile("./Pictures/Banners/Баннер3.png")
    inb = KeyboardButton(text='Хорошо!')
    inkb = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, one_time_keyboard=True, keyboard=[[inb], ])
    await message.answer_photo(photo, "А также после каждого модуля следуют *тестовые задания:*", reply_markup=inkb)


@dp.message(lambda message: 'Хорошо!' in message.text, FSM.Introduction)
async def okay_then(message: types.message):
    await message.answer("Кстати! Мы забыли представить тебе кое-кого 👀", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await message.answer_sticker("CAACAgIAAxkBAAEJEAZka6s4RR8aGymE9q6Mtn0qsUFVvQACbwAD29t-AAGZW1Coe5OAdC8E")
    await asyncio.sleep(2)
    await message.answer("Знакомься! Это `Котобот` — твой личный компаньон!")
    await asyncio.sleep(2)
    inb = KeyboardButton(text='Приятно познакомиться!')
    inkb = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, one_time_keyboard=True, keyboard=[[inb], ])
    await message.answer("Он поможет тебе в освоении материала и будет сопровождать тебя на протяжении всего обучения 😼", reply_markup=inkb)


@dp.message(lambda message: 'Приятно познакомиться!' in message.text, FSM.Introduction)
async def intro_end(message: types.message):
    photo = FSInputFile("./Pictures/Banners/Баннер4.png")
    inb = KeyboardButton(text='Супер, я готов приступать!')
    inkb = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, one_time_keyboard=True, keyboard=[[inb], ])
    await message.answer_photo(photo, "Вот также *несколько других механик курса*, с которыми ты сможешь познакомиться в процессе обучения:", reply_markup=inkb)


@dp.message(lambda message: 'Супер, я готов приступать!' in message.text, FSM.Introduction)
async def intro_end(message: types.message, state: FSMContext):
    await message.answer("Теперь ты знаешь, что ждет тебя на нашем курсе, и готов начать свое обучение!\n\nМы желаем тебе удачи 🍀", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await message.answer("*Доступные команды бота*:\n\n📄 Теоретический материал — /learn\n📐 Тестовые задания — /test\n📀 Установка Astra Linux — /install\n💬 Твой профиль — /profile\n🏅 Таблица лидеров — /board\nℹ Справка — /help")
    await state.set_state(FSM.Learning)


@dp.message(Command(commands=["install"]))
async def install(message: types.Message, state: FSMContext) -> None:
    if await state.get_state() == FSM.Introduction:
        return
    inb = InlineKeyboardButton(text='Установка Astra Linux 📝', web_app=WebAppInfo(url='https://astralinuxedu.tilda.ws/install'))
    inkb = InlineKeyboardMarkup(inline_keyboard=[[inb], ])
    await message.answer("На случай, если на твоем компьютере ещё не установлена Astra Linux,\nмы подготовили для тебя *специальный модуль* с инструкцией по её инсталляции и краткой информацией об её версиях 🙌", reply_markup=inkb)
    await asyncio.sleep(1)
    await message.answer_sticker("CAACAgIAAxkBAAEJG_Zkb8Hcb3KKjskWUu_zqkEqxEc3bwACPwAD29t-AAH05pw4AeSqaS8E")


@dp.message(Command(commands=["help"]))
async def help_c(message: types.Message, state: FSMContext) -> None:
    if await state.get_state() == FSM.Introduction:
        return
    await message.answer("*Доступные команды бота*:\n\n📄 Теоретический материал — /learn\n📐 Тестовые задания — /test\n📀 Установка Astra Linux — /install\n💬 Твой профиль — /profile\n🏅 Таблица лидеров — /board\nℹ Справка — /help")
    await asyncio.sleep(1)
    await message.answer("Если у тебя возникнут какие-либо трудности в использовании бота, ты заметил ошибку в тексте или готов предложить идею по улучшению, пиши нам @exsec2!")


@dp.message(Command(commands=["test"]))
async def test(message: types.Message, state: FSMContext) -> None:
    if await state.get_state() == FSM.Introduction:
        return
    inb1 = InlineKeyboardButton(text='Модуль 1', callback_data="Модуль 1")
    inb2 = InlineKeyboardButton(text='Модуль 2', callback_data="Модуль 2")
    inb3 = InlineKeyboardButton(text='Модуль 3', callback_data="Модуль 3")
    inb4 = InlineKeyboardButton(text='Модуль 4', callback_data="Модуль 4")
    inkb = InlineKeyboardMarkup(inline_keyboard=[[inb1], [inb2], [inb3], [inb4]])
    await message.answer("📋 Меню тестовых заданий:", reply_markup=inkb)


@dp.callback_query(lambda call: "Модуль" in call.data)
async def module(callback_query: types.CallbackQuery, state: FSMContext):
    num = callback_query.data.split(' ')[1]
    back_button = InlineKeyboardButton(text='Назад ◀️', callback_data='Назад')
    if num == '1' or (await db.get_status(callback_query.message.chat.id, str(int(num)-1))).count('1') == 6:
        correct = await db.get_status(callback_query.message.chat.id, num)
        symbols = correct.replace('1', '✅').replace('0', '❌').replace('❌', ' ', 1)
        temp = [f'Тест {num}.1', f'Тест {num}.2', f'Тест {num}.3', f'Тест {num}.4', f'Тест {num}.5', f'Тест {num}.6']
        flag = False
        for i in range(6):
            if flag:
                temp[i] = 'Недоступно'
            else:
                if correct[i] == '1':
                    temp[i] = 'Выполнено ' + temp[i][5:]
                else:
                    flag = True
        inb1 = InlineKeyboardButton(text=f'Тест {num}.1 {symbols[0]}', callback_data=temp[0])
        inb2 = InlineKeyboardButton(text=f'Тест {num}.2 {symbols[1]}', callback_data=temp[1])
        inb3 = InlineKeyboardButton(text=f'Тест {num}.3 {symbols[2]}', callback_data=temp[2])
        inb4 = InlineKeyboardButton(text=f'Тест {num}.4 {symbols[3]}', callback_data=temp[3])
        inb5 = InlineKeyboardButton(text=f'Тест {num}.5 {symbols[4]}', callback_data=temp[4])
        inb6 = InlineKeyboardButton(text=f'Тест {num}.6 {symbols[5]}', callback_data=temp[5])
    else:
        inb1 = InlineKeyboardButton(text=f'Тест {num}.1 ❌', callback_data=f'Недоступно')
        inb2 = InlineKeyboardButton(text=f'Тест {num}.2 ❌', callback_data=f'Недоступно')
        inb3 = InlineKeyboardButton(text=f'Тест {num}.3 ❌', callback_data=f'Недоступно')
        inb4 = InlineKeyboardButton(text=f'Тест {num}.4 ❌', callback_data=f'Недоступно')
        inb5 = InlineKeyboardButton(text=f'Тест {num}.5 ❌', callback_data=f'Недоступно')
        inb6 = InlineKeyboardButton(text=f'Тест {num}.6 ❌', callback_data=f'Недоступно')
    if num in ["3", "4", "5", "6"]:  # Ограничение на доступность
        inb1 = InlineKeyboardButton(text=f'Тест {num}.1 ❌', callback_data=f'Unreleased')
        inb2 = InlineKeyboardButton(text=f'Тест {num}.2 ❌', callback_data=f'Unreleased')
        inb3 = InlineKeyboardButton(text=f'Тест {num}.3 ❌', callback_data=f'Unreleased')
        inb4 = InlineKeyboardButton(text=f'Тест {num}.4 ❌', callback_data=f'Unreleased')
        inb5 = InlineKeyboardButton(text=f'Тест {num}.5 ❌', callback_data=f'Unreleased')
        inb6 = InlineKeyboardButton(text=f'Тест {num}.6 ❌', callback_data=f'Unreleased')
    inkb = InlineKeyboardMarkup(inline_keyboard=[[back_button], [inb1, inb2], [inb3, inb4], [inb5, inb6]])
    await callback_query.message.delete()
    user_data = await state.get_data()
    try:
        await bot.delete_message(callback_query.message.chat.id, user_data["toDelete"][0].message_id)
        await bot.delete_message(callback_query.message.chat.id, user_data["toDelete"][1].message_id)
    except Exception:
        ...
    await callback_query.message.answer("📋 Меню тестовых заданий:", reply_markup=inkb)
    await callback_query.answer()


@dp.callback_query(lambda call: call.data == "Недоступно")
async def unavailable(callback_query: types.CallbackQuery):
    await callback_query.answer(text="Сначала выполни предыдущие задания!", show_alert=True)


@dp.callback_query(lambda call: "Выполнено" in call.data)
async def unavailable(callback_query: types.CallbackQuery):
    await callback_query.answer(text="✅ Ты уже выполнил это задание!")
    await callback_query.message.delete()
    test_num = callback_query.data.split(' ')[1]
    inb = InlineKeyboardButton(text='Назад ◀️', callback_data=f"Модуль {test_num[0]}")
    inkb = InlineKeyboardMarkup(inline_keyboard=[[inb], ])
    photo = FSInputFile(f"./Pictures/Test pictures/Тест {test_num}.png")
    await callback_query.message.answer_photo(photo, f'*Тест {test_num}* — {keys[test_num]["Баллы"]} очков\n\n{keys[test_num]["Пояснение"]}', reply_markup=inkb)


@dp.callback_query(lambda call: call.data == "Назад")
async def back(callback_query: types.CallbackQuery):
    inb1 = InlineKeyboardButton(text='Модуль 1', callback_data="Модуль 1")
    inb2 = InlineKeyboardButton(text='Модуль 2', callback_data="Модуль 2")
    inb3 = InlineKeyboardButton(text='Модуль 3', callback_data="Модуль 3")
    inb4 = InlineKeyboardButton(text='Модуль 4', callback_data="Модуль 4")
    inkb = InlineKeyboardMarkup(inline_keyboard=[[inb1], [inb2], [inb3], [inb4]])
    await callback_query.message.edit_reply_markup(callback_query.id, inkb)
    await callback_query.answer()


keys = {
    "1.1": {
        "Баллы": 5,
        "Пояснение": "GPL (General Public License) — это свободная лицензия, которая позволяет пользователям свободно использовать, изменять и распространять программное обеспечение, защищенное этой лицензией, при условии, что они будут сохранять эти же свободы для других пользователей. Эта лицензия используется в Linux.",
        "Ответ": "Б",
        "Дополнение": "",
        "Подсказка": ""
    },
    "1.2": {
        "Баллы": 5,
        "Пояснение": "Линус Торвальдс является создателем ядра Linux, которое является основой операционной системы. Он также является сторонником открытого программного обеспечения и предоставил ядро Linux под лицензией GPL, которая обеспечивает свободу использования, изменения и распространения программного обеспечения.\nБлагодаря этому решению, Linux стал одной из самых популярных операционных систем в мире.",
        "Ответ": "Г",
        "Дополнение": "",
        "Подсказка": ""
    },
    "1.3": {
        "Баллы": 5,
        "Пояснение": "Дистрибутив Linux — это полноценная операционная система, которая включает в себя ядро Linux и другие программные компоненты, такие как системные утилиты, графические интерфейсы, приложения и т.д.",
        "Ответ": "В",
        "Дополнение": "",
        "Подсказка": ""
    },
    "1.4": {
        "Баллы": 5,
        "Пояснение": "Одним из главных преимуществ Linux является его бесплатность и доступность. Большинство дистрибутивов Linux можно скачать бесплатно из интернета, а также использовать их на своих компьютерах без необходимости покупки лицензии.",
        "Ответ": "Б",
        "Дополнение": "",
        "Подсказка": ""
    },
    "1.5": {
        "Баллы": 10,
        "Пояснение": "Astra Linux — это российская операционная система на базе Linux, которая была разработана специально для использования в государственных структурах, таких как правительство, военные и правоохранительные органы. Она обеспечивает высокую степень защиты данных и имеет сертификаты соответствия российских стандартов безопасности информации.",
        "Ответ": "А",
        "Дополнение": "",
        "Подсказка": ""
    },
    "1.6": {
        "Баллы": 10,
        "Пояснение": "Операционная система Astra Linux предназначена для использования в государственных структурах, где требуется высокий уровень безопасности и защиты конфиденциальной информации. Это могут быть правительственные организации, оборонные, научные и многие другие, где важна секретность данных.\n\nОднако, эта система может быть полезна и для личного использования, особенно для тех, кто хочет обеспечить максимальную защиту своих данных на компьютере.",
        "Ответ": "В",
        "Дополнение": "`Котоботу` было очень интересно читать про Linux и слушать твои ответы на вопросы, но теперь, кажется, он хочет самостоятельно изучить Astra Linux и не знает, где больше всего ему может пригодится эта система 🤔",
        "Стикер": "CAACAgIAAxkBAAEJH51kceqDSc5aOJtX8Q4BmzyPs5aVGQACXwAD29t-AAGEsFSbEa7K4y8E",
        "Подсказка": ""
    },
    "2.1": {
        "Баллы": 5,
        "Пояснение": "Для перехода в текстовый режим консоли в Linux можно воспользоваться сочетанием клавиш `Ctrl+Alt+F1`. Это переключит вас на первую консоль, где вы сможете войти в текстовый режим, ввести команды и работать с системой.\nДля возврата в графический режим нужно нажать сочетание клавиш `Ctrl+Alt+F7`.",
        "Ответ": "Б",
        "Дополнение": "",
        "Подсказка": ""
    },
    "2.2": {
        "Баллы": 5,
        "Пояснение": "Когда вы первый раз запускаете систему в текстовом режиме консоли, то в самой первой строке будет отображено название и версия используемого дистрибутива Linux.\nЭто может быть полезно при отладке и поиске проблем в процессе загрузки системы.",
        "Ответ": "А",
        "Дополнение": "",
        "Подсказка": "Открой консоль на своем ПК сочетанием клавиш Ctrl+Alt+F1"
    },
    "2.3": {
        "Баллы": 5,
        "Пояснение": "Символ # используется в приглашении командной строки для обозначения пользователя с правами администратора, также известного как суперпользователь (root). Когда пользователь работает от имени суперпользователя, он имеет полный доступ к системе и может выполнять любые операции. Символ $ используется для обозначения обычного пользователя, который не имеет таких привилегий.",
        "Ответ": "Г",
        "Дополнение": "",
        "Подсказка": ""
    },
    "2.4": {
        "Баллы": 5,
        "Пояснение": "Рабочий стол в Astra Linux представляет собой рабочее пространство, где пользователь может запустить приложения и управлять файлами. Это основной интерфейс для работы с операционной системой, который обычно содержит иконки приложений, панель задач, меню и другие элементы управления.",
        "Ответ": "Б",
        "Дополнение": "",
        "Подсказка": ""
    },
    "2.5": {
        "Баллы": 10,
        "Пояснение": "Терминал Fly - это эмулятор терминала, который позволяет работать с командной строкой и запускать приложения в операционной системе Astra Linux. Это важный инструмент для системных администраторов и опытных пользователей, которые предпочитают работать с командной строкой, а не с графическим интерфейсом.\n\nТерминал Fly включает в себя множество функций, таких как поддержка многих языков программирования, возможность копирования и вставки текста, поддержка многих консольных команд и т.д.",
        "Ответ": "В",
        "Дополнение": "",
        "Подсказка": ""
    },
    "2.6": {
        "Баллы": 10,
        "Пояснение": "Автоматический вход - это функция, которая позволяет пользователям войти в операционную систему без ввода логина и пароля. Эта функция может быть полезна в случаях, когда нужно быстро запустить систему без ввода учетных данных.\n\nИнструкцию по его настройке ты можешь найти в конце 2 Модуля 😉",
        "Ответ": "Б",
        "Дополнение": "`Котобот`, посмотрев на тебя, тоже решил установить себе новенькую Astra Linux и уже начал активно ей пользоваться 🖥\n\nНо так уж вышло, что он очень часто отвлекается от работы, и экран его монитора постоянно гаснет... Поэтому ему приходится вводить пароль снова и снова 😤",
        "Стикер": "CAACAgIAAxkBAAEJJ79kdiQYlLg6fB5wWRS4s1ZbgjT0yAACYgAD29t-AAGOFzVmmxPyHC8E",
        "Подсказка": ""
    }
}


@dp.callback_query(lambda call: "Тест" in call.data)
async def module(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    if keys[callback_query.data.split(' ')[1]]["Дополнение"] != '':
        mes1 = await callback_query.message.answer(keys[callback_query.data.split(' ')[1]]["Дополнение"])
        await asyncio.sleep(1)
        mes2 = await callback_query.message.answer_sticker(keys[callback_query.data.split(' ')[1]]["Стикер"])
        await asyncio.sleep(2)
        await state.update_data(toDelete=[mes1, mes2])
    inb1 = InlineKeyboardButton(text='А', callback_data=f"Check А {callback_query.data.split(' ')[1]}")
    inb2 = InlineKeyboardButton(text='Б', callback_data=f"Check Б {callback_query.data.split(' ')[1]}")
    inb3 = InlineKeyboardButton(text='В', callback_data=f"Check В {callback_query.data.split(' ')[1]}")
    inb4 = InlineKeyboardButton(text='Г', callback_data=f"Check Г {callback_query.data.split(' ')[1]}")
    inb5 = InlineKeyboardButton(text='Назад ◀️', callback_data=f"Модуль {callback_query.data.split(' ')[1][0]}")
    if keys[callback_query.data.split(' ')[1]]["Подсказка"] != '':
        inb6 = InlineKeyboardButton(text='Подсказка 💡', callback_data=f"Подсказка {callback_query.data.split(' ')[1]}")
        inkb = InlineKeyboardMarkup(inline_keyboard=[[inb1, inb2], [inb3, inb4], [inb6], [inb5]])
    else:
        inkb = InlineKeyboardMarkup(inline_keyboard=[[inb1, inb2], [inb3, inb4], [inb5]])
    photo = FSInputFile(f"./Pictures/Test pictures/{callback_query.data}.png")
    await callback_query.message.answer_photo(photo, f'*{callback_query.data}* — {keys[callback_query.data.split(" ")[1]]["Баллы"]} очков', reply_markup=inkb)
    await callback_query.answer()


def get_badge(score: int) -> str:
    badges = ["👨‍💻 Новичок", "🌐 Open-Source деятель", "🖥 UNIX-мастер", "🧙‍♂️ Root-волшебник", "🦸‍♂️ Пользователь-супергерой"]
    badge = ''
    if score < 20:
        badge = badges[0]
    elif score < 40:
        badge = badges[1]
    elif score < 60:
        badge = badges[2]
    elif score < 80:
        badge = badges[3]
    elif score < 100:
        badge = badges[4]
    return badge


@dp.callback_query(lambda call: "Check" in call.data)
async def module(callback_query: types.CallbackQuery):
    answer = callback_query.data.split(' ')[1]
    test_num = callback_query.data.split(' ')[2]
    if answer == keys[test_num]["Ответ"]:
        await callback_query.answer(text=f'Верно ✅ (+{keys[test_num]["Баллы"]})')
        prev_b = get_badge(int(await db.get_score(callback_query.message.chat.id)))
        await db.set_score(callback_query.message.chat.id, keys[test_num]["Баллы"])
        cur_b = get_badge(int(await db.get_score(callback_query.message.chat.id)))
        if prev_b != cur_b:
            await callback_query.message.answer(f"Ты делаешь большие успехи! Поздравляем с новым достижением 🎉\n\nТвой новый бейдж:\n*{cur_b}*")
        await callback_query.message.edit_caption(callback_query.inline_message_id, f'*Тест {test_num}* — {keys[test_num]["Баллы"]} очков\n\n{keys[test_num]["Пояснение"]}')
        if int(test_num[2]) < 6:
            next_num = test_num[:2] + str(int(test_num[2]) + 1)
            inb1 = InlineKeyboardButton(text='Назад ◀️', callback_data=f"Модуль {test_num[0]}")
            inb2 = InlineKeyboardButton(text='Далее ▶️', callback_data=f"Тест {next_num}")
            inkb = InlineKeyboardMarkup(inline_keyboard=[[inb1], [inb2]])
            await callback_query.message.edit_reply_markup(callback_query.id, inkb)
        else:
            inb1 = InlineKeyboardButton(text='Назад ◀️', callback_data=f"Модуль {test_num[0]}")
            inkb = InlineKeyboardMarkup(inline_keyboard=[[inb1], ])
            await callback_query.message.edit_reply_markup(callback_query.id, inkb)
        await db.set_status(callback_query.message.chat.id, test_num[0], test_num[2])
    else:
        await callback_query.answer(text="Неверно ❌", show_alert=True)


@dp.message(Command(commands=["learn"]))
async def learn(message: types.Message, state: FSMContext) -> None:
    if await state.get_state() == FSM.Introduction:
        return
    inb1 = InlineKeyboardButton(text='Модуль 1', web_app=WebAppInfo(url='https://astralinuxedu.tilda.ws/page1'))
    module1 = await db.get_status(message.chat.id, "1")
    if module1.count("1") == 6:
        inb2 = InlineKeyboardButton(text='Модуль 2', web_app=WebAppInfo(url='https://astralinuxedu.tilda.ws/page2'))
        inb3 = InlineKeyboardButton(text='Модуль 3 ❌', callback_data="Unreleased")  # Ограничение на доступность
        inb4 = InlineKeyboardButton(text='Модуль 4 ❌', callback_data="Unreleased")  # Ограничение на доступность
    else:
        inb2 = InlineKeyboardButton(text='Модуль 2 ❌', callback_data="Закрыто")
        inb3 = InlineKeyboardButton(text='Модуль 3 ❌', callback_data="Unreleased")  # Ограничение на доступность
        inb4 = InlineKeyboardButton(text='Модуль 4 ❌', callback_data="Unreleased")  # Ограничение на доступность
    inkb = InlineKeyboardMarkup(inline_keyboard=[[inb1], [inb2], [inb3], [inb4]])
    await message.answer("📝 Теоретический материал:", reply_markup=inkb)


@dp.callback_query(lambda call: call.data == "Закрыто")
async def unavailable(callback_query: types.CallbackQuery):
    await callback_query.answer(text="Сначала выполни тестовые задания предыдущего модуля!", show_alert=True)


@dp.callback_query(lambda call: call.data == "Unreleased")  # Ограничение на доступность
async def unreleased(callback_query: types.CallbackQuery):
    await callback_query.answer(text="На данный момент этот модуль ещё не добавлен в бота :(", show_alert=True)


@dp.callback_query(lambda call: "Подсказка" in call.data)
async def tip(callback_query: types.CallbackQuery):
    await callback_query.answer(text=keys[callback_query.data.split(' ')[1]]["Подсказка"], show_alert=True)


@dp.message(Command(commands=["board"]))
async def board(message: types.Message, state: FSMContext) -> None:
    if await state.get_state() == FSM.Introduction:
        return
    await message.answer(await db.get_rating(str(message.chat.id)))
    await asyncio.sleep(1)
    await message.answer_sticker("CAACAgIAAxkBAAEJIRdkco6bwqrAOQZplX2lftPbNE1x4wACcAAD29t-AAHqAAG3tyaYON0vBA")


@dp.message(Command(commands=["profile"]))
async def profile(message: types.Message, state: FSMContext) -> None:
    if await state.get_state() == FSM.Introduction:
        return
    name = message.from_user.first_name
    surname = message.from_user.last_name
    if name is None:
        name = ''
    if surname is None:
        surname = ''
    if name is None and surname is None:
        name = 'Неизвестный пользователь'
    score = await db.get_score(message.chat.id)
    position = (await db.get_position(str(message.chat.id))) + ' Место'
    if position == '1 Место':
        position += " 🥇"
    elif position == '2 Место':
        position += " 🥈"
    elif position == '3 Место':
        position += " 🥉"
    badge = get_badge(int(score))
    await message.answer(f"🔖 *Твой профиль:*\n\n*Имя:* {name} {surname}\n*Бейдж:* {badge}\n*Рейтинг:* {position}\n*Очки:* {score} 🪙")


@dp.shutdown()
async def on_shut():
    print("Бот выключен")


if __name__ == "__main__":
    bot.parse_mode = 'MARKDOWN'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling(bot))
