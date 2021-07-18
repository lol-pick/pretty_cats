import config
import logging

from cat import Cats

from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt
from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

button_agree = KeyboardButton("Да🐱!")
button_dis = KeyboardButton("Нет, я собака🐶")

button_agree_1 = KeyboardButton("Да!")
button_dis_2 = KeyboardButton("Нет, спасибо")

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_agree).add(button_dis)
greet_kb_1 = (
    ReplyKeyboardMarkup(resize_keyboard=True).add(button_agree_1).add(button_dis_2)
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["subscribe"])
async def subscribe(msg: types.Message):
    await msg.answer("Нажмите: /start, чтобы посмотреть что я умею :)")


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer(
        """Привет! Я бот, который немного знает о котиках🐱. Хочешь расскажу он них немного больше??!""",
        reply_markup=greet_kb,
    )


@dp.message_handler(text=["Нет, я собака🐶"])
async def process_command_1(message: types.Message):
    await message.answer("Очень жаль, когда будет время заходи((😔")
    await message.reply(
        "Убираю сообщения на выбор, если захотите начать все с начала, нажмите на: /start",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler(text=["Да🐱!"])
async def process_command_1(message: types.Message):
    await message.answer(
        "Отлично! Следуй инструкции: Напиши кодовое слово /cat и породу кошки с большой буквы через пробел,\
 например: /cat Персидская кошка или /cat Персидская",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler(commands=["cat"])
async def give_info(msg: types.Message):
    url = Cats.search_cat(msg.text[5:])
    if url != -1:
        review = Cats.give_photo_cat(url)
        info, moments = Cats.give_info_cat(url)
        text = ""
        for el in info:
            text = text + "◾️ " + el + "\n"
        text += "\n"
        for el in moments:
            text = text + "🐾 " + el + "\n"
        await msg.answer(
            f"{fmt.hide_link(review)}" + text, parse_mode=types.ParseMode.HTML
        )
        await msg.answer(
            "Хотите побольше прочитать про данную породу кошки??",
            reply_markup=greet_kb_1,
        )

        @dp.message_handler(text=["Да!"])
        async def give_url(msg: types.Message):
            await msg.answer(
                "Тогда просто перейдите по ссылке ниже:\t" + url,
                reply_markup=ReplyKeyboardRemove(),
                disable_web_page_preview=True,
            )
            await msg.answer("Чтобы начать все сначала, нажмите: /start")

    else:
        await msg.answer(
            "Увы такой породы я не знаю, либо Вы написали неправильно, тогда попробуйте еще раз!"
        )
        await msg.answer("Если вы запутались, то нажмите на кнопку: /start")


@dp.message_handler(text=["Нет, спасибо"])
async def process_rm_command(message: types.Message):
    await message.reply(
        "Убираю сообщения на выбор, если захотите начать все с начала, нажмите на: /start",
        reply_markup=ReplyKeyboardRemove(),
    )


# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
