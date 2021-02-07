import requests
import json
import os
import re
import time
import random
import html2text
import pygtrie
import getmac

from chart import *


#topic_index = 1330 # for testing
topic_index = 1344

op_name = "LuiCat"
op_uid = 8502
op_psw = "1f145578899cd2a1c9f307df7d1ecd35"

op_token = None
op_cookies = None

eid = 43

time_script = int(time.time())

ma_version = 4 * 0x10000 + 3 * 0x100 + 0


def bkdr(s):
    seed = 131
    hash = 0
    for c in s:
        hash = (hash * seed + ord(c)) & 0xFFFFFFFFFFFFFFFF
    return hash

def h2t(html):
    return html2text.html2text(html).strip()

def request_text(url):
    response = requests.get(
        url, params = dict(t = time_script),
        cookies = op_cookies,
        headers = {
            "Origin": "http://m.mugzone.net",
            "Referer": "http://m.mugzone.net/index",
            "X-CSRFToken": op_cookies["csrftoken"] if op_cookies is not None else None,
            "X-Requested-With": "XMLHttpRequest"
        }
    )
    print("GET %s" % response.url)
    if response != None and response.ok:
        print()
        return response.text
    print("!!!!!!!!!! Request Failed: %s !!!!!!!!!!" % response.status_code)
    #print(response.text)
    #print("!!!!!!!!!! response above !!!!!!!!!!")
    print()
    return None

def request_json(url):
    return json.loads(request_text(url))

def request_talk_list(key):
    talk_list = []
    latest_time = 0
    
    while True:
        request_url = "http://m.mugzone.net/plugin/talk/list?key=%s&order=1&start=%d" % (key, latest_time)
        obj = request_json(request_url)
        if obj == None or "data" not in obj or "list" not in obj["data"]:
            break

        data = obj["data"]
        replies = data["list"]
        talk_list.extend(replies)

        if len(replies) == 0 or "next" not in data or not data["next"]:
            break

        for reply in replies:
            if reply["time"] > latest_time:
                latest_time = reply["time"]

    return talk_list

def request_session(force_update = False):
    global op_cookies
    if op_cookies is not None and not force_update:
        return
    response = requests.get("http://m.mugzone.net/wiki/2119")
    if not response.ok:
        print("Cannot load wiki")
        return None
    response = requests.post("http://m.mugzone.net/accounts/login",
        data = dict(email = op_name, psw = op_psw),
        cookies = response.cookies,
        headers = {
            "Origin": "http://m.mugzone.net",
            "Referer": "http://m.mugzone.net/index",
            "X-CSRFToken": response.cookies["csrftoken"],
            "X-Requested-With": "XMLHttpRequest"
        })
    op_cookies = response.cookies if "sessionid" in response.cookies else None
    return op_cookies

def request_token(force_update = False):
    global op_token
    if op_token is not None and not force_update:
        return
    url = "http://m.mugzone.net/cgi/login"
    response = requests.post(url,
        data = {
            "name": op_name,
            "psw": op_psw,
            "v": ma_version,
            "h": bkdr(getmac.get_mac_address())
        },
        headers = {
	        "MaVersion": str(ma_version),
	        "Referer": "http://m.mugzone.net",
            "X-Requested-With": "XMLHttpRequest"
        })
    op_token = json.loads(response.text)["data"]["key"] if response.ok else None
    return op_token

def request_update_wiki(key, content):
    request_session()
    response = requests.post("http://m.mugzone.net/wiki/edit",
        data = dict(key = "wiki_%s_1" % key, content = content),
        cookies = op_cookies,
        headers = {
            "Origin": "http://m.mugzone.net",
            "Referer": "http://m.mugzone.net/index",
            "X-CSRFToken": op_cookies["csrftoken"],
            "X-Requested-With": "XMLHttpRequest"
        })
    if not response.ok:
        print("!!!!!!!!!! Wiki %d Update Failed: %s !!!!!!!!!!" % (key, response.status_code))
    return response.ok

def request_update_store(cids):
    request_token()
    response = requests.post("http://m.mugzone.net/cgi/chart/update",
        params = dict(uid = op_uid, key = op_token),
        data = dict(eid = eid, cid = "[" + (",".join(str(cid) for cid in cids) + "]")),
        headers = {
	        "MaVersion": str(ma_version),
	        "Referer": "http://m.mugzone.net",
            "X-Requested-With": "XMLHttpRequest"
        })
    if not response.ok:
        print("!!!!!!!!!! Store Update Failed: %s !!!!!!!!!!" % response.status_code)
        return False
    obj = json.loads(response.text)
    if "code" not in obj or obj["code"] != 0:
        print("!!!!!!!!!! Store Update Failed, Code: %s !!!!!!!!!!" % obj["code"])
        return False
    return response.ok


def get_submissions(header_index = 0, report_index = 1, submissions_start_index = 2):
    submissions = {}
    talk_list = request_talk_list("topic_%s" % topic_index)

    for index, reply in enumerate(talk_list):
        if index < submissions_start_index:
            continue
        content = h2t(reply["content"])

        match = re.search("(?:s|song\/)(\d+)", content)
        if not match:
            continue

        sid = int(match.groups()[0])
        uid = reply["uid"]
        author = reply["name"]
        submissions[uid] = (sid, author)

        print("%s (uid %d): s%d" % (author, uid, sid))

    print()
    return submissions

def get_user_avatar(uid):
    request_session()
    response = request_text("http://m.mugzone.net/accounts/user/%d" % uid)
    if response == None:
        return None

    match = re.search(
        "<div class=\"coverb\">\n"
        "<img src=\"([^\"]+)\"",
        response
    )
    groups = match.groups()

    return groups[0]

