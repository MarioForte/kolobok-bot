from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import time
from collections import defaultdict


database = defaultdict(int) # База данных «ключ-значение» для хранения количества попыток пользователя с числовым значением по умолчанию
mobs = {} # По такому же принципу хранит того, кто съел колобка на данном этапе
tg_story_router = Router() # Идентификация роутера


# Описание десяти шагов истории
class Form(StatesGroup):
    one = State()
    two = State()
    three = State()
    four = State()
    five = State()
    six = State()
    seven = State()
    eight = State()
    nine = State()
    ten = State()


# Обработчик для неправильного ответа
@tg_story_router.callback_query(F.data == "False")
async def decr(callback: types.CallbackQuery):
    database[callback.from_user.id] -= 1 # Вычитает одну попытку
    if database[callback.from_user.id] <= 0: # если не осталось попыток
        await callback.message.delete_reply_markup() # удаление клавиатуры
        await callback.message.answer(f"{mobs[callback.from_user.id]} съел колобка.")
        await start(callback.message) # рестарт
    else:
        await callback.message.answer(f"Неправильно! Осталось {database[callback.from_user.id]} попыток")


@tg_story_router.message(Command(commands="start"))
async def start(message: types.Message):
    kb = [[types.InlineKeyboardButton(text="Начать", callback_data='one')]] # создание клавиатуры, перебрасивыющей на первый вопрос
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb) 
    database[message.from_user.id] = 3 # Добавление трех попыток пользователю
    await message.answer(reply_markup=keyboard,
                         text="Представляю интерактивное приключение. В этом приключении нам надо помочь колобку добраться до дома. Чтобы добраться до дома нужно будет ответить на 2 вопроса у каждого персонажа, которые встанут на пути у колобка. Проект предоставлен в виде \"вопрос-ответ\".")


@tg_story_router.callback_query(F.data == "one")
async def one(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.one) # устанавливаем первый вопрос
    await callback.message.delete_reply_markup() # удаляем прошлую клавиатуру из сообщения
    mobs[callback.from_user.id] = "Заяц" # установка того, кто съест колобка при окончании попыток
    await callback.message.answer("""Катится колобок по дороге, а навстречу ему заяц:
— Колобок, колобок! Я тебя съем.
— Не ешь меня, косой зайчик! Я тебе на вопросы отвечу и ты меня отпустишь.""", reply_markup=ReplyKeyboardRemove())
    time.sleep(1) # пауза в одну секунду
    kb = [
        [
            types.InlineKeyboardButton(
                text="считывания данных с клавиатуры", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="вывода данных на экран", callback_data="True")
        ]
    ] # варианты ответа
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb) 
    await callback.message.answer(text="Команда print() используется для", reply_markup=keyboard)


@tg_story_router.callback_query(Form.one, F.data == "True") # Условие and (И): Ответ должен быть от первого вопроса и правильным.
async def two(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.two)
    await callback.message.delete_reply_markup()
    await callback.message.answer("Правильно! Следующий вопрос.")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="/", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="//", callback_data="True")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Оператор целочисленного деления, который используется для деления двух операндов с результатом, показывающим только цифры перед десятичной точкой.", reply_markup=keyboard)


@tg_story_router.callback_query(Form.two, F.data == "True")
async def three(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.three)
    await callback.message.delete_reply_markup()
    mobs[callback.from_user.id] = "Волк"
    await callback.message.answer("Правильно! И покатился колобок себе дальше.")
    await callback.message.answer("""Катится колобок, а навстречу ему волк:
— Колобок, колобок! Я тебя съем!

— Не ешь меня, серый волк! Я тебе на вопросы отвечу и ты меня отпустишь, — сказал колобок""")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="Останавливает выполнение всего кода.", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="Останавливает цикл.", callback_data="True")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Что делает оператор break?", reply_markup=keyboard)


@tg_story_router.callback_query(Form.three, F.data == "True")
async def four(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.four)
    await callback.message.delete_reply_markup()
    await callback.message.answer("Правильно! Следующий вопрос.")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="Продолжает выполнять цикл, до оператора break.", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="Начинает следующий проход цикла, минуя оставшееся тело цикла.", callback_data="True")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Что делает оператор continue?", reply_markup=keyboard)


