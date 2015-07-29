#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import json
import datetime

from .common import *


class Author:

    """用户类，用用户主页地址作为参数来构造对象，其他参数可选."""

    def __init__(self, session, url, name=None, motto=None, follower_num=None,
                 question_num=None, answer_num=None, upvote_num=None,
                 thank_num=None, photo_url=None):
        """类对象初始化.

        :param str url: 用户主页地址，形如 http://www.zhihu.com/people/7sdream
        :param str name: 用户名字，可选
        :param str motto: 用户简介，可选
        :param int follower_num: 用户粉丝数，可选
        :param int question_num: 用户提问数，可选
        :param int answer_num: 用户答案数，可选
        :param int upvote_num: 用户获得赞同数，可选
        :param str photo_url: 用户头像地址，可选
        :return: Author对象
        :rtype: Author
        """
        if url is not None:
            if re_author_url.match(url) is None:
                raise ValueError('URL invalid')
            if url.endswith('/') is False:
                url += '/'
        self.url = url
        self._session = session
        self.soup = None
        self.card = None
        self._nav_list = None
        self._name = name
        self._motto = motto
        self._follower_num = follower_num
        self._question_num = question_num
        self._answer_num = answer_num
        self._upvote_num = upvote_num
        self._thank_num = thank_num
        self._photo_url = photo_url
        self._xsrf = None
        self._hash_id = None

    def _make_soup(self):
        if self.soup is None and self.url is not None:
            r = self._session.get(self.url)
            self.soup = BeautifulSoup(r.content)
            self._nav_list = self.soup.find(
                'div', class_='profile-navbar').find_all('a')
            self._xsrf = self.soup.find(
                'input', attrs={'name': '_xsrf'})['value']
            div = self.soup.find('div', class_='zm-profile-header-op-btns')
            if div is not None:
                self._hash_id = div.button['data-id']
            else:
                ga = self.soup.find('script', attrs={'data-name': 'ga_vars'})
                self._hash_id = json.loads(ga.text)['user_hash']

    def _make_card(self):
        if self.card is None and self.url is not None:
            params = {'url_token': self.id}
            real_params = {'params': json.dumps(params)}
            r = self._session.get(Get_Profile_Card_URL, params=real_params)
            self.card = BeautifulSoup(r.content)

    @property
    def id(self):
        """获取用户id，就是网址最后那一部分.

        :return: 用户id
        :rtype: str
        """
        return re.match(r'^.*/([^/]+)/$', self.url).group(1)

    @property
    @check_soup('_name')
    def name(self):
        """获取用户名字.

        :return: 用户名字
        :rtype: str
        """
        if self.url is None:
            return '匿名用户'
        return self.soup.find('div', class_='title-section ellipsis').span.text

    @property
    @check_soup('_motto')
    def motto(self):
        """获取用户自我介绍，由于历史原因，我还是把这个属性叫做motto吧.

        :return: 用户自我介绍
        :rtype: str
        """
        if self.url is None:
            return ''
        else:
            bar = self.soup.find(
                'div', class_='title-section ellipsis')
            if len(bar.contents) < 4:
                return ''
            else:
                return bar.contents[3].text

    @property
    @check_soup('_photo_url', '_make_card')
    def photo_url(self):
        """获取用户头像图片地址.

        :return: 用户头像url
        :rtype: str
        """
        if self.url is not None:
            if self.soup is not None:
                img = self.soup.find(
                    'img', class_='avatar avatar-l')['src']
                return img.replace('_l', '_r')
            else:
                assert(self.card is not None)
                return self.card.img['src'].replace('_m', '_l')
        else:
            return 'http://pic1.zhimg.com/da8e974dc_r.jpg'

    @property
    @check_soup('_followee_num')
    def followee_num(self):
        """获取关注了多少人.

        :return: 关注的人数
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            number = int(self.soup.find(
                'div', class_='zm-profile-side-following').a.strong.text)
            return number

    @property
    @check_soup('_follower_num')
    def follower_num(self):
        """获取追随者数量，就是关注此人的人数.

        :return: 追随者数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            number = int(self.soup.find(
                'div', class_='zm-profile-side-following zg-clear').find_all(
                'a')[1].strong.text)
            return number

    @property
    @check_soup('_upvote_num')
    def upvote_num(self):
        """获取收到的的赞同数量.

        :return: 收到的的赞同数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            number = int(self.soup.find(
                'span', class_='zm-profile-header-user-agree').strong.text)
            return number

    @property
    @check_soup('_thank_num')
    def thank_num(self):
        """获取收到的感谢数量.

        :return: 收到的感谢数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            number = int(self.soup.find(
                'span', class_='zm-profile-header-user-thanks').strong.text)
            return number

    @property
    @check_soup('_question_num')
    def question_num(self):
        """获取提问数量.

        :return: 提问数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[1].span.text)

    @property
    @check_soup('_answer_num')
    def answer_num(self):
        """获取答案数量.

        :return: 答案数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[2].span.text)

    @property
    @check_soup('_post_num')
    def post_num(self):
        """获取专栏文章数量.

        :return: 专栏文章数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[3].span.text)

    @property
    @check_soup('_collection_num')
    def collection_num(self):
        """获取收藏夹数量.

        :return: 收藏夹数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[4].span.text)

    @property
    def questions(self):
        """获取此人问过的所有问题对象，返回生成器.

        :return: 每次迭代返回一个问题对象，获取到的问题对象自带
            标题，关注人数，答案数量三个属性
        :rtype: Question.Iterable
        """
        from .question import Question

        if self.url is None or self.question_num == 0:
            return
        for page_index in range(1, (self.question_num - 1) // 20 + 2):
            html = self._session.get(
                self.url + 'asks?page=' + str(page_index)).text
            soup = BeautifulSoup(html)
            question_links = soup.find_all('a', class_='question_link')
            question_datas = soup.find_all(
                'div', class_='zm-profile-section-main')
            for link, data in zip(question_links, question_datas):
                url = Zhihu_URL + link['href']
                title = link.text
                answer_num = int(
                    re_get_number.match(data.div.contents[4]).group(1))
                follower_num = int(
                    re_get_number.match(data.div.contents[6]).group(1))
                q = Question(self._session, url, title, follower_num,
                             answer_num)
                yield q

    @property
    def answers(self):
        """获取此人写的所有答案对象，返回生成器.

        :return: 此人的所有答案，能直接获取所在问题，答主，赞同数三个属性。
            其中所在问题对象可以直接获取标题。答主对象即为此对象本身。
        :rtype: Answer.Iterable
        """
        from .question import Question
        from .answer import Answer

        if self.url is None or self.answer_num == 0:
            return
        for page_index in range(1, (self.answer_num - 1) // 20 + 2):
            html = self._session.get(
                self.url + 'answers?page=' + str(page_index)).text
            soup = BeautifulSoup(html)
            questions = soup.find_all('a', class_='question_link')
            upvotes = soup.find_all('a', class_='zm-item-vote-count')
            for q, upvote in zip(questions, upvotes):
                answer_url = Zhihu_URL + q['href']
                question_url = Zhihu_URL + re_a2q.match(q['href']).group(1)
                question_title = q.text
                upvote = int(upvote['data-votecount'])
                question = Question(self._session, question_url,
                                    question_title)
                yield Answer(self._session, answer_url, question, self, upvote)

    @property
    def followers(self):
        """获取此关注此用户的人.

        :return: 关注此用户的人的生成器
        :rtype: Author.Iterable
        """
        for x in self._follow_ee_ers('er'):
            yield x

    @property
    def followees(self):
        """获取此用户关注的人.

        :return: 用户关注的人的生成器
        :rtype: Author.Iterable
        """
        for x in self._follow_ee_ers('ee'):
            yield x

    def _follow_ee_ers(self, t):
        if self.url is None:
            return
        if t == 'er':
            all_number = self.follower_num
            request_url = Get_More_Followers_URL
        else:
            all_number = self.followee_num
            request_url = Get_More_Followees_URL
        if all_number == 0:
            return
        params = {"order_by": "created", "offset": 0, "hash_id": self._hash_id}
        data = {'_xsrf': self._xsrf, 'method': 'next', 'params': ''}
        for i in range(0, all_number, 20):
            params['offset'] = i
            data['params'] = json.dumps(params)
            res = self._session.post(request_url, data=data)
            for html in res.json()['msg']:
                soup = BeautifulSoup(html)
                h2 = soup.find('h2')
                author_name = h2.a.text
                author_url = h2.a['href']
                author_motto = soup.find('div', class_='zg-big-gray').text
                author_photo = soup.a.img['src'].replace('_m', '_r')
                numbers = [int(re_get_number.match(x.text).group(1))
                           for x in soup.find_all('a', target='_blank')]
                yield Author(self._session, author_url, author_name,
                             author_motto, *numbers, thank_num=None,
                             photo_url=author_photo)

    @property
    def collections(self):
        """获取此人收藏夹对象集合，返回生成器.

        :return: 此人所有的收藏夹， 能直接获取拥有者，收藏夹名字，关注人数三个属性。
            其中拥有者即为此对象本身。
        :rtype: Collection.Iterable
        """
        from .collection import Collection

        if self.url is None or self.collection_num == 0:
            return
        else:
            collection_num = self.collection_num
            for page_index in range(1, (collection_num - 1) // 20 + 2):
                html = self._session.get(
                    self.url + 'collections?page=' + str(page_index)).text
                soup = BeautifulSoup(html)
                collections_names = soup.find_all(
                    'a', class_='zm-profile-fav-item-title')
                collection_follower_nums = soup.find_all(
                    'div', class_='zm-profile-fav-bio')
                for c, f in zip(collections_names, collection_follower_nums):
                    c_url = Zhihu_URL + c['href']
                    c_name = c.text
                    c_fn = int(re_get_number.match(f.contents[2]).group(1))
                    yield Collection(self._session, c_url, self, c_name, c_fn)

    @property
    def columns(self):
        """获取此人专栏，返回生成器.

        :return: 此人所有的专栏，能直接获取拥有者，名字，网址，文章数，关注人数。
        :rtype: Column.Iterable
        """
        from .column import Column

        if self.url is None or self.post_num == 0:
            return
        soup = BeautifulSoup(self._session.get(self.url + 'posts').text)
        column_tags = soup.find_all('div', class_='column')
        for column_tag in column_tags:
            name = column_tag.div.a.span.text
            url = column_tag.div.a['href']
            follower_num = int(re_get_number.match(
                column_tag.div.div.a.text).group(1))
            footer = column_tag.find('div', class_='footer')
            if footer is None:
                post_num = 0
            else:
                post_num = int(
                    re_get_number.match(footer.a.text).group(1))
            yield Column(self._session, url, name, follower_num, post_num)

    @property
    def activities(self):
        """获取用户的最近动态.

        :return: 最近动态生成器，根据不同的动态类型提供不同的成员
        :rtype: Activity.Iterable
        """
        from .activity import Activity
        from .acttype import ActType
        from .question import Question
        from .answer import Answer
        from .column import Column
        from .post import Post
        from .topic import Topic

        if self.url is None:
            return
        self._make_soup()
        gotten_feed_num = 20
        start = '0'
        while gotten_feed_num == 20:
            data = {'_xsrf': self._xsrf, 'start': start}
            res = self._session.post(self.url + 'activities', data=data)
            gotten_feed_num = res.json()['msg'][0]
            soup = BeautifulSoup(res.json()['msg'][1])
            acts = soup.find_all(
                'div', class_='zm-profile-section-item zm-item clearfix')
            start = acts[-1]['data-time'] if len(acts) > 0 else 0
            for act in acts:
                act_time = datetime.datetime.fromtimestamp(
                    int(act['data-time']))
                useless_tag = act.div.find('a', class_='zg-link')
                if useless_tag is not None:
                    useless_tag.extract()
                type_string = next(act.div.stripped_strings)
                if type_string in ['赞同了', '在']:    # 赞同文章 or 发表文章
                    act_type = ActType.UPVOTE_POST \
                        if type_string == '赞同了' else ActType.PUBLISH_POST

                    column_url = act.find('a', class_='column_link')['href']
                    column_name = act.find('a', class_='column_link').text
                    column = Column(self._session, column_url, column_name)
                    try:
                        author_tag = act.find('div', class_='author-info')
                        author_url = Zhihu_URL + author_tag.a['href']
                        author_info = list(author_tag.stripped_strings)
                        author_name = author_info[0]
                        author_motto = author_info[1] \
                            if len(author_info) > 1 else ''
                        photo_tag = act.div.a.img
                        photo_url = photo_tag['src'].replace('_s', '_r') \
                            if photo_tag is not None else None
                    except TypeError:
                        author_url = None
                        author_name = '匿名用户'
                        author_motto = ''
                        photo_url = None
                    author = Author(self._session, author_url, author_name,
                                    author_motto, photo_url=photo_url)
                    post_url = act.find('a', class_='post-link')['href']
                    post_title = act.find('a', class_='post-link').text
                    post_comment_num, post_upvote_num = self._parse_un_cn(act)
                    post = Post(self._session, post_url, column, author,
                                post_title, post_upvote_num, post_comment_num)

                    yield Activity(act_type, act_time, post=post)
                elif type_string == '关注了专栏':
                    act_type = ActType.FOLLOW_COLUMN
                    column = Column(self._session, act.div.a['href'],
                                    act.div.a.text)
                    yield Activity(act_type, act_time, column=column)
                elif type_string == '关注了问题':
                    act_type = ActType.FOLLOW_QUESTION
                    question = Question(self._session,
                                        Zhihu_URL + act.div.a['href'],
                                        act.div.a.text)
                    yield Activity(act_type, act_time, question=question)
                elif type_string == '提了一个问题':
                    act_type = ActType.ASK_QUESTION
                    question = Question(self._session,
                                        Zhihu_URL +
                                        act.div.contents[3]['href'],
                                        list(act.div.children)[3].text)
                    yield Activity(act_type, act_time, question=question)
                elif type_string == '赞同了回答':
                    act_type = ActType.UPVOTE_ANSWER
                    question_url = Zhihu_URL + re_a2q.match(
                        act.div.a['href']).group(1)
                    question_title = act.div.a.text
                    question = Question(self._session, question_url,
                                        question_title)

                    try_find_author = act.find('h3').find_all(
                        'a', href=re.compile('^/people/[^/]*$'))
                    if len(try_find_author) == 0:
                        author_url = None
                        author_name = '匿名用户'
                        author_motto = ''
                        photo_url = None
                    else:
                        try_find_author = try_find_author[-1]
                        author_url = Zhihu_URL + try_find_author['href']
                        author_name = try_find_author.text
                        try_find_motto = try_find_author.parent.strong
                        if try_find_motto is None:
                            author_motto = ''
                        else:
                            author_motto = try_find_motto['title']
                        photo_url = try_find_author.parent.a.img['src']\
                            .replace('_s', '_r')
                    author = Author(self._session, author_url, author_name,
                                    author_motto, photo_url=photo_url)

                    answer_url = Zhihu_URL + act.div.a['href']
                    answer_comment_num, answer_upvote_num = \
                        self._parse_un_cn(act)
                    answer = Answer(self._session, answer_url, question,
                                    author, answer_upvote_num)

                    yield Activity(act_type, act_time, answer=answer)
                elif type_string == '回答了问题':
                    act_type = ActType.ANSWER_QUESTION
                    question_url = Zhihu_URL + re_a2q.match(
                        act.div.find_all('a')[-1]['href']).group(1)
                    question_title = act.div.find_all('a')[-1].text
                    question = Question(self._session, question_url,
                                        question_title)

                    answer_url = Zhihu_URL + \
                        act.div.find_all('a')[-1]['href']
                    answer_comment_num, answer_upvote_num = \
                        self._parse_un_cn(act)
                    answer = Answer(self._session, answer_url, question, self,
                                    answer_upvote_num)

                    yield Activity(act_type, act_time, answer=answer)
                elif type_string == '关注了话题':
                    act_type = ActType.FOLLOW_TOPIC
                    topic_url = Zhihu_URL + act.div.a['href']
                    topic_name = act.div.a['title']

                    yield Activity(self._session, act_type, act_time,
                                   topic=Topic(topic_url, topic_name))

    def is_zero_user(self):
        """返回当前用户是否为三零用户，其实是四零，分别为： 赞同0，感谢0，提问0，回答0.

        :return: 是否是三零用户
        :rtype: bool
        """
        return self.upvote_num + self.thank_num + \
            self.question_num + self.answer_num == 0

    @staticmethod
    def _parse_un_cn(act):
        upvote_num = int(act.find(
            'a', class_='zm-item-vote-count')['data-votecount'])
        comment = act.find('a', class_='toggle-comment')
        comment_text = next(comment.stripped_strings)
        comment_num_match = re_get_number.match(comment_text)
        comment_num = int(comment_num_match.group(1)) \
            if comment_num_match is not None else 0
        return comment_num, upvote_num
