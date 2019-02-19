import time
import json, bson

from telebot import types
from records.record import Skill


def com2str(command):
    '''c[command], p[page]'''
    h = {"c":"go","p":command}
    return json.dumps(h)

class CALLBACK:
    GO_ADD_SKILL     = com2str("ADDS")
    GO_VIEW_SKILLS   = com2str("SKILLS")
    GO_VIEW_HELP     = com2str("HELP")
    GO_BACK          = com2str("BACK")
    GO_BASE_SCREEN   = com2str("BASE_SCREEN")

class STATE:
    BASE_SCREEN      = "BASE_SCREEN"
    VIEW_SKILLS      = "SKILLS"
    VIEW_ADDED_SKILL = "VIEW_ADDED_SKILL"
    VIEW_HELP        = "HELP"

    ADD_SKILL        = "ADDS"
    ADD_SKILL_TITLE  = "ADDS_TITLE"
    ADD_SKILL_FREQ   = "ADDS_FREQ"
    ADD_SKILL_COUNT  = "ADDS_COUNT"

class Action:
    def __init__(_, prev = None, next = None, call = None, text = ""):
        '''
        prev_state
        next_state
        callback_data
        state
        '''
        _.prev  = prev
        _.next  = next
        _.call  = call
        _.text  = text

    def __eq__(_, o):
        eq = True

        if not ((_.prev == None or o.prev == None) or (_.prev == o.prev )):
            eq = False

        if not ((_.next == None or o.next == None) or (_.next == o.next )):
            eq = False

        if not ((_.call == None or o.call == None or _.call == "" or o.cal == "") or (_.call == o.call )):
            eq = False

        if not ((_.text == "" or o.text == "") or (_.text == o.text )):
            eq = False

        return eq

    def __hash__(_):
        return hash((_.prev, _.next, _.call, _.text))


