import telebot
import random, time
import requests
import json, bson
import pymongo
import signal
import sys

import threading
from threading import Timer

import ipdb
from telebot import types
from records.record import Skill
from action import CALLBACK, STATE, ActionSM
import action as act

def signal_handler(signal, frame):
        N=0
        print('You pressed Ctrl+C!')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

import ksmod.config as conf

admins = ['bimodaling', 'IraKarpetskaya']
users  = ['bimodaling', 'IraKarpetskaya']

db = 'KILSKIL'
coll_skills = 'skills'
coll_users  = 'users'

con = pymongo.MongoClient('localhost', port=27017)
dbdata  = con[db][coll_skills]
dbusers = con[db][coll_users]

class Session:
    def __init__(_):
        _.db = dbdata
        _.rec = Skill()
        _.username = None
        _.reset_state()
        _.reset_action()

    def reset_state(_):
        _.sm      = ActionSM(_)

    def reset_action(_):
        _.input = {"text" : "", "call" : None}

sessions = {}

bot = telebot.TeleBot(conf.API_TOKEN)

base_screen   = types.InlineKeyboardMarkup()
item_addskill = types.InlineKeyboardButton(text='Add Skill ▶️', callback_data = CALLBACK.GO_ADD_SKILL)
item_skills   = types.InlineKeyboardButton(text='Skills 📜',  callback_data = CALLBACK.GO_VIEW_SKILLS)
item_help     = types.InlineKeyboardButton(text='Help 🔍', callback_data    = CALLBACK.GO_VIEW_HELP)
base_screen.add(item_addskill)
base_screen.row(item_skills, item_help)

screen_add_skill = types.InlineKeyboardMarkup()
item_back = types.InlineKeyboardButton(text='Back', callback_data = CALLBACK.GO_BACK)
screen_add_skill.add(item_back)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
Hi there, I am Kil Skil Bot.
I am here to improve you!\
""", reply_markup=base_screen)

@bot.message_handler(commands=['commands'])
def send_welcome(message):
    bot.reply_to(message, """I have next commands: addurl, find, list, keys, findurl, modtags.""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def answer_message(message):
    username = message.from_user.username
    if username not in users:
        return

    ses = check_user(sessions, username, message)
    ses.input["text"] = message.text

    dialog(bot, ses)

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    username = call.from_user.username
    if username not in users:
        return

    ses = check_user(sessions, username, call.message)
    ses.chat_id = call.message.chat.id
    ses.input["call"] = call.data

    dialog(bot, ses)

def check_user(sessions, username, message):
    if username not in sessions:
        sessions[username] = Session()

        sessions[username].sm.ses   = sessions[username]
        sessions[username].username = username
        sessions[username].chat_id  = message.chat.id

        user = dbusers.find_one_and_replace({"username":username},
                                        {"chat_id":message.chat.id},
                                        return_document=pymongo.ReturnDocument.AFTER)

        print("USER!", user)
        if not user:
            dbusers.insert_one({"username":username, "chat_id":message.chat.id})

    return sessions[username]


def dialog(bot, ses):
    sm = ses.sm
    action = sm.input2action(ses.input)
    if type(action) == list:
        for a in action:
            sm.do(a)
            screen = sm.menu_by_state(sm.path[-1])
            bot.send_message(ses.chat_id, screen["text"], reply_markup=screen["ui"]);
    else:
        sm.do(action)
        screen = sm.menu_by_state(sm.path[-1])
        bot.send_message(ses.chat_id, screen["text"], reply_markup=screen["ui"]);


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def check_skills(bot=bot):
    print("check skills for time")
    freqs = {
        "freq_1m":60,
        "freq_30m":60*30,
        "freq_1h":60*60,
        "freq_90m":60*90,
        "freq_4h":60*60*4,
        "freq_12h":60*60*12,
        "freq_1d":60*60*24,
        "freq_3d":60*60*24*3,
        "freq_1w":60*60*24*7
    }
    for skill in dbdata.find():
        ts = time.time()
        period = freqs[skill["freq"]]
        username = skill["username"]
        #print(skill)
        if username in sessions:
            ses = sessions[username]
            sm  = ses.sm
            if not skill["waitlist"] and skill["progress"] < skill["count"] and ts > skill["last_present"] + period:
                id = bson.ObjectId(skill["_id"])
                screen = sm.remind(skill)
                #ipdb.set_trace()
                bot.send_message(ses.chat_id, screen["text"], reply_markup=screen["ui"]);
                dbdata.find_one_and_update({"_id": id}, {"$set": {"last_present" : ts}})



timer = RepeatTimer(5, check_skills)
timer.start()

C = 0
N = 5
while N > 0:
    try:
        bot.polling()
    except Exception as e:
        time.sleep(10)
        print(e)
    C += 1
    N -= 1

timer.cancel()
