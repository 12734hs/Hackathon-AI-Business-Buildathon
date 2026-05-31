import telebot
import uuid
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

if not CHANNEL_ID:
    raise RuntimeError("TELEGRAM_CHANNEL_ID is not set")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(msg):
    username = msg.from_user.username or msg.from_user.first_name

    bot.send_message(msg.chat.id, f'Welcome to PeerMatch AI Bot, {username}!')
    bot.send_message(
        msg.chat.id,
        'We are glad to have you here! This is your convenient bridge to stay connected with our team'
    )

    bot.send_message(msg.chat.id, 'Please write here the subject of your application:')

    bot.register_next_step_handler(msg, get_subject)


def get_subject(msg):
    subj = msg.text

    bot.send_message(msg.chat.id, 'Please write here the main text of your application:')

    bot.register_next_step_handler(msg, get_main_text, subj)


def get_main_text(msg, subj):
    text = msg.text

    username = msg.from_user.username or msg.from_user.first_name
    app_id = uuid.uuid4()
    application = f"""
    New application

    From: @{username}
    Application ID: {app_id}

    Subject:
    {subj}
    
    Text:
    {text}
    """

    bot.send_message(CHANNEL_ID, application)

    bot.send_message(
        msg.chat.id,
        'Your application was gotten and was redirected to our support team.'
    )

    bot.send_message(
        msg.chat.id,
        'Thank you for your application :). For a new one, just type the command /new'
    )

    print('Subject:', subj)
    print('Text:', text)


@bot.message_handler(commands=['new'])
def new_application(msg):
    bot.send_message(msg.chat.id, 'Please write here the subject of your application:')
    bot.register_next_step_handler(msg, get_subject)


bot.infinity_polling()