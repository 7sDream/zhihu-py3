#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

from .common import *


class Answer:
    """答案类，用一个答案的网址作为参数构造对象，其他参数可选."""

    def __init__(self, session, url, question=None, author=None,
                 upvote_num=None,
                 content=None):
        """类对象初始化.

        :param str url: 答案网址，形如
            http://www.zhihu.com/question/28297599/answer/40327808
        :param Question question: 答案所在的问题对象，自己构造对象不需要此参数
        :param Author author: 答案的回答者对象，同上。
        :param int upvote_num: 此答案的赞同数量，同上。
        :param str content: 此答案内容，同上。
        :return: 答案对象。
        :rtype: Answer
        """
        if re_ans_url.match(url) is None:
            raise ValueError('URL invalid')
        if url.endswith('/') is False:
            url += '/'
        self.url = url
        self._session = session
        self.soup = None
        self._question = question
        self._author = author
        self._upvote_num = upvote_num
        self._content = content

    def _make_soup(self):
        if self.soup is None:
            r = self._session.get(self.url)
            self.soup = BeautifulSoup(r.content)
            self._aid = self.soup.find(
                'div', class_='zm-item-answer')['data-aid']

    @property
    @check_soup('_html')
    def html(self):
        """获取网页html源码……话说我写这个属性是为了干啥来着.

        :return: 网页源码
        :rtype: str
        """
        return self.soup.prettify()

    @property
    @check_soup('_author')
    def author(self):
        """获取答案作者对象.

        :return: 答案作者对象
        :rtype: Author
        """
        from .author import Author

        author = self.soup.find('h3', class_='zm-item-answer-author-wrap')
        url, name, motto, photo = parser_author_from_tag(author)
        return Author(self._session, url, name, motto, photo_url=photo)

    @property
    @check_soup('_question')
    def question(self):
        """获取答案所在问题对象.

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
        return Question(self._session, url, title, followers_num,
                        answers_num)

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
        """获取答案点赞用户，返回迭代器.

        :return: 点赞用户迭代器
        :rtype: Author.Iterable
        """
        from .author import Author

        self._make_soup()
        next_req = '/answer/' + self._aid + '/voters_profile'
        while next_req != '':
            data = self._session.get(Zhihu_URL + next_req).json()
            next_req = data['paging']['next']
            for html in data['payload']:
                soup = BeautifulSoup(html)
                author_tag = soup.find('div', class_='body')
                if author_tag.string is None:
                    author_name = author_tag.div.a['title']
                    author_url = author_tag.div.a['href']
                    author_motto = author_tag.div.span.text
                    photo_url = soup.a.img['src'].replace('_m', '_r')
                    numbers_tag = soup.find_all('li')
                    numbers = [int(re_get_number.match(
                        x.get_text()).group(1)) for x in numbers_tag]
                else:
                    author_url = None
                    author_name = '匿名用户'
                    author_motto = ''
                    numbers = [None] * 4
                    photo_url = None
                # noinspection PyTypeChecker
                yield Author(self._session, author_url, author_name,
                             author_motto, None, numbers[2], numbers[3],
                             numbers[0], numbers[1], photo_url)

    @property
    @check_soup('_content')
    def content(self):
        """返回答案内容，以处理过的Html代码形式.

        :return: 答案内容
        :rtype: str
        """
        content = self.soup.find('div', class_=' zm-editable-content clearfix')
        content = answer_content_process(content)
        return content

    def save(self, filepath=None, filename=None, mode="html"):
        """保存答案为Html文档或markdown文档.

        :param str filepath: 要保存的文件所在的绝对目录或相对目录，
            不填为当前目录下以问题标题命名的目录, 设为"."则为当前目录
        :param str filename: 要保存的文件名，
            不填则默认为 所在问题标题 - 答主名.html/md
            如果文件已存在，自动在后面加上数字区分。
            自定义文件名时请不要输入后缀 .html 或 .md
        :return: None
        :rtype: None
        """
        if mode not in ["html", "md", "markdown"]:
            return
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

    @property
    def id(self):
        """答案的ID，也就是网址最后的那串数字.

        :return: 答案ID
        :rtype: int
        """
        print(self.url)
        return int(re.match(r'.*/(\d+)/$', self.url).group(1))
