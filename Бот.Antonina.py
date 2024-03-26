from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext



API_TOKEN = "6593751485:AAE0UTOblOQ42acElTVRktbLYkBXXHdEXto"
storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage)


class ProfileStatesgroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    description = State()


def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("/create"))
    return kb


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("welcome! so as to create profile - type /create",
                         reply_markup=get_kb())


@dp.message_handler(commands=["create"])
async def cmd_create(message: types.Message):
    await message.answer("Let's create your profile! to begin with , send me your photo")
    await ProfileStatesgroup.photo.set()  # устанавливаем состояние фото с помощью метода set


@dp.message_handler(content_types=["photo"], state=ProfileStatesgroup.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await message.reply(text="send me your name")
    await ProfileStatesgroup.next()


@dp.message_handler(state=ProfileStatesgroup.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await message.answer("send me your age")
    await ProfileStatesgroup.next()


@dp.message_handler(state=ProfileStatesgroup.age)
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text
    await message.answer("tell me youself")
    await ProfileStatesgroup.next()  


@dp.message_handler(state=ProfileStatesgroup.description)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await message.answer("your profile create")
    await state.finish()    



if __name__=="__main__":
    executor.start_polling(dp,
                           skip_updates=True)
