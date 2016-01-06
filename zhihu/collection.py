#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .common import *
from .base import BaseZhihu

class Collection(BaseZhihu):

    """收藏夹，请使用``ZhihuClient.collection``方法构造对象."""

    @class_common_init(re_collection_url)
    def __init__(self, url, owner=None, name=None, follower_num=None,
                 session=None):
        """创建收藏夹类实例.

        :param str url: 收藏夹主页url，必须
        :param Author owner: 收藏夹拥有者，可选
        :param str name: 收藏夹标题，可选
        :param int follower_num: 收藏夹关注人数，可选
        :param Session session: 使用的网络会话，为空则使用新会话。
        :return: 收藏夹对象
        :rtype: Collection
        """
        self.url = url
        self._session = session
        self.soup = None
        self._name = name
        self._owner = owner
        self._follower_num = follower_num
        self._id = int(re.match(r'.*/(\d+)', self.url).group(1))

    @property
    def id(self):
        """获取收藏夹id（网址最后的部分）.

        :return: 收藏夹id
        :rtype: int
        """
        return self._id

    @property
    @check_soup('_cid')
    def cid(self):
        """获取收藏夹内部Id（用不到忽视就好）

        :return: 内部Id
        :rtype: int
        """
        return int(re_get_number.match(
            self.soup.find('a', attrs={'name': 'focus'})['id']).group(1))

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
    @check_soup('_name')
    def name(self):
        """获取收藏夹名字.

        :return: 收藏夹名字
        :rtype: str
        """
        return re_del_empty_line.match(
            self.soup.find('h2', id='zh-fav-head-title').text).group(1)

    @property
    @check_soup('_owner')
    def owner(self):
        """获取收藏夹拥有者，返回Author对象.

        :return: 收藏夹拥有者
        :rtype: Author
        """
        from .author import Author

        a = self.soup.find('h2', class_='zm-list-content-title').a
        name = a.text
        url = Zhihu_URL + a['href']
        motto = self.soup.find(
            'div', id='zh-single-answer-author-info').div.text
        photo_url = PROTOCOL + self.soup.find(
            'img', class_='zm-list-avatar-medium')['src'].replace('_m', '_r')
        return Author(url, name, motto, photo_url=photo_url,
                      session=self._session)

    @property
    @check_soup('_follower_num')
    def follower_num(self):
        """获取关注此收藏夹的人数.

        :return: 关注此收藏夹的人数
        :rtype: int
        """
        href = re_collection_url_split.match(self.url).group(1)
        return int(self.soup.find('a', href=href + 'followers').text)

    @property
    def followers(self):
        """获取关注此收藏夹的用户

        :return: 关注此收藏夹的用户
        :rtype: Author.Iterable
        """
        self._make_soup()
        followers_url = self.url + 'followers'
        for x in common_follower(followers_url, self.xsrf, self._session):
            yield x

    @property
    def questions(self):
        """获取收藏夹内所有问题对象.

        :return: 收藏夹内所有问题，返回生成器
        :rtype: Question.Iterable
        """
        self._make_soup()
        # noinspection PyTypeChecker
        for question in self._page_get_questions(self.soup):
            yield question
        i = 2
        while True:
            soup = BeautifulSoup(self._session.get(
                self.url[:-1] + '?page=' + str(i)).text)
            for question in self._page_get_questions(soup):
                if question == 0:
                    return
                yield question
            i += 1

    @property
    def answers(self):
        """获取收藏夹内所有答案对象.

        :return: 收藏夹内所有答案，返回生成器
        :rtype: Answer.Iterable
        """
        self._make_soup()
        # noinspection PyTypeChecker
        for answer in self._page_get_answers(self.soup):
            yield answer
        i = 2
        while True:
            soup = BeautifulSoup(self._session.get(
                self.url[:-1] + '?page=' + str(i)).text)
            for answer in self._page_get_answers(soup):
                if answer == 0:
                    return
                yield answer
            i += 1

    @property
    def logs(self):
        """获取收藏夹日志

        :return: 收藏夹日志中的操作，返回生成器
        :rtype: CollectActivity.Iterable
        """
        import time
        from datetime import datetime
        from .answer import Answer
        from .acttype import CollectActType

        self._make_soup()
        gotten_feed_num = 20
        offset = 0
        data = {
            'start': 0,
            '_xsrf': self.xsrf
        }
        api_url = self.url + 'log'
        while gotten_feed_num == 20:
            data['offset'] = offset
            res = self._session.post(url=api_url, data=data)
            gotten_feed_num = res.json()['msg'][0]
            soup = BeautifulSoup(res.json()['msg'][1])
            offset += gotten_feed_num
            zm_items = soup.find_all('div', class_='zm-item')

            for zm_item in zm_items:
                act_time = datetime.strptime(zm_item.find('time').text, "%Y-%m-%d %H:%M:%S")

                if zm_item.find('ins'):
                    try:
                        answer = Answer(Zhihu_URL + zm_item.find('ins').a['href'],
                                        session=self._session)
                        type = CollectActType.INSERT_ANSWER
                        yield CollectActivity(type, act_time, self.owner, self, answer)
                    except ValueError:
                        type = CollectActType.CREATE_COLLECTION
                        yield CollectActivity(type, act_time, self.owner, self)
                elif zm_item.find('del'):
                    type = CollectActType.DELETE_ANSWER
                    answer = Answer(Zhihu_URL + zm_item.find('del').a['href'],
                                    session=self._session)
                    yield CollectActivity(type, act_time, self.owner, self, answer)
                else:
                    continue

            data['start'] = zm_items[-1]['id'][8:]
            time.sleep(0.5)

    def _page_get_questions(self, soup):
        from .question import Question

        question_tags = soup.find_all("div", class_="zm-item")
        if len(question_tags) == 0:
            yield 0
            return
        else:
            for question_tag in question_tags:
                if question_tag.h2 is not None:
                    question_title = question_tag.h2.a.text
                    question_url = Zhihu_URL + question_tag.h2.a['href']
                    yield Question(question_url, question_title,
                                   session=self._session)

    def _page_get_answers(self, soup):
        from .question import Question
        from .author import Author
        from .answer import Answer

        answer_tags = soup.find_all("div", class_="zm-item")
        if len(answer_tags) == 0:
            yield 0
            return
        else:
            question = None
            for tag in answer_tags:
                # 判断是否是'建议修改的回答'等情况
                url_tag = tag.find('a', class_='answer-date-link')
                if url_tag is None:
                    reason = tag.find('div', id='answer-status').p.text
                    print("pass a answer, reason %s ." % reason)
                    continue
                author_name = '匿名用户'
                author_motto = ''
                author_url = None
                if tag.h2 is not None:
                    question_title = tag.h2.a.text
                    question_url = Zhihu_URL + tag.h2.a['href']
                    question = Question(question_url, question_title,
                                        session=self._session)
                answer_url = Zhihu_URL + url_tag['href']
                div = tag.find('div', class_='zm-item-answer-author-info')
                author_link = div.find('a', class_='author-link')
                if author_link is not None:
                    author_url = Zhihu_URL + author_link['href']
                    author_name = author_link.text
                    motto_span = div.find('span', class_='bio')
                    if motto_span is not None:
                        author_motto = motto_span['title']
                author = Author(author_url, author_name, author_motto,
                                session=self._session)
                upvote = int(tag.find(
                    'a', class_='zm-item-vote-count')['data-votecount'])
                answer = Answer(answer_url, question, author,
                                upvote, session=self._session)
                yield answer


