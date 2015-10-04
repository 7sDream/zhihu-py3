#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import json

from .common import *


class Question:

    """问题类，请使用``ZhihuClient.question``方法构造对象."""

    @class_common_init(re_question_url)
    def __init__(self, url, title=None, followers_num=None,
                 answer_num=None, session=None):
        """创建问题类实例.

        :param str url: 问题url
        :param str title: 问题标题，可选,
        :param int followers_num: 问题关注人数，可选
        :param int answer_num: 问题答案数，可选
        :return: 问题对象
        :rtype: Question
        """
        self._session = session
        self.url = url
        self._title = title
        self._answer_num = answer_num
        self._followers_num = followers_num
        self._id = int(re.match(r'.*/(\d+)', self.url).group(1))

    def _make_soup(self):
        if self.soup is None:
            r = self._session.get(self.url)
            self.soup = BeautifulSoup(r.content)

    @property
    def id(self):
        """获取问题id（网址最后的部分）.

        :return: 问题id
        :rtype: int
        """
        return self._id

    @property
    @check_soup('_qid')
    def qid(self):
        """获取问题内部id（用不到就忽视吧）

        :return: 问题内部id
        :rtype: int
        """
        return int(self.soup.find(
            'div', id='zh-question-detail')['data-resourceid'])

    @property
    @check_soup('_xsrf')
    def xsrf(self):
        """获取知乎的反xsrf参数（用不到就忽视吧~）

        :return: xsrf参数
        :rtype: str
        """
        return self.soup.find(
            'input', attrs={'name': '_xsrf'})['value']

    @property
    @check_soup('_html')
    def html(self):
        """获取页面源码.

        :return: 页面源码
        :rtype: str
        """
        return self.soup.prettify()

    @property
    @check_soup('_title')
    def title(self):
        """获取问题标题.

        :return: 问题标题
        :rtype: str
        """
        return self.soup.find('h2', class_='zm-item-title') \
            .text.replace('\n', '')

    @property
    @check_soup('_details')
    def details(self):
        """获取问题详细描述，目前实现方法只是直接获取文本，效果不满意……等更新.

        :return: 问题详细描述
        :rtype: str
        """
        return self.soup.find("div", id="zh-question-detail").div.text

    @property
    @check_soup('_answers_num')
    def answer_num(self):
        """获取问题答案数量.

        :return: 问题答案数量
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

        :return: 问题所属话题
        :rtype: list(str)
        """
        topics_list = []
        for topic in self.soup.find_all('a', class_='zm-item-tag'):
            topics_list.append(topic.text.replace('\n', ''))
        return topics_list

    @property
    def followers(self):
        """获取关注此问题的用户

        :return: 关注此问题的用户
        :rtype: Author.Iterable
        :问题: 要注意若执行过程中另外有人关注，可能造成重复获取到某些用户
        """
        self._make_soup()
        followers_url = self.url + 'followers'
        for x in common_follower(followers_url, self.xsrf, self._session):
            yield x

    @property
    def answers(self):
        """获取问题的所有答案.

        :return: 问题的所有答案，返回生成器
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
        data = {'_xsrf': self.xsrf,
                'method': 'next',
                'params': ''}
        for i in range(0, (self.answer_num - 1) // 50 + 1):
            if i == 0:
                # 修正各种建议修改的回答……
                error_answers = self.soup.find_all('div', id='answer-status')
                for each in error_answers:
                    each['class'] = 'zm-editable-content'
                # 正式处理
                authors = self.soup.find_all(
                    'h3', class_='zm-item-answer-author-wrap')
                urls = self.soup.find_all('a', class_='answer-date-link')
                upvote_nums = self.soup.find_all('div',
                                                 class_='zm-item-vote-info')
                contents = self.soup.find_all(
                    'div', class_='zm-editable-content')
                for author, url, upvote_num, content in \
                        zip(authors, urls, upvote_nums, contents):
                    a_url, name, motto, photo = parser_author_from_tag(author)
                    author_obj = Author(a_url, name, motto, photo_url=photo,
                                        session=self._session)
                    url = Zhihu_URL + url['href']
                    upvote_num = int(upvote_num['data-votecount'])
                    content = answer_content_process(content)
                    yield Answer(url, self, author_obj, upvote_num, content,
                                 session=self._session)
            else:
                params['offset'] = i * 50
                data['params'] = json.dumps(params)
                r = self._session.post(Question_Get_More_Answer_URL, data=data,
                                       headers=new_header)
                answer_list = r.json()['msg']
                for answer_html in answer_list:
                    yield self._parse_answer_html(answer_html, Author, Answer)

    @property
    def top_answer(self):
        """获取排名第一的答案.

        :return: 排名第一的答案
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

        :param int i: 获取前几个
        :return: 答案对象，返回生成器
        :rtype: Answer.Iterable
        """
        for j, a in enumerate(self.answers):
            if j <= i - 1:
                yield a
            else:
                return

    def _parse_answer_html(self, answer_html, Author, Answer):
        soup = BeautifulSoup(answer_html)
        # 修正各种建议修改的回答……
        error_answers = soup.find_all('div', id='answer-status')
        for each in error_answers:
            each['class'] = 'zm-editable-content'
        answer_url = \
            self.url + 'answer/' + soup.div['data-atoken']
        author = soup.find(
            'h3', class_='zm-item-answer-author-wrap')
        upvote_num = int(soup.find(
            'div', class_='zm-item-vote-info')['data-votecount'])
        content = soup.find(
            'div', class_='zm-editable-content')
        content = answer_content_process(content)
        a_url, name, motto, photo = parser_author_from_tag(author)
        author_obj = Author(a_url, name, motto, photo_url=photo,
                            session=self._session)
        return Answer(answer_url, self, author_obj,
                      upvote_num, content, session=self._session)
