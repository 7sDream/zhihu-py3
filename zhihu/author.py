#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from .common import *
from .base import BaseZhihu


class Author(BaseZhihu):

    """用户类，请使用``ZhihuClient.answer``方法构造对象."""

    @class_common_init(re_author_url, True)
    def __init__(self, url, name=None, motto=None, follower_num=None,
                 question_num=None, answer_num=None, upvote_num=None,
                 thank_num=None, photo_url=None, session=None):
        """创建用户类实例.

        :param str url: 用户主页url，形如 http://www.zhihu.com/people/7sdream
        :param str name: 用户名字，可选
        :param str motto: 用户简介，可选
        :param int follower_num: 用户粉丝数，可选
        :param int question_num: 用户提问数，可选
        :param int answer_num: 用户答案数，可选
        :param int upvote_num: 用户获得赞同数，可选
        :param int thank_num: 用户获得感谢数，可选
        :param str photo_url: 用户头像地址，可选
        :param Session session: 使用的网络会话，为空则使用新会话。
        :return: 用户对象
        :rtype: Author
        """
        self.url = url
        self._session = session
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

    def _gen_soup(self, content):
        self.soup = BeautifulSoup(content)
        self._nav_list = self.soup.find(
            'div', class_='profile-navbar').find_all('a')

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
        return re.match(r'^.*/([^/]+)/$', self.url).group(1) if self.url is not None else ''

    @property
    @check_soup('_xsrf')
    def xsrf(self):
        """获取知乎的反xsrf参数（用不到就忽视吧~）

        :return: xsrf参数
        :rtype: str
        """
        self._make_soup()
        return self.soup.find(
            'input', attrs={'name': '_xsrf'})['value']

    @property
    @check_soup('_hash_id')
    def hash_id(self):
        """获取作者的内部hash id（用不到就忽视吧~）

        :return: 用户hash id
        :rtype: str
        """
        div = self.soup.find('div', class_='zm-profile-header-op-btns')
        if div is not None:
            return div.button['data-id']
        else:
            ga = self.soup.find('script', attrs={'data-name': 'ga_vars'})
            return json.loads(ga.text)['user_hash']

    @property
    @check_soup('_name', '_make_card')
    def name(self):
        """获取用户名字.

        :return: 用户名字
        :rtype: str
        """
        if self.url is None:
            return '匿名用户'
        if self.soup is not None:
            return self.soup.find('div', class_='title-section').span.text
        else:
            assert self.card is not None
            return self.card.find('span', class_='name').text

    @property
    @check_soup('_motto', '_make_card')
    def motto(self):
        """获取用户自我介绍，由于历史原因，我还是把这个属性叫做motto吧.

        :return: 用户自我介绍
        :rtype: str
        """
        if self.url is None:
            return ''
        else:
            if self.soup is not None:
                bar = self.soup.find(
                    'div', class_='title-section')
                if len(bar.contents) < 4:
                    return ''
                else:
                    return bar.contents[3].text
            else:
                assert self.card is not None
                motto = self.card.find('div', class_='tagline')
                return motto.text if motto is not None else ''

    @property
    @check_soup('_photo_url', '_make_card')
    def photo_url(self):
        """获取用户头像图片地址.

        :return: 用户头像url
        :rtype: str
        """
        if self.url is not None:
            if self.soup is not None:
                img = 'http:' + self.soup.find(
                    'img', class_='avatar avatar-l')['src']
                return img.replace('_l', '_r')
            else:
                assert(self.card is not None)
                return PROTOCOL + self.card.img['src'].replace('_xs', '_r')
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
    @check_soup('_weibo_url')
    def weibo_url(self):
        """获取用户微博链接.

        :return: 微博链接地址，如没有则返回 ‘unknown’
        :rtype: str
        """
        if self.url is None:
            return None
        else:
            tmp = self.soup.find(
                'a', class_='zm-profile-header-user-weibo')
            return tmp['href'] if tmp is not None else 'unknown'

    @property
    def business(self):
        """用户的行业.

        :return: 用户的行业，如没有则返回 ‘unknown’
        :rtype: str
        """
        return self._find_user_profile('business')

    @property
    def location(self):
        """用户的所在地.

        :return: 用户的所在地，如没有则返回 ‘unknown’
        :rtype: str
        """
        return self._find_user_profile('location')

    @property
    def education(self):
        """用户的教育状况.

        :return: 用户的教育状况，如没有则返回 ‘unknown’
        :rtype: str
        """
        return self._find_user_profile('education')

    def _find_user_profile(self, t):
        self._make_soup()
        if self.url is None:
            return 'unknown'
        else:
            res = self.soup.find(
                'span', class_=t)
            if res and 'title' in res:
                return res['title']
            else:
                return 'unknown'

    @property
    @check_soup('_gender')
    def gender(self):
        """用户的性别.

        :return: 用户的性别（male/female/unknown)
        :rtype: str
        """
        if self.url is None:
            return 'unknown'
        else:
            return 'female' if self.soup.find('i', class_='icon-profile-female') else 'male'

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
    @check_soup('_followed_column_num')
    def followed_column_num(self):
        """获取用户关注的专栏数

        :return: 关注的专栏数
        :rtype: int
        """
        if self.url is not None:
            tag = self.soup.find('div', class_='zm-profile-side-columns')
            if tag is not None:
                return int(re_get_number.match(tag.parent.strong.text).group(1))
        return 0

    @property
    @check_soup('_followed_topic_num')
    def followed_topic_num(self):
        """获取用户关注的话题数

        :return: 关注的话题数
        :rtype: int
        """
        if self.url is not None:
            tag = self.soup.find('div', class_='zm-profile-side-topics')
            if tag is not None:
                return int(re_get_number.match(tag.parent.strong.text).group(1))
        return 0

    @property
    def questions(self):
        """获取用户的所有问题.

        :return: 用户的所有问题，返回生成器.
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
                q = Question(url, title, follower_num, answer_num,
                             session=self._session)
                yield q

    @property
    def answers(self):
        """获取用户的所有答案.

        :return: 用户所有答案，返回生成器.
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
                question = Question(question_url, question_title,
                                    session=self._session)
                yield Answer(answer_url, question, self, upvote,
                             session=self._session)

    @property
    def followers(self):
        """获取关注此用户的人.

        :return: 关注此用户的人，返回生成器
        :rtype: Author.Iterable
        """
        for x in self._follow_ee_ers('er'):
            yield x

    @property
    def followees(self):
        """获取用户关注的人.

        :return: 用户关注的人的，返回生成器
        :rtype: Author.Iterable
        """
        for x in self._follow_ee_ers('ee'):
            yield x

    def _follow_ee_ers(self, t):
        if self.url is None:
            return
        if t == 'er':
            request_url = Author_Get_More_Followers_URL
        else:
            request_url = Author_Get_More_Followees_URL
        self._make_card()
        if self.hash_id is None:
            self._make_soup()
        headers = dict(Default_Header)
        headers['Referer'] = self.url + 'follow' + t + 's'
        params = {"order_by": "created", "offset": 0, "hash_id": self.hash_id}
        data = {'_xsrf': self.xsrf, 'method': 'next', 'params': ''}
        gotten_date_num = 20
        offset = 0
        while gotten_date_num == 20:
            params['offset'] = offset
            data['params'] = json.dumps(params)
            res = self._session.post(request_url, data=data, headers=headers)
            json_data = res.json()
            gotten_date_num = len(json_data['msg'])
            offset += gotten_date_num
            for html in json_data['msg']:
                soup = BeautifulSoup(html)
                h2 = soup.find('h2')
                author_name = h2.a.text
                author_url = h2.a['href']
                author_motto = soup.find('div', class_='zg-big-gray').text
                author_photo = PROTOCOL + soup.a.img['src'].replace('_m', '_r')
                numbers = [int(re_get_number.match(x.text).group(1))
                           for x in soup.find_all('a', target='_blank')]
                yield Author(author_url, author_name, author_motto, *numbers,
                             photo_url=author_photo, session=self._session)

    @property
    def collections(self):
        """获取用户收藏夹.

        :return: 用户收藏夹，返回生成器
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
                    yield Collection(c_url, self, c_name, c_fn,
                                     session=self._session)

    @property
    def columns(self):
        """获取用户专栏.

        :return: 用户专栏，返回生成器
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
            yield Column(url, name, follower_num, post_num,
                         session=self._session)

    @property
    def followed_columns(self):
        """获取用户关注的专栏.

        :return: 用户关注的专栏，返回生成器
        :rtype: Column.Iterable
        """
        from .column import Column
        if self.url is None:
            return
        if self.followed_column_num > 0:
            tag = self.soup.find('div', class_='zm-profile-side-columns')
            if tag is not None:
                for a in tag.find_all('a'):
                    yield Column(a['href'], a.img['alt'], session=self._session)
            if self.followed_column_num > 7:
                offset = 7
                gotten_data_num = 20
                while gotten_data_num == 20:
                    params = {'hash_id': self.hash_id, 'limit': 20, 'offset': offset}
                    data = {'method': 'next', '_xsrf': self.xsrf, 'params': json.dumps(params)}
                    j = self._session.post(Author_Get_More_Follow_Column_URL, data=data).json()
                    gotten_data_num = len(j['msg'])
                    offset += gotten_data_num
                    for msg in map(BeautifulSoup, j['msg']):
                        name = msg.strong.text
                        url = msg.a['href']
                        post_num = int(re_get_number.match(msg.span.text).group(1))
                        yield Column(url, name, post_num=post_num, session=self._session)

    @property
    def followed_topics(self):
        """获取用户关注的话题.

        :return: 用户关注的话题，返回生成器
        :rtype: Topic.Iterable
        """
        from .topic import Topic
        if self.url is None:
            return
        if self.followed_topic_num > 0:
            tag = self.soup.find('div', class_='zm-profile-side-topics')
            if tag is not None:
                for a in tag.find_all('a'):
                    yield Topic(Zhihu_URL + a['href'], a.img['title'], session=self._session)
            if self.followed_topic_num > 7:
                offset = 7
                gotten_data_num = 20
                while gotten_data_num == 20:
                    data = {'start': 0, 'offset': offset, '_xsrf': self.xsrf}
                    j = self._session.post(Author_Get_More_Follow_Topic_URL.format(self.id), data=data).json()
                    gotten_data_num = j['msg'][0]
                    offset += gotten_data_num
                    for div in BeautifulSoup(j['msg'][1]).find_all('div', class_='zm-profile-section-item'):
                        name = div.strong.text
                        url = Zhihu_URL + div.a['href']
                        yield Topic(url, name, session=self._session)

    @property
    def activities(self):
        """获取用户的最近动态.

        :return: 最近动态，返回生成器，具体说明见 :class:`.Activity`
        :rtype: Activity.Iterable
        """
        from .activity import Activity

        if self.url is None:
            return
        self._make_soup()
        gotten_feed_num = 20
        start = '0'
        api_url = self.url + 'activities'
        while gotten_feed_num == 20:
            data = {'_xsrf': self.xsrf, 'start': start}
            res = self._session.post(api_url, data=data)
            gotten_feed_num = res.json()['msg'][0]
            soup = BeautifulSoup(res.json()['msg'][1])
            acts = soup.find_all('div', class_='zm-profile-section-item zm-item clearfix')

            start = acts[-1]['data-time'] if len(acts) > 0 else 0
            for act in acts:
                # --- ignore Round Table temporarily ---
                if act.attrs['data-type-detail'] == "member_follow_roundtable":
                    continue
                # --- --- --- --- -- --- --- --- --- ---
                yield Activity(act, self._session, self)

    @property
    def last_activity_time(self):
        """获取用户最后一次活动的时间

        :return: 用户最后一次活动的时间，返回值为 unix 时间戳
        :rtype: int
        """
        self._make_soup()
        act = self.soup.find(
            'div', class_='zm-profile-section-item zm-item clearfix')
        return int(act['data-time']) if act is not None else -1

    def is_zero_user(self):
        """返回当前用户是否为三零用户，其实是四零： 赞同0，感谢0，提问0，回答0.

        :return: 是否是三零用户
        :rtype: bool
        """
        return self.upvote_num + self.thank_num + \
            self.question_num + self.answer_num == 0