def get_song_stat(sid):
    response = request_text("http://m.mugzone.net/song/%d" % sid)
    if response == None:
        return None

    match = re.search(
        "<h2 class=\"textfix title\"><span class=\"textfix artist\">([^<]*)</span> - ([^<]*)</h2>",
        response
    )
    groups = match.groups("0")

    artist = h2t(groups[0])
    title = h2t(groups[1])

    match = re.search(
        "<div class=\"cover\" style=\"background-image:url\(([^)]+)\)\"></div>",
        response
    )
    groups = match.groups()

    cover = groups[0]

    matches = re.findall(
        "<h2 class=\"item\">"
        "(?:[^<]|<[^/]|</[^h]|\n)+"  # matches any string with newline that don't include "</h"
        "/chart/(\d+)"
        "(?:[^<]|<[^/]|</[^h]|\n)+"
        "/user/(\d+)"
        "(?:[^<]|<[^/]|</[^h]|\n)+"
        "</h2>",
        response
    )

    diffs = []
    for cid_s, uid_s in matches:
        diffs.append(Chart(
            sid = sid,
            cid = int(cid_s),
            uid = int(uid_s)
        ))

    print("%s - %s, s%d, %d diffs" % (artist, title, sid, len(diffs)))
    print()

    return Song(
        sid = sid,
        artist = artist,
        title = title,
        cover = cover,
        diffs = diffs
    )


def get_chart_stat(cid):
    response = request_text("http://m.mugzone.net/chart/%d" % cid)
    if response == None:
        return None

    match = re.search(
        "<div class=\"song_title g_rblock\">"
        "\n(?:.*\n)*"
        "<div class=\"tail\">\n"
        "<a href=\"/song/(\d+)\">Back to song</a>\n"
        "(?:.*\n)*"
        "<em class=\"t\d\">([^<]*)</em>\n"
        "<span class=\"textfix artist\">([^<]*)</span> - ([^<]*)</h2>\n"
        "(?:.*\n)*"
        "<img src=\"/static/img/mode/mode-(\d).png\".*\n"
        "<span>([^<]*)</span>(?:\n.*)*Created by:"
        ".*\n.*\n"
        "<a href=\"/accounts/user/(\d+)\">([^<]*)</a>",
        response
    )
    groups = match.groups("0")

    sid = int(groups[0])
    state = groups[1].lower()
    artist = h2t(groups[2])
    title = h2t(groups[3])
    mode = mode_names[int(groups[4])]
    diff = h2t(groups[5])
    uid = int(groups[6])
    author = h2t(groups[7])
    print("%s - %s [%s] (%s), s%d c%d, by %s (uid %d), %s" % (artist, title, mode, diff, sid, cid, author, uid, state))

    match = re.search(
        "<div class=\"[^\"]*like_area\">"
        "(?:\n.*)+<span class=\"l\">(\d+).*"
        "(?:\n.*)+<span class=\"l\">(\d+).*"
        "(?:\n.*)+<span class=\"l\">(\d+).*",
        response
    )
    groups = match.groups("0")

    hot = int(groups[0])
    rcmd = int(groups[1])
    unrcmd = int(groups[2])
    print("hot: %d, rcmd: %d/%d" % (hot, rcmd, unrcmd))

    matches = re.findall(
        "<div class=\"donate_area g_tmpl_grouplist\">\n"
        "(?:.*\n)*"
        "<a class=\"textfix\" href=\"/accounts/user/(\d+)\">"
        ".*\n.*"
        "Support:(\d+) gold",
        response
    )

    supporters = []
    for uid_supporter, gold in matches:
        supporters.append(Supporter(int(gold), int(uid_supporter)))
        print("uid%s supported %s gold" % (uid_supporter, gold))
    
    print()

    comments = request_talk_list("chart_%s" % cid)

    comments_count = 0
    recommends = []
    kudos = []
    kudos_name_pending = pygtrie.Trie()
    kudos_uid_given = set()
    for comment in comments:
        comment_type = comment.get("type", 0)
        commenter = comment["name"]
        uid_commenter = int(comment["uid"])
        content = h2t(comment["content"])

        if comment_type == 0:
            comments_count += 1

            if "kudos" in content.lower():
                for m in re.finditer('@', content):
                    content_left = content[m.end():]
                    name_pending = kudos_name_pending.longest_prefix(content_left)
                    if name_pending.key != None:
                        uid_giver = kudos_name_pending.pop(name_pending.key)
                        kudos.append(Kudos(False, uid_giver))
                        kudos_uid_given.add(uid_giver)
                        print("Kudos to %s (uid %d)" % (''.join(name_pending.key), uid_giver))
                    elif content_left.startswith(author) and uid_commenter in kudos_uid_given:
                        kudos_uid_given.remove(uid_commenter)
                        kudos.append(Kudos(True, uid_commenter))
                        print("Kudos from %s (uid %d)" % (commenter, uid_commenter))

            if uid_commenter != uid:
                kudos_name_pending[commenter] = uid_commenter

        elif comment_type == 1:
            print("%s from %s (uid %d)" % (content.split(',')[0], commenter, uid_commenter))
            recommends.append(Recommend("Not" not in content, uid_commenter))

    print()
    return Chart(
        cid = cid,
        sid = sid,
        uid = uid,
        author = author,
        artist = artist,
        title = title,
        mode = mode,
        diff = diff,
        state = state,
        hot = hot,
        rcmd = rcmd,
        unrcmd = unrcmd,
        supporters = supporters,
        comments_count = comments_count,
        recommends = recommends,
        kudos = kudos,
    )

