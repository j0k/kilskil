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
#from records.record import Skill
#from action import CALLBACK, STATE, ActionSM
#import action as act

from ksmod.session import *

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

import ksmod.config as conf

admins = ['bimodaling', 'IraKarpetskaya']
users  = ['bimodaling', 'IraKarpetskaya']

sessions = {}
bot = telebot.TeleBot(conf.API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
Hi there, I am Kil Skil Bot.
I am here to improve you!\
""", reply_markup=base_screen)


@bot.message_handler(commands=['commands'])
def send_welcome(message):
    bot.reply_to(message, """I have next commands: addurl, find, list, keys, findurl, modtags.""")


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
