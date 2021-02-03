from datetime import datetime

from malody_web import *
from chart import *
from ranking import *


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

submissions_stat

submissions = get_submissions()
for uid, sid in submissions.items():
    for cid in get_cid_list(uid, sid):
        chart = get_chart_stat(cid)
        if validate_chart(chart):
            cids.append(chart.cid)


history_submission = load_history_submission()


history_submission[dts] = dict(sids = submission_sids, cids = submission_cids)

save_history_submission(history_submission, dts)


# todo: update wiki with a template file
# todo: randomly select charts for store, and save the total selected count as a file
# todo: ban list
