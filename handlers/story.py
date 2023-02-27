from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import time
from collections import defaultdict


database = defaultdict(int)
mobs = {}
tg_story_router = Router()


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


@tg_story_router.callback_query(F.data == "False")
async def decr(callback: types.CallbackQuery):
    database[callback.message.from_user.id] -= 1
    if database[callback.message.from_user.id] <= 0:
        await callback.message.delete_reply_markup()
        await callback.message.answer(f"{mobs[callback.message.from_user.id]} съел колобка.")
        await start(callback.message)
    else:
        await callback.message.answer(f"Неправильно! Осталось {mobs[callback.message.from_user.id]} попыток")


@tg_story_router.message(Command(commands="start"))
async def start(message: types.Message):
    kb = [[types.InlineKeyboardButton(text="Начать", callback_data='one')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    database[message.from_user.id] = 3
    await message.answer(reply_markup=keyboard, text="Представляю интерактивное приключение. В этом приключении нам надо помочь колобку добраться до дома. Чтобы добраться до дома нужно будет ответить на 2 вопроса у каждого персонажа, которые встанут на пути у колобка. Проект предоставлен в виде \"вопрос-ответ\".")


@tg_story_router.callback_query(F.data == "one")
async def one(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.one)
    await callback.message.delete_reply_markup()
    mobs[callback.message.from_user.id] = "Заяц"
    await callback.message.answer("""Катится колобок по дороге, а навстречу ему заяц:
— Колобок, колобок! Я тебя съем.
— Не ешь меня, косой зайчик! Я тебе на вопросы отвечу и ты меня отпустишь.""")
    time.sleep(1)
    kb = [
        [
            types.InlineKeyboardButton(
                text="считывания данных с клавиатуры", callback_data="False")
        ],
        [
            types.InlineKeyboardButton(
                text="вывода данных на экран", callback_data="True")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer(text="Команда print() используется для", reply_markup=keyboard)


@tg_story_router.callback_query(Form.one, F.data == "True")
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
    mobs[callback.message.from_user.id] = "Волк"
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
