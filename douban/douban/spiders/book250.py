import scrapy
from lxml import etree
from douban.items import DoubanItem ## --？
class Book250Spider(scrapy.Spider):
    # 定义爬虫名称
    name = 'book250'
    allowed_domains = ['book.douban.com']
    # 起始URL列表
    start_urls = ['http://book.douban.com/top250']

    def start_requests(self):
        # for i in range(0,10):
        #     uri = f'https://book.douban.com/top250?start={i*25}'
        #     yield scrapy.Request(url=uri,callback=self.parse)
        uri = 'http://book.douban.com/top250'
        yield scrapy.Request(url=uri,callback=self.parse)

    def parse(self, response):
        html = etree.HTML(response.text)
        book_tr_list = html.xpath('//*[@id="content"]//div[@class="article"]//tr[@class="item"]')
        for tr in book_tr_list:
            image = tr.xpath("./td[1]//img/@src")[0]
            title = tr.xpath(".//div[@class='pl2']/a/@title")[0]
            link = tr.xpath(".//div[@class='pl2']/a/@href")[0]
            item = DoubanItem()
            item['image'] = image
            item['title'] = title
            item['link'] = link
            yield scrapy.Request(url=link,meta={'item': item},callback=self.parseToDetail)

        # tr = book_tr_list[3]
        # image = tr.xpath("./td[1]//img/@src")
        # title = tr.xpath(".//div[@class='pl2']/a/@title")
        # link = tr.xpath(".//div[@class='pl2']/a/@href")
        # item = DoubanItem()
        # item['image'] = image
        # item['title'] = title
        # item['link'] = link
        # yield scrapy.Request(url=link[0],meta={'item': item},callback=self.parseToDetail)

    def parseToDetail(self,response):
        item = response.meta['item']
        html = etree.HTML(response.text)
        href = html.xpath("//div[@class='mod-hd']//span[@class='pl']/a/@href")[0]
        yield scrapy.Request(url=href,meta={'item':item},callback=self.parseGetCommons)


    def parseGetCommons(self,response):
        item = response.meta['item']
        commonList = []
        html = etree.HTML(response.text)
        commons = html.xpath("//div[@id='comments']//span[@class='short']/text()")
        for com in commons:
           yield commonList.append(com)

        item['commons'] = commonList
        yield item
        
        