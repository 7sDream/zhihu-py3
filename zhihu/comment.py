#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Comment:

    """评论类，一般不直接使用，而是作为``Answer.comments``迭代器的返回类型."""

    def __init__(self, cid, answer, author,
                 upvote_num, content, time_string, group_id=None):
        """创建评论类实例.

        :param int cid: 评论ID
        :param int group_id: 评论所在的组ID
        :param Answer answer: 评论所在的答案对象
        :param Author author: 评论的作者对象
        :param int upvote_num: 评论赞同数量
        :param str content: 评论内容
        :param str time_string: 表示评论时间的字符串
        :return: 评论对象
        :rtype: Comment
        """

        self.cid = cid
        self.answer = answer
        self.author = author
        self.upvote_num = upvote_num
        self.content = content
        self.time_string = time_string
        self._group_id = group_id
