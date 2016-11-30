class ProductCommentSummary:
    def __init__(self, item):
        self.skuid = item[0]
        self.commentCount = item[1]
        self.goodCount = item[2]
        self.generalCount = item[3]
        self.poorCount = item[4]
        self.averageScore = item[5]
        self.goodRate = item[6]
        self.poorRate = item[7]
        self.generalRate = item[8]


class Comment:
    def __init__(self, item):
        self.id = item[0]
        self.productid = item[1]
        self.commentid = item[2]
        self.content = item[3]
        self.creationtime = item[4]
        self.referenceTime = item[5]
        self.score = item[6]
        self.userProvince = item[7]
        self.userRegisterTime = item[8]
        self.userLevelName = item[9]
        self.userClientShow = item[10]
        self.isMobile = item[11]
        self.days = item[12]
        # self.imageCount = item[11]


class HotTag:
    def __init__(self, item):
        self.id = item[0]
        self.productid = item[1]
        self.name = item[2]
        self.count = item[3]


class PriceTrend:
    def __init__(self, item):
        self.skuid = item[0]
        self.first_price = item[1]
        self.hislowest = item[2]
        self.hishighest = item[3]
        self.current_price = item[4]
        self.min_date = item[5]
        self.max_date = item[6]
        self.lowest_price = item[7]
        self.highest_price = item[8]
        self.shopfesday_price = item[9]