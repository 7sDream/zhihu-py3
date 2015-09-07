#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

from .common import *


class Column:

    """专栏类，请使用``ZhihuClient.column``方法构造对象."""

    @class_common_init(re_column_url)
    def __init__(self, url, name=None, follower_num=None,
                 post_num=None, session=None):
        """创建专栏类实例.

        :param str url: 专栏url
        :param str name: 专栏名，可选
        :param int follower_num: 关注者数量，可选
        :param int post_num: 文章数量，可选
        :param Session session: 使用的网络会话，为空则使用新会话。
        :return: 专栏对象
        :rtype: Column
        """
        self._in_name = re_column_url.match(url).group(1)
        self.url = url
        self._session = session
        self._name = name
        self._follower_num = follower_num
        self._post_num = post_num

    def _make_soup(self):
        if self.soup is None:
            origin_host = self._session.headers.get('Host')
            self._session.headers.update(Host='zhuanlan.zhihu.com')
            res = self._session.get(Column_Data.format(self._in_name))
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

        :return: 专栏所有文章，返回生成器
        :rtype: Post.Iterable
        """
        origin_host = self._session.headers.get('Host')
        for offset in range(0, (self.post_num - 1) // 10 + 1):
            self._session.headers.update(Host='zhuanlan.zhihu.com')
            res = self._session.get(
                Column_Posts_Data.format(self._in_name, offset * 10))
            soup = res.json()
            self._session.headers.update(Host=origin_host)
            for post in soup:
                yield self._parse_post_data(post)

    def _parse_post_data(self, post):
        from .author import Author
        from .post import Post

        url = Column_Url + post['url']
        template = post['author']['avatar']['template']
        photo_id = post['author']['avatar']['id']
        photo_url = template.format(id=photo_id, size='r')
        author = Author(post['author']['profileUrl'],
                        post['author']['name'], post['author']['bio'],
                        photo_url=photo_url, session=self._session)
        title = post['title']
        upvote_num = post['likesCount']
        comment_num = post['commentsCount']
        print(url)
        return Post(url, self, author, title, upvote_num, comment_num,
                    session=self._session)
