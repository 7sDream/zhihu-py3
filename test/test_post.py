#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals
import unittest
import os
import json

from zhihu import Post
from test_utils import TEST_DATA_PATH


class ColumnTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = 'http://zhuanlan.zhihu.com/xiepanda/20202275'

        post_path = os.path.join(TEST_DATA_PATH, 'column_post.json')
        with open(post_path, 'r') as f:
            post_json = json.load(f)

        post_saved_path = os.path.join(TEST_DATA_PATH, 'post.md')
        with open(post_saved_path, 'rb') as f:
            cls.post_saved = f.read()

        cls.post = Post(url)
        cls.post.soup = post_json
        cls.expected = {'column_in_name': 'xiepanda', 'slug': 20202275,
                        'column_name': '谢熊猫出没注意',
                        'author_name': '谢熊猫君', 'author_id': 'xiepanda',
                        'title': '为了做一个称职的吃货，他决定连着吃一百天转基因食物',
                        'upvote_num': 963, 'comment_num': 199}

    def test_column_in_name(self):
        self.assertEqual(self.expected['column_in_name'],
                         self.post.column_in_name)

    def test_slug(self):
        self.assertEqual(self.expected['slug'], self.post.slug)

    def test_author(self):
        self.assertEqual(self.expected['author_name'], self.post.author.name)
        self.assertEqual(self.expected['author_id'], self.post.author.id)

    def test_title(self):
        self.assertEqual(self.expected['title'], self.post.title)

    def test_upvote_num(self):
        self.assertEqual(self.expected['upvote_num'], self.post.upvote_num)

    def test_comment_num(self):
        self.assertEqual(self.expected['comment_num'], self.post.comment_num)

    def test_save(self):
        save_name = 'post_save'
        self.post.save(filepath=TEST_DATA_PATH, filename=save_name)
        post_saved_path = os.path.join(TEST_DATA_PATH, save_name + '.md')
        with open(post_saved_path, 'rb') as f:
            post_saved = f.read()
        os.remove(post_saved_path)
        self.assertEqual(self.post_saved, post_saved)
