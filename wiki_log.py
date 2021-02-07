from history import *
from wiki_common import *


def line_submission_add(detail):
    return link_user(detail) + " submitted " + link_song_with_charts(detail) + "."

def line_submission_change(detail_old, detail):
    return link_user(detail) + " changed submission " + link_song(detail_old) + " to " + link_song_with_charts(detail) + "."

def line_submission_remove(detail_old):
    return link_user(detail) + " removed submission " + link_song(detail_old) + "."

def line_submission_rename(detail_old, detail):
    return link_user(detail) + " modified song name " + link_song(detail_old) + " to " + link_song(detail) + "."

def line_submission_diff_add(detail, cid):
    return link_user(detail) + " added new chart " + link_chart(detail, cid) + " for " + link_song(detail) + "."

def line_submission_diff_remove(detail_old, cid):
    return link_user(detail) + " removed chart " + link_chart(detail_old, cid) + " for " + link_song(detail_old) + "."

def line_submission_diff_rename(detail_old, detail, cid):
    return link_user(detail) + " renamed chart " + link_chart(detail_old, cid) + " to " + link_chart(detail, cid) + " for " + link_song(detail) + "."

def lines_submission_diff(detail_old, detail, cid):
    result = []
    if str(cid) not in detail_old["diffs"]:
        result.append(line_submission_diff_add(detail, cid))
    elif str(cid) not in detail["diffs"]:
        result.append(line_submission_diff_remove(detail_old, cid))
    elif detail["diffs"][str(cid)] != detail_old["diffs"][str(cid)]:
        result.append(line_submission_diff_rename(detail_old, detail, cid))
    return result

def lines_submission(detail_old, detail):
    result = []
    if detail_old is None:
        result.append(line_submission_add(detail))
    elif detail is None:
        result.append(line_submission_remove(detail_old))
    elif detail["sid"] != detail_old["sid"]:
        result.append(line_submission_change(detail_old, detail))
    elif detail["name"] != detail_old["name"]:
        result.append(line_submission_rename(detail_old, detail))
    else:
        cids = set(detail_old["cids"]).union(set(detail["cids"]))
        for cid in cids:
            result.extend(lines_submission_diff(detail_old, detail, cid))
    return result

def lines_submissions(details_old, details):
    result = []
    uids = set(details_old.keys()).union(set(details.keys()))
    for uid in uids:
        result.extend(lines_submission(details_old.get(uid), details.get(uid)))
    return result

def block_history_update(dt, details_old, details):
    lines = lines_submissions(details_old, details)
    if len(lines) == 0:
        return None
    return "\n\n".join(["=== Since " + dt.strftime("%Y/%m/%d %H:%M:%S GMT+8") + " ==="]  + lines)

def block_history(history):
    blocks = []
    dt_sorted = sorted([ s2dt(dts) for dts in history ])
    details_old = {}
    for dt in dt_sorted:
        details = history[dt2s(dt)]
        block = block_history_update(dt, details_old, details)
        if block is not None:
            blocks.append(block)
        details_old = details
    return "\n\n".join(blocks)

def line_submission_table_charts(detail):
    return "@newline".join(links_charts(detail)) if len(detail["cids"]) > 0 else "[#aaaaaa:Empty]"

def line_submission_table(detail):
    cells = [
        link_user(detail),
        link_song(detail),
        line_submission_table_charts(detail),
        str(detail["hot"]),
        str(detail["gold"]),
        str(detail["re"]) + "/" + str(detail["un"]),
        str(detail["comments"]),
        str(detail["kudos_in"]) + "/" + str(detail["kudos_out"]),
    ]
    return "| " + " | ".join(cells) + " |"

def block_submission_table(dt, details):
    lines = [
        "Update time: " + dt.strftime("%Y/%m/%d %H:%M:%S GMT+8"),
        "",
        "|-",
        "|! Author | Song | Charts | Hot | Gold | Re/Un | Comments | Kudos In/Out |"
    ]
    for uid, detail in details.items():
        lines.append(line_submission_table(detail))
    return "\n".join(lines)

def wiki_submission_history(dt, history_submission):
    blocks = [
        "== Current Submissions ==",
        block_submission_table(dt, history_submission["latest"]),
        "== History ==",
        block_history(history_submission["history"])
    ]
    return "\n\n".join(blocks)


"""
== Current Submissions ==

Update time: 2021/2/4 12:34

|-
|! Author | Song | Charts | Hot | Gold | Re/Un | Comments | Kudos In/Out |
| [http://m.mugzone.net/accounts/user/8502 LuiCat] | [http://m.mugzone.net/song/4870 dj Hellix - Quakes] | [http://m.mugzone.net/chart/78003 Extra Lv.29]@newline[http://m.mugzone.net/chart/78003 Extra Lv.29]@newline[http://m.mugzone.net/chart/78003 Extra Lv.29] | 123 | 12345 | 12/34 | 12 | 12/34 |
| [http://m.mugzone.net/accounts/user/8502 LuiCat] | [http://m.mugzone.net/song/4870 dj Hellix - Quakes] | [#aaaaaa:Empty] | 123 | 12345 | 12/34 | 12 | 12/34 |

== History ==

=== 2021/2/4 12:34 ===

[http://m.mugzone.net/accounts/user/8502 LuiCat] submitted song [http://m.mugzone.net/song/4870 dj Hellix - Quakes] with **[http://m.mugzone.net/chart/78003 Extra Lv.29]**, [http://m.mugzone.net/chart/78003 Extra Lv.29], [http://m.mugzone.net/chart/78003 Extra Lv.29]

[http://m.mugzone.net/accounts/user/8502 LuiCat] submitted song [http://m.mugzone.net/song/4870 dj Hellix - Quakes] without charts

[http://m.mugzone.net/accounts/user/8502 LuiCat] changed submission to song [http://m.mugzone.net/song/4870 dj Hellix - Quakes] with  
[http://m.mugzone.net/chart/78003 Extra Lv.29], [http://m.mugzone.net/chart/78003 Extra Lv.29], [http://m.mugzone.net/chart/78003 Extra Lv.29]

[http://m.mugzone.net/accounts/user/8502 LuiCat] changed submission to song [http://m.mugzone.net/song/4870 dj Hellix - Quakes] without charts

[http://m.mugzone.net/accounts/user/8502 LuiCat] removed submission on song [http://m.mugzone.net/song/4870 dj Hellix - Quakes]

[http://m.mugzone.net/accounts/user/8502 LuiCat] added new chart [http://m.mugzone.net/chart/78003 Extra Lv.29] for [http://m.mugzone.net/song/4870  dj Hellix - Quakes]

[http://m.mugzone.net/accounts/user/8502 LuiCat] removed chart [http://m.mugzone.net/chart/78003 Extra Lv.29] for [http://m.mugzone.net/song/4870  dj Hellix - Quakes]

[http://m.mugzone.net/accounts/user/8502 LuiCat] modified song name [http://m.mugzone.net/song/4870 dj Hellix - Quakes] to  [http://m.mugzone.net/song/4870 dj Hellix - Quakes]

[http://m.mugzone.net/accounts/user/8502 LuiCat] modified chart difficulty name [http://m.mugzone.net/chart/78003 Extra Lv.29] to  [http://m.mugzone.net/chart/78003 Extra Lv.29]
"""
