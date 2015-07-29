#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

from .common import *


class Column:

    """专栏类，用专栏网址为参数来构造对象."""

    def __init__(self, session, url, name=None, follower_num=None,
                 post_num=None):
        """类对象初始化.

        :param str url: 专栏网址
        :param str name: 专栏名
        :param int follower_num: 关注者数量
        :param int post_num: 文章数量
        :return: 专栏对象
        :rtype: Column
        """
        match = re_column_url.match(url)
        if match is None:
            raise ValueError('URL invalid')
        else:
            self._in_name = match.group(1)
        if url.endswith('/') is False:
            url += '/'
        self.url = url
        self._session = session
        self.soup = None
        self._name = name
        self._follower_num = follower_num
        self._post_num = post_num

    def _make_soup(self):
        if self.soup is None:
            origin_host = self._session.headers.get('Host')
            self._session.headers.update(Host='zhuanlan.zhihu.com')
            res = self._session.get(Columns_Data.format(self._in_name))
            self._session.headers.update(Host=origin_host)
            self.soup = res.json()

    @property
    @check_soup('_name')
    def name(self):
        """获取专栏名称.

        :return: 专栏名称
        :rtype: str
        """
        return self.soup['name']

    @property
    @check_soup('_follower_num')
    def follower_num(self):
        """获取关注人数.

        :return: 关注人数
        :rtype: int
        """
        return int(self.soup['followersCount'])

    @property
    @check_soup('_post_num')
    def post_num(self):
        """获取专栏文章数.

        :return: 专栏文章数
        :rtype: int
        """
        return int(self.soup['postsCount'])

    @property
    def posts(self):
        """获取专栏的所有文章.

        :return: 专栏所有文章的迭代器
        :rtype: Post.Iterable
        """
        from .author import Author
        from .post import Post

        origin_host = self._session.headers.get('Host')
        for offset in range(0, (self.post_num - 1) // 10 + 1):
            self._session.headers.update(Host='zhuanlan.zhihu.com')
            res = self._session.get(
                Columns_Posts_Data.format(self._in_name, offset * 10))
            soup = res.json()
            self._session.headers.update(Host=origin_host)
            for post in soup:
                url = Columns_Prefix + post['url']
                template = post['author']['avatar']['template']
                photo_id = post['author']['avatar']['id']
                photo_url = template.format(id=photo_id, size='r')
                author = Author(self._session, post['author']['profileUrl'],
                                post['author']['name'], post['author']['bio'],
                                photo_url=photo_url)
                title = post['title']
                upvote_num = post['likesCount']
                comment_num = post['commentsCount']
                print(url)
                yield Post(self._session, url, self, author, title, upvote_num,
                           comment_num)
