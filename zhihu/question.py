#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import json

from .common import *


class Question:

    """问题类，请使用zhihu.ZhihuClient.getQuestion()创建"""

    def __init__(self, session, url, title=None, followers_num=None,
                 answer_num=None):
        """类对象初始化.

        :param str url: 问题地址，形如： http://www.zhihu.com/question/27936038
        :param str title: 可选, 问题标题
        :param int followers_num: 可选，问题关注人数
        :param int answer_num: 可选，问题答案数
        :return: Question对象
        :rtype: Question
        """
        if re_question_url.match(url) is None:
            raise ValueError('URL invalid')
        else:
            if url.endswith('/') is False:
                url += '/'
            self._session = session
            self.soup = None
            self.url = url
            self._title = title
            self._answer_num = answer_num
            self._followers_num = followers_num
            self._xsrf = ''

    def _make_soup(self):
        if self.soup is None:
            r = self._session.get(self.url)
            self.soup = BeautifulSoup(r.content)
            self._xsrf = self.soup.find(
                'input', attrs={'name': '_xsrf'})['value']

    @property
    @check_soup('_html')
    def html(self):
        """获取页面HTML源码.

        :return: html源码
        :rtype: str
        """
        return self.soup.prettify()

    @property
    @check_soup('_title')
    def title(self):
        """获取问题标题.

        :return: title of question
        :rtype: str
        """
        return self.soup.find('h2', class_='zm-item-title') \
            .text.replace('\n', '')

    @property
    @check_soup('_details')
    def details(self):
        """获取问题详细描述。 **目前实现方法只是直接获取文本，效果不满意……等更新.

        :return: 问题详细描述文本
        :rtype: str
        """
        return self.soup.find("div", id="zh-question-detail").div.text

    @property
    @check_soup('_answers_num')
    def answer_num(self):
        """获取问题答案数量.

        :return: 答案数量
        :rtype: int
        """
        answer_num_block = self.soup.find('h3', id='zh-question-answer-num')
        # 当0人回答或1回答时，都会找不到 answer_num_block，
        # 通过找答案的赞同数block来判断到底有没有答案。
        # （感谢知乎用户 段晓晨 提出此问题）
        if answer_num_block is None:
            if self.soup.find('span', class_='count') is not None:
                return 1
            else:
                return 0
        return int(answer_num_block['data-num'])

    @property
    @check_soup('_follower_num')
    def follower_num(self):
        """获取问题关注人数.

        :return: 问题关注人数
        :rtype: int
        """
        follower_num_block = self.soup.find('div', class_='zg-gray-normal')
        # 无人关注时 找不到对应block，直接返回0 （感谢知乎用户 段晓晨 提出此问题）
        if follower_num_block.strong is None:
            return 0
        return int(follower_num_block.strong.text)

    @property
    @check_soup('_topics')
    def topics(self):
        """获取问题所属话题.

        :return: 问题所属话题列表
        :rtype: list(str)
        """
        topics_list = []
        for topic in self.soup.find_all('a', class_='zm-item-tag'):
            topics_list.append(topic.text.replace('\n', ''))
        return topics_list

    @property
    def answers(self):
        """获取问题的所有答案，返回可迭代生成器.

        :return: 每次迭代返回一个Answer对象， 获取到的Answer对象自带
            所在问题、答主、赞同数量、回答内容四个属性。获取其他属性需要解析另外的网页。
        :rtype: Answer.Iterable
        """
        from .author import Author
        from .answer import Answer

        self._make_soup()
        new_header = dict(Default_Header)
        new_header['Referer'] = self.url
        params = {"url_token": self.id,
                  'pagesize': '50',
                  'offset': 0}
        data = {'_xsrf': self._xsrf,
                'method': 'next',
                'params': ''}
        for i in range(0, (self.answer_num - 1) // 50 + 1):
            if i == 0:
                # 修正各种建议修改的回答……
                error_answers = self.soup.find_all('div', id='answer-status')
                for each in error_answers:
                    each['class'] = ' zm-editable-content clearfix'
                # 正式处理
                authors = self.soup.find_all(
                    'h3', class_='zm-item-answer-author-wrap')
                urls = self.soup.find_all('a', class_='answer-date-link')
                upvote_nums = self.soup.find_all('div',
                                                 class_='zm-item-vote-info')
                contents = self.soup.find_all(
                    'div', class_=' zm-editable-content clearfix')
                for author, url, upvote_num, content in \
                        zip(authors, urls, upvote_nums, contents):
                    a_url, name, motto, photo = parser_author_from_tag(author)
                    author_obj = Author(self._session, a_url, name, motto,
                                        photo_url=photo)
                    url = Zhihu_URL + url['href']
                    upvote_num = int(upvote_num['data-votecount'])
                    content = answer_content_process(
                        self.soup.new_tag(content))
                    yield Answer(self._session, url, self, author_obj,
                                 upvote_num, content)
            else:
                params['offset'] = i * 50
                data['params'] = json.dumps(params)
                r = self._session.post(Get_More_Answer_URL, data=data,
                                       headers=new_header)
                answer_list = r.json()['msg']
                for answer_html in answer_list:
                    soup = BeautifulSoup(answer_html)
                    # 修正各种建议修改的回答……
                    error_answers = soup.find_all('div', id='answer-status')
                    for each in error_answers:
                        each['class'] = ' zm-editable-content clearfix'
                    answer_url = \
                        self.url + 'answer/' + soup.div['data-atoken']
                    author = soup.find(
                        'h3', class_='zm-item-answer-author-wrap')
                    upvote_num = int(soup.find(
                        'div', class_='zm-item-vote-info')['data-votecount'])
                    content = soup.find(
                        'div', class_='zm-editable-content')
                    content = answer_content_process(content)
                    author_obj = parser_author_from_tag(author)
                    yield Answer(self._session, answer_url, self, author_obj,
                                 upvote_num, content)

    @property
    def top_answer(self):
        """获取排名第一的答案.

        :return: 排名第一的答案对象，能直接获取的属性参见answers方法
        :rtype: Answer
        """
        for a in self.answers:
            return a

    def top_i_answer(self, i):
        """获取排名某一位的答案.

        :param int i: 要获取的答案的排名
        :return: 答案对象，能直接获取的属性参见answers方法
        :rtype: Answer
        """
        for j, a in enumerate(self.answers):
            if j == i - 1:
                return a

    def top_i_answers(self, i):
        """获取排名在前几位的答案.

        :param int i: 获取高位排名答案数量
        :return: 答案对象生成器，这些对象能直接获取的属性参见answers方法
        :rtype: Answer.Iterable
        """
        for j, a in enumerate(self.answers):
            if j <= i - 1:
                yield a

    @property
    def id(self):
        """获取答问题id，就是网址最后那串数字.

        :return: 问题id
        :rtype: int
        """
        return int(re.match(r'.*/(\d+)', self.url).group(1))
