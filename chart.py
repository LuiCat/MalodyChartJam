mode_names = ["key", "step", "dj", "catch", "pad", "taiko", "ring", "slide"]

class Chart:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

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
        self.inward = upvote
        self.uid = uid

