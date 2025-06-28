import telebot
import yt_dlp
import os
from telebot.types import IndlineKeyboardMarkup,IndlineKeyboardButton

TOKEN = '7500354841:AAE-4Stt5hGdRGA9Yqpa--nzpWfpn_0Bcec'
bot = telebot.Telebot(TOKEN)

user_states = {} # مدیریت حالت کاربران

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('🎵 دانلود آهنگ از SoundCloud',callback_data='download_music')
    markup.add(btn)
    bot.send_message(message.chat.id, "سلام خوش اومدی یکی از گزینه های زیر رو انتخاب کن",reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'download_music')
    def ask_for_link(call):
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,"لطفا لینک آهنگی که از soundcloud کپی کردی رو بدون متن اضافه ای بفرست واسم😄🎧")
        user_states[call.message.chat.id] ='waiting_for_link'

@bot.message_handler(func=lambda message: True)
def handler_messages(message):
    state = user_states.get(message.chat.id)
    if state == 'waiting_for_link':
        download_sc(message)
        user_states.pop(message.chat.id)
    else:
        bot.send_message(message.chat.id, "برای شروغ دکمه /start رو بزن😃")

def download_sc(message):
    url = message.text.script()
    if 'soundcloud.com' not in url:
        bot.reply_to(message:, "مطمئنی این لینک soundcloud هستش 😐! لینک معتبر بده")
        return

bot.reply_to(message, "خوب خوب ببینیم داشتی چی گوش میدادی🤨! وایسا دانلودش کنم...")

try:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s'
        'noplaylist': True,
    'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download+True)
        file_path= ydl.prepare_filename(info_dict)

with open(file_path, 'rb') as audio:
    bot.send_audio(message.chat.id, audio)

os.remove(file_path)

except Exception as 3:
bot.reply_to(message, "خطا متاسفانه نتونستم دانلود کنم مجدد لینکت رو بفرست😢!\n{str(e)}")

bot.infinity_polling()
