
import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db import add_dataDB, data_infoDB, dataFull_infoDB


TOKEN = "6653599012:AAEKp42a5w1VH9dDeMBsBcwxjdMPOEQ3gZM"
bot = Bot(token=TOKEN)
form_router = Router()
dp = Dispatcher()



class AddKurs(StatesGroup):
    kurs_name = State()
    kurs_price = State()
    kurs_info = State()
    kurs_master = State()

def inline_btns():
    btns = InlineKeyboardBuilder()
    data = data_infoDB()
    for i in data:
        btn = InlineKeyboardButton(text=f"{i}", callback_data=f"{i}".lower())
        btns.row(btn)
    return btns.as_markup()



def start_buttons() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text="O'quv kurslar")
    button_2 = KeyboardButton(text='Bizning afzalliklarimiz')
    button_3 = KeyboardButton(text="Kurs qo'shish")

    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [button_1, button_2],
            [button_3],
        ], resize_keyboard=True
    )
    return reply_buttons

AdminId = 5398301010

@dp.message(CommandStart())
async def start_bot(message: Message):
    userId = message.from_user.id
    adminId = message.chat.id
    print(userId)
    print(adminId)
    
    full_name = message.from_user.full_name
    await message.answer(f"Assalomu aleykum {full_name}, \nSizga qanday yordam kerak", reply_markup=start_buttons())

@form_router.message(F.text == 'Bizning afzalliklarimiz')
async def bizni_afzalliklar(message: Message):
    text = """Bizda o'qisangiz Ish bilan taminlaymiz"""
    await message.answer(text=text)

@form_router.message(F.text == "Kurs qo'shish")
async def added_kurs(message: Message, state: FSMContext):
    if AdminId == message.from_user.id:
        text = "Kurs nomini kiriting."
        await message.answer(text=text)
        await state.set_state(AddKurs.kurs_name)
    else:
        text = "Kechirasiz siz admin emassiz"
        await message.answer(text=text)
    
@form_router.message(AddKurs.kurs_name)
async def added_kurs_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  
    text = "Kurs narxini kiriting"  
    await message.answer(text)
    await state.set_state(AddKurs.kurs_price)
    
@form_router.message(AddKurs.kurs_price)
async def added_kurs_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)  
    text = "Kurs haqida to'liq ma'lumotlarni kiriting"  
    await message.answer(text)
    await state.set_state(AddKurs.kurs_info)
    
    
@form_router.message(AddKurs.kurs_info)
async def added_kurs_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text)  
    text = "Kurs O'quvchisining ismini kiriting"  
    await message.answer(text)
    await state.set_state(AddKurs.kurs_master)
    
@form_router.message(AddKurs.kurs_master)
async def added_kurs_info(message: Message, state: FSMContext):
    await state.update_data(master=message.text) 
    data = await state.get_data()
    add_dataDB(data["name"], data["price"], data["info"], data["master"])  
    await message.answer("Siz yuborgan ma'lumotlar saqlandi.", reply_markup=start_buttons())
    await state.clear()
    

@form_router.message(F.text == "O'quv kurslar")
async def added_kurs(message: Message):
    data = data_infoDB()
    if data:
        text = "Bizda quydagi kurslar mavjud."
        await message.answer(text=text, reply_markup=inline_btns())
    else: 
        await message.answer("Bizda hozircha kurslar mavjud emas!")

@form_router.callback_query()
async def process_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    db_data = dataFull_infoDB()
    for i in db_data:
        if data.lower() == i[1].lower():
            resp = f"Kurs nomi: {i[1]}, \nNarxi: {i[2]}$, \nMa'lumotlar: {i[3]}, \nUstoz: Mr. {i[4]}"
            await callback_query.message.answer(resp)




async def main():
    print("Succesully")
    dp.include_router(form_router)
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())
    