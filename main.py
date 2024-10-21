import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '7286912828:AAHYG3t_AGNGMb747z2WqcJn2i-IBjsczl4'

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class Registration(StatesGroup):
    waiting_for_name = State()

button_news = KeyboardButton('Yangiliklar📰')
button_register = KeyboardButton('Contact📞')
button_feedback = KeyboardButton('Otziv Qoldirish📨')
button_help = KeyboardButton('Yordam🤖')
button_star = KeyboardButton('Evaluate the service⭐')
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(button_news, button_register)
menu_keyboard.add(button_feedback, button_help)
menu_keyboard.add(button_star)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assallomu Aleykum! Botga xush kelibsiz. Iltimos, ismingizni kiriting:")
    await Registration.waiting_for_name.set()

@dp.message_handler(state=Registration.waiting_for_name, content_types=types.ContentTypes.TEXT)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    await state.update_data(user_name=user_name)

    await state.finish()

    await message.reply(f"Rahmat, {user_name}! Ro'yxatdan o'tdingiz. Birini tanlang 👇🏻", reply_markup=menu_keyboard)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assallomu Aleykum! Botga xush kelibsiz. Iltimos, ismingizni kiriting:")
    await Registration.waiting_for_name.set()

@dp.message_handler(lambda message: message.text == "Yangiliklar📰")
async def send_news(message: types.Message):
    await message.reply(
        """Yuqori lavozimdagi mansabdor pora bilan qo‘lga olindi
Toshkentda davlat vazirliklaridan biri yuqori lavozimdagi mansabdor pora olishda ayblanib qo‘lga olindi. Huquq-tartibot organlari ma’lumotlariga ko‘ra, pora miqdori 50 ming dollarni tashkil qilgan. Mansabdor shaxs noqonuniy qurilish loyihalariga yordam berishda gumon qilinmoqda.

Samarqandda antikorrupsiya operatsiyasi natijasida bir necha shahar hokimiyati xodimlari qo‘lga olindi. Dastlabki ma’lumotlarga ko‘ra, jinoyatchilar shahar infratuzilmasini rivojlantirish uchun ajratilgan 1 milliard so‘mni o‘zlashtirganlar"""
    )


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.message_handler(lambda message: message.text == "Contact📞")
async def register_user(message: types.Message):
    website_button = InlineKeyboardButton(text="Saytimiz", url="https://tushungan.netlify.app/")

    keyboard = InlineKeyboardMarkup().add(website_button)

    await message.reply("Bizning kontakt ma'lumotlarimiz:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Otziv Qoldirish📨")
async def get_feedback(message: types.Message):
    await message.reply("Iltimos, fikr-mulohazangizni yuboring...")


@dp.message_handler(lambda message: message.text == "Yordam🤖")
async def send_help(message: types.Message):
    help_text = (
        "Yordam haqida ma'lumot:\n\n"
        "* /start* - Botni ishga tushiradi va ro'yxatdan o'tish jarayonini boshlaydi.\n"
        "* Yangiliklar📰* - O'zbekiston korruptsiyasi haqidagi so'nggi yangiliklarni ko'rsatadi.\n"
        "* Contact📞* - Bizning kontakt ma'lumotlarimizni ko'rsatadi.\n"
        "* Otziv Qoldirish📨* - Sizning fikr va mulohazalaringizni qabul qiladi.\n"
        "* Evaluate the service⭐* - Xizmatni baholash uchun so'rov yuboradi.\n\n"
        "Qo'shimcha ma'lumot uchun, iltimos, biz bilan bog'laning yoki quyidagi havolalardan foydalaning:\n"
        "[Saytga o'tish](https://tushungan.netlify.app/)\n"
    )

    await message.reply(help_text, parse_mode='Markdown')


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_rating_keyboard():
    keyboard = InlineKeyboardMarkup()

    for i in range(1, 6):
        button = InlineKeyboardButton(text='⭐' * i, callback_data=f'rating_{i}')
        keyboard.add(button)

    return keyboard


@dp.message_handler(lambda message: message.text == "Evaluate the service⭐")
async def evaluate_service(message: types.Message):
    await message.reply(
        "Iltimos, xizmatimizni baholang. Har bir yulduzni bosing, sizga qanchalik yoqdi:",
        reply_markup=create_rating_keyboard()
    )


@dp.callback_query_handler(lambda c: c.data.startswith('rating_'))
async def handle_rating(callback_query: types.CallbackQuery):
    rating = int(callback_query.data.split('_')[1])

    await bot.send_message(callback_query.from_user.id, f"Rahmat! Siz {rating} yulduz bilan baholadingiz.")

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
