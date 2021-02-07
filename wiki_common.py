def link_user(detail):
    return "[http://m.mugzone.net/accounts/user/%d %s]" % (detail["uid"], detail["author"])

def link_song(detail):
    return "[http://m.mugzone.net/song/%d %s]" % (detail["sid"], detail["name"])

def link_chart(detail, cid):
    return "[http://m.mugzone.net/chart/%d %s]" % (cid, detail["diffs"][str(cid)])

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
