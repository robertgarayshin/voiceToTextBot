import re
from datetime import datetime, timedelta
import telebot
from vosk import Model

import language_recognizer as lang
import commander
import downloader
import text_recognizer as recognizer
import iam_token as iam
import punctuation_predictor as punc
import translate

model_ru = Model('../vosk-model-ru-0.42')
model_en = Model('../vosk-model-en-us-0.42-gigaspeech')
bot = telebot.TeleBot('6088935436:AAGeLUqygWNlfW4qScaOes2j3vwnrw4Doqo')
iam_token = iam.get_token()
token_lifetime_started = datetime.now()
print('System started')
result = ''
language = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Hey! This bot can help you to transcribe video into the text!\n'
                                           'First of all, send me link to video on YouTube')


@bot.message_handler(content_types=['text', 'audio'])
def get_text_messages(message):
    global result
    global language
    if datetime.now() - token_lifetime_started > timedelta(hours=2):
        iam.get_token()
    # bot.send_message(message.from_user.id, 'Wait...')

    try:
        downloader.download(message)

        wavefile, pcmfile = commander.convert()
        language = lang.run(iam_token, pcmfile)

        if language == 'ru-RU':
            transcript = recognizer.recognize(wavefile, model_ru)
            result = punc.predict_ru(transcript)
        elif language == 'en-US':
            transcript = recognizer.recognize(wavefile, model_en)
            result = punc.predict_en(transcript)
        commander.remove()
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(telebot.types.InlineKeyboardButton(text='Original', callback_data='o'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='Translated', callback_data='t'))
        bot.send_message(message.from_user.id, 'Select language', reply_markup=keyboard)
    except Exception as e:
        commander.remove()
        bot.send_message(message.from_user.id, 'Some error occurred while opening the link')
        print(e)
        bot.send_message(message.from_user.id, 'Now you can enter new link')



@bot.callback_query_handler(func=lambda call: True)
def send_message(call):
    if call.data == 'o':
        bot.send_message(call.message.chat.id,
                         '\n'.join(line.strip() for line in re.findall(r'.{1,150}(?:\s+|$)', result)))
        bot.send_message(call.message.chat.id, 'Now you can enter new link')
    else:
        if language == 'ru-RU':
            final = translate.translate(iam_token, target_lang='en', text=result)
            bot.send_message(call.message.chat.id,
                             '\n'.join(line.strip() for line in re.findall(r'.{1,150}(?:\s+|$)', final)))
            bot.send_message(call.message.chat.id, 'Now you can enter new link')
        else:
            final = translate.translate(iam_token, target_lang='ru', text=result)
            bot.send_message(call.message.chat.id,
                             '\n'.join(line.strip() for line in re.findall(r'.{1,150}(?:\s+|$)', final)))
            bot.send_message(call.message.chat.id, 'Now you can enter new link')


bot.polling(none_stop=True, interval=0)