class CollectActivity:
    """收藏夹操作, 请使用``Collection.logs``构造对象."""

    def __init__(self, type, time, owner, collection, answer=None):
        """创建收藏夹操作类实例

        :param acttype.CollectActType type: 操作类型
        :param datetime.datetime time: 进行操作的时间
        :param Author owner: 收藏夹的拥有者
        :param Collection collection: 所属收藏夹
        :param Answer answer: 收藏的答案，可选
        :return: CollectActivity
        """
        self._type = type
        self._time = time
        self._owner = owner
        self._collection = collection
        self._answer = answer

    @property
    def type(self):
        """
        :return: 收藏夹操作类型, 具体参见 :class:`.CollectActType`
        :rtype: :class:`.CollectActType`
        """
        return self._type

    @property
    def answer(self):
        """
        :return: 添加或删除收藏的答案, 若是创建收藏夹操作返回 None
        :rtype: Answer or None
        """
        return self._answer

    @property
    def time(self):
        """
        :return: 进行操作的时间
        :rtype: datetime.datetime
        """
        return self._time

    @property
    def owner(self):
        """
        :return: 收藏夹的拥有者
        :rtype: Author
        """
        return self._owner

    @property
    def collection(self):
        """
        :return: 所属收藏夹
        :rtype: Collection
        """
        return self._collection
