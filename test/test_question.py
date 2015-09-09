#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals
import unittest
import os

from test_utils import TEST_DATA_PATH
from zhihu import Question, Author, Answer
from zhihu.common import BeautifulSoup


description = ("从小父母和大家庭里，长辈都教我们得到别人帮助时要说“谢谢”。"
               "比方说家庭聚餐，亲人们帮忙夹了菜要感谢。无论多么亲密,父母还是"
               "兄妹，都要说声谢谢。   后来上了高中，大学。也习惯性的及时表达"
               "对他人帮助的感谢。  但室友们，还有男朋友，都不喜欢我这样。他们"
               "说，这样说的话会感觉双方很有距离感很生疏。尤其是男朋友，不喜"
               "欢我这样，他说这样很不亲密，情侣之间就不分得那么清，不需要谢"
               "谢的。但我从小习惯了，别人帮了我我不说的话，会很不自在。  "
               '怎么办？我还要继续这样吗？什么时候不该说"谢谢”？？')


class QuestionTest(unittest.TestCase):
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
        cls.expected = {'id': 24825703, 'qid': 2112271,
                        'xsrf': 'cfd489623d34ca03adfdc125368c6426',
                        'html': soup.prettify(),
                        'title': '关系亲密的人之间要说「谢谢」吗？',
                        'details': description, 'answer_num': 621,
                        'follower_num': 4427, 'top_answer_id': 39753456,
                        'top_answer_author_name': '芝士就是力量',
                        'top_answer_upvote_num': 97, 'top_50_ans_id': 31003847,
                        'top_50_ans_author_name': '圭多达莱佐',
                        'top_50_ans_upvote_num': 31, 'more_ans_id': 39958704,
                        'more_ans_author_name': '柳蜻蜓',
                        'more_ans_upvote_num': 1,
                        'topics': ['心理学', '恋爱', '社会', '礼仪',
                                   '亲密关系'],
                        }

        more_ans_file_path = os.path.join(TEST_DATA_PATH,
                                          'question_more_answer.html')
        with open(more_ans_file_path, 'rb') as f:
            cls.more_ans_html = f.read()

    def test_id(self):
        self.assertEqual(self.expected['id'], self.question.id)

    def test_qid(self):
        self.assertEqual(self.expected['qid'], self.question.qid)

    def test_xsrf(self):
        self.assertEqual(self.expected['xsrf'], self.question.xsrf)

    def test_html(self):
        self.assertEqual(self.expected['html'], self.question.html)

    def test_title(self):
        self.assertEqual(self.expected['title'], self.question.title)

    def test_details(self):
        self.assertEqual(self.expected['details'], self.question.details)

    def test_answer_num(self):
        self.assertEqual(self.expected['answer_num'], self.question.answer_num)

    def test_follower_num(self):
        self.assertEqual(self.expected['follower_num'],
                         self.question.follower_num)

    def test_topics(self):
        self.assertEqual(self.expected['topics'], self.question.topics)

    def test_top_answer(self):
        answer = self.question.top_answer
        self.assertEqual(self.expected['top_answer_id'], answer.id)
        self.assertEqual(self.expected['top_answer_author_name'],
                         answer.author.name)
        self.assertEqual(self.expected['top_answer_upvote_num'],
                         answer.upvote_num)

    def test_top_i_answer(self):
        answer = self.question.top_i_answer(50)
        self.assertEqual(self.expected['top_50_ans_id'], answer.id)
        self.assertEqual(self.expected['top_50_ans_author_name'],
                         answer.author.name)
        self.assertEqual(self.expected['top_50_ans_upvote_num'],
                         answer.upvote_num)

    def test_parse_answer_html(self):
        answer = self.question._parse_answer_html(self.more_ans_html, Author,
                                                  Answer)
        self.assertEqual(self.expected['more_ans_id'], answer.id)
        self.assertEqual(self.expected['more_ans_author_name'],
                         answer.author.name)
        self.assertEqual(self.expected['more_ans_upvote_num'],
                         answer.upvote_num)

    def test_top_i_answers(self):
        answers = [a for a in self.question.top_i_answers(1)]
        answer = answers[0]
        self.assertEqual(self.expected['top_answer_id'], answer.id)
        self.assertEqual(self.expected['top_answer_author_name'],
                         answer.author.name)
        self.assertEqual(self.expected['top_answer_upvote_num'],
                         answer.upvote_num)
