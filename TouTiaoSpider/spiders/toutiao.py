# -*- coding: utf-8 -*-
import scrapy
from TouTiao.items import ToutiaoItem
from copy import deepcopy
import re
import requests
import execjs
import json
from lxml import etree
import time
import pandas as pd
from urllib.parse import urlencode
import datetime
import pymongo


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
    name = 'toutiao'
    headers = {
        'Accept-Language': 'zh-CN',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
        'x-requested-with': 'XMLHttpRequest',
    }
    uid_list = [55301399445]
    client = pymongo.MongoClient(host='localhost', port=27017)
    collection = client['spider']['toutiao_user']
    uid_item = collection.find()[:]
    a_week_before = get_days_before_today(7)

    def start_requests(self):
        max_behot_time = 0
        # for user_id in self.uid_list:
        for user_item in self.uid_item:
            user_id = user_item['user_id']
            article = user_item['toutiao']
            if not article:
                continue

            headers = deepcopy(self.headers)
            headers['referer'] = f'https://www.toutiao.com/c/user/{user_id}/'
            params = {'max_behot_time': max_behot_time, 'visit_user_id': user_id, 'category': 'pc_profile_ugc'}
            prefix_url = 'https://www.toutiao.com/api/pc/feed/'
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
                behot_time = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(d['base_cell']['behot_time'])), '%Y-%m-%d')
                if (behot_time - self.a_week_before).days < 0:
                    stop = True
                    continue
                d2 = json.loads(d['concern_talk_cell']['packed_json_str'])
                item = ToutiaoItem()
                item['user_id'] = params['visit_user_id']
                item['share_title'] = d2['share']['share_title']
                item['source'] = d2['user']['name']
                item['content'] = d2['content']
                item['share_url'] = d2['share_url']
                item['comment_count'] = d2['comment_count']
                item['digg_count'] = d2['digg_count']
                item['read_count'] = d2['read_count']
                item['behot_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d['base_cell']['behot_time']))
                yield item

        if not stop and request_number < 15:
            url = get_full_url(prefix_url, params)
            yield scrapy.Request(url=url, callback=self.parse, headers=headers,
                                 meta={'params': params, 'prefix_url': prefix_url, 'headers': headers, 'request_number': request_number + 1})
