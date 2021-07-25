def link_user(user):
    return "[http://m.mugzone.net/accounts/user/%d %s]" % (user["uid"], user["name"])

def link_song(detail):
    return "[http://m.mugzone.net/song/%d %s]" % (detail["sid"], detail["name"])

def link_chart(detail, cid):
    return "[http://m.mugzone.net/chart/%d %s]" % (cid, detail["diffs"][str(cid)])

def link_team_name(detail, link = None):
    return detail["team"] if link is None else "[%s %s]" % (link, detail["team"])

def link_team_members(detail, separator = ", "):
    return separator.join([link_user(user) for user in detail["authors"]])

def links_charts(detail):
    links = []
    for cid in detail["cids"]:
        links.append(link_chart(detail, cid))
    return links

def link_song_charts(detail):
    return ("with " + ", ".join(links_charts(detail))) if len(detail["cids"]) > 0 else "without charts"

def link_song_with_charts(detail):
    return link_song(detail) + " " + link_song_charts(detail)

def image_url(url, width):
    return "[img:%s@%d]" % (url, width)

def image_mode(mid, width = 40):
    return "[img:http://m.mugzone.net/static/img/mode/mode-%d.png@%d]" % (mid, width)


def line_team(detail):
    return link_team_name(detail) + "@newline" + link_team_members(detail, "@newline")

def line_modes(detail, width = 40):
    return "".join([image_mode(mid, width) for mid in detail["mids"]])

def line_song(detail):
    return link_song(detail) + ("@newline" + detail["meta"] if detail["meta"] is not None else "")
