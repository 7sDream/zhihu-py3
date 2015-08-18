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
