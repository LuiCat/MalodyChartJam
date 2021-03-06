import os
import json

from datetime import datetime

history_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history")


def dt2s(dt):
    return dt.strftime("%Y%m%d-%H%M%S")

def s2dt(s):
    return datetime.strptime(s, "%Y%m%d-%H%M%S")


def load_history(name):
    filename = os.path.join(history_dir, "%s.json" % name)
    return json.load(open(filename)) if os.path.exists(filename) else {}

def save_history(name, history, backup_suffix = None):
    filename = os.path.join(history_dir, "%s.json" % name)
    json.dump(history, open(filename, "w"))
    if backup_suffix is not None:
        filename = os.path.join(history_dir, "%s-%s.json" % (name, backup_suffix))
        json.dump(history, open(filename, "w"))
