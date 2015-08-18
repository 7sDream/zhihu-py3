#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

from .common import *


class Topic:

    """答案类，请使用``ZhihuClient.topic``方法构造对象."""

    @class_common_init(re_topic_url)
    def __init__(self, url, name=None, session=None):
        """创建话题类实例.

        :param url: 话题url
        :param name: 话题名称，可选
        :return: Topic
        """
        self.url = url
        self._session = session
        self._name = name

    def _make_soup(self):
        if self.soup is None:
            self.soup = BeautifulSoup(self._session.get(self.url).content)

    @property
    @check_soup('_name')
    def name(self):
        """获取话题名称.

        :return: 话题名称
        :rtype: str
        """
        return self.soup.find('h1').text

    @property
    @check_soup('_follower_num')
    def follower_num(self):
        """获取话题关注人数.

        :return: 关注人数
        :rtype: int
        """
        follower_num_block = self.soup.find(
            'div', class_='zm-topic-side-followers-info')
        # 无人关注时 找不到对应block，直接返回0 （感谢知乎用户 段晓晨 提出此问题）
        if follower_num_block.strong is None:
            return 0
        return int(follower_num_block.strong.text)

    @property
    @check_soup('_photo_url')
    def photo_url(self):
        """获取话题头像图片地址.

        :return: 话题头像url
        :rtype: str
        """
        img = self.soup.find('a', id='zh-avartar-edit-form').img['src']
        return img.replace('_m', '_r')

    @property
    @check_soup('_description')
    def description(self):
        """获取话题描述信息.

        :return: 话题描述信息
        :rtype: str
        """
        desc = self.soup.find('div', class_='zm-editable-content').text
        return desc

    @property
    def top_answers(self):
        """获取话题下的精华答案.

        :return: 话题下的精华答案，返回生成器.
        :rtype: Answer.Iterable
        """
        from .question import Question
        from .answer import Answer
        from .author import Author
        if self.url is None:
            return
        for page_index in range(1, 50):
            html = self._session.get(
                self.url + 'top-answers?page=' + str(page_index)).text
            soup = BeautifulSoup(html)
            # 不够50页，来到错误页面 返回
            if soup.find('div', class_='error') is not None:
                return
            questions = soup.find_all('a', class_='question_link')
            answers = soup.find_all(
                'a', class_=re.compile(r'answer-date-link.*'))
            authors = soup.find_all('h3', class_='zm-item-answer-author-wrap')
            upvotes = soup.find_all('a', class_='zm-item-vote-count')
            for ans, up, q, au in zip(answers, upvotes, questions, authors):
                answer_url = Zhihu_URL + ans['href']
                question_url = Zhihu_URL + q['href']
                question_title = q.text
                upvote = int(up['data-votecount'])
                question = Question(question_url, question_title,
                                    session=self._session)
                if au.a is None:
                    author_url = None
                    author_name = '匿名用户'
                    author_motto = ''
                else:
                    author_url = Zhihu_URL + au.a['href']
                    author_name = au.a.text
                    author_motto = au.strong['title'] if au.strong else ''

                author = Author(author_url, author_name, author_motto,
                                session=self._session)
                yield Answer(answer_url, question, author, upvote,
                             session=self._session)
