
import os
import time
import telebot
from threading import Timer

TOKEN = "7989443793:AAH5i9xzqyraJ4jAJ66LYtp3Oz-1PQtZ5t8"
bot = telebot.TeleBot(TOKEN)

# دیکشنری برای ذخیره فایل‌های آپلود شده همراه با تایمر حذف
user_files = {}

@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
def handle_file(message):
    file_id = message.document.file_id if message.document else (
              message.photo[-1].file_id if message.photo else (
              message.video.file_id if message.video else message.audio.file_id))
    
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    filename = file_info.file_path.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(downloaded_file)

    msg = bot.send_document(message.chat.id, open(filename, 'rb'))
    bot.reply_to(message, "فایل برای شما ارسال شد و تا ۱ دقیقه دیگر حذف خواهد شد.")

    # زمان‌بندی حذف فایل
    def delete_file():
        try:
            os.remove(filename)
        except:
            pass

    Timer(60.0, delete_file).start()

bot.polling()
