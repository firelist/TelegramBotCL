from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot
from aiogram import types, Dispatcher
from database.sql_commands import Database

async def start_button(massage: types.Message):
    print(massage)
    Database().sql_insert_users(
        telegram_id=massage.from_user.id,
        username=massage.from_user.username,
        first_name=massage.from_user.first_name,
        last_name=massage.from_user.last_name,
    )
    await massage.reply(text=f"Hello {massage.from_user.first_name}")


async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Следуйщая Викторина",
        callback_data="button_call_1"
    )
    button_call_2 = InlineKeyboardButton(
        "Следуйщая Викторина",
        callback_data="button_call_2"
    )
    markup.row(
        button_call_1,
        button_call_2
    )

    question = "Who invented Python"
    options = [
        "Voldemort",
        "Harry Potter",
        "Linus Torvalds",
        "Guido Van Rossum"
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=options,
        is_anonymous=False,
        type="quiz",
        correct_option_id=3,
        reply_markup=markup
    )


async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Male",
        callback_data="answer_male"
    )
    button_call_2 = InlineKeyboardButton(
        "Female",
        callback_data="answer_female"
    )
    markup.row(
        button_call_1,
        button_call_2
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Male or Female',
        reply_markup=markup
    )


async def answer_male(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="You are male"
    )


async def answer_female(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="You are female"
    )

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=["start"])
    dp.register_message_handler(quiz_1, commands=["quiz"])
    # dp.register_message_handler(quiz_2, commands=["quiz2"])
    dp.register_callback_query_handler(quiz_2,  lambda call: call.data == "button_call_1")
    dp.register_callback_query_handler(answer_male,  lambda call: call.data == "answer_male")
    dp.register_callback_query_handler(answer_female,  lambda call: call.data == "answer_female")