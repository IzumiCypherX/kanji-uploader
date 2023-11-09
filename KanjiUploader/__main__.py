from KanjiUploader import DELAY, CHANNEL_ID, LOG_ID, OWNER_ID, app
from KanjiUploader.helpers import KanjiToday

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, filters

START_TEXT = """Hello @{}.
This is KanjiUploadBot which was made for @JapaneseByIzumi .
This bot aims at automation of the uploading process, making life easier.

Made with 💝 by Sidhartha Rao < @TheSidharthaRao > 

Source can be found at https://github.com/IzumiCypherX/kanji-uploader"""

RESP_TEXT = """Kanji Character: {}

Meaning: {}

Onyomi: {}

Kunyomi: {}

Strokes: {}

By @JapaneseByIzumi

#kanji #writing 
"""
kanji = KanjiToday()

async def start(update: Update, context: CallbackContext):
    await update.effective_message.reply_text(START_TEXT.format(update.effective_user.username),
                                              disable_web_page_preview=True)

async def send_kanji(context: CallbackContext):
    kanji.get_todays_kanji()
    message = RESP_TEXT.format(kanji.character,
                                kanji.meanings, 
                                kanji.on_readings, 
                                kanji.kun_readings, 
                                kanji.stroke_count)
    await context.bot.send_message(chat_id=LOG_ID, 
                                   text=f'posted {kanji.character}')
    await context.bot.send_video(chat_id=context.job.chat_id, 
                                   video=kanji.strokevideo,
                                   caption=f'{message}')

async def send(update: Update, context: CallbackContext):
    # Set the alarm:
    context.job_queue.run_repeating(send_kanji, 
                                    interval=DELAY, 
                                    chat_id=CHANNEL_ID)


if __name__ == "__main__":
    app.add_handler(CommandHandler('start', start))
    # Only Owner can start the scheduler
    app.add_handler(CommandHandler('send', send, filters=filters.User(user_id=OWNER_ID)))    

    print("Starting Bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)