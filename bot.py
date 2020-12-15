import telebot
import time
from telebot import types
import msg
import config
from database_config import DB


class Bot:

    def __init__(self):

        # vars
        self.plan = None
        self.type_plan = None
        self.user_id = None

        # classes
        self.db = DB()

        # telebot
        self.bot = telebot.TeleBot(config.token)

        # keyboard stuff
        self.plan_keyboard = types.InlineKeyboardMarkup(row_width=1)
        self.extended_keyboard = types.InlineKeyboardMarkup(row_width=2)
        for i in range(4):
            self.plan_keyboard.add(types.InlineKeyboardButton(text=msg.choose_main_text[i], callback_data=msg.choose_main_callback[i]))
        for i in range(len(msg.choose_plan)):
            self.extended_keyboard.add(types.InlineKeyboardButton(text=msg.choose_plan[i], callback_data=msg.choose_plan[i]))
        self.extended_keyboard.row(types.InlineKeyboardButton(text='⬅Back', callback_data='start'))

        # messages stuff
        self.choose_the_fst = None
        self.extended_choose = None
        self.user_message = None

        print('init done')

    def mainloop(self):

        # starting chat
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.user_message = message
            self.user_id = message.from_user.id
            self.choose_the_fst = self.bot.send_message(message.chat.id, msg.greeting, reply_markup=self.plan_keyboard)

        @self.bot.callback_query_handler(func=lambda call: True)
        def buttons(call):
            if call.data in msg.choose_main_callback:
                self.plan = call.data
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.choose_the_fst.message_id,
                                           text=f"Choose plan for {msg.choose_main_text[msg.choose_main_callback.index(call.data)]}",
                                           reply_markup=self.extended_keyboard)

            elif call.data in msg.choose_plan:
                self.type_plan = call.data
                self.extended_choose = self.bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                               text=f"You have been sucsesfully subscribed to {self.plan} at level {self.type_plan}.")
                self.write_user()

            elif call.data == 'start':
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.choose_the_fst.message_id,
                                           text=msg.greeting,
                                           reply_markup=self.plan_keyboard)

        self.bot.polling()

    # writing user to all types of db
    # also returning to main menu by /start
    def write_user(self):
        print(
            f'{self.user_message.from_user.first_name} {self.user_message.from_user.last_name} who have userid {self.user_id} '
            f'choosed {self.plan} at level {self.type_plan}')
        self.db.write_data([self.user_id, self.plan, self.type_plan], group=True)
        str_plan = str(self.plan) + ' ' + str(self.type_plan)
        self.db.write_data([self.user_id, str_plan], user=True)

    # simple and easy mailing
    def mailing(self, group, plan, message):
        users_list = self.db.get_group(group=group, plan=plan)
        for i in users_list:
            print(f"Sending to {i} message = '{message}'")
            self.bot.send_message(i, message)


if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
