# -*- coding: UTF-8 -*-

import requests
import urllib
import json
import re
import time
import datetime
from bs4 import BeautifulSoup
import JDCommentScraping.Database
from JDCommentScraping.SpiderEntity import ProductCommentSummary, Comment, HotTag, PriceTrend

MOBILE_COMMENT_TABLE = "jd_comments_refrigerator"

class JDCommentDriver(object):
    def __init__(self, productid, url):
        self.url = url
        self.comments = requests.get(url).text
        # self.comments = self.comments[self.comments.find('(') + 1:][:-2]
        self.productid = productid
        self.comment_json = json.loads(self.comments)

    def storeProductCommentSummary(self):
        try:
            storage = JDCommentScraping.Database.MySQLStorage()
            for comment in self.comment_json['CommentsCount']:
                skuid = comment['SkuId']
                commentCount = int(comment['CommentCount'])
                goodCount = int(comment['GoodCount'])
                generalCount = int(comment['GeneralCount'])
                poorCount = int(comment['PoorCount'])
                averageScore = float(comment['AverageScore'])
                goodRate = float(comment['GoodRate'])
                poorRate = float(comment['PoorRate'])
                generalRate = float(comment['GeneralRate'])
                item = [skuid, commentCount, goodCount, generalCount,
                        poorCount, averageScore, goodRate, poorRate, generalRate]
                productSummary = ProductCommentSummary(item)
                storage.saveProductCommentSummary("jd_productsum_ac", productSummary)

        except Exception as err:
            print(err)

    def storeHotCommentTagStatistics(self):
        try:
            storage = JDCommentScraping.Database.MySQLStorage()
            cnt = 1
            for comment in self.comment_json['hotCommentTagStatistics']:
                productId = comment['productId']
                name = comment['name']
                count = int(comment['count'])
                item = [cnt, productId, name, count]
                hotTag = HotTag(item)
                storage.saveHotTag("jd_hottag_book", hotTag)
                cnt += 1

        except Exception as err:
            print(err)


    def storeComments(self, cnt):
        try:
            storage = JDCommentScraping.Database.MySQLStorage()

            if len(self.comment_json['comments']) == 0:
                return -1, cnt

            for comment in self.comment_json['comments']:
                id = cnt
                productid = self.productid
                commentid = comment['id']
                content = comment['content']
                if content != "":
                    content.replace(',', '')
                creationtime = comment['creationTime']
                referenceTime = comment['referenceTime']
                score = comment['score']
                userProvince = comment['userProvince']
                userRegisterTime = comment['userRegisterTime']
                userLevelName = comment['userLevelName']
                userClientShow = comment['userClientShow']
                if userClientShow != "" and len(userClientShow) > 0:
                    client_re = re.compile(r">(.*?)<")
                    userClientShow = re.findall(client_re, userClientShow)[0]
                isMobile = comment['isMobile']
                days = comment['days']
                # imageCount = comment['imageCount']
                item = [id, productid, commentid, content, creationtime, referenceTime, score,
                        userProvince, userRegisterTime, userLevelName, userClientShow,
                        isMobile, days]
                productComment = Comment(item)
                storage.saveComments(MOBILE_COMMENT_TABLE, productComment)
                cnt += 1
            return 1, cnt
        except Exception as err:
            print(err)
            raise Exception(self.productid)

    def timestamp2date(self, timestamp):
        if timestamp != "":
            timestamp = int(timestamp)
            timestruc = time.localtime(timestamp)
            date_time = time.strftime("%Y-%m-%d", timestruc)
            return date_time

    def strtodatetime(self, datestr, format = "%Y-%m-%d"):
        return datetime.datetime.strptime(datestr, format)

    def datediff(self, beginDate, endDate):
        format = "%Y-%m-%d"
        bd = self.strtodatetime(beginDate, format)
        ed = self.strtodatetime(endDate, format)
        oneday = datetime.timedelta(days=1)
        count = 0
        while bd != ed:
            ed = ed - oneday
            count += 1
        return count

    def getLowestPriceFromRange(self, priceRange):
        return min(priceRange)

    def getHighestPriceFromRange(self, priceRange):
        return max(priceRange)

    def getLowestPriceDate(self, max_stamp, priceRange):
        max_day = datetime.datetime.fromtimestamp(max_stamp)
        lowest_price = self.getLowestPriceFromRange(priceRange)
        diff = max([i for i, price in enumerate(priceRange) if price == lowest_price])
        diff = len(priceRange) - diff - 1
        lowest_date = max_day - datetime.timedelta(days=diff)
        return lowest_date, lowest_price

    def getHighestPriceDate(self, max_stamp, priceRange):
        max_day = datetime.datetime.fromtimestamp(max_stamp)
        highest_price = self.getHighestPriceFromRange(priceRange)
        diff = max([i for i, price in enumerate(priceRange) if price == highest_price])
        diff = len(priceRange) - diff - 1
        highest_date = max_day - datetime.timedelta(days=diff)
        return highest_date, highest_price

    def getShopFesDayPrice(self, max_stamp, priceRange):
        max_day = self.timestamp2date(max_stamp)
        shopfesday = "2016-11-11"
        diff = self.datediff(shopfesday, max_day) + 1
        shopfesday_price = priceRange[-diff]
        return shopfesday_price

    def storeProductPriceTrend(self):
        try:
            storage = JDCommentScraping.Database.MySQLStorage()
            for comment in self.comment_json['store']:
                first_price = comment['first_price']
                hislowest = comment['lowest']
                hishighest = comment['highest']
                current_price = comment['current_price']
                priceRange = comment['all_line']
                min_stamp = int(comment['min_stamp'])
                max_stamp = int(comment['max_stamp'])
                shopfesday_price = self.getShopFesDayPrice(max_stamp, priceRange)
                min_date, lowest_price = self.getLowestPriceDate(max_stamp, priceRange)
                max_date, highest_price = self.getHighestPriceDate(max_stamp, priceRange)
                item = [self.productid, first_price, hislowest, hishighest, current_price, min_date,
                        max_date, lowest_price, highest_price, shopfesday_price]
                priceTrend = PriceTrend(item)
                storage.savePriceTrend("jd_pricetrend_refrigerator", priceTrend)

        except Exception as err:
            print(err)


