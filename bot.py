import telebot
import time
from telebot import types
import msg
import config
from database_config import DB


class Bot:

    def __init__(self):

        # vars
        self.type_plan = None
        self.user_id = None
        self.choice = None

        # classes
        self.db = DB()

        # telebot
        self.bot = telebot.TeleBot(config.token)

        # keyboard stuff
        self.start_keyboard = telebot.types.ReplyKeyboardMarkup()
        self.plan_keyboard = telebot.types.ReplyKeyboardMarkup()
        self.return_keyboard = telebot.types.ReplyKeyboardMarkup()
        self.return_keyboard.row("/start")
        for i in msg.choose_main:
            self.start_keyboard.row(i)
        for i in msg.choose_plan:
            self.plan_keyboard.row(i)

    def mainloop(self):

        # starting chat
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, msg.greeting, reply_markup=self.start_keyboard)

        # menu choice
        @self.bot.message_handler(content_types=['text'])
        def send_text(message):
            if message.text.lower() == '🐋whale inflows':
                self.plan_choose(message, type_plan='whale')

            elif message.text.lower() == '🦜sopr':
                self.plan_choose(message, type_plan='sopr')

            elif message.text.lower() == '👴hodler volumes':
                self.plan_choose(message, type_plan='volumes')

            elif message.text.lower() == '⛰large transactions':
                self.plan_choose(message, type_plan='txes')
            # follow instructions in bot, or you'll go away
            else:
                self.bot.send_message(message.chat.id, "Слышь бля, ты мне тут хуету не пиши",
                                      reply_markup=self.start_keyboard)

        self.bot.polling()

    # choosing pro or recomended notifications
    def plan_choose(self, message, type_plan):

        # making vars clear
        self.user_id = None
        self.choice = None

        # whale handler
        if type_plan == "whale":
            self.bot.send_message(message.chat.id, "Choose your plan",
                                  reply_markup=self.plan_keyboard)  # first message and keyboard
            # printing all the plans
            for i in msg.whale:
                answer = self.bot.send_message(message.chat.id, i, parse_mode='Markdown')
            self.user_id = message.from_user.id
            self.choice = 'whale'
            self.bot.register_next_step_handler(answer, self.write_user)

        # sopr handler
        elif type_plan == "sopr":
            self.bot.send_message(message.chat.id, "Choose your plan",
                                  reply_markup=self.plan_keyboard)  # first message and keyboard
            # printing all the plans
            for i in msg.sopr:
                answer = self.bot.send_message(message.chat.id, i, parse_mode='Markdown')
            self.user_id = message.from_user.id
            self.choice = 'sopr'
            self.bot.register_next_step_handler(answer, self.write_user)

        # volumes handler
        elif type_plan == "volumes":
            self.bot.send_message(message.chat.id, "Choose your plan",
                                  reply_markup=self.plan_keyboard)  # first message and keyboard
            # printing all the plans
            for i in msg.volumes:
                answer = self.bot.send_message(message.chat.id, i, parse_mode='Markdown')
            self.user_id = message.from_user.id
            self.choice = 'volumes'
            self.bot.register_next_step_handler(answer, self.write_user)

        # large txes handler
        elif type_plan == "txes":
            self.bot.send_message(message.chat.id, "Choose your plan",
                                  reply_markup=self.plan_keyboard)  # first message and keyboard
            # printing all the plans
            for i in msg.txes:
                answer = self.bot.send_message(message.chat.id, i, parse_mode='Markdown')
            self.user_id = message.from_user.id
            self.choice = 'txes'
            self.bot.register_next_step_handler(answer, self.write_user)

        # follow instructions in bot, or you'll go away
        else:
            self.bot.send_message(message.chat.id, "Слышь бля, ты мне тут хуету не пиши",
                                  reply_markup=self.plan_keyboard)

    # writing user to all types of db
    # also returning to main menu by /start
    def write_user(self, message):
        print(f'{message.from_user.first_name} {message.from_user.last_name} who have userid {self.user_id} choosed {self.choice} at level {message.text}')
        self.db.write_data([self.user_id, self.choice, message.text], group=True)
        str_plan = str(self.choice) + ' ' + str(message.text)
        self.db.write_data([self.user_id, str_plan], user=True)
        self.bot.send_message(message.chat.id, "Thank you for your choice.\n"
                                               "Click /start or simply write it, to add subscrtiptions", reply_markup=self.return_keyboard)

    # simple and easy mailing
    def mailing(self, group, plan, message):
        users_list = self.db.get_group(group=group, plan=plan)
        for i in users_list:
            print(f"Sending to {i} message = '{message}'")
            self.bot.send_message(i, message)


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
