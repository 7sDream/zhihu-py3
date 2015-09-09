#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals
import unittest
import os

from test_utils import TEST_DATA_PATH
from zhihu import Collection
from zhihu.common import BeautifulSoup


class CollectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = 'http://www.zhihu.com/collection/28698204'
        file_path = os.path.join(TEST_DATA_PATH, 'collection.html')
        with open(file_path, 'rb') as f:
            html = f.read()
        soup = BeautifulSoup(html)

        cls.collection = Collection(url)
        cls.collection._session = None
        cls.collection.soup = soup
        cls.expected = {'cid': 3725428, 'name': '可以用来背的答案',
                        'xsrf': 'cfd489623d34ca03adfdc125368c6426',
                        'owner_id': 'buhuilengyoumo', 'owner_name': '树叶',
                        'follower_num': 6328, 'top_ques_id': 26092705,
                        'top_ques_title': ('一直追求（吸引）不到喜欢的异性，'
                                           '感觉累了怎么办？'),
                        'top_ans_id': 32989919, 'top_ans_author_name': '朱炫',
                        'top_ans_upvote_num': 16595,
                        'top_ans_author_id': 'zhu-xuan-86'
                        }

    def test_cid(self):
        self.assertEqual(self.expected['cid'], self.collection.cid)

    def test_name(self):
        self.assertEqual(self.expected['name'], self.collection.name)

    def test_xsrf(self):
        self.assertEqual(self.expected['xsrf'], self.collection.xsrf)

    def test_owner(self):
        owner = self.collection.owner
        self.assertEqual(self.expected['owner_id'], owner.id)
        self.assertEqual(self.expected['owner_name'], owner.name)

    def test_follower_num(self):
        self.assertEqual(self.expected['follower_num'],
                         self.collection.follower_num)

    def test_page_get_questions(self):
        questions = [q for q in
                     self.collection._page_get_questions(self.collection.soup)]
        ques = questions[0]
        self.assertEqual(self.expected['top_ques_id'], ques.id)
        self.assertEqual(self.expected['top_ques_title'], ques.title)

    def test_page_get_answers(self):
        answers = [a for a in
                   self.collection._page_get_answers(self.collection.soup)]
        ans = answers[0]
        self.assertEqual(self.expected['top_ans_id'], ans.id)
        self.assertEqual(self.expected['top_ans_upvote_num'], ans.upvote_num)
        self.assertEqual(self.expected['top_ans_author_name'], ans.author.name)
        self.assertEqual(self.expected['top_ans_author_id'], ans.author.id)

    def test_questions(self):
        qs = self.collection.questions
        ques = next(qs)
        self.assertEqual(self.expected['top_ques_id'], ques.id)
        self.assertEqual(self.expected['top_ques_title'], ques.title)

    def test_answers(self):
        anses = self.collection.answers
        ans = next(anses)
        self.assertEqual(self.expected['top_ans_id'], ans.id)
        self.assertEqual(self.expected['top_ans_upvote_num'], ans.upvote_num)
        self.assertEqual(self.expected['top_ans_author_name'], ans.author.name)
        self.assertEqual(self.expected['top_ans_author_id'], ans.author.id)
