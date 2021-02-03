from datetime import datetime

from malody_web import *
from chart import *
from ranking import *
from history import *


dt = datetime.now()
dts = dt2s(dt)


cookies = request_session()
if cookies == None:
    print("?")
    exit(0)
else:
    print("I'm online!")

token = request_token()
if token == None:
    print("??")
    exit(0)
else:
    print("I'm in-game online!")
print()

submissions_detail = {}

submissions = get_submissions()
for uid, sid in submissions.items():
    song = get_song_stat(sid)
    detail = { "uid": uid, "sid": sid, "cids": [], "song": None, "diffs": [] }
    for cid in get_cid_list(uid, sid):
        chart = get_chart_stat(cid)
        if validate_chart(chart):
            detail["song"] = "%s - %s" % (chart.artist, chart.title)
            detail["cids"].append(chart.cid)
            detail["diffs"].append(chart.diff)
    submissions_detail[uid] = detail


history_submission = load_history("submission")
history_submission[dts] = submissions_detail
save_history("submission", history_submission, dts)

history_changes = load_history("changes")
#history_changes[dts] = ?
save_history("changes", history_changes, dts)


# todo: get song stat & song name
# todo: history diff
# todo: update wiki with a template file
# todo: randomly select charts for store, and save the total selected count as a file
# todo: ban list
