# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DoubanPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        commons = item['commons']
        output = f'{title}\t{link}\t{commons}\n\n'
        self.article = open('./doubanbook.txt', 'a+', encoding='utf-8')
        self.article.write(output)
        self.article.close()
        return item
