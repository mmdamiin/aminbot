import telebot
import requests
import re

# توکن ربات
API_TOKEN = '7500354841:AAHYfeQQirUBL6Aca0s0qwYJZulZp-HA7j8'
OWNER_ID = 5770789775  # عدد آیدی عددی خودت رو اینجا بذار (از @userinfobot بگیر)

bot = telebot.TeleBot(API_TOKEN)

# هندلر استارت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! به ربات خوش اومدی 😄")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎧 دانلود آهنگ از ساندکلاد", "💬 چت با محمدامین")
    bot.send_message(message.chat.id, "یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=markup)

    # اطلاع به مالک ربات
    bot.send_message(OWNER_ID, f"یک نفر وارد ربات شد: {message.from_user.first_name} | @{message.from_user.username}")

# دکمه‌ها
@bot.message_handler(func=lambda message: message.text == "💬 چت با محمدامین")
def handle_chat_request(message):
    bot.send_message(message.chat.id, "پیام‌تو بنویس تا برای محمدامین ارسال بشه:")
    bot.register_next_step_handler(message, forward_to_owner)

def forward_to_owner(message):
    text = f"📩 پیام از {message.from_user.first_name} (@{message.from_user.username}):\n{message.text}"
    bot.send_message(OWNER_ID, text)
    bot.send_message(message.chat.id, "✅ پیام‌ت فرستاده شد برای محمدامین.")

@bot.message_handler(func=lambda message: message.text == "🎧 دانلود آهنگ از ساندکلاد")
def ask_for_soundcloud_link(message):
    bot.send_message(message.chat.id, "لینک آهنگ ساندکلاد رو بفرست:")
    bot.register_next_step_handler(message, download_soundcloud)

def download_soundcloud(message):
    link = message.text
    if not re.match(r'https?://(www\.)?soundcloud\.com/.+', link):
        bot.send_message(message.chat.id, "❌ لینک معتبر ساندکلاد نیست.")
        return

    bot.send_message(message.chat.id, "🔄 در حال پردازش لینک...")

    try:
        # این آدرس ممکنه در آینده فیلتر یا بسته بشه، جایگزین قابل تغییره
        api = f"https://api.vevioz.com/api/button/mp3/{link}"
        response = requests.get(api)
        match = re.search(r'href=\"(https://[^\"]+\.mp3)\"', response.text)

        if match:
            mp3_url = match.group(1)
            bot.send_message(message.chat.id, "✅ دانلود شروع شد")
            bot.send_audio(message.chat.id, audio=mp3_url)
        else:
            bot.send_message(message.chat.id, "⚠️ نشد آهنگ رو بگیریم. ممکنه لینک مشکلی داشته باشه.")

    except Exception as e:
        bot.send_message(message.chat.id, f"🚫 خطا هنگام دریافت آهنگ: {e}")

print("ربات فعال شد")
bot.infinity_polling()
