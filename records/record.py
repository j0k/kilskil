import json
import time

class Skill:
    @staticmethod
    def fromRec(mrec):
        rec = Skill()
        for field in rec.h.keys():
            if field == "_id":
                rec.h[field] = str(mrec[field])
            elif field in mrec:
                rec.h[field] = mrec[field]

        return rec

    def __init__(_):
        _.h = {
            "username":"owner",
            "title"   : "Skill title",
            "freq"    : "1d",
            "count"   : 0,
            "progress"    : 0,
            "date_created": time.time(),
            "last_probe":0,
            "last_present" :0,
            "waitlist" : False
        }



    def toDIC(_):
        h = _.h

        return h

    def toJSON(_):
        return json.dumps(_.toDIC())

    def toMRKD(_):
        md = "*{title}*\n{progress} / {count}\n{freq}\n{date_created}".format(** _.h)

        return md

    def toMRKD_VIEWALL(_):
        md = "Title: *{title}*\nProgress: {progress} / {count}\nFrequency: {freq}\nAdded: {date_created}".format(** _.h)

        return md
