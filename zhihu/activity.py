#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from .common import *
from .acttype import ActType
from .question import Question
from .answer import Answer
from .column import Column
from .post import Post
from .topic import Topic
from .author import Author
from .collection import Collection


class Activity:

    """用户动态类，请使用Author.activities获取."""
    def __init__(self, act, session, author):
        """创建用户动态类实例.

        :param bs4.element.Tag act: 表示用户动态的页面元素
        :param Session session: 使用的网络会话
        :param Author author: Activity 所属的用户对象
        :return: 用户动态对象
        :rtype: Activity

        :说明:
            根据Activity.type的不同可以获取的属性，具体请看 :class:`.ActType`

        """
        self._session = session
        self._author = author
        self.type = ActType.from_str(act.attrs['data-type-detail'])

        useless_tag = act.div.find('a', class_='zg-link')
        if useless_tag is not None:
            useless_tag.extract()

        attribute = self._get_assemble_method(self.type)(act)
        self._attr = attribute.__class__.__name__.lower()
        setattr(self, self._attr, attribute)
        self._time = datetime.fromtimestamp(int(act['data-time']))

    @property
    def content(self):
        """获取此对象中能提供的那个属性，对应表请查看ActType类.

        :return: 对象提供的对象
        :rtype: Author or Question or Answer or Topic or Column or Post
        """
        return getattr(self, self._attr)

    @property
    def time(self):
        """
        :return: 返回用户执行 Activity 操作的时间
        :rtype: datetime.datetime
        """
        return self._time

    def __find_post(self, act):
        column_url = act.find('a', class_='column_link')['href']
        column_name = act.find('a', class_='column_link').text
        column = Column(column_url, column_name, session=self._session)
        try:
            author_tag = act.find('div', class_='author-info')
            author_url = Zhihu_URL + author_tag.a['href']
            author_info = list(author_tag.stripped_strings)
            author_name = author_info[0]
            author_motto = author_info[1] \
                if len(author_info) > 1 else ''
        except TypeError:
            author_url = None
            author_name = '匿名用户'
            author_motto = ''
        author = Author(author_url, author_name, author_motto, session=self._session)
        post_url = act.find('a', class_='post-link')['href']
        post_title = act.find('a', class_='post-link').text
        post_comment_num, post_upvote_num = self._parse_un_cn(act)
        return Post(post_url, column, author, post_title,
                    post_upvote_num, post_comment_num,
                    session=self._session)

    def _assemble_create_post(self, act):
        return self.__find_post(act)

    def _assemble_voteup_post(self, act):
        return self.__find_post(act)

    def _assemble_follow_column(self, act):
        return Column(act.div.a['href'], act.div.a.text, session=self._session)

    def _assemble_follow_topic(self, act):
        topic_url = Zhihu_URL + act.div.a['href']
        topic_name = act.div.a['title']
        return Topic(topic_url, topic_name, session=self._session)

    def _assemble_answer_question(self, act):
        question_url = Zhihu_URL + re_a2q.match(act.div.find_all('a')[-1]['href']).group(1)
        question_title = act.div.find_all('a')[-1].text
        question = Question(question_url, question_title, session=self._session)
        answer_url = Zhihu_URL + act.div.find_all('a')[-1]['href']
        answer_comment_num, answer_upvote_num = self._parse_un_cn(act)
        return Answer(answer_url, question, self._author, answer_upvote_num, session=self._session)

    def _assemble_voteup_answer(self, act):
        question_url = Zhihu_URL + re_a2q.match(act.div.a['href']).group(1)
        question_title = act.div.a.text
        question = Question(question_url, question_title, session=self._session)
        try_find_author = act.find_all('a', class_='author-link', href=re.compile('^/people/[^/]*$'))

        if len(try_find_author) == 0:
            author_url = None
            author_name = '匿名用户'
            author_motto = ''
            photo_url = None
        else:
            try_find_author = try_find_author[-1]
            author_url = Zhihu_URL + try_find_author['href']
            author_name = try_find_author.text
            try_find_motto = try_find_author.parent.span
            if try_find_motto is None:
                author_motto = ''
            else:
                author_motto = try_find_motto['title']
            photo_url = PROTOCOL + try_find_author.parent.a.img[
                'src'].replace('_s', '_r')

        author = Author(author_url, author_name, author_motto,
                        photo_url=photo_url, session=self._session)
        answer_url = Zhihu_URL + act.div.a['href']
        answer_comment_num, answer_upvote_num = self._parse_un_cn(act)
        return Answer(answer_url, question, author, answer_upvote_num, session=self._session)

    def _assemble_ask_question(self, act):
        return Question(Zhihu_URL + act.div.contents[3]['href'],
                        list(act.div.children)[3].text,
                        session=self._session)

    def _assemble_follow_question(self, act):
        return Question(Zhihu_URL + act.div.a['href'], act.div.a.text, session=self._session)

    def _assemble_follow_collection(self, act):
        url = act.div.a['href']
        if not url.startswith('http'):
            url = Zhihu_URL + url
        return Collection(url, session=self._session)

    def _get_assemble_method(self, act_type):
        assemble_methods = {
            ActType.UPVOTE_POST: self._assemble_voteup_post,
            ActType.FOLLOW_COLUMN: self._assemble_follow_column,
            ActType.UPVOTE_ANSWER: self._assemble_voteup_answer,
            ActType.ANSWER_QUESTION: self._assemble_answer_question,
            ActType.ASK_QUESTION: self._assemble_ask_question,
            ActType.FOLLOW_QUESTION: self._assemble_follow_question,
            ActType.FOLLOW_TOPIC: self._assemble_follow_topic,
            ActType.PUBLISH_POST: self._assemble_create_post,
            ActType.FOLLOW_COLLECTION: self._assemble_follow_collection
        }

        if act_type in assemble_methods:
            return assemble_methods[act_type]
        else:
            raise ValueError('invalid activity type')

    @staticmethod
    def _parse_un_cn(act):
        upvote_num = int(act.find('a', class_='zm-item-vote-count')['data-votecount'])
        comment = act.find('a', class_='toggle-comment')
        comment_text = next(comment.stripped_strings)
        comment_num_match = re_get_number.match(comment_text)
        comment_num = int(comment_num_match.group(1)) if comment_num_match is not None else 0
        return comment_num, upvote_num