class JDItem(object):
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html)

    def get_product(self):
        try:
            product_re = re.compile(r'compatible: true,(.*?)};', re.S)
            product_info = re.findall(product_re, self.html)[0]
            return product_info
        except:
            pass

    def isJDSelfRun(self):
        try:
            jdTag = self.soup.find(class_='u-jd')

            if jdTag:
                return 'Y'
            return 'N'
        except Exception as err:
            print(err)

    def get_product_name(self):
        try:
            product_info = self.get_product()
            name_re = re.compile(r"name: '(.*?)',")
            name = re.findall(name_re, product_info)[0]
            name = name.encode("utf-8").decode("unicode-escape")
            return name
        except Exception as err:
            print(err)

    def get_product_price(self):
        try:
            price = None

            skuid = self.get_product_skuid()
            name = self.get_product_name()

            url = 'http://p.3.cn/prices/mgets?skuIds=J_' + skuid + '&type=1'

            price_json = json.load(urllib.urlopen(url))[0]

            if price_json['p']:
                price = price_json['p']
            return price
        except:
            pass

    def getLowest_price(self, product_url):
        try:
            url = "http://www.huihui.cn/api/myzhushou/productSense?" \
                  "callback=img&phu=%s&_=1478753066171" % (product_url)
            price_text = requests.get(url)
            price_re = re.compile(r'"min":(.*?),')
            lowestprice = re.findall(price_re, price_text.text)
            return lowestprice
        except Exception as err:
            print(err)

    def getHighest_price(self, product_url):
        try:
            url = "http://www.huihui.cn/api/myzhushou/productSense?" \
                  "callback=img&phu=%s&_=1478753066171" % (product_url)
            price_text = requests.get(url)
            price_re = re.compile(r'"max":(.*?),')
            highestprice = re.findall(price_re, price_text.text)
            return highestprice
        except Exception as err:
            print(err)

    def getToday_price(self, product_url):
        try:
            url = "http://www.huihui.cn/api/myzhushou/productSense?" \
                  "callback=img&phu=%s&_=1478753066171" % (product_url)
            price_text = requests.get(url)
            price_re = re.compile(r'"today":(.*?),')
            highestprice = re.findall(price_re, price_text.text)
            return highestprice
        except Exception as err:
            print(err)

    def getPrice(self, product_url):
        try:
            url = "http://www.huihui.cn/api/myzhushou/productSense?" \
                  "callback=img&phu=%s&_=1478753066171" % (product_url)
            price_text = requests.get(url)
            match_obj = re.match(r'.*"max":(\d*),"min":(\d*),"today":(\d*)', price_text.text)

            if match_obj:
                max_price = match_obj.group(1)
                min_price = match_obj.group(2)
                today_price = match_obj.group(3)
            else:
                max_price, min_price, today_price = 0, 0, 0

            return max_price, min_price, today_price
        except:
            pass


if __name__ == '__main__':
    # print("SpiderUtil")
    # timestamp = 1457612634
    # timestruc = time.localtime(timestamp)
    # date_time = time.strftime("%Y-%m-%d", timestruc)
    # print
    timestamp = 1479131401
    timestruc = time.localtime(timestamp)
    date_time = time.strftime("%Y-%m-%d", timestruc)
    d11 = "2016-11-11"
    # cnt = datediff(d11, date_time) + 1
    d = datetime.datetime.fromtimestamp(timestamp)
    # d1 = d + datetime.timedelta(days=-3)
    # print(d1.strftime("%Y-%m-%d"))

    times = [1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1999,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1799,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1399,1399,1399,1399,1399,1399,1399,1399,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1599,1598,1599,1599,1599,1599,1599,1599,1599,1598,1599,1111,2222,1599,1599]
    print(min(times))
    # low = times.index(1399)
    # diff = max([i for i, a in enumerate(times) if a == 1399])
    # diff = len(times) - diff - 1
    # lowday = d - datetime.timedelta(days=diff)
    # print(lowday.strftime("%Y-%m-%d"))
