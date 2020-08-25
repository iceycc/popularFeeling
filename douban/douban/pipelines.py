# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline

import scrapy

# from chinazproject.items import ChinazprojectWebInfoItem,ChinazprojectTagItem
import os
# 取出配置文件
from scrapy.utils.project import get_project_settings


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


# os.remove()# 重命名
#  获取settings文件的信息
images_store = get_project_settings().get('IMAGES_STORE')


class ChinazProjectImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        """
        根据图片的url地址，构造requuests请求
        :param item:
        :param info:
        :return:
        """
        # 获取图片地址，发起请求
        img_url = item['image']
        print('获取图片地址', img_url)
        yield scrapy.Request(img_url)

        # 如果有多个图片地址,item['coverImage']对应的是一个列表
        # img_urls = item['coverImage']
        # return [scrapy.Request(x) for x in img_urls]

    def item_completed(self, results, item, info):
        """
        图片下载之后的回调结果
        :param results: [(True/False,{'path':'图片下载之后的一个储存路径','url':'图片的url地址','ckecksum':'经过HASH加密的一个字符串'})]:图片下载成功还是失败
        :param item:
        :param info:
        :return:
        """
        paths = [result['path'] for status, result in results if status]
        print('图片下载结果', results)
        if len(paths) > 0:
            print('图片下载成功')
            # 使用os的rename方法修改文件的名称
            os.rename(images_store+'/' + paths[0], images_store+'/'+item['title']+'.jpg')
            image_path = images_store+'/'+item['title']+'.jpg'
            print('修改后的路径', image_path)
            item['locakImgePath'] = image_path

        else:
            # 如果没有成功获取到图片，将这个item丢弃
            from scrapy.exceptions import DropItem
            raise DropItem('没有获取到图片，遗弃item')
     # 获取图片地址，交给下一个管道处理
        return item
