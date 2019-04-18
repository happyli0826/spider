# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    comments_count = scrapy.Field()
    # chinese_tag = scrapy.Field()
    tag = scrapy.Field()
    label = scrapy.Field()
    abstract = scrapy.Field()
    behot_time = scrapy.Field()
    content = scrapy.Field()
    go_detail_count = scrapy.Field()
    user_id = scrapy.Field()







class VideoItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    comments_count = scrapy.Field()
    # chinese_tag = scrapy.Field()
    tag = scrapy.Field()
    abstract = scrapy.Field()
    behot_time = scrapy.Field()
    content = scrapy.Field()
    detail_play_effective_count = scrapy.Field()
    user_id = scrapy.Field()
    video_duration_str = scrapy.Field()
    image_url = scrapy.Field()
    video_url = scrapy.Field()


class ToutiaoItem(scrapy.Item):
    share_title = scrapy.Field()
    source = scrapy.Field()
    share_url = scrapy.Field()
    comment_count = scrapy.Field()
    behot_time = scrapy.Field()
    content = scrapy.Field()
    read_count = scrapy.Field()
    user_id = scrapy.Field()
    digg_count = scrapy.Field()