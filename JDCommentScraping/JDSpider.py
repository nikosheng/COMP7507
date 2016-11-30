# -*- coding: UTF-8 -*-

import re
import requests
import JDCommentScraping.SpiderUtil
from JDCommentScraping.Database import MySQLStorage
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf-8')

product_dic = {}
# product_dic['JD_Mobile_Huawei'] = "http://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_8557"
# product_dic['JD_Mobile_Apple'] = "http://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_14026"
# product_dic['JD_Mobile_Mi'] = "http://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_18374"
# product_dic['JD_Mobile_Samsung'] = "http://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_15127"
# product_dic['JD_Mobile_Meizu'] = "http://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_12669"
# product_dic['JD_Laptop_Thinkpad'] = "http://list.jd.com/list.html?cat=670,671,672&ev=exbrand_11518"
# product_dic['JD_Laptop_Dell'] = "http://list.jd.com/list.html?cat=670,671,672&ev=exbrand_5821"
# product_dic['JD_Laptop_Apple'] = "http://list.jd.com/list.html?cat=670,671,672&ev=exbrand_14026"
# product_dic['JD_Laptop_HP'] = "http://list.jd.com/list.html?cat=670,671,672&ev=exbrand_8740"
# product_dic['JD_TV_International'] = "http://list.jd.com/list.html?cat=737,794,798&ev=5305_7189"
# product_dic['JD_TV_Domestic'] = "http://list.jd.com/list.html?cat=737,794,798&ev=5305_7188"
# product_dic['JD_TV_Internet'] = "http://list.jd.com/list.html?cat=737,794,798&ev=5305_89541"
# product_dic['JD_AC_Wallhang'] = "http://list.jd.com/list.html?cat=737,794,870&ev=1554_584893"
# product_dic['JD_AC_Packaged'] = "http://list.jd.com/list.html?cat=737,794,870&ev=1554_584894"
# product_dic['JD_Refrigerator_multi'] = "http://list.jd.com/list.html?cat=737,794,878&ev=1015_5131"
# product_dic['JD_Refrigerator_half'] = "http://list.jd.com/list.html?cat=737,794,878&ev=1015_5130"
# product_dic['JD_MicroCamera'] = "http://list.jd.com/list.html?cat=652,654,5012"
# product_dic['JD_Laptop'] = "http://list.jd.com/list.html?cat=670,671,672"
# product_dic['JD_Pad'] = "http://list.jd.com/list.html?cat=670,671,2694"
# product_dic['JD_WashingMachine'] = "http://list.jd.com/list.html?cat=737,794,880"
# product_dic['JD_Refrigerator'] = "http://list.jd.com/list.html?cat=737,794,878"
product_dic['JD_Book_Novel'] = "http://list.jd.com/list.html?cat=1713,3258"
product_dic['JD_Book_Literature'] = "http://list.jd.com/list.html?cat=1713,3259"
product_dic['JD_Book_Victory'] = "http://list.jd.com/list.html?cat=1713,3267"
# product_dic['JD_Earphone'] = "http://list.jd.com/list.html?cat=652,828,842"
# product_dic['JD_Router'] = "http://list.jd.com/list.html?cat=670,699,700"
# product_dic['JD_SmartBracelet'] = "http://list.jd.com/list.html?cat=652,12345,12347"
# product_dic['JD_Mobile_Harddisk'] = "http://list.jd.com/list.html?cat=670,686,693"
product_dic['JD_Book_Finance'] = "http://list.jd.com/list.html?cat=1713,3265"
product_dic['JD_Book_Computer'] = "http://list.jd.com/list.html?cat=1713,3287"
product_dic['JD_Book_Psychology'] = "http://list.jd.com/list.html?cat=1713,3279"

for category in product_dic.keys():
    tablename = category

    base_url = r'%s%s' % (product_dic[category], "%s")
    page = r'&page=%d'

    skuids = set()

    sku_re = re.compile(r'data-sku="(\d+)"', re.MULTILINE | re.IGNORECASE)
    # ids = re.findall(sku_re, first_try.text)
    # print(ids)
    # print('find...', len(ids))
    # skuids |= set(ids)

    i = 4
    while True:
        url = base_url % (page % i)
        html = requests.get(url)
        ids = set(re.findall(sku_re, html.text))
        if i == 10 or len(ids) == 0:
            break
        else:
            i += 1
        skuids |= set(ids)
        total = len(skuids)
        print('Total:', total)

    storage = MySQLStorage()
    # storage.createTable(tablename)
    storage.insertProductTable(tablename, skuids)
    storage.closeConnection()

    # with open(filename, mode='wb') as s:
    #     try:
    #         for sku in skuids:
    #             sku_url = 'http://item.jd.com/%s.html' % (str(sku))
    #             jp = JdPrice(sku_url)
    #             item = sku + '\n'
    #             # s.write(sku + ',' + jp.get_product_name() + ',' + jp.get_product_price() + '\n')
    #             s.write(item)
    #     except:
    #         pass
    #
    # s.close()