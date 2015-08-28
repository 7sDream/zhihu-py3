#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

from .common import *
import time


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
        self._id = int(re_topic_url.match(self.url).group(1))

    def _make_soup(self):
        if self.soup is None:
            self.soup = BeautifulSoup(self._session.get(self.url).content)

    @property
    def id(self):
        """获取话题Id（网址最后那串数字）

        :return: 话题Id
        :rtype: int
        """
        return self._id

    @property
    @check_soup('_xsrf')
    def xsrf(self):
        """获取知乎的反xsrf参数（用不到就忽视吧~）

        :return: xsrf参数
        :rtype: str
        """
        return self.soup.find('input', attrs={'name': '_xsrf'})['value']

    @property
    @check_soup('_tid')
    def tid(self):
        """话题内部Id，有时候要用到

        :return: 话题内部Id
        :rtype: int
        """
        return int(self.soup.find(
            'div', id='zh-topic-desc')['data-resourceid'])

    @property
    @check_soup('_name')
    def name(self):
        """获取话题名称.

        :return: 话题名称
        :rtype: str
        """
        return self.soup.find('h1').text

    @property
    def parents(self):
        """获取此话题的父话题。
        注意：由于没找到有很多父话题的话题来测试，
        所以本方法可能再某些时候出现问题，请不吝反馈。

        :return: 此话题的父话题，返回生成器
        :rtype: Topic.Iterable
        """
        self._make_soup()
        parent_topic_tag = self.soup.find('div', class_='parent-topic')
        if parent_topic_tag is None:
            return []
        else:
            for topic_tag in parent_topic_tag.find_all('a'):
                yield Topic(Zhihu_URL + topic_tag['href'],
                            topic_tag.text.strip(),
                            session=self._session)

    @property
    def children(self):
        """获取此话题的子话题

        :return: 此话题的子话题， 返回生成器
        :rtype: Topic.Iterable
        """
        self._make_soup()
        child_topic_tag = self.soup.find('div', class_='child-topic')
        if child_topic_tag is None:
            return []
        elif '共有' not in child_topic_tag.contents[-2].text:
            for topic_tag in child_topic_tag.div.find_all('a'):
                yield Topic(Zhihu_URL + topic_tag['href'],
                            topic_tag.text.strip(),
                            session=self._session)
        else:
            flag = 'load'
            child = ''
            data = {'_xsrf': self.xsrf}
            params = {
                'parent': self.id
            }
            while flag == 'load':
                params['child'] = child
                res = self._session.post(Topic_Get_Children_Url,
                                         params=params, data=data)
                j = map(lambda x: x[0], res.json()['msg'][1])
                *topics, last = j
                for topic in topics:
                    yield Topic(Zhihu_URL + '/topic/' + topic[2], topic[1],
                                session=self._session)
                flag = last[0]
                child = last[2]
                if flag == 'topic':
                    yield Topic(Zhihu_URL + '/topic/' + last[2], last[1],
                                session=self._session)

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
    def followers(self):
        """获取话题关注者

        :return: 话题关注者，返回生成器
        :rtype: Author.Iterable
        """
        from .author import Author
        self._make_soup()
        gotten_data_num = 20
        data = {
            '_xsrf': self.xsrf,
            'start': '',
            'offset': 0
        }
        while gotten_data_num == 20:
            res = self._session.post(
                Topic_Get_More_Follower_Url.format(self.id), data=data)
            j = res.json()['msg']
            gotten_data_num = j[0]
            data['offset'] += gotten_data_num
            soup = BeautifulSoup(j[1])
            divs = soup.find_all('div', class_='zm-person-item')
            for div in divs:
                h2 = div.h2
                url = Zhihu_URL + h2.a['href']
                name = h2.a.text
                motto = h2.next_element.text
                yield Author(url, name, motto, session=self._session)
            data['start'] = int(re_get_number.match(divs[-1]['id']).group(1))

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
    def top_authors(self):
        """获取最佳回答者

        :return: 此话题下最佳回答者，一般来说是5个，要不就没有，返回生成器
        :rtype: Author.Iterable
        """
        from .author import Author
        self._make_soup()
        t = self.soup.find('div', id='zh-topic-top-answerer')
        if t is None:
            return
        for d in t.find_all('div', class_='zm-topic-side-person-item-content'):
            url = Zhihu_URL + d.a['href']
            name = d.a.text
            motto = d.div['title']
            yield Author(url, name, motto, session=self._session)

    @property
    def top_answers(self):
        """获取话题下的精华答案.

        :return: 话题下的精华答案，返回生成器.
        :rtype: Answer.Iterable
        """
        from .question import Question
        from .answer import Answer
        from .author import Author
        top_answers_url = Topic_Top_Answers_Url.format(self.id)
        params = {'page': 1}
        while True:
            # 超出50页直接返回
            if params['page'] > 50:
                return
            res = self._session.get(top_answers_url, params=params)
            params['page'] += 1
            soup = BeautifulSoup(res.content)
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

    @property
    def questions(self):
        """获取话题下的所有问题（按时间降序排列）

        :return: 话题下的所有问题，返回生成器
        :rtype: Question.Iterable
        """
        from .question import Question
        question_url = Topic_Question_Url.format(self.id)
        params = {'page': 1}
        older_time_stamp = int(time.time()) * 1000
        while True:
            res = self._session.get(question_url, params=params)
            soup = BeautifulSoup(res.content)
            if soup.find('div', class_='error') is not None:
                return
            questions = soup.find_all('div', class_='question-item')
            questions = list(filter(
                lambda x: int(x.h2.span['data-timestamp']) < older_time_stamp,
                questions))
            for qu_div in questions:
                url = Zhihu_URL + qu_div.h2.a['href']
                title = qu_div.h2.a.text
                yield Question(url, title, session=self._session)
            older_time_stamp = int(questions[-1].h2.span['data-timestamp'])
            params['page'] += 1

    @property
    def answers(self):
        """获取话题下所有答案（按时间降序排列）

        :return: 话题下所有答案，返回生成器
        :rtype: Answer.Iterable
        """
        from .question import Question
        from .answer import Answer
        from .author import Author
        newest_url = Topic_Newest_Url.format(self.id)
        params = {'start': 0, '_xsrf': self.xsrf}
        res = self._session.get(newest_url)
        soup = BeautifulSoup(res.content)
        while True:
            divs = soup.find_all('div', class_='folding')
            # 如果话题下无答案，则直接返回
            if len(divs) == 0:
                return
            last_score = divs[-1]['data-score']
            for div in divs:
                q = div.find('a', class_="question_link")
                question_url = Zhihu_URL + q['href']
                question_title = q.text
                question = Question(question_url, question_title,
                                    session=self._session)

                ans = div.find('a', class_='answer-date-link')
                answer_url = Zhihu_URL + ans['href']

                up = div.find('a', class_='zm-item-vote-count')
                upvote = int(up['data-votecount'])

                au = div.find('h3', class_='zm-item-answer-author-wrap')
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

            params['offset'] = last_score
            res = self._session.post(newest_url, data=params)
            gotten_feed_num = res.json()['msg'][0]
            # 如果得到内容数量为0则返回
            if gotten_feed_num == 0:
                return
            soup = BeautifulSoup(res.json()['msg'][1])

    @property
    def hot_questions(self):
        """获取话题下热门的问题

        :return: 话题下的热门动态中的问题，按热门度顺序返回生成器
        :rtype: Question.Iterable
        """
        from .question import Question
        hot_questions_url = Topic_Hot_Questions_Url.format(self.id)
        params = {'start': 0, '_xsrf': self.xsrf}
        res = self._session.get(hot_questions_url)
        soup = BeautifulSoup(res.content)
        while True:
            questions_duplicate = soup.find_all('a', class_='question_link')
            # 如果话题下无问题，则直接返回
            if len(questions_duplicate) == 0:
                return
                # 去除重复的问题
            questions = list(set(questions_duplicate))
            questions.sort(key=self._get_score, reverse=True)
            last_score = soup.find_all(
                'div', class_='feed-item')[-1]['data-score']
            for q in questions:
                question_url = Zhihu_URL + q['href']
                question_title = q.text
                question = Question(question_url, question_title,
                                    session=self._session)
                yield question
            params['offset'] = last_score
            res = self._session.post(hot_questions_url, data=params)
            gotten_feed_num = res.json()['msg'][0]
            # 如果得到问题数量为0则返回
            if gotten_feed_num == 0:
                return
            soup = BeautifulSoup(res.json()['msg'][1])

    @property
    def hot_answers(self):
        """获取话题下热门的回答

        :return: 话题下的热门动态中的回答，按热门度顺序返回生成器
        :rtype: Question.Iterable
        """
        from .question import Question
        from .author import Author
        from .answer import Answer
        hot_questions_url = Topic_Hot_Questions_Url.format(self.id)
        params = {'start': 0, '_xsrf': self.xsrf}
        res = self._session.get(hot_questions_url)
        soup = BeautifulSoup(res.content)
        while True:
            answers_div = soup.find_all('div', class_='feed-item')
            last_score = answers_div[-1]['data-score']
            for div in answers_div:
                # 没有 text area 的情况是：答案被和谐。
                if not (div.h3 and div.textarea):
                    continue
                question_url = Zhihu_URL + div.h2.a['href']
                question_title = div.a.text
                question = Question(question_url, question_title,
                                    session=self._session)
                if div.h3.a is None:
                    author_url = None
                    author_name = '匿名用户'
                    author_motto = ''
                else:
                    author_url = Zhihu_URL + div.h3.a['href']
                    author_name = div.h3.a.text
                    author_motto = div.strong['title'] if div.strong else ''
                author = Author(author_url, author_name, author_motto,
                                session=self._session)

                answer_url = Zhihu_URL + BeautifulSoup(
                    ''.join(map(str, div.textarea.contents))).find(
                    'a', class_='answer-date-link')['href']
                upvote_num = int(div.find(
                    'a', class_='zm-item-vote-count')['data-votecount'])

                yield Answer(answer_url, question, author, upvote_num,
                             session=self._session)

            params['offset'] = last_score
            res = self._session.post(hot_questions_url, data=params)
            gotten_feed_num = res.json()['msg'][0]
            # 如果得到问题数量为0则返回
            if gotten_feed_num == 0:
                return
            soup = BeautifulSoup(res.json()['msg'][1])

    @staticmethod
    def _get_score(tag):
        h2 = tag.parent
        div = h2.parent
        try:
            _ = h2['class']
            return div['data-score']
        except KeyError:
            return div.parent.parent['data-score']
