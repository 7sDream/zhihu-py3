#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals
import unittest
import os
import json

from test_utils import TEST_DATA_PATH
from zhihu import Column, Post


class ColumnTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = 'http://zhuanlan.zhihu.com/xiepanda'
        file_path = os.path.join(TEST_DATA_PATH, 'column.json')
        with open(file_path, 'r') as f:
            soup = json.load(f)

        post_path = os.path.join(TEST_DATA_PATH, 'column_post.json')
        with open(post_path, 'r') as f:
            cls.post_json = json.load(f)

        cls.column = Column(url)
        cls.column.soup = soup
        cls.expected = {'name': '谢熊猫出没注意', 'follower_num': 76605,
                        'post_num': 69, 'post_author_id': 'xiepanda',
                        'post_title': ("为了做一个称职的吃货，他决定连着吃"
                                       "一百天转基因食物"),
                        'post_upvote_num': 963, 'post_comment_num': 199}

    def test_name(self):
        self.assertEqual(self.expected['name'], self.column.name)

    def test_folower_num(self):
        self.assertEqual(self.expected['follower_num'],
                         self.column.follower_num)

    def test_post_num(self):
        self.assertEqual(self.expected['post_num'], self.column.post_num)

    def test_parse_post_data(self):
        post = self.column._parse_post_data(self.post_json)
        self.assertEqual(self.expected['post_author_id'], post.author.id)
        self.assertEqual(self.expected['post_title'], post.title)
        self.assertEqual(self.expected['post_upvote_num'], post.upvote_num)
        self.assertEqual(self.expected['post_comment_num'], post.comment_num)

    def test_posts(self):
        ps = self.column.posts
        post = next(ps)
        self.assertTrue(isinstance(post, Post))
