from bs4 import BeautifulSoup
import requests
import json
from JDCommentScraping.Database import MySQLStorage

class SuningSpider:
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html)

    def prettify(self):
        print(self.soup.prettify())

    def searchProducts(self):
        try:
            products = self.soup.find_all(class_='res-info')

            for child in products:
                productid = child.find("em")['datasku']
                productid = productid[:productid.find('|')]
                isselfrun = child.find(class_="seller").span.i.string
                product = self.getProductInfo(productid)
                product.isselfrun = isselfrun
                storage = MySQLStorage()
                storage.insertSuningProductTable("suning_product", product)

            storage.closeConnection()
        except Exception as err:
            print(err)

    def getProductInfo(self, productid):
        try:
            product = SuningProduct()
            product.productid = productid
            url = "http://browser.gwdang.com/brwext/dp_query?permanent_id=f0b699c1d7ff63690744e794ce5efd03" \
                  "&union=union_gwdang" \
                  "&url=http://product.suning.com/0000000000/%s.html&site=suning" % (productid)
            content = requests.get(url).text
            content_json = json.loads(content)
            info = content_json['collectInfo']
            title = info['title']
            price = content_json['code-server']['price']
            product.price = float(price)
            product.title = title
            product = self.getCommentCount(product)
            return product

        except Exception as err:
            print(err)

    def getCommentCount(self, product):
        try:
            url = "http://review.suning.com/ajax/review_satisfy/general-000000000%s-0000000000-----satisfy.htm" % (product.productid)
            content = requests.get(url).text
            content = content[content.find("(") + 1:-1]
            content_json = json.loads(content)

            for item in content_json['reviewCounts']:
                product.commentCount = int(item['totalCount'])
                product.oneStarCount = int(item['oneStarCount'])
                product.twoStarCount = int(item['twoStarCount'])
                product.threeStarCount = int(item['threeStarCount'])
                product.fourStarCount = int(item['fourStarCount'])
                product.fiveStarCount = int(item['fiveStarCount'])
                product.qualityStar = float(item['qualityStar'])
            return product
        except Exception as err:
            print(err)


class SuningProduct:
    def __init__(self):
        self.productid = ""
        self.title = ""
        self.price = ""
        self.totalCount = ""
        self.oneStarCount = ""
        self.twoStarCount = ""
        self.threeStarCount = ""
        self.fourStarCount = ""
        self.fiveStarCount = ""
        self.qualityStar = ""
        self.isselfrun = ""


if __name__ == '__main__':
    pagesize = 11
    for page in range(1, pagesize):
        url = "http://list.suning.com/0-20006-%s.html" % (page)
        spider = SuningSpider(url)
        spider.searchProducts()