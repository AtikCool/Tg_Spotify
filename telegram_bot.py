import sys
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.fsm.context import FSMContext
import os
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from parser_spotify import *

from aiogram.types import FSInputFile
from aiogram.filters import CommandStart, Command
import download_songs
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

TOKEN = '6699193279:AAGsTofjJtbY70qk2VPr04k8qfatcDGf6Sc'
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class UserState(StatesGroup):
    wait_playlist = State()


async def send_files_in_folder(folder_path, user_id):
    # Получаем список файлов в папке
    files = os.listdir(folder_path)

    # Отправляем каждый файл пользователю
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            await bot.send_message(user_id, file_path)
            file = FSInputFile(path=file_path, filename=file_name)
            await bot.send_document(user_id, file)
    download_songs.delete_path(user_id)



@dp.message(Command('start'))
async def start(message:types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Скачать песню', callback_data='download_song')
    builder.button(text='Скачать плейлист',callback_data="download_playlist")
    await message.answer("Some text here", reply_markup=builder.as_markup())

#Здесь начинается функции скачивания плейлиста
async def get_playlist_url(message:types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
        text='Здравствуйте!Это бот по скачиванию песен прямо из вашего плейлиста  Spotify,введите ссылку на ваш Spotify плейлист')
    await state.set_state(UserState.wait_playlist)

@dp.callback_query()
async def get_playlist_url_button(callback: types.CallbackQuery, message:types.Message, state: FSMContext):
    await get_playlist_url(message, state)

@dp.message(Command("download_playlist_songs"))
async def get_playlist_url_command(message:types.Message, state: FSMContext):

    await get_playlist_url(message, state)


@dp.message(UserState.wait_playlist)
async def download_playlist_songs(message: types.Message, state: FSMContext):
    # Обработка полученного названия песни
    playlist_url = message.text
    try:
        playlist_id = playlist_url.split('/')[4].split('?')[0]
    except IndexError:
        await bot.send_message(chat_id=message.from_user.id, text='Возможно вы вели неправильный URL.Перепроверьте свой URL адрес,убедившись что ссылка рабочая,вызовите команду /download_playlist_songs заново,и введите корректный URL адрес на свой плейлист')
    playlist_data = get_playlist_data(playlist_url)

    #download_songs.download_music(playlist_url, message.from_user.id)
    # Далее можно добавить логику обработки полученного названия плейлиста
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.RECORD_VOICE)
    await message.bot.send_photo(chat_id=message.from_user.id, photo=str(playlist_data['playlist_img']),
        caption=f"Вы запросили скачать песни из плейлиста под названием{playlist_data['playlist_name']}. Скачивание может занять несколько минут")

    # Получаем идентификатор пользователя
    user_id = message.from_user.id
    # Указываем путь к папке с файлами
    folder_path = f'C:/Users/atikc/PycharmProjects/TgSpotify/songs/{user_id}/'
    print(folder_path)
    # Отправляем файлы пользователю
    download_songs.download_music(playlist_id, user_id)
    await send_files_in_folder(folder_path, user_id)
    await state.clear()
#Здесь заканчивается функции загрузки из плейлиста

    



    # Initialize Bot instance with a default parse mode which will be passed to all API calls


    # And the run events dispatching
async def main():
   await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())






