from history import *
from wiki_common import *


def line_submission_add(detail):
    return "**" + link_team_name(detail) + "** submitted " + link_song_with_charts(detail) + ", with members " + link_team_members(detail) + "."

def line_submission_change(detail_old, detail):
    return "**" + link_team_name(detail) + "** changed submission " + link_song(detail_old) + " to " + link_song_with_charts(detail) + "."

def line_submission_remove(detail_old):
    return "**" + link_team_name(detail_old) + "** removed submission " + link_song(detail_old) + "."

def line_submission_rename(detail_old, detail):
    return "**" + link_team_name(detail) + "** modified song name " + link_song(detail_old) + " to " + link_song(detail) + "."

def line_submission_diff_add(detail, cid):
    return "**" + link_team_name(detail) + "** added new chart " + link_chart(detail, cid) + " for " + link_song(detail) + "."

def line_submission_diff_remove(detail_old, cid):
    return "**" + link_team_name(detail_old) + "** removed chart " + link_chart(detail_old, cid) + " for " + link_song(detail_old) + "."

def line_submission_diff_rename(detail_old, detail, cid):
    return "**" + link_team_name(detail) + "** renamed chart " + link_chart(detail_old, cid) + " to " + link_chart(detail, cid) + " for " + link_song(detail) + "."

def line_submission_team_rename(detail_old, detail):
    return "**" + link_team_name(detail_old) + "** renamed team name to " + link_team_name(detail) + "."

def line_submission_team_member_change(detail):
    return "**" + link_team_name(detail) + "** modified team member, now with " + link_team_members(detail) + "."

def line_submission_team_member_change_check(detail_old, detail):
    s = {}
    for author in detail_old["authors"]:
        s[author["uid"]] = True
    for author in detail["authors"]:
        if author["uid"] not in s:
            return line_submission_team_member_change(detail)
        s[author["uid"]] = False
    for author in detail_old["authors"]:
        if s[author["uid"]] == True:
            return line_submission_team_member_change(detail)
    return None

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
    else:
        if detail["sid"] != detail_old["sid"]:
            result.append(line_submission_change(detail_old, detail))
        elif detail["name"] != detail_old["name"]:
            result.append(line_submission_rename(detail_old, detail))
        else:
            cids = set(detail_old["cids"]).union(set(detail["cids"]))
            for cid in cids:
                result.extend(lines_submission_diff(detail_old, detail, cid))
        if detail["team"] != detail_old["team"]:
            result.append(line_submission_team_rename(detail_old, detail))
        else:
            result.extend(line_submission_team_member_change_check(detail_old, detail))
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
        line_team(detail),
        line_song(detail),
        line_modes(detail),
        line_submission_table_charts(detail),
        str(detail["hot"]),
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
        "|! Team | Song | Mode | Charts | Hot | Re/Un | Comments | Kudos In/Out |"
    ]
    for _, detail in details.items():
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

