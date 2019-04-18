# -*- coding: utf-8 -*-
import scrapy
from TouTiao.items import ArticleItem
from copy import deepcopy
import re
import requests
import execjs
import json
from lxml import etree
import time
import pandas as pd
from urllib.parse import urlencode
import re
import datetime
import pymongo

import logging


def get_as_ap():
    f = open(r".\static\as.js", 'r', encoding='UTF-8')
    ctx = execjs.compile(f.read())
    data = ctx.call('a')
    return data


def get_js():
    f = open(r".\static\tt.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    return ctx.call('get_as_cp_signature')


# def get_signature(uid, next_time):
#     chrome_server_url = "http://10.0.0.115:9000/"
#     data = {'url': f'http://127.0.0.1:8000/spider/get_toutiao_signature/?id={uid}&next={next_time}'}
#     r = requests.post(chrome_server_url, data=json.dumps(data))
#     data = json.loads(r.content.decode())
#     html = etree.HTML(data['content'])
#     sig = html.xpath('//div[@id="id"]/text()')
#     return sig[0]


# def get_signature(uid, next_time):
#     splash_url = f"http://192.168.245.72:8050/render.html"
#     url = f'http://10.0.0.115:8000/spider/get_toutiao_signature/?id={uid}&next={next_time}'
#     args = {"url": url, "timeout": 2, "image": 0}
#     response = requests.get(splash_url, params=args)
#     html = etree.HTML(response.content.decode())
#     sign_str = html.xpath('//div[@id="id"]/text()')[0]
#     signc = sign_str.split(',')
#     sign = {
#         'as': signc[0],
#         'cp': signc[1],
#         '_signature': signc[2]
#     }
#     return sign


def get_sign(uid, next_time):
    with open(r".\static\tt.js", 'r') as f:
        content = f.read()
    ctx = execjs.compile(content)
    sign = ctx.call('get_sign', uid, next_time)
    return sign


def get_full_url(url, params):
    data = urlencode(params)
    full_url = url + "?" + data
    return full_url


def get_days_before_today(n=0):
    '''''
    date format = "YYYY-MM-DD HH:MM:SS"
    '''
    now = datetime.datetime.now()
    if (n < 0):
        return datetime.datetime(now.year, now.month, now.day)
    else:
        n_days_before = now - datetime.timedelta(days=n)
    return datetime.datetime(n_days_before.year, n_days_before.month, n_days_before.day)


class TouTiao(scrapy.Spider):
    name = 'article'
    headers = {
        'Accept-Language': 'zh-CN',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
        'x-requested-with': 'XMLHttpRequest',
    }
    # uid_list = [6103873752]
    client = pymongo.MongoClient(host='localhost', port=27017)
    collection = client['spider']['toutiao_user']
    uid_item = collection.find()[:]
    a_week_before = get_days_before_today(7)

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message, level=logging.DEBUG, **kw):
        """Log the given message at the given log level

        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.
        """
        self.logger.log(level, message, **kw)

    def start_requests(self):
        max_behot_time = 0
        # for user_id in self.uid_list:
        for user_item in self.uid_item:
            user_id = user_item['user_id']
            article = user_item['article']
            if not article:
                continue

            headers = deepcopy(self.headers)
            headers['referer'] = f'https://www.toutiao.com/c/user/{user_id}/'
            params = {'max_behot_time': max_behot_time, 'user_id': user_id, 'page_type': 1, 'count': 20}
            sign = get_sign(user_id, max_behot_time)
            params.update(sign)  # 加入加密参数
            prefix_url = 'https://www.toutiao.com/c/user/article/'
            url = get_full_url(prefix_url, params)
            yield scrapy.Request(url=url, callback=self.parse, headers=headers,
                                 meta={'params': params, 'prefix_url': prefix_url, 'headers': headers, 'request_number': 1})

    def parse(self, response):
        data = json.loads(response.body.decode())
        params = response.meta['params']
        prefix_url = response.meta['prefix_url']
        headers = response.meta['headers']
        request_number = response.meta['request_number']
        stop = False
        if data['data']:
            request_number = 0
            params['max_behot_time'] = data['next']['max_behot_time']
            for d in data['data']:
                behot_time = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(d['behot_time'])), '%Y-%m-%d')
                if (behot_time - self.a_week_before).days < 0:
                    stop = True
                    break
                if d['has_video']:
                    continue
                item = ArticleItem()
                item['user_id'] = params['user_id']
                item['title'] = d['title']
                item['source'] = d['source']
                # item['source_url'] = 'https://www.toutiao.com' + d['source_url']
                item['source_url'] = 'https://www.toutiao.com/i' + d['item_id']
                item['comments_count'] = d['comments_count']
                # item['chinese_tag'] = d['chinese_tag']
                item['tag'] = d['tag']
                item['go_detail_count'] = d['go_detail_count']
                item['abstract'] = d['abstract']
                item['behot_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d['behot_time']))
                yield scrapy.Request(url=item['source_url'], callback=self.detail_parse, headers=headers, meta={'item': item, 'headers': headers})

        if not stop and request_number < 15:
            sign = get_sign(params['user_id'], params['max_behot_time'])
            params.update(sign)  # 加入加密参数
            url = get_full_url(prefix_url, params)
            yield scrapy.Request(url=url, callback=self.parse, headers=headers,
                                 meta={'params': params, 'prefix_url': prefix_url, 'headers': headers, 'request_number': request_number + 1})

    def detail_parse(self, response):
        item = response.meta['item']
        headers = response.meta['headers']
        url = response.request.url
        if url.find('www.toutiao.com') != -1:
            item = response.meta['item']
            content = response.xpath('//script/text()')[4].re(r'content:(.*?),')[0]
            item['content'] = content
            yield item
        elif url.find('wallstreetcn') != -1:
            reg = re.findall(r'(<article>.*?</article>)', response.body.decode(), re.S)
            content = re.sub(r'\n', '', reg[0])
            item['content'] = content
            yield item
        elif url.find('snssdk') != -1:
            article_id = url.replace(r'https://www.toutiao.com/', '').replace(r'/', '')
            url = f"http://is.snssdk.com/column/v3/app/article/content/?article_id={article_id}"
            yield scrapy.Request(url=url, callback=self.snssdk_parse, headers=headers, meta={'item': item})
        else:
            print(item)
            raise Exception('未实现的解析')

    def snssdk_parse(self, response):
        item = response.meta['item']
        data = json.loads(response.body)
        item['content'] = data['data']['partial_content']
        yield item
