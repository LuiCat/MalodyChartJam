import re

#response = """
#"""
#
#match = re.search(
#"",
#response
#)
#
#print(match.groups()[0])

from chartjam import *

dt = datetime.now()
dts = dt2s(dt)

details, members = fetch_submissions()
print(details)

sids = []
for _, detail in details.items():
    sid = detail["sid"]
    if sid not in sids:
        sids.append(sid)

rankings_kudos = calculate_rankings_kudos(charts, sids, members)

#history_submission = {}
#history_submission["history"] = {}
#history_submission["history"][dts] = details
#history_submission["latest"] = details
#
#wiki_text = wiki_submission_history(dt, history_submission)
#print(wiki_text)

