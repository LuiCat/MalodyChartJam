from history import *
from wiki_common import *


def line_ranking_table(detail, ranking):
    cells = [
        image_url(detail["cover"], 100) + "@newline" + link_song(detail),
        image_url(detail["avatar"], 100) + "@newline" + link_user(detail),
        "@newline".join(links_charts(detail)),
        str(ranking)
    ]
    return "| " + " | ".join(cells) + " |"

def block_ranking_table(ranking_title, details, rankings, hidden = True):
    lines = [
        "== " + ranking_title + " ==",
        "#hidden" if hidden else "",
        "|-",
        "|! Song | Chart Creator | Charts | Ranking Score |"
    ]
    uid_sorted = sorted(rankings.keys(), key = lambda uid: rankings[uid], reverse = True)
    for uid in uid_sorted:
        lines.append(line_ranking_table(details[str(uid)], rankings[uid]))
    lines.append("#end" if hidden else "")
    return "\n".join(lines)


"""
== Kudos Ranking ==

|-
|! Song | Chart Creator | Charts | Ranking Score |
| [img:http://cni.malody.cn/cover/8054!small?time=1612403848@100] @newline BEMANI Sound Team - EMERALDAS |  [img:http://cni.malody.cn/avatar/95645!avatar?time=1612076099@100] @newline 2nurupo_  | [http://m.mugzone.net/chart/85796 Oni Lv.26] @newline [http://m.mugzone.net/chart/85796 Oni Lv.26]@newline [http://m.mugzone.net/chart/85796 Oni Lv.26] | 12345 |
| [#aaaaaa:No Cover]  @newline  Test | [http://m.mugzone.net/chart/85796 Oni Lv.26] | No Name  | 12345 |
"""
