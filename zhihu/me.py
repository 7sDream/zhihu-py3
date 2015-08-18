#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import json

from .common import *
from .author import Author


class Me(Author):
    """封装了相关操作（如点赞，关注问题）的类，需要登录后使用"""

    def __init__(self, url, name, motto, photo_url, session):
        super(Me, self).__init__(url, name, motto,
                                 photo_url=photo_url, session=session)

    def upvote_answer(self, answer):
        """给答案点赞

        :param Answer answer: 需要点赞的答案
        :return: 二元素元组，第一个元素为0表示成功，失败时第二个元素表示原因。
        :rtype: (int, str)
        """
        from .answer import Answer
        if isinstance(answer, Answer) is False:
            raise ValueError('type of answer need to be zhihu.Answer')
        params = {'answer_id': str(answer.aid)}
        data = {'_xsrf': answer.xsrf,
                'method': 'vote_up',
                'params': json.dumps(params)
                }
        headers = dict(Default_Header)
        headers['Referer'] = answer.question.url[:-1]
        res = self._session.post(Upvote_Answer_Url, headers=headers, data=data)
        return res.json()['r'], res.json()['msg']

    def upvote_article(self, article):
        """给文章点赞

        :param Article article: 需要点赞的文章
        :return: 无
        """
        pass

    def follow_author(self, author):
        """关注某位用户

        :param Author author: 需要关注的用户
        :return: 无
        """
        pass
