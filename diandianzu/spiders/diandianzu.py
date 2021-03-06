import scrapy
from threading import Timer

import time
import pymysql
from ..items.items import DiandianzuItem
import re

class DianDianZuSpider(scrapy.Spider):
    name = 'diandianzu'
    allowed_domains = ['diandianzu.com']

    # 设置下载延时
    download_delay = 5
    start_urls = 'http://sz.diandianzu.com/listing/bt1r'

    db = pymysql.connect('rm-wz970j84167q2388a.mysql.rds.aliyuncs.com','voffice_sz','******','ziguan_local',charset = 'utf8')
    cursor = db.cursor()

    # 抓取深圳所有区域数据
    def start_requests(self):
        for i in  range(4,13):
            url = self.start_urls +'%s'%i + '/'
            page = scrapy.Request(url)
            yield page

    # # 暂时只抓取南山区域数据
    # def start_requests(self):
    #     url = self.start_urls + '4/'
    #     page = scrapy.Request(url)
    #     yield page

    def parse(self, response):
        for sel in response.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div'):
            item = dict()
            item['tradingArea'] = sel.xpath('string(./div/div[2]/div[2]/span[1])').extract()
            item['tradingArea'] = item['tradingArea'][0] if len(item['tradingArea']) > 0 else ''

            item['updateTime'] = sel.xpath('string(./div/div[2]/div[3]/span[1])').extract()
            item['updateTime'] = item['updateTime'][0] if len(item['updateTime']) > 0 else ''

            item['realName'] = sel.xpath('string(./div/div[2]/div[1]/h2/a)').extract()
            item['realName'] = item['realName'][0] if len(item['realName']) > 0 else ''

            item['averagePrice'] = sel.xpath('string(./div/div[2]/div[1]/div)').extract()
            item['averagePrice'] = item['averagePrice'][0] if len(item['averagePrice']) > 0 else ''
            # 去除'\n'、'\t'、'\r'
            item['averagePrice'] = item['averagePrice'].replace('\n', '').replace('\t', '').replace(' ', '')
            item['averagePrice'] = item['averagePrice'][:-3]

            url = sel.xpath('./div/div[2]/div[1]/h2/a/@href').extract()
            url = url[0] if len(url) > 0 else ''
            # 设置时间间隔
            url = 'http://sz.diandianzu.com/' + url
            time.sleep(5)
            yield response.follow(url,
                                  meta={'item': item},
                                  method='GET',
                                  dont_filter=True,
                                  callback=self.parse_detail)

    def parse_detail(self,response):
        item = DiandianzuItem()
        tempItem = response.meta['item']
        item['tradingArea'] = tempItem['tradingArea']
        item['updateTime'] = tempItem['updateTime']

        item['realName'] = tempItem['realName']
        item['averagePrice'] = tempItem['averagePrice']
        item['averagePrice'] = re.sub("\D", "", item['averagePrice'])
        item['averagePrice'] = item['averagePrice'] if len(item['averagePrice']) > 0 else '0'

        item['city'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[1]/div/div[2]/p[1]/a[1])').extract()
        item['city'] = item['city'][0] if len(item['city']) > 0 else ''
        item['region'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[1]/div/div[2]/p[1]/a[2])').extract()
        item['region'] = item['region'][0] if len(item['region']) > 0 else ''

        item['profile'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[6]/div[1])').extract()
        item['profile'] = item['profile'][0] if len(item['profile']) > 0 else ''
        item['completionTime'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[1]/ul/li[1]/span[2])').extract()
        item['completionTime'] = item['completionTime'][0] if len(item['completionTime']) > 0 else ''

        item['location'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[1]/ul/li[2]/span[2]/a)').extract()
        item['location'] = item['location'][0] if len(item['location']) > 0 else ''
        item['layerHeight'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/ul/li[1]/span[2])').extract()
        item['layerHeight'] = item['layerHeight'][0] if len(item['layerHeight']) > 0 else ''

        item['layerNum'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/ul/li[2]/span[2])').extract()
        item['layerNum'] = item['layerNum'][0] if len(item['layerNum']) > 0 else ''
        item['property'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/ul/li[3]/span[2])').extract()
        item['property'] = item['property'][0] if len(item['property']) > 0 else ''

        item['propertyCosts'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[3]/ul/li[1]/span[2])').extract()
        item['propertyCosts'] = item['propertyCosts'][0] if len(item['propertyCosts']) > 0 else '0'
        item['propertyCosts'] = re.sub("\D", "", item['propertyCosts'])
        item['propertyCosts'] = item['propertyCosts'] if len(item['propertyCosts']) > 0 else '0'
        item['parkingSpace'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[3]/ul/li[2]/span[2])').extract()
        item['parkingSpace'] = item['parkingSpace'][0] if len(item['parkingSpace']) > 0 else ''

        item['parkingRent'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[3]/ul/li[3]/span[2])').extract()
        item['parkingRent'] = item['parkingRent'][0] if len(item['parkingRent']) > 0 else ''
        item['parkingRent'] = re.sub("\D", "", item['parkingRent'])
        item['parkingRent'] =item['parkingRent'] if len(item['parkingRent']) > 0 else '0'
        item['airConditioning'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[4]/ul/li[1]/span[2])').extract()
        item['airConditioning'] = item['airConditioning'][0] if len(item['airConditioning']) > 0 else ''

        item['airfee'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[4]/ul/li[2]/span[2])').extract()
        item['airfee'] = item['airfee'][0] if len(item['airfee']) > 0 else '0'
        item['airfee'] = re.sub("\D", "", item['airfee'])
        item['airfee'] = item['airfee'] if len(item['airfee']) > 0 else '0'
        item['airhours'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[4]/ul/li[3]/span[2])').extract()
        item['airhours'] = item['airhours'][0] if len(item['airhours']) > 0 else ''

        item['elevator'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[5]/ul/li[1]/span[2])').extract()
        item['elevator'] = item['elevator'][0] if len(item['elevator']) > 0 else ''
        item['network'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[5]/ul/li[2]/span[2])').extract()
        item['network'] = item['network'][0] if len(item['network']) > 0 else ''

        item['checkBusiness'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[4]/div[5]/ul/li[3]/span[2])').extract()
        item['checkBusiness'] = item['checkBusiness'][0] if len(item['checkBusiness']) > 0 else ''
        item['priceRange'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[1]/div/div[2]/p[1]/a[1])').extract()
        item['priceRange'] = item['priceRange'][0] if len(item['priceRange']) > 0 else ''

        item['buildingAveragePrice'] = response.xpath('string(/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2])').extract()
        item['buildingAveragePrice'] = item['buildingAveragePrice'][0] if len(item['buildingAveragePrice']) > 0 else '0'
        item['buildingAveragePrice'] = re.sub("\D", "", item['buildingAveragePrice'])
        item['buildingAveragePrice'] = item['buildingAveragePrice']  if len(item['buildingAveragePrice']) > 0 else '0'

        sql = 'INSERT INTO diandianzu_spider(city, region,tradingArea,averagePrice,buildingName,profile,completionTime,location,layerHeight,layerNum,property,propertyCosts,parkingSpace,parkingRent,airConditioning,airfee,airhours,elevator,network,checkBusiness,priceRange,buildingAveragePrice)' \
              ' VALUES (\'%s\', \'%s\',\'%s\',%f,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%f,\'%s\',\'%s\',\'%s\',%f,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%f)'\
              % (item['city'], item['region'],item['tradingArea'],float(item['averagePrice']),item['realName'],item['profile'],item['completionTime'],item['location'],item['layerHeight'],item['layerNum'],item['property'],float(item['propertyCosts']),item['parkingSpace'],item['parkingRent'],item['airConditioning'],float(item['airfee']),item['airhours'],item['elevator'],item['network'],item['checkBusiness'],item['priceRange'],float(item['buildingAveragePrice']))
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()
        pass