class ActionSM:
    def __init__(_, session):
        _.ses = session
        _.reset()

    def reset(_):
        _.path = [STATE.BASE_SCREEN]
        _.data = {"username": _.ses.username}

    def input2action(_, input):
        state = _.path[-1]
        call  = input["call"]
        text  = input["text"]

        try:
            print(call)
            obj = json.loads(call)
            #import ipdb; ipdb.set_trace()
            if 'id' in obj:
                if 'c' in obj and obj['c'] == 'do':
                    #_.ses.db.find_one({"_id":bson.ObjectId(obj['id'])})

                    _.ses.db.find_one_and_update({"_id":bson.ObjectId(obj['id'])},
                        {
                            "$inc": {"progress":1},
                            "$set": {
                                "last_probe" :time.time(),
                                }
                        })

                if 'c' in obj and obj['c'] == 'wa':
                    if 'a' in obj and len(obj['a']) > 0:
                        _.ses.db.find_one_and_update({"_id":bson.ObjectId(obj['id'])},
                            {
                                "$set": {
                                    "waitlist"   : obj['a'][0]
                                    }
                            })
                    else:
                        rec = _.ses.db.find_one({"_id":bson.ObjectId(obj['id'])})
                        _.ses.db.find_one_and_update({"_id":bson.ObjectId(obj['id'])},
                            {
                                "$set": {                                    
                                    "waitlist"   : not rec["waitlist"]
                                    }
                            })


        except Exception as e:
            print(e)

        if call == CALLBACK.GO_BACK:
            prev = STATE.BASE_SCREEN
            if len(_.path)>1:
                prev =  _.path[-2]
                return Action(state, prev)
            return Action(prev)

        if state == STATE.BASE_SCREEN and call == CALLBACK.GO_ADD_SKILL:
            return Action(state, STATE.ADD_SKILL_TITLE)
        elif state == STATE.ADD_SKILL_TITLE and (text != ""):
            return Action(state, STATE.ADD_SKILL_FREQ, text=text)
        elif state == STATE.ADD_SKILL_FREQ and (text != "" or call != None):
            return Action(state, STATE.ADD_SKILL_COUNT, text=text, call=call)
        elif state == STATE.ADD_SKILL_COUNT and (text != ""):
            return [Action(state, STATE.VIEW_ADDED_SKILL, text=text, call=call), Action()]

        if call == CALLBACK.GO_VIEW_HELP:
            return [Action(state, STATE.VIEW_HELP), Action()]

        if call == CALLBACK.GO_VIEW_SKILLS:
            return [Action(state, STATE.VIEW_SKILLS), Action(next=STATE.BASE_SCREEN)]


        return Action(next=STATE.BASE_SCREEN)

    def do(_, action):
        if action.next == STATE.ADD_SKILL_FREQ:
            _.data["title"] = action.text

        if action.next == STATE.ADD_SKILL_COUNT:
            _.data["freq"] = action.call

        if action.prev == STATE.ADD_SKILL_COUNT:
            _.data["count"] = int(action.text)
            _.data["username"] = _.ses.username

            skill = Skill.fromRec(_.data)
            _.ses.db.insert_one(skill.toDIC())


        if action.next == None or action.next == STATE.BASE_SCREEN:
            _.reset()
        else:
            _.path.append(action.next)

        return _.path

    def menu_by_state(_, state):
        '''
        return {"text":,"ui" (with buttons):}
        '''
        screen = {
            "text":"",
            "ui":None
        }

        if state == STATE.BASE_SCREEN:
            text = "I am Kil Skil Bot and I am here to improve you!"

            ui   = types.InlineKeyboardMarkup()
            item_addskill = types.InlineKeyboardButton(text='Add Skill ▶️', callback_data = CALLBACK.GO_ADD_SKILL)
            item_skills   = types.InlineKeyboardButton(text='Skills 📜',  callback_data = CALLBACK.GO_VIEW_SKILLS)
            item_help     = types.InlineKeyboardButton(text='Help 🔍', callback_data    = CALLBACK.GO_VIEW_HELP)
            ui.add(item_addskill)
            ui.row(item_skills, item_help)

            screen["text"] = text
            screen["ui"]  = ui

        elif state == STATE.VIEW_SKILLS:
            print("DB!")
            skills_str = ""
            for rec in _.ses.db.find({"username": _.ses.username}):
                skills_str += Skill.fromRec(rec).toMRKD_VIEWALL() + "\n\n"

            text = "Your skills:\n\n" + skills_str
            screen["text"] = text
        elif state == STATE.VIEW_HELP:
            text = "You can add skills to train them regulary."
            screen["text"] = text
        elif state == STATE.VIEW_ADDED_SKILL:
            print(_.data)
            text = "Skill: {title}\nFrequency:{freq}\nTODO:{count}".format(** _.data)
            screen["text"] = text
        elif state == STATE.ADD_SKILL_TITLE:
            text  = 'Enter the skill title:'
            ui    = types.InlineKeyboardMarkup()
            item_back = types.InlineKeyboardButton(text='Back', callback_data = CALLBACK.GO_BACK)
            ui.add(item_back)

            screen["text"] = text
            screen["ui"]  = ui
        elif state == STATE.ADD_SKILL_FREQ:
            text      = 'How often do you plan to train this skill:'
            ui   = types.InlineKeyboardMarkup()
            item_1m = types.InlineKeyboardButton(text='1 per min', callback_data = "freq_1m")
            item_30m = types.InlineKeyboardButton(text='1 per 30 min', callback_data = "freq_30m")
            item_1h = types.InlineKeyboardButton(text='1 per hour', callback_data = "freq_1h")

            item_90m = types.InlineKeyboardButton(text='1 per 1.5 hour', callback_data = "freq_90m")
            item_4h = types.InlineKeyboardButton(text='1 per 4 hours', callback_data = "freq_4h")
            item_12h = types.InlineKeyboardButton(text='1 per 12 hours', callback_data = "freq_12h")

            item_1d = types.InlineKeyboardButton(text='1 per day', callback_data = "freq_1d")
            item_3d = types.InlineKeyboardButton(text='1 per 3 days', callback_data = "freq_3d")
            item_1w = types.InlineKeyboardButton(text='1 per week', callback_data = "freq_1w")

            ui.row(item_1m,item_30m,item_1h)
            ui.row(item_90m,item_4h,item_12h)
            ui.row(item_1d, item_3d,item_1w)

            screen["text"] = text
            screen["ui"]  = ui
        elif state == STATE.ADD_SKILL_COUNT:
            text      = 'How many times you plan to train this skill:'
            screen["text"] = text

        return screen

    def remind(_, skill):
        screen = {
            "text": "",
            "ui":None
        }

        id = str(skill["_id"])
        def skill_act(command, id, argv=[], to_JSON = True):
            callback = {
                "c":command,
                "id":id
                }

            if len(argv) > 0:
                callback["a"] = argv

            if to_JSON:
                callback = json.dumps(callback)

            return callback

        skill_done = skill_act("do", id)
        skill_waitlist = skill_act("wa", id)

        desc = Skill.fromRec(skill).toMRKD_VIEWALL()
        text = "{}.\n Let's do it!".format(desc)

        ui   = types.InlineKeyboardMarkup()
        item_do = types.InlineKeyboardButton(text='Done', callback_data = skill_done)
        item_skip = types.InlineKeyboardButton(text='Skip', callback_data = "2")
        item_wait = types.InlineKeyboardButton(text='Toggle@waitlist', callback_data = skill_waitlist)
        item_edit = types.InlineKeyboardButton(text='Edit', callback_data = "4")

        ui.row(item_do,item_skip)
        ui.row(item_wait,item_edit)

        screen["text"] = text
        screen["ui"]  = ui

        return screen
