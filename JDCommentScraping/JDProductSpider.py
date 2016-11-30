from JDCommentScraping.SpiderUtil import JDCommentDriver
from JDCommentScraping.Database import MySQLStorage
import time

PAGESIZE = 20

# TABLE_LIST = ['jd_mobile_apple',
#               'jd_mobile_huawei',
#               'jd_mobile_meizu',
#               'jd_mobile_mi',
#               'jd_mobile_samsung']

# TABLE_LIST = ['jd_laptop_apple',
#               'jd_laptop_dell',
#               'jd_laptop_hp',
#               'jd_laptop_thinkpad']

# TABLE_LIST = ['jd_tv_domestic',
#               'jd_tv_internet',
#               'jd_tv_international']

# TABLE_LIST = ['jd_book_computer',
#               'jd_book_finance',
#               'jd_book_literature',
#               'jd_book_novel',
#               'jd_book_psychology']

# TABLE_LIST = ['jd_ac_wallhang',
#               'jd_ac_packaged']

TABLE_LIST = ['jd_refrigerator_half',
              'jd_refrigerator_multi']

def getProductComment():
    count = 1
    for table in TABLE_LIST:
        skuids = MySQLStorage().getSkuIDList(table)

        for skuid in skuids:
            try:
                skuid = int(''.join(list(skuid)))
                for page_cnt in range(PAGESIZE):
                    url = "http://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=1" \
                          "&page=%s&pageSize=10" % (skuid, page_cnt)
                    driver = JDCommentDriver(skuid, url)
                    flag, count = driver.storeComments(count)

                    if flag == -1:
                        break
            except Exception as err:
                print(err)

def getProductSummary():
    for table in TABLE_LIST:
        skuids = MySQLStorage().getSkuIDList(table)

        for skuid in skuids:
            try:
                skuid = int(''.join(list(skuid)))
                url = "http://club.jd.com/comment/productCommentSummaries.action?referenceIds=%s" % (skuid)
                driver = JDCommentDriver(skuid, url)
                driver.storeProductCommentSummary()

            except Exception as err:
                print(err)

def getProductHotTag():
    for table in TABLE_LIST:
        skuids = MySQLStorage().getSkuIDList(table)

        for skuid in skuids:
            try:
                skuid = int(''.join(list(skuid)))
                url = "http://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=1" \
                          "&page=0&pageSize=10" % (skuid)
                driver = JDCommentDriver(skuid, url)
                driver.storeHotCommentTagStatistics()

            except Exception as err:
                print(err)

def getProductPriceTrend():
    for table in TABLE_LIST:
        skuids = MySQLStorage().getSkuIDList(table)

        for skuid in skuids:
            try:
                skuid = int(''.join(list(skuid)))
                url = "http://browser.gwdang.com/extension?ac=price_trend&dp_id=%s-3" % (skuid)
                driver = JDCommentDriver(skuid, url)
                driver.storeProductPriceTrend()

            except Exception as err:
                print(err)

if __name__ == '__main__':
    # getProductPriceTrend()
    # getProductSummary()
    getProductHotTag()
    # getProductComment()