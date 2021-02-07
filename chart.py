mode_names = ["key", "step", "dj", "catch", "pad", "taiko", "ring", "slide"]

class Song:
    def __init__(self, **kwargs):
        self.sid = None,
        self.artist = None,
        self.title = None,
        self.cover = None,
        self.diffs = [],
        self.__dict__.update({ k: v for k,v in kwargs.items() if k in self.__dict__ })

class Chart:
    def __init__(self, **kwargs):
        self.cid = None,
        self.sid = None,
        self.uid = None,
        self.author = None,
        self.artist = None,
        self.title = None,
        self.mode = None,
        self.diff = None,
        self.state = None,
        self.hot = 0,
        self.rcmd = 0,
        self.unrcmd = 0,
        self.supporters = [],
        self.comments_count = 0,
        self.recommends = [],
        self.kudos = [],
        self.__dict__.update({ k: v for k,v in kwargs.items() if k in self.__dict__ })

class Supporter:
    def __init__(self, gold, uid):
        self.gold = gold
        self.uid = uid

class Kudos:
    def __init__(self, inward, uid):
        self.inward = inward
        self.uid = uid

class Recommend:
    def __init__(self, upvote, uid):
        self.upvote = upvote
        self.uid = uid

