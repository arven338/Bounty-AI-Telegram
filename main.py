import telebot
import requests
import io
import urllib.parse
import colorama
import os
from telebot import types
from translator import AI_Translator
from colorama import *

colorama.init(autoreset=True)

dp = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'))

ts = AI_Translator()

@dp.message_handler(commands=['start'])
def start(message):
    full_name = f'{message.from_user.first_name} {message.from_user.last_name or ""}'.strip()
    dp.reply_to(message, f"Вітаю, {full_name}! \nТи запустив Bounty-AI🥥 – нейромережевий сервіс, який створює медіа за один запит. \n \nСформулюй свій запит, і ШІ згенерує шедеври 🌄 \n \nЦе все - БЕСКОШТОВНО! Готовий створювати контент 😏?")

    print(Fore.GREEN + f"[ OK ] {full_name} запустив бота! IDS: {message.from_user.id}")

@dp.message_handler(content_types=['text'])
def generate_image(message):
    prompt = message.text.strip()
    english_prompt = ts.translate(prompt)
    
    msg = dp.reply_to(message, "🔄 Генерую зображення... Зачекай кілька секунд 😎")

    print(Fore.YELLOW + f"[ INFO ] {message.from_user.id} запитав сгенерувати зображення з запитом: {prompt}")
    print(f"Перекладений запит: {english_prompt}")

    try:
        encoded_prompt = urllib.parse.quote(english_prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&model=turbo"

        response = requests.get(image_url, timeout=120)

        if response.status_code == 200:
            dp.send_photo(
                message.chat.id,
                io.BytesIO(response.content),
                caption=f"Готово! ШІ створив ваш шедевр – який ви очікували 🌄\n \n📝 <b>Ваш запит:</b> <code>{prompt}</code>",
                parse_mode="HTML"
            )

            print(Fore.GREEN + f"[ + ] Зображення успішно згенеровано та відправлено користувачу {message.from_user.id}")
        else:
            dp.reply_to(message, "⚠️ Не вдалося отримати зображення.")
            print(Fore.RED + f"[ - ] Користувачу {message.from_user.id} не вдалося отримати зображення.")

    except Exception as e:
        dp.reply_to(message, f"❌ Упс... Схоже, ШІ не вспів сгенерувати зображення. Будь ласка, спробуйте трішки пізніше 😉", parse_mode="HTML")
        print(f"ERROR {e}")

print("🤖 Bounty-AI🥥 запущено!")
dp.polling(none_stop=True)