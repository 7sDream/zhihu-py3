#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

from .common import *


class Topic:

    """答案类，请使用``ZhihuClient.topic``方法构造对象."""

    @class_common_init(re_topic_url)
    def __init__(self, url, name=None, session=None):
        """创建话题类实例.

        :param url: 话题url
        :param name: 话题名称，可选
        :return: Topic
        """
        self.url = url
        self._session = session
        self._name = name

    def _make_soup(self):
        if self.soup is None:
            self.soup = BeautifulSoup(self._session.get(self.url).content)

    @property
    @check_soup('_name')
    def name(self):
        """获取话题名称.

        :return: 话题名称
        :rtype: str
        """
        return self.soup.find('h1').text

    @property
    @check_soup('_follower_num')
    def follower_num(self):
        """获取话题关注人数.

        :return: 关注人数
        :rtype: int
        """
        follower_num_block = self.soup.find('div', class_='zm-topic-side-followers-info')
        # 无人关注时 找不到对应block，直接返回0 （感谢知乎用户 段晓晨 提出此问题）
        if follower_num_block.strong is None:
            return 0
        return int(follower_num_block.strong.text)
    
    @property
    @check_soup('_photo_url')
    def photo_url(self):
        """获取话题头像图片地址.

        :return: 话题头像url
        :rtype: str
        """
        if self.soup is not None:
            img = self.soup.find(
                'a', id='zh-avartar-edit-form').img['src']
            return img.replace('_m', '_r')
    @property
    @check_soup('_description')
    def description(self):
        """获取话题描述信息.

        :return: 话题描述信息
        :rtype: str
        """
        if self.soup is not None:
            desc = self.soup.find(
                'div', class_='zm-editable-content').text
            return desc
