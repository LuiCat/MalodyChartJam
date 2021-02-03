
        
def validate_chart(chart):
    if chart == None:
        print("Invalid chart c%d" % chart.cid)
        return False

    if chart.mode != "taiko":
        print("Wrong mode [%s] c%d" % (chart.mode, chart.cid))
        return False

    if chart.state == "stable":
        print("No stable chart c%d" % chart.cid)
        
    return True


def rankings_kudos(charts):
    rankings = {}
    for chart in charts:
        rankings[chart.uid] = 0
    for chart in charts:
        for kudos in chart.kudos:
            if kudos.uid in rankings:
                rankings[chart.uid if kudos.inward else kudos.uid] += 1
    return rankings


def ranking_popular(charts):
    rankings = {}
    for chart in charts:
        rankings[chart.uid] = chart.hot + chart.rcmd * 20 + chart.unrcmd * 20 + chart.comments_count * 100
    return rankings


def ranking_scoring(charts):
    rankings = {}
    for chart in charts:
        score = 0
        for supporter in chart.supporters:
            if supporter.uid == chart.uid:
                continue
            score += supporter.gold
        for recommend in chart.recommends:
            if recommend.uid == chart.uid:
                continue
            score += 500 if recommend.upvote else -500
        rankings[chart.uid] = score
    return rankings

