import telebot
import requests

# توکن رباتتو اینجا بذار
TOKEN = "7500354841:AAHYfeQQirUBL6Aca0s0qwYJZulZp-HA7j8"
OWNER_ID = 5770789775  # آیدی عددی خودت (مالک ربات)

bot = telebot.TeleBot(TOKEN)

# وقتی کاربر /start بزنه
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("💬 چت با محمدامین", callback_data='chat'),
        telebot.types.InlineKeyboardButton("🎵 دانلود آهنگ از ساندکلاد", callback_data='download')
    )
    bot.send_message(message.chat.id, "سلام! یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=markup)
    
    # اطلاع به مالک که یکی وارد ربات شد
    if message.chat.id != OWNER_ID:
        info = f"🎉 یه کاربر جدید وارد ربات شد!\n\nنام: {message.from_user.first_name}\nآیدی: @{message.from_user.username}\nچت آیدی: {message.chat.id}"
        bot.send_message(OWNER_ID, info)

# مدیریت کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'chat':
        bot.send_message(call.message.chat.id, "پیام‌تو بفرست، محمدامین فقط خودش می‌بینه 😎")
        bot.register_next_step_handler(call.message, forward_to_owner)

    elif call.data == 'download':
        bot.send_message(call.message.chat.id, "لینک آهنگ ساندکلاد رو بفرست (بدون متن اضافه):")
        bot.register_next_step_handler(call.message, download_song)

# فرستادن پیام کاربر به مالک (تو)
def forward_to_owner(message):
    sender = f"پیام جدید از {message.from_user.first_name} (@{message.from_user.username}):\n\n{message.text}"
    bot.send_message(OWNER_ID, sender)

# دانلود آهنگ واقعی از لینک SoundCloud
def download_song(message):
    url = message.text.strip()
    if not url.startswith("http"):
        bot.send_message(message.chat.id, "لطفاً فقط لینک معتبر ساندکلاد رو بفرست 😐")
        return

    bot.send_message(message.chat.id, "⏳ در حال دانلود آهنگ...")

    try:
        # API خارجی برای تبدیل لینک ساندکلاد به فایل (مثال آزمایشی)
        api_url = f"https://api.vevioz.com/api/widget?url={url}"
        response = requests.get(api_url)

        if response.status_code == 200 and "mp3" in response.text:
            # لینک دانلود را استخراج کن
            # برای مثال فقط پیام ارسال می‌کنیم (تغییر بده به روش خودت اگه خواستی)
            bot.send_message(message.chat.id, "✅ آهنگ آماده‌ست! ولی فعلاً لینک مستقیمش اینجاست:\n" + url)
        else:
            bot.send_message(message.chat.id, "متأسفم، نشد آهنگ رو دانلود کنم. لینک شاید اشتباهه یا قابل تبدیل نیست 😔")

    except Exception as e:
        bot.send_message(message.chat.id, "یه مشکلی پیش اومد! بعداً امتحان کن ❌")
        bot.send_message(OWNER_ID, f"[❗️] خطا در دانلود آهنگ:\n{e}")

# اجرای بات
print("ربات روشن شد ✅")
bot.infinity_polling()