@tg_story_router.callback_query(Form.four, F.data == "True")
async def five(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.five)
    await callback.message.delete_reply_markup()
    mobs[callback.from_user.id] = "Медведь"
    await callback.message.answer("Правильно!")
    await callback.message.answer("""И покатился себе дальше; только волк его и видел!
Катится колобок, а навстречу ему медведь:

— Колобок, колобок! Я тебя съем.
— Не ешь меня, косолапый! Я тебе на вопросы отвечу и ты меня отпустишь, — сказал колобок""")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="Объект, принимающий аргументы и возвращающий значение", callback_data="True")
        ],
        [
            types.InlineKeyboardButton(
                text="Структура, определяющая поведение объекта", callback_data="False")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Что такое функция?", reply_markup=keyboard)


@tg_story_router.callback_query(Form.five, F.data == "True")
async def six(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.six)
    await callback.message.delete_reply_markup()
    await callback.message.answer("Правильно! Следующий вопрос.")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="function", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="def", callback_data="True")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Какое ключевое слово используется для создания функции?", reply_markup=keyboard)


@tg_story_router.callback_query(Form.six, F.data == "True")
async def seven(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.seven)
    await callback.message.delete_reply_markup()
    mobs[callback.from_user.id] = "Лис"
    await callback.message.answer("Правильно!")
    await callback.message.answer("""И опять укатился, только медведь его и видел!
Катится, катится «колобок, а навстречу ему лис:

— Здравствуй, колобок! Какой ты хорошенький. Колобок, колобок! Я тебя съем.
— Не ешь меня, лис! Я тебе на вопросы отвечу и ты меня отпустишь, — сказал колобок:""")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="Чтобы указать, что эта переменная имеет самое важное значение в программе", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="Чтобы переменную можно было изменять за пределами текущей области видимости", callback_data="True")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Для чего нужно ключевое слово global?", reply_markup=keyboard)


@tg_story_router.callback_query(Form.seven, F.data == "True")
async def eight(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.eight)
    await callback.message.delete_reply_markup()
    await callback.message.answer("Правильно! Следующий вопрос.")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="Функция, которая курсирует между модулями", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="Функция которая возвращает саму себя", callback_data="True")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Что такое рекурсивная функция?", reply_markup=keyboard)


@tg_story_router.callback_query(Form.eight, F.data == "True")
async def nine(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.nine)
    await callback.message.delete_reply_markup()
    mobs[callback.from_user.id] = "Дедка"
    await callback.message.answer("Правильно! И покатился колобок себе дальше.")
    await callback.message.answer("""Докатился колобок обратно до избушки к старику и старухе.
Здравствуй, колобок! Где ты был? Какой ты хорошенький. Колобок, колобок! Я тебя съем.
— Не ешь меня, старушка! Я тебе на вопросы отвечу и ты меня отпустишь, — сказал колобок:""")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="строковая операция для получения подстроки или некоторой части списка.", callback_data="True")
        ],
        [
            types.InlineKeyboardButton(
                text="числовая операция для создания подстроки или некоторой части списка", callback_data="False")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("Срезы – это", reply_markup=keyboard)


@tg_story_router.callback_query(Form.nine, F.data == "True")
async def ten(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.ten)
    await callback.message.delete_reply_markup()
    await callback.message.answer("Правильно! Следующий вопрос.")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="Числа, множества", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="Числа, строки, кортежи", callback_data="True")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer("В качестве ключа словаря могут быть использованы:", reply_markup=keyboard)


@tg_story_router.callback_query(Form.ten, F.data == "True")
async def result(callback: types.CallbackQuery, state: FSMContext):
    await state.clear() # очистка шагов истории
    await callback.message.delete_reply_markup() # удаление клавиатуры
    await callback.message.answer("""— Какая славно! — сказала старушка. — Но ведь я, колобок, стара стала, плохо слышу; сядь-ка ко мне ближе
— Спасибо, колобок!  И съела колобка…""",
                                  reply_markup=ReplyKeyboardMarkup(
                                      keyboard=[
                                          [
                                              KeyboardButton(text="/start"), # добавление кнопки перезапуска
                                          ]
                                      ],
                                      resize_keyboard=True, # адаптивный размер кнопки
                                  ))
