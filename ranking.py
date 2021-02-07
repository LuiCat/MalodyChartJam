
        
def validate_chart(chart):
    if chart == None:
        print("Invalid chart c%d" % chart.cid)
        print()
        return False

    if chart.mode != "taiko":
        print("Wrong mode [%s] c%d" % (chart.mode, chart.cid))
        print()
        return False

    if chart.state == "stable":
        print("No stable chart c%d" % chart.cid)
        print()
        return False
        
    return True


def calculate_rankings_kudos(charts):
    rankings = {}
    for chart in charts:
        rankings[chart.uid] = 0
    for chart in charts:
        for kudos in chart.kudos:
            if kudos.uid in rankings:
                rankings[chart.uid if kudos.inward else kudos.uid] += 1
    return rankings


def calculate_rankings_popular(charts):
    rankings = {}
    for chart in charts:
        rankings[chart.uid] = 0
    for chart in charts:
        rankings[chart.uid] += chart.hot + chart.rcmd * 20 + chart.unrcmd * 20 + chart.comments_count * 100
    return rankings


def calculate_rankings_scoring(charts):
    rankings = {}
    for chart in charts:
        rankings[chart.uid] = 0
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
        rankings[chart.uid] += score
    return rankings

def calculate_rankings_store_delta(rankings_kudos, rankings_popular, rankings_scoring):
    rankings = {}
    for uid in rankings_kudos:
        rankings[uid] = round(1000 +                      # base increment
            rankings_kudos[uid] * 1000 +                  # kudos
            rankings_popular[uid] * 1 +                   # popular
            max(0, 200 - rankings_popular[uid]) * 10 +    # discovery
            rankings_scoring[uid] * 0.1)                  # scoring
    return rankings

def number_of_chart_for_store(charts_count):
    return min(6, round(charts_count / 2))
