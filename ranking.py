
def validate_diff(diff, submission):
    return diff.uid in submission.uids

def validate_chart(chart, submission):
    if not validate_chart_rule_sancheck(chart): return False
    if not validate_chart_rule_banlist(chart): return False
    if not validate_chart_rule_nonstable(chart): return False
    return True


def validate_chart_rule_sancheck(chart):
    if chart == None:
        print("Invalid chart c%d" % chart.cid)
        print()
        return False
    return True
    
def validate_chart_rule_banlist(chart):
    return True
    
def validate_chart_rule_nonstable(chart):
    if chart.state == "stable":
        print("No stable chart c%d" % chart.cid)
        print()
        return False
    return True


def calculate_rankings_kudos(charts, sids, members):
    rankings = dict.fromkeys([str(sid) for sid in sids], 0)
    for chart in charts:
        for kudos in chart.kudos:
            member_key = str(kudos.uid)
            if member_key not in members:
                continue
            member = members[str(kudos.uid)]
            kudos_sid = member["sid"]
            if kudos_sid in rankings:
                rankings[str(chart.sid if kudos.inward else kudos_sid)] += 1
    return rankings


def calculate_rankings_popular(charts, sids):
    rankings = dict.fromkeys([str(sid) for sid in sids], 0)
    for chart in charts:
        rankings[str(chart.sid)] += chart.hot + chart.rcmd * 20 + chart.unrcmd * 20 + chart.comments_count * 100
    return rankings


def calculate_rankings_scoring(charts, sids):
    rankings = dict.fromkeys([str(sid) for sid in sids], 0)
    for chart in charts:
        score = 0
        # for supporter in chart.supporters:
        #     if supporter.uid == chart.uid:
        #         continue
        #     score += supporter.gold
        for recommend in chart.recommends:
            if recommend.uid == chart.uid:
                continue
            score += 500 if recommend.upvote else -500
        rankings[str(chart.sid)] += score
    return rankings

def calculate_rankings_store_delta(rankings_kudos, rankings_popular, rankings_scoring):
    rankings = {}
    for sid in rankings_kudos:
        rankings[sid] = round(500 +                       # base increment
            rankings_kudos[sid] * 1000 +                  # kudos
            rankings_popular[sid] * 1 +                   # popular
            max(0, 200 - rankings_popular[sid]) * 10 +    # discovery
            rankings_scoring[sid] * 0.2)                  # scoring
    return rankings

def number_of_chart_for_store(charts_count):
    return min(8, round((charts_count + 0.1) / 2))
