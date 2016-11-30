# -*- coding: UTF-8 -*-
import mysql.connector

import JDCommentScraping.SpiderUtil

# reload(sys)
# sys.setdefaultencoding('utf-8')

PRODUCT_COMMENT_SUMMARY_TABLE = "jd_product_comment_sum"
COMMENT_TABLE = "jd_comments"

class MySQLStorage:
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='abcd1234', database='spider')

    def createTable(self, tablename):
        try:
            cursor = self.conn.cursor()
            cursor.execute('drop table if exists %s' % (tablename))
            self.conn.commit()
            cursor.execute('create table %s(skuid varchar(32) primary key, product_name varchar(128), selfrun varchar(1))' % (tablename))
            self.conn.commit()
        except:
            pass
        finally:
            cursor.close()

    def insertSuningProductTable(self, tablename, product):
        try:
            cursor = self.conn.cursor()
            sql = "insert into %s(productid, title, price, commentCount, oneStarCount, twoStarCount, threeStarCount," \
                  "fourStarCount, fiveStarCount, qualityStar, isselfrun) values('%s', \"%s\", %f, %d, %d, %d, %d, " \
                  "%d, %d, %f, '%s')" % \
                  (tablename,
                   product.productid,
                   product.title,
                   product.price,
                   product.commentCount,
                   product.oneStarCount,
                   product.twoStarCount,
                   product.threeStarCount,
                   product.fourStarCount,
                   product.fiveStarCount,
                   product.qualityStar,
                   product.isselfrun
                   )
            cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def insertProductTable(self, tablename, skuids):
        try:
            cursor = self.conn.cursor()
            for skuid in skuids:
                sku_url = 'http://item.jd.com/%s.html' % (str(skuid))
                item = JDCommentScraping.SpiderUtil.JDItem(sku_url)
                sku_name = item.get_product_name()
                sku_selfrun = item.isJDSelfRun()
                sql = "insert into %s(skuid, product_name, selfrun) values('%s', \"%s\", '%s')" % (tablename, skuid, sku_name, sku_selfrun)
                cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def getSkuIDList(self, tablename):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT skuid FROM %s' % (tablename))
            skuids = cursor.fetchall()
            return skuids
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def saveProductCommentSummary(self, tablename, item):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO %s VALUES('%s', %d, %d, %d, %d, %f, %f, %f, %f)" % \
                   (tablename,
                    item.skuid,
                    item.commentCount,
                    item.goodCount,
                    item.generalCount,
                    item.poorCount,
                    item.averageScore,
                    item.goodRate,
                    item.poorRate,
                    item.generalRate)
            cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def saveComments(self, tablename, item):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO %s VALUES(%d, '%s', '%s', '%s', \"%s\", '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                   (tablename,
                    item.id,
                    item.productid,
                    item.commentid,
                    item.content,
                    item.creationtime,
                    item.referenceTime,
                    item.score,
                    item.userProvince,
                    item.userRegisterTime,
                    item.userLevelName,
                    item.userClientShow,
                    item.isMobile,
                    item.days)
            cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def saveHotTag(self, tablename, item):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO %s VALUES(%d, '%s', '%s', %d)" % \
                   (tablename,
                    item.id,
                    item.productid,
                    item.name,
                    item.count)
            cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def savePriceTrend(self, tablename, item):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO %s VALUES('%s','%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d)" % \
                   (tablename,
                    item.skuid,
                    item.first_price,
                    item.hislowest,
                    item.hishighest,
                    item.current_price,
                    item.min_date,
                    item.max_date,
                    item.lowest_price,
                    item.highest_price,
                    item.shopfesday_price)
            cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def getQualityandCount(self, tablename):
        try:
            cursor = self.conn.cursor()
            sql = "SELECT PoorRate, SUM(CommentCount), SUM(PoorCount) " \
                  "FROM %s " \
                  "WHERE CommentCount >= 50 " \
                  "GROUP BY PoorRate " \
                  "ORDER BY PoorRate" % (tablename)
            cursor.execute(sql)
            values = cursor.fetchall()

            items = []
            item = []

            for value in values:
                poorrate = value[0]
                count = int(value[1])
                poorcount = int(value[2])
                item = [1, poorrate, count]
                items.append(item)

            print(items)
            # self.conn.commit()
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def getUserRegistrationLevel(self):
        try:
            cursor = self.conn.cursor()
            data = []
            years = [2010, 2011, 2012, 2013, 2014, 2015, 2016]
            for year in years:
                # sql = "SELECT userProvince, a.userRegisterYear, COUNT(commentid), " \
                #       "SUM(b.current_price), AVG(a.userLevelWeight) as avgweight " \
                #       "FROM jd_comments_all a, jd_pricetrend_all b " \
                #       "WHERE a.productid = b.skuid " \
                #       "AND EXISTS ( SELECT 1 FROM provinces WHERE userProvince = provinces.province) " \
                #       "AND a.userRegisterYear = %d " \
                #       "GROUP BY userProvince, userRegisterYear" % (year)
                sql = "SELECT userProvince, userRegisterYear, " \
                      "userLevelWeight, COUNT(commentid) " \
                      "FROM jd_comments_all " \
                      "WHERE EXISTS ( SELECT 1 FROM provinces WHERE userProvince = provinces.province) " \
                      "AND userRegisterYear = %d " \
                      "AND userLevelWeight IS NOT NULL " \
                      "GROUP BY userProvince, userRegisterYear, userLevelWeight " \
                      "ORDER BY userProvince, userRegisterYear " % (year)
                cursor.execute(sql)
                values = cursor.fetchall()

                items = []
                item = []

                lastprovince = values[0][0]
                item = [0, 0, 0, 0, 0, lastprovince]
                for value in values:
                    # userCnt = value[2]
                    # userprovince = value[0]
                    # userConsumption = float(value[3])
                    # userAvgLevel = float(value[4])
                    # item = [userConsumption, userAvgLevel, userCnt, userprovince]
                    # items.append(item)
                    userprovince = value[0]
                    userLevel = value[2]
                    levelCnt = int(value[3])
                    if userprovince == lastprovince:
                        item[userLevel - 1] = levelCnt
                    else:
                        items.append(item)
                        item = [0, 0, 0, 0, 0, userprovince]
                        item[userLevel - 1] = levelCnt
                    lastprovince = userprovince

                data.append(items)
                # self.conn.commit()
            print(data)
        except Exception as err:
            print(err)
        finally:
            cursor.close()


    def closeConnection(self):
        self.conn.close()

if __name__ == '__main__':
    # print("Database")
    storage = MySQLStorage()
    storage.getUserRegistrationLevel()