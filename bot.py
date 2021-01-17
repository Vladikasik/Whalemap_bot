import telebot
import time
from telebot import types
try:
    import msg
    import config
    from database_config import DB
except:
    import Whalemap_bot.msg as msg
    import Whalemap_bot.config as config
    from Whalemap_bot.database_config import DB



class Bot:

    def __init__(self):

        # vars
        self.plan = {}
        self.type_plan = {}
        self.user_id = None

        # classes
        self.db = DB()

        # telebot
        self.bot = telebot.TeleBot(config.token)

        # keyboard stuff
        self.plan_keyboard = types.InlineKeyboardMarkup(row_width=1)
        self.extended_keyboard = types.InlineKeyboardMarkup(row_width=2)
        self.make_keybord('init', 'init')
        buttons = msg.plan_choose_func()
        for i in range(4):
            self.plan_keyboard.add(types.InlineKeyboardButton(text=msg.choose_main_text[i], callback_data=msg.choose_main_callback[i]))

        # messages stuff
        self.choose_the_fst = {}
        self.plan_msg = {}
        self.user_message = {}

        print('init done')

    def mainloop(self):

        # starting chat
        @self.bot.message_handler(commands=['start', 'settings'])
        def start_message(message):
            self.user_message[message.from_user.id] = message
            self.user_id = message.from_user.id
            self.choose_the_fst[message.from_user.id] = self.bot.send_message(message.chat.id, msg.greeting, reply_markup=self.plan_keyboard)

        @self.bot.callback_query_handler(func=lambda call: True)
        def buttons(call):
            if call.data in msg.choose_main_callback:
                try:
                    self.plan[call.from_user.id] = call.data
                    data = self.db.get_user_btns(call.from_user.id, call.data)
                    print(f'excended - {self.db.get_user_btns(call.from_user.id, call.data)}')
                    self.make_keybord(data['pro'], data['rec'])
                    self.plan_msg[call.from_user.id] = msg.choose_main_text[msg.choose_main_callback.index(call.data)]
                    self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.choose_the_fst[call.from_user.id].message_id,
                                               text=f"Choose plan for {msg.choose_main_text[msg.choose_main_callback.index(call.data)]}",
                                               reply_markup=self.extended_keyboard)
                except Exception as ex:
                    print('Error in buttons probably\nLines 57-68')
                    print(ex)

            elif call.data in msg.choose_plan:
                try:
                    data = self.db.get_user_btns(call.from_user.id, self.plan[call.from_user.id])
                    self.type_plan[call.from_user.id] = call.data
                    if data[call.data]:
                        self.delete_user(call.from_user.id)
                        data = self.db.get_user_btns(call.from_user.id, self.plan[call.from_user.id])
                        self.make_keybord(data['pro'], data['rec'])
                        self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                   message_id=self.choose_the_fst[call.from_user.id].message_id,
                                                   text=f"Choose plan for {self.plan_msg[call.from_user.id]}",
                                                   reply_markup=self.extended_keyboard)
                        self.bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                                       text=f"You have been sucsesfully unsubscribed to {self.plan[call.from_user.id]} at level {self.type_plan[call.from_user.id]}.")
                except Exception as ex:
                    print('Error in unsibscribing pro/rec\nLines 72-86')
                    print(ex)


                else:
                    try:
                        self.write_user(call.from_user.id)
                        data = self.db.get_user_btns(call.from_user.id, self.plan[call.from_user.id])
                        self.make_keybord(data['pro'], data['rec'])
                        self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                   message_id=self.choose_the_fst[call.from_user.id].message_id,
                                                   text=f"Choose plan for {self.plan_msg[call.from_user.id]}",
                                                   reply_markup=self.extended_keyboard)
                        self.bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                                       text=f"You have been sucsesfully subscribed to {self.plan[call.from_user.id]} at level {self.type_plan[call.from_user.id]}.")
                    except Exception as ex:
                        print('Error in subscribing\nLines 91-99')
                        print(ex)

            elif call.data == 'start':
                try:
                    self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.choose_the_fst[call.from_user.id].message_id,
                                           text=msg.greeting,
                                           reply_markup=self.plan_keyboard)
                except Exception as ex:
                    print('Error in going back to menu\nLines 106')

        self.bot.polling()

    def make_keybord(self, pro, rec):
        self.extended_keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = msg.plan_choose_func(pro=pro, recomended=rec)
        for i in range(2):
            self.extended_keyboard.add(
                types.InlineKeyboardButton(text=buttons[i], callback_data=msg.choose_plan[i]))
        self.extended_keyboard.row(types.InlineKeyboardButton(text='⬅Back', callback_data='start'))

    # writing user to all types of db
    # also returning to main menu by /start
    def write_user(self, user_id):
        print(
            f'{self.user_message[user_id].from_user.first_name} {self.user_message[user_id].from_user.last_name} who have userid {user_id} '
            f'choosed {self.plan[user_id]} at level {self.type_plan[user_id]}')
        self.db.write_data([user_id, self.plan[user_id], self.type_plan[user_id]], group=True)
        str_plan = self.plan[user_id] + ' ' + str(self.type_plan[user_id])
        self.db.write_data([user_id, str_plan], user=True)

    def delete_user(self, user_id):
        print(f'{self.user_message[user_id].from_user.first_name} {self.user_message[user_id].from_user.last_name} who have userid {user_id} '
              f'canceled subscription to choosed {self.plan[user_id]} at level {self.type_plan[user_id]}')
        data_to_delete = [user_id, self.plan[user_id], self.type_plan[user_id]]
        self.db.delete_data(data_to_delete)

    # simple and easy mailing
    def mailing_text(self, group, plan, message):
        users_list = self.db.get_group(group=group, plan=plan)
        for i in users_list:
            # print(f"Sending to {i} message = '{message}'")
            self.bot.send_message(i, message)

    def mailing_image(self, group, plan, path_to_image):
        with open(path_to_image, 'rb') as photo:
            users_list = self.db.get_group(group=group, plan=plan)
            for i in users_list:
                # print(f"Sending to {i} image")
                self.bot.send_photo(i, photo)

if __name__ == '__main__':
    bot = Bot()
    bot.mainloop()
