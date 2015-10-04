#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

from .common import *


class Answer:
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

    def _make_soup(self):
        if self.soup is None:
            r = self._session.get(self.url)
            self.soup = BeautifulSoup(r.content)

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
        return self.soup.find(
            'input', attrs={'name': '_xsrf'})['value']

    @property
    @check_soup('_aid')
    def aid(self):
        """获取答案的内部id，某些POST操作需要此参数

        :return: 答案内部id
        :rtype: str
        """
        self._make_soup()
        return int(self.soup.find(
            'div', class_='zm-item-answer')['data-aid'])

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

        author = self.soup.find('h3', class_='zm-item-answer-author-wrap')
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
        content = self.soup.find('div', class_='zm-editable-content')
        content = answer_content_process(content)
        return content

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
