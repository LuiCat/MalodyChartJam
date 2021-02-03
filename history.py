import json
from datetime import datetime


def dt2s(dt):
    return dt.strftime("%Y%m%d-%H%M%S")

def s2dt(s):
    return datetime.strptime(s, "%Y%m%d-%H%M%S")


def load_history_submission():
    return json.loads("history_submission.json") or {}

def save_history_submission(history, backup_suffix = None):
    json.dumps(history, "history_submission.json")
    if backup_suffix is not None:
        json.dumps(history, "history_submission-%s.json" % backup_suffix)
