# -*- coding: utf-8 -*-
import scrapy
from TouTiao.items import VideoItem
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
import base64
from scrapy import Selector, selector


def get_sign(uid, next_time):
    with open(r"G:\code\html\anjuke\tt.js", 'r') as f:
        content = f.read()
    ctx = execjs.compile(content)
    sign = ctx.call('get_sign', uid, next_time)
    return sign


def get_video_url(video_id):
    with open(r"G:\code\html\anjuke\video.js", 'r') as f:
        content = f.read()
    ctx = execjs.compile(content)
    url = ctx.call('get_video_url', video_id)
    return url


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
    name = 'toutiao_video'
    headers = {
        'Accept-Language': 'zh-CN',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
        'x-requested-with': 'XMLHttpRequest',
    }
    # uid_list = [3410443345]
    client = pymongo.MongoClient(host='localhost', port=27017)
    collection = client['spider']['toutiao_user']
    uid_item = collection.find()[143:]
    a_week_before = get_days_before_today(7)

    def start_requests(self):
        max_behot_time = 0
        # for user_id in self.uid_list:
        for user_item in self.uid_item:
            user_id = user_item['user_id']
            video = user_item['video']
            if not video:
                continue

            headers = deepcopy(self.headers)
            headers['referer'] = f'https://www.toutiao.com/c/user/{user_id}/'
            params = {'max_behot_time': max_behot_time, 'user_id': user_id, 'page_type': 0, 'count': 20}
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
                    continue
                item = VideoItem()
                item['user_id'] = params['user_id']
                item['title'] = d['title']
                item['source'] = d['source']
                item['source_url'] = 'http://www.365yg.com/i' + d['item_id']
                item['comments_count'] = d['comments_count']
                item['tag'] = d['tag']
                item['detail_play_effective_count'] = d['detail_play_effective_count']
                item['abstract'] = d['abstract']
                item['video_duration_str'] = d['video_duration_str'] if d.get('video_duration_str') else ''
                item['image_url'] = 'http:' + d['image_url']
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
        video_id = Selector(response).re(r"videoId: '(.*?)'")
        video_url = get_video_url(video_id)
        yield scrapy.Request(url=video_url, callback=self.video_parse, headers=headers, meta={'item': item})

    def video_parse(self, response):
        item = response.meta['item']
        data = json.loads(response.body.decode())
        main_url = data['data']['video_list']['video_1']['main_url']
        video_url = base64.b64decode(main_url)
        item['video_url'] = video_url.decode()
        yield item
