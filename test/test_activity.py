#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals
import unittest
import os
import datetime

from zhihu import Question, Activity, ActType
from zhihu.common import BeautifulSoup

from test_utils import TEST_DATA_PATH


class ActivityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = 'http://www.zhihu.com/question/24825703'
        file_path = os.path.join(TEST_DATA_PATH, 'question.html')
        with open(file_path, 'rb') as f:
            html = f.read()
        soup = BeautifulSoup(html)

        cls.question = Question(url)
        cls.question._session = None
        cls.question.soup = soup

        act_time = datetime.datetime.fromtimestamp(1439395600)
        act_type = ActType.FOLLOW_QUESTION
        cls.activity = Activity(act_type, act_time, question=cls.question)

    def test_content(self):
        self.assertIs(self.question, self.activity.content)

    def test_init_errors(self):
        act_time = datetime.datetime.fromtimestamp(1439395600)
        act_type = ActType.FOLLOW_QUESTION

        with self.assertRaises(ValueError):
            Activity(100, act_time)
        with self.assertRaises(ValueError):
            Activity(act_type, act_time)
