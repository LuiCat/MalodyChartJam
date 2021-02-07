from datetime import datetime

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

if request_token() is None:
    print("??")
    exit(0)
else:
    print("I'm in-game online!")
print()


charts = []
details = {}


def fetch_submissions():
    submissions = get_submissions()
    for uid, (sid, author) in submissions.items():
        song = get_song_stat(sid)
        avatar = get_user_avatar(uid)

        detail = {
            "name": "%s - %s" % (song.artist, song.title), "author": author, "cover": song.cover, "avatar": avatar,
            "uid": uid, "sid": sid, "cids": [], "diffs": {},
            "hot": 0, "gold": 0, "re": 0, "un": 0, "comments": 0, "kudos_in": 0, "kudos_out": 0
        }

        for diff in song.diffs:
            if diff.uid != uid:
                continue
            chart = get_chart_stat(diff.cid)
            if validate_chart(chart):
                charts.append(chart)

                detail["cids"].append(chart.cid)
                detail["diffs"][str(chart.cid)] = chart.diff

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
                
        details[str(uid)] = detail


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
    request_update_wiki(2133, wiki_text)


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
        rankings_kudos = calculate_rankings_kudos(charts)
        rankings_popular = calculate_rankings_popular(charts)
        rankings_scoring = calculate_rankings_scoring(charts)
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

    for uid, ranking_delta in rankings_store_delta.items():
        if uid not in rankings_store:
            rankings_store[uid] = 0
        rankings_store[uid] += ranking_delta

    rankings_store_number = number_of_chart_for_store(len(rankings_store))
    rankings_store_selected = dict(sorted(rankings_store.items(), key = lambda item: item[1], reverse = True)[:rankings_store_number])
    
    for uid in rankings_store_selected:
        rankings_store[uid] = 0
    
    history_store["ranking"] = rankings_store
    history_store["delta"] = rankings_store_delta
    save_history("store", history_store, dts)

    wiki_blocks = [
        block_ranking_table("Current In Store", details, rankings_store_selected, False),
        block_ranking_table("Kudos Ranking", details, rankings_kudos),
        block_ranking_table("Popular Ranking", details, rankings_popular),
        block_ranking_table("Scoring Ranking", details, rankings_scoring),
    ]
    
    wiki_text = "\n\n".join(wiki_blocks)
    request_update_wiki(2134, wiki_text)

    store_cids = []
    for uid in rankings_store_selected:
        store_cids.extend(details[str(uid)]["cids"])

    request_update_store(store_cids)




# todo: randomly select charts for store, and save the total selected count as a file
# todo: ban list
