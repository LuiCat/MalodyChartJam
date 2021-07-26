from history import *
from wiki_common import *


def iter_sid_detail(details, rankings):
    sid_to_key = {}
    for key, detail in details.items():
        sid_to_key[str(detail["sid"])] = key
    return [(sid, details[sid_to_key[sid]]) for sid in sorted(rankings.keys(), key = lambda sid: rankings[sid], reverse = True)]


def line_ranking_table(detail, *rankings):
    cells = [
        image_url(detail["cover"], 100) + "@newline" + link_song(detail),
        line_team(detail),
        "@newline".join(links_charts(detail)),
    ]
    cells.extend([str(ranking) for ranking in rankings])
    return "| " + " | ".join(cells) + " |"

def block_ranking_table_store(title, details, rankings, rankings_delta, hidden = True):
    lines = [
        "== " + title + " ==",
        "#hidden" if hidden else "",
        "|-",
        "|! Song | Team | Charts | Ranking Rate (Delta) |"
    ]
    for sid, detail in iter_sid_detail(details, rankings):
        lines.append(line_ranking_table(detail, "%s (%s)" % (rankings[sid], rankings_delta[sid])))
    lines.append("#end" if hidden else "")
    return "\n".join(lines)

def block_ranking_table_kudos(title, details, rankings, hidden = True):
    lines = [
        "== " + title + " ==",
        "#hidden" if hidden else "",
        "|-",
        "|! Song | Team | Charts | Kudos In/Out | Score |"
    ]
    for sid, detail in iter_sid_detail(details, rankings):
        lines.append(line_ranking_table(detail,
            str(detail["kudos_in"]) + "/" + str(detail["kudos_out"]),
            rankings[sid]))
    lines.append("#end" if hidden else "")
    return "\n".join(lines)

def block_ranking_table_popular(title, details, rankings, hidden = True):
    lines = [
        "== " + title + " ==",
        "#hidden" if hidden else "",
        "|-",
        "|! Song | Team | Charts | Hot | Re/Un | Comments | Score |"
    ]
    for sid, detail in iter_sid_detail(details, rankings):
        lines.append(line_ranking_table(detail,
            str(detail["hot"]),
            str(detail["re"]) + "/" + str(detail["un"]),
            str(detail["comments"]),
            rankings[sid]))
    lines.append("#end" if hidden else "")
    return "\n".join(lines)

def block_ranking_table_score(title, details, rankings, hidden = True):
    lines = [
        "== " + title + " ==",
        "#hidden" if hidden else "",
        "|-",
        "|! Song | Team | Charts | Score |"
    ]
    for sid, detail in iter_sid_detail(details, rankings):
        lines.append(line_ranking_table(detail, rankings[sid]))
    lines.append("#end" if hidden else "")
    return "\n".join(lines)



"""
== Kudos Ranking ==

|-
|! Song | Chart Creator | Charts | Ranking Score |
| [img:http://cni.malody.cn/cover/8054!small?time=1612403848@100] @newline BEMANI Sound Team - EMERALDAS |  [img:http://cni.malody.cn/avatar/95645!avatar?time=1612076099@100] @newline 2nurupo_  | [http://m.mugzone.net/chart/85796 Oni Lv.26] @newline [http://m.mugzone.net/chart/85796 Oni Lv.26]@newline [http://m.mugzone.net/chart/85796 Oni Lv.26] | 12345 |
| [#aaaaaa:No Cover]  @newline  Test | [http://m.mugzone.net/chart/85796 Oni Lv.26] | No Name  | 12345 |
"""
