from datetime import datetime
from random import random

from malody_web import *
from chart import *
from ranking import *
from history import *
from wiki_log import *
from wiki_ranking import *

dt = datetime.now()
dts = dt2s(dt)

if request_session() is None:
    print("?")
    exit(0)
else:
    print("I'm online!")
print(flush=True)

if request_token() is None:
    print("??")
    exit(0)
else:
    print("I'm in-game online!")
print(flush=True)


# I don't know how to eliminate these static states.
# To eliminate them, we need also to decouple
# update_history() and update_ranking() from them and each other.

charts = []
details = {}  # str(sid) -> submission dict
members = {}  # str(uid) -> member dict


def fetch_submissions():
    submissions = get_submissions()
    for submission in submissions:
        song = get_song_stat(submission.sid)
        if song is None:
            continue

        authors = []
        for uid in submission.uids:
            user = get_user_stat(uid)
            authors.append({
                "name": user.name,
                "uid": user.uid,
                "avatar": user.avatar,
                "effective": False,
            })

        detail = {
            "index": submission.index,
            "name": "%s - %s" % (song.artist, song.title), "authors": authors, "cover": song.cover, "team": submission.name, "meta": submission.meta,
            "sid": song.sid, "cids": [], "diffs": {}, "mids": [],
            "hot": 0, "gold": 0, "re": 0, "un": 0, "comments": 0, "kudos_in": 0, "kudos_out": 0
        }

        for diff in song.diffs:
            if not validate_diff(diff, submission):
                continue
            chart = get_chart_stat(diff.cid)
            if validate_chart(chart, submission):
                charts.append(chart)

                detail["cids"].append(chart.cid)
                if chart.mid not in detail["mids"]:
                    detail["mids"].append(chart.mid)

                detail["diffs"][str(chart.cid)] = chart.diff + " (" + chart.mode.capitalize() + ")"

                detail["hot"] += chart.hot
                for supporter in chart.supporters:
                    if supporter.uid != uid:
                        detail["gold"] += supporter.gold
                detail["re"] += chart.rcmd
                detail["un"] += chart.unrcmd
                detail["comments"] += chart.comments_count
                for kudos in chart.kudos:
                    if kudos.inward:
                        detail["kudos_in"] += 1
                    else:
                        detail["kudos_out"] += 1
        
        detail_key = str(submission.index)
        details[detail_key] = detail

    members = load_history("member")
    for member in members.values():
        member["submissions_active"] = []  # start fresh on active submissions

    for _, detail in details.items():
        for author in detail["authors"]:
            submission_index = detail["index"]
            sid = detail["sid"]
            uid = author["uid"]
            member_key = str(uid)

            member = members[member_key] if member_key in members else {
                "uid": uid,
                "sid": None,
                "submission": None,
                "submissions_active": [],
                "submissions_allpast": [],
                "switch_count": 0,
            }

            if member["submission"] is None:
                member["submission"] = submission_index
                member["sid"] = sid

            if submission_index not in member["submissions_active"]:
                member["submissions_active"].append(submission_index)
            if submission_index not in member["submissions_allpast"]:
                member["submissions_allpast"].append(submission_index)

            members[member_key] = member

    # check if member dropped from the effective team
    for member in members.values():
        if len(member["submissions_active"]) == 0:
            member["submission"] = None
            member["sid"] = None
        elif member["submission"] not in member["submissions_active"]:
            member["submission"] = random.choice(member["submissions_active"])
            member["sid"] = details[str(member["submission"])]["sid"]
            member["switch_count"] += 1

    for _, detail in details.items():
        for author in detail["authors"]:
            if members[str(author["uid"])]["submission"] == detail["index"]:
                author["effective"] = True

    save_history("member", members, dts)
    
    return details, members

def update_history(load_only):
    history_submission = load_history("submission")

    if load_only:
        details.update(history_submission["latest"])
    else:
        if "history" not in history_submission:
            history_submission["history"] = {}
        history_submission["history"][dts] = details
        history_submission["latest"] = details
        save_history("submission", history_submission, dts)

    wiki_text = wiki_submission_history(dt, history_submission)
    request_update_wiki("log", wiki_text)


def update_ranking(load_only):
    rankings_kudos = {}
    rankings_popular = {}
    rankings_scoring = {}
    
    if load_only:
        history_submission = load_history("ranking")
        rankings_kudos = history_submission["latest"]["kudos"]
        rankings_popular = history_submission["latest"]["popular"]
        rankings_scoring = history_submission["latest"]["scoring"]

    else:
        sids = []
        for _, detail in details.items():
            sid = detail["sid"]
            if sid not in sids:
                sids.append(sid)

        rankings_kudos = calculate_rankings_kudos(charts, sids, members)
        rankings_popular = calculate_rankings_popular(charts, sids)
        rankings_scoring = calculate_rankings_scoring(charts, sids)
        history_ranking = {
            "latest": {
                "kudos": rankings_kudos,
                "popular": rankings_popular,
                "scoring": rankings_scoring,
            }
        }
        save_history("ranking", history_ranking, dts)

    history_store = load_history("store")
    rankings_store = history_store.get("ranking") or {}
    rankings_store_delta = calculate_rankings_store_delta(rankings_kudos, rankings_popular, rankings_scoring)

    for ranking_key in list(rankings_store.keys()):
        if ranking_key not in rankings_store_delta:
            rankings_store.pop(ranking_key)

    for ranking_key, ranking_delta in rankings_store_delta.items():
        if ranking_key not in rankings_store:
            rankings_store[ranking_key] = 0
        rankings_store[ranking_key] += ranking_delta

    rankings_store_number = number_of_chart_for_store(len(rankings_store))
    rankings_store_selected = dict(sorted(rankings_store.items(), key = lambda item: item[1], reverse = True)[:rankings_store_number])
    
    for ranking_key in rankings_store_selected:
        rankings_store[ranking_key] = 0
    
    history_store["ranking"] = rankings_store
    history_store["delta"] = rankings_store_delta
    save_history("store", history_store, dts)

    wiki_blocks = [
        block_ranking_table_store("Currently In Store", details, rankings_store_selected, rankings_store_delta, False),
        block_ranking_table_kudos("Kudos Ranking", details, rankings_kudos),
        block_ranking_table_popular("Popular Ranking", details, rankings_popular),
        block_ranking_table_score("Scoring Ranking", details, rankings_scoring),
    ]
    
    wiki_text = "\n\n".join(wiki_blocks)
    request_update_wiki("rank", wiki_text)

    store_cids = []
    for _, detail in iter_sid_detail(details, rankings_store_selected):
        store_cids.extend(detail["cids"])

    request_update_store(store_cids)

