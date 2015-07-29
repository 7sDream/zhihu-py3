#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

from .common import *


class Topic:

    """话题类，传入话题网址构造对象."""

    def __init__(self, session, url, name=None):
        """类对象初始化.

        :param url: 话题地址
        :param name: 话题名称
        :return: Topic
        """
        if re_topic_url.match(url) is None:
            raise ValueError('URL invalid')
        if url.endswith('/') is False:
            url += '/'
        self.url = url
        self._session = session
        self._name = name
        self.soup = None

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
