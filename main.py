
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "توکن_تو_اینجا_بزار"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("💬 چت با محمدامین", callback_data="chat"),
        InlineKeyboardButton("🎵 دانلود آهنگ", callback_data="download")
    )
    bot.send_message(message.chat.id, "سلام! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "chat":
        bot.send_message(call.message.chat.id, "سلام! می‌خواستی با من حرف بزنی؟ 😀 خوب پس بگو...")
    elif call.data == "download":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔗 دانلود از ساندکلاد", callback_data="sc_download"))
        bot.send_message(call.message.chat.id, "از کجا می‌خوای آهنگ دانلود کنی؟", reply_markup=markup)
    elif call.data == "sc_download":
        bot.send_message(call.message.chat.id, "پس آهنگ می‌خوای 😁 لطفاً لینکت رو بدون پیام اضافی ارسال کن

مثال:
https://soundcloud.com/artist-name/track-name")
        bot.register_next_step_handler(call.message, handle_sc_link)

def handle_sc_link(message):
    link = message.text.strip()
    msg = bot.send_message(message.chat.id, "⏳ چند لحظه وایسا، الان پیداش می‌کنم...")
    try:
        # جای دانلود واقعی، یه آهنگ آزمایشی می‌فرستیم
        bot.send_audio(message.chat.id, audio=open("sample.mp3", "rb"))
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, "🎶 اینم آهنگت! اگه خوشت اومد، یکی دیگه بفرست 😎")
    except Exception as e:
        bot.send_message(message.chat.id, f"یه مشکلی پیش اومد 😓
{e}")

bot.infinity_polling()
