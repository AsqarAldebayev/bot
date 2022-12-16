import logging
from aiogram import Bot, Dispatcher, executor, types

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ChatType, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = '5627414647:AAEHUWxbNQ1USonlZn0raOXWHfEA0vh4Z14'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class dialog(StatesGroup):
	manzil = State()
	telefon = State()
	murojaat= State()


user_dict = {}

lang={
	'kr':{
	1:" Famılıya atıńızdı kiritiń 👤",
 	2:" Adresińizdi kiritiń 🏢",
 	3:" Telefon nomerińizdi kirgiziw ushın tuymeni basıń📞☎️",
 	4:" Shaqırıq mazmunın kiritiń 📨",
 	5:" Tuymeni basıń"
	},
	'uz':{
	1:"Familiya ismingizni kiriting 👤",
	2:"Manzilingizni kiriting 🏢",
	3:"Telefon raqamingizni kiritish uchun tugmani bosing📞☎️",
	4:"Murojaat mazmunini kiriting 📨",
	5:"Tugmani bosing"
	},
	'ru':{
	1: "Введите свою фамилию 👤",
	2: "Введите свой адрес 🏢",
	3: "Нажмите кнопку, чтобы ввести свой номер телефона📞 ☎️",
	4: "Введите содержание обращение📨",
	5: "Нажмите кнопку"
	}

}

#User sinfi yaratiladi va ma'lumotlar ushbu sinfda saqlanadi
class User:
	def __init__(self, name):
		self.name = name
		self.manzil = None
		self.telefon = None
		self.id = None


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	categoryMenu = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Qaraqalpaq🇬🇦", callback_data="kr"),
        InlineKeyboardButton(text="O'zbek🇸🇱", callback_data="uz"),
    ],
    [
        InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru"),
    ],
])

	await message.answer("<b>***Assalomu alaykum***\n Hurmatli fuqaro, bu bot orqali siz, Qoraqalpog'iston Respublikasi Ellikqal'a tumani hokimligiga o'z murojaatingizni yo'llashingiz mumkin✅. \n\nTilni tanlang!🔽</b>", parse_mode="HTML", reply_markup=categoryMenu)


@dp.callback_query_handler()
async def start_command(call:CallbackQuery, state: FSMContext):
	await call.message.delete()
	global language
	language=call.data
	await call.message.answer(f"{lang[call.data][1]}")
	await dialog.manzil.set()


@dp.message_handler(state=dialog.manzil)
async def start_command2(message: Message, state: FSMContext):
	chat_id = message.chat.id
	name = message.text
	user = User(name)
	user.id=chat_id
	user_dict[chat_id] = user
	await message.answer(f"{lang[language][2]}")
	await dialog.telefon.set()


@dp.message_handler(state=dialog.telefon)
async def start_command3(message: Message, state: FSMContext):
	chat_id = message.chat.id
	adres = message.text
	user = user_dict[chat_id]
	user.manzil = adres
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
	keyboard.add(types.InlineKeyboardButton(text=f"{lang[language][3]}", request_contact=True))
	await message.answer(f"{lang[language][3]}", reply_markup=keyboard)
	await dialog.murojaat.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=dialog.murojaat)
async def start_command4(message: Message, state: FSMContext):
	if message.contact:
		chat_id = message.chat.id
		phone = message.contact.phone_number
		user = user_dict[chat_id]
		user.telefon = phone
		await message.answer(f"{lang[language][4]}")
		await state.finish()
	else:
		await message.answer(f"{lang[language][5]}")
		await dialog.telefon.set()


@dp.message_handler(chat_type=[ChatType.SUPERGROUP, ChatType.GROUP])
async def send_welcome2(message: types.Message):
	global group_id
	group_id=message.chat.id
	print(group_id)
	if message.reply_to_message:
		a=message.reply_to_message.text.split("/n")
		await bot.send_message(a[0], f"🤵‍♂️ Ma'sul shaxsdan javob 📩\n {message.text}")
	else:
		await message.reply("Javob yozish uchun reply qiling 🚫")
		


@dp.message_handler(content_types='text')
async def exo(message: types.Message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	await bot.send_message(group_id, f"{user.id}\n\n<b>Fuqaro 👨‍💼</b>: {user.name}\n\n<b>Manzili 🏠</b>: {user.manzil}\n\n<b>Telefon raqami ☎️</b>: {user.telefon}\n\n<b>Murojaat mazmuni📩 </b>\n🔽🔽🔽🔽🔽🔽🔽🔽🔽\n\n{message.text}",  parse_mode="HTML")


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)