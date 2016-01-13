#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from .common import *
from .base import BaseZhihu
from .collection import Collection
from .author import Author


class Answer(BaseZhihu):
    """答案类，请使用``ZhihuClient.answer``方法构造对象."""

    @class_common_init(re_ans_url)
    def __init__(self, url, question=None, author=None,
                 upvote_num=None, content=None, session=None):
        """创建答案类实例.

        :param str url: 答案url
        :param Question question: 答案所在的问题对象，可选
        :param Author author: 答案回答者对象，可选
        :param int upvote_num: 答案赞同数量，可选
        :param str content: 答案内容，可选
        :param Session session: 使用的网络会话，为空则使用新会话
        :return: 答案对象
        :rtype: Answer
        """
        self.url = url
        self._session = session
        self._question = question
        self._author = author
        self._upvote_num = upvote_num
        self._content = content
        self._deleted = None

    @property
    def id(self):
        """答案的id

        :return: 答案id
        :rtype: int
        """
        return int(re.match(r'.*/(\d+)/$', self.url).group(1))

    @property
    @check_soup('_xsrf')
    def xsrf(self):
        """获取知乎的反xsrf参数（用不到就忽视吧~）

        :return: xsrf参数
        :rtype: str
        """
        return self.soup.find('input', attrs={'name': '_xsrf'})['value']

    @property
    @check_soup('_aid')
    def aid(self):
        """获取答案的内部id，某些POST操作需要此参数

        :return: 答案内部id
        :rtype: str
        """
        return int(self.soup.find('div', class_='zm-item-answer')['data-aid'])

    @property
    @check_soup('_html')
    def html(self):
        """获取网页源码

        :return: 网页源码
        :rtype: str
        """
        return self.soup.prettify()

    @property
    @check_soup('_author')
    def author(self):
        """获取答案作者.

        :return: 答案作者
        :rtype: Author
        """
        from .author import Author

        author = self.soup.find('div', class_='zm-item-answer-author-info')
        url, name, motto, photo = parser_author_from_tag(author)
        return Author(url, name, motto, photo_url=photo, session=self._session)

    @property
    @check_soup('_question')
    def question(self):
        """获取答案所在问题.

        :return: 答案所在问题
        :rtype: Question
        """
        from .question import Question

        question_link = self.soup.find(
            "h2", class_="zm-item-title zm-editable-content").a
        url = Zhihu_URL + question_link["href"]
        title = question_link.text
        followers_num = int(self.soup.find(
            'div', class_='zh-question-followers-sidebar').div.a.strong.text)
        answers_num = int(re_get_number.match(self.soup.find(
            'div', class_='zh-answers-title').h3.a.text).group(1))
        return Question(url, title, followers_num, answers_num,
                        session=self._session)

    @property
    @check_soup('_upvote_num')
    def upvote_num(self):
        """获取答案赞同数量.

        :return: 答案赞同数量
        :rtype: int
        """
        return int(self.soup.find(
            'div', class_='zm-item-vote-info')['data-votecount'])

    @property
    def upvoters(self):
        """获取答案点赞用户，返回生成器.

        :return: 点赞用户
        :rtype: Author.Iterable
        """
        self._make_soup()
        next_req = '/answer/' + str(self.aid) + '/voters_profile'
        while next_req != '':
            data = self._session.get(Zhihu_URL + next_req).json()
            next_req = data['paging']['next']
            for html in data['payload']:
                soup = BeautifulSoup(html)
                yield self._parse_author_soup(soup)

    @property
    @check_soup('_content')
    def content(self):
        """以处理过的Html代码形式返回答案内容.

        :return: 答案内容
        :rtype: str
        """
        answer_wrap = self.soup.find('div', id='zh-question-answer-wrap')
        content = answer_wrap.find('div', class_='zm-editable-content')
        content = answer_content_process(content)
        return content

    @property
    @check_soup('_creation_time')
    def creation_time(self):
        """获取答案创建时间

        :return: 答案创建时间
        :rtype: datetime.datetime
        """
        return datetime.fromtimestamp(int(self.soup.find(
                'div', class_='zm-item-answer')['data-created']))

    @property
    @check_soup('_collect_num')
    def collect_num(self):
        """获取答案收藏数

        :return:  答案收藏数量
        :rtype: int
        """
        element = self.soup.find("a", {
            "data-za-a": "click_answer_collected_count"
        })
        if element is None:
            return 0
        else:
            return int(element.get_text())

    @property
    def collections(self):
        """获取包含该答案的收藏夹

        :return: 包含该答案的收藏夹
        :rtype: Collection.Iterable

        collect_num 未必等于 len(collections)，比如:
        https://www.zhihu.com/question/20064699/answer/13855720
        显示被收藏 38 次，但只有 30 个收藏夹
        """
        import time
        gotten_feed_num = 20
        offset = 0
        data = {
            'method':'next',
            '_xsrf': self.xsrf
        }
        while gotten_feed_num >= 10:
            data['params'] = "{\"answer_url\": %d,\"offset\": %d}" % (self.id, offset)
            res = self._session.post(url=Get_Collection_Url, data=data)
            gotten_feed_num = len(res.json()['msg'])
            offset += gotten_feed_num
            soup = BeautifulSoup(''.join(res.json()['msg']))
            for zm_item in soup.find_all('div', class_='zm-item'):
                url = Zhihu_URL + zm_item.h2.a['href']
                name = zm_item.h2.a.text
                links = zm_item.div.find_all('a')
                owner = Author(links[0]['href'], session=self._session)
                follower_num = int(links[1].text.split()[0])
                yield Collection(url, owner=owner, name=name,
                                 follower_num=follower_num,
                                 session=self._session)

            time.sleep(0.2)  # prevent from posting too quickly

    def save(self, filepath=None, filename=None, mode="html"):
        """保存答案为Html文档或markdown文档.

        :param str filepath: 要保存的文件所在的目录，
            不填为当前目录下以问题标题命名的目录, 设为"."则为当前目录。
        :param str filename: 要保存的文件名，
            不填则默认为 所在问题标题 - 答主名.html/md。
            如果文件已存在，自动在后面加上数字区分。
            **自定义文件名时请不要输入后缀 .html 或 .md。**
        :param str mode: 保存类型，可选 `html` 、 `markdown` 、 `md` 。
        :return: 无
        :rtype: None
        """
        if mode not in ["html", "md", "markdown"]:
            raise ValueError("`mode` must be 'html', 'markdown' or 'md',"
                             " got {0}".format(mode))
        file = get_path(filepath, filename, mode, self.question.title,
                        self.question.title + '-' + self.author.name)
        with open(file, 'wb') as f:
            if mode == "html":
                f.write(self.content.encode('utf-8'))
            else:
                import html2text
                h2t = html2text.HTML2Text()
                h2t.body_width = 0
                f.write(h2t.handle(self.content).encode('utf-8'))

    def _parse_author_soup(self, soup):
        from .author import Author

        author_tag = soup.find('div', class_='body')
        if author_tag.string is None:
            author_name = author_tag.div.a['title']
            author_url = author_tag.div.a['href']
            author_motto = author_tag.div.span.text
            photo_url = PROTOCOL + soup.a.img['src'].replace('_m', '_r')
            numbers_tag = soup.find_all('li')
            numbers = [int(re_get_number.match(x.get_text()).group(1))
                       for x in numbers_tag]
        else:
            author_url = None
            author_name = '匿名用户'
            author_motto = ''
            numbers = [None] * 4
            photo_url = None
        # noinspection PyTypeChecker
        return Author(author_url, author_name, author_motto, None,
                      numbers[2], numbers[3], numbers[0], numbers[1],
                      photo_url, session=self._session)

    @property
    @check_soup('_comment_num')
    def comment_num(self):
        """
        :return: 答案下评论的数量
        :rtype: int
        """
        comment_num_string = self.soup.find('a', class_=' meta-item toggle-comment').text
        number = comment_num_string.split()[0]
        return int(number) if number.isdigit() else 0

    @property
    def comments(self):
        """获取答案下的所有评论.

        :return: 答案下的所有评论，返回生成器
        :rtype: Comments.Iterable
        """
        from .author import Author
        from .comment import Comment
        r = self._session.get(Answer_Comment_Box_URL,
                              params='params='+json.dumps({'answer_id': self.aid, 'load_all': True}))
        soup = BeautifulSoup(r.content)
        comment_items = soup.find_all('div', class_='zm-item-comment')
        for comment_item in comment_items:
            comment_id = int(comment_item['data-id'])
            content = comment_item.find(
                'div', class_='zm-comment-content').text.replace('\n', '')
            upvote_num = int(comment_item.find('span', class_='like-num').em.text)
            time_string = comment_item.find('span', class_='date').text
            a_url, a_name, a_photo_url = parser_author_from_comment(comment_item)
            author_obj = Author(a_url, a_name, photo_url=a_photo_url,
                                session=self._session)
            yield Comment(comment_id, self, author_obj, upvote_num, content, time_string)

    def refresh(self):
        """刷新 Answer object 的属性. 
        例如赞同数增加了, 先调用 ``refresh()`` 
        再访问 upvote_num属性, 可获得更新后的赞同数.
        
        :return: None
        """
        super().refresh()
        self._html = None
        self._upvote_num = None
        self._content = None
        self._collect_num = None
        self._comment_num = None

    @property
    @check_soup('_deleted')
    def deleted(self):
        """答案是否被删除, 被删除了返回 True, 为被删除返回 False
        :return: True or False
        """
        return self._deleted