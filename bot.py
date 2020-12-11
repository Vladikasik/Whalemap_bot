import telebot
import time
from telebot import types
import msg
import config


class Bot:

    def __init__(self):

        self.bot = telebot.TeleBot(config.token)

    def mainloop(self):
        start_keyboard = telebot.types.ReplyKeyboardMarkup()
        for i in msg.choose_main:
            start_keyboardkeyboard.row(i)

        # starting chat
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, msg.greeting, reply_markup=start_keyboardkeyboard)

        # menu choice
        @self.bot.message_handler(content_types=['text'])
        def send_text(message):
            if message.text.lower() == '🐋whale inflows':
                self.whale(msg)
            elif message.text.lower() == '🦜sopr':
                self.sopr(msg)
            elif message.text.lower() == '👴hodler volumes':
                self.volumes(msg)
            elif message.text.lower() == '⛰large transactions':
                self.txes(msg)

        # choose plan for whale inflows
        def whale(msg):
            pass

        # choose plan for sopr
        def sopr(msg):
            pass

        # choose plan for hodler volumes
        def volumes(msg):
            pass

        # choose plan for large txes
        def txes(msg):
            pass

        self.bot.polling()


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
