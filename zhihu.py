#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import time
import re
import os
import json
import functools

import requests
from bs4 import BeautifulSoup


# Setting

_Zhihu_URL = 'http://www.zhihu.com'
_Login_URL = _Zhihu_URL + '/login'
_Captcha_URL_Prefix = _Zhihu_URL + '/captcha.gif?r='
_Cookies_File_Name = 'cookies.json'
_Get_More_Answer_URL = 'http://www.zhihu.com/node/QuestionAnswerListV2'

# global var
_session = None
_header = {'X-Requested-With': 'XMLHttpRequest',
           'Referer': 'http://www.zhihu.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; '
                         'Trident/7.0; Touch; LCJB; rv:11.0)'
                         ' like Gecko',
           'Host': 'www.zhihu.com'}

_re_question_url = re.compile(r'http://www\.zhihu\.com/question/\d+/?')
_re_ans_url = re.compile(
    r'http://www\.zhihu\.com/question/\d+/answer/\d+/?')
_re_author_url = re.compile(r'http://www\.zhihu\.com/people/.*/?')
_re_collection_url = re.compile(r'http://www\.zhihu\.com/collection/\d+/?')
_re_a2q = re.compile(r'(.*)/a.*')
_re_collection_url_split = re.compile(r'.*(/c.*)')
_re_get_number = re.compile(r'[^\d]*(\d+).*')
_re_del_empty_line = re.compile(r'\n*(.*)\n*')


def _check_soup(attr):
    def real(func):
        @functools.wraps(func)
        def wrapper(self):
            # noinspection PyTypeChecker
            value = getattr(self, attr) if hasattr(self, attr) else None
            if value is None:
                self.make_soup()
                value = func(self)
                setattr(self, attr, value)
                return value
            else:
                return value

        return wrapper

    return real


def _save_captcha(url):
    global _session
    r = _session.get(url)
    with open('code.gif', 'wb') as f:
        f.write(r.content)


def _init():
    global _session
    if _session is None:
        _session = requests.session()
        _session.headers.update(_header)
        if os.path.isfile(_Cookies_File_Name):
            with open(_Cookies_File_Name, 'r') as f:
                cookies_dict = json.load(f)
                _session.cookies.update(cookies_dict)
        else:
            print('no cookies file, this may make something wrong.')
            print('if you will run create_cookies or login next, '
                  'please ignore me.')
            _session.post(_Login_URL, data={})
    else:
        raise Exception('call init func two times')


def get_captcha_url():
    """获取验证码网址

    :return: 验证码网址
    :rtype: str
    """
    return _Captcha_URL_Prefix + str(int(time.time() * 1000))


def login(email='', password='', captcha='', savecookies=True):
    """不使用cookies.json，手动登陆知乎

    :param str email: 邮箱
    :param str password: 密码
    :param str captcha: 验证码
    :param bool savecookies: 是否要储存cookies文件
    :return: 一个二元素元祖 , 第一个元素代表是否成功（0表示成功），
        如果未成功则第二个元素表示失败原因
    :rtype: (int, dict)
    """
    global _session
    global _header
    data = {'email': email, 'password': password,
            'rememberme': 'y', 'captcha': captcha}
    r = _session.post(_Login_URL, data=data)
    j = r.json()
    c = int(j['r'])
    m = j['msg']
    if c == 0 and savecookies is True:
        with open(_Cookies_File_Name, 'w') as f:
            json.dump(_session.cookies.get_dict(), f)
    return c, m


def create_cookies():
    """创建cookies文件, 请跟随提示操作

    :return: None
    :rtype: None
    """
    if os.path.isfile(_Cookies_File_Name) is False:
        email = input('email: ')
        password = input('password: ')
        url = get_captcha_url()
        _save_captcha(url)
        print('please check code.gif for captcha')
        captcha = input('captcha: ')
        code, msg = login(email, password, captcha)

        if code == 0:
            print('cookies file created!')
        else:
            print(msg)
        os.remove('code.gif')
    else:
        print('Please delete [' + _Cookies_File_Name + '] first.')


def remove_invalid_char(text):
    """去除字符串中的无效字符，一般用于保存文件时保证文件名的有效性

    :param str text: 待处理的字符串
    :return: 处理后的字符串
    :rtype: str
    """
    invalid_char_list = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n']
    res = ''
    for char in text:
        if char not in invalid_char_list:
            res += char
    return res


def _parser_author_from_tag(author):
    if author.text == '匿名用户':
        author_name = '匿名用户'
        # noinspection PyTypeChecker
        author_obj = Author(None, author_name, '')
    else:
        author_name = author.contents[3].text
        author_motto = author.strong['title'] \
            if author.strong is not None else ''
        author_url = _Zhihu_URL + author.contents[3]['href']
        author_obj = Author(author_url, author_name, author_motto)
    return author_obj


def _answer_content_process(content):
    del content['class']
    soup = BeautifulSoup(
        '<html><head><meta charset="utf-8"></head><body></body></html>')
    soup.body.append(content)
    no_script_list = soup.find_all("noscript")
    for no_script in no_script_list:
        no_script.extract()
    img_list = soup.find_all(
        "img", class_="origin_image zh-lightbox-thumb lazy")
    for img in img_list:
        new_img = soup.new_tag('img', src=img['data-original'])
        img.replace_with(new_img)
        new_img.insert_after(soup.new_tag('br'))
        if img.previous_sibling is None or img.previous_sibling.name != 'br':
            new_img.insert_before(soup.new_tag('br'))
    useless_list = soup.find_all("i", class_="icon-external")
    for useless in useless_list:
        useless.extract()
    return soup.prettify()


def _text2int(text):
    try:
        return int(text)
    except ValueError:
        if text[-1] == 'K':
            return int(float(text[:-1]) * 1000)
        elif text[-1] == 'W':  # 知乎有没有赞同数用万做单位的回答来着？？先写着吧~
            return int(float(text[:-1]) * 10000)


class Question:
    """问题类，用一个问题的网址来构造对象,其他参数皆为可选"""
    def __init__(self, url, title=None, followers_num=None, answers_num=None):
        """

        :param str url: 问题地址，形如： http://www.zhihu.com/question/27936038
        :param str title: 可选, 问题标题
        :param int followers_num: 可选，问题关注人数
        :param int answers_num: 可选，问题答案数
        :return: Question对象
        :rtype: Question
        """
        global _session
        if _re_question_url.match(url) is None:
            raise Exception('URL invalid')
        else:
            if url.endswith('/') is False:
                url += '/'
            self.soup = None
            self.url = url
            self._title = title
            self._answers_num = answers_num
            self._followers_num = followers_num

    def make_soup(self):
        """**请不要手动调用此方法，当获取需要解析网页的属性时会自动掉用**
        当然你非要调用我也没办法……

        :return: None
        :rtype: None
        """
        if self.soup is None:
            r = _session.get(self.url)
            self.soup = BeautifulSoup(r.content)

    @property
    @_check_soup('_html')
    def html(self):
        """获取页面HTML源码

        :return: html源码
        :rtype: str
        """
        return self.soup.prettify()

    @property
    @_check_soup('_title')
    def title(self):
        """获取问题标题

        :return: title of question
        :rtype: str
        """
        return self.soup.find('h2', class_='zm-item-title') \
            .text.replace('\n', '')

    @property
    @_check_soup('_details')
    def details(self):
        """获取问题详细描述。
        **目前实现方法只是直接获取文本，效果不满意……等更新**

        :return: 问题详细描述文本
        :rtype: str
        """
        return self.soup.find("div", id="zh-question-detail").div.text

    @property
    @_check_soup('_answers_num')
    def answers_num(self):
        """获取问题答案数量

        :return: 答案数量
        :rtype: int
        """
        return _text2int(
            self.soup.find('h3', id='zh-question-answer-num')['data-num'])

    @property
    @_check_soup('_followers_num')
    def followers_num(self):
        """获取问题关注人数

        :return: 问题关注人数
        :rtype: int
        """
        return _text2int(self.soup.find(
            'div', class_='zg-gray-normal').strong.text)

    @property
    @_check_soup('_topics')
    def topics(self):
        """获取问题所属话题

        :return: 问题所属话题列表
        :rtype: list(str)
        """
        topics_list = []
        for topic in self.soup.find_all('a', class_='zm-item-tag'):
            topics_list.append(topic.text.replace('\n', ''))
        return topics_list

    @property
    def answers(self):
        """获取问题的所有答案，返回可迭代生成器

        :return: 每次迭代返回一个Answer对象， 获取到的Answer对象自带所在问题、答主、赞同数量、
            回答内容四个属性。获取其他属性需要解析另外的网页。
        :rtype: Answer.Iterable
        """
        self.make_soup()
        for i in range(0, (self.answers_num - 1) // 50 + 1):
            if i == 0:
                # 修正各种建议修改的回答……
                error_answers = self.soup.find_all('div', id='answer-status')
                for each in error_answers:
                    each['class'] = ' zm-editable-content clearfix'
                # 正式处理
                authors = self.soup.find_all(
                    'h3', class_='zm-item-answer-author-wrap')
                urls = self.soup.find_all('a', class_='answer-date-link')
                upvotes = self.soup.find_all('span', class_='count')
                contents = self.soup.find_all(
                    'div', class_=' zm-editable-content clearfix')
                for author, url, upvote, content in \
                        zip(authors, urls, upvotes, contents):
                    author_obj = _parser_author_from_tag(author)
                    url = _Zhihu_URL + url['href']
                    upvote = _text2int(upvote.text)
                    content = _answer_content_process(content)
                    yield Answer(url, self, author_obj, upvote, content)
            else:
                global _session
                global _header
                _xsrf = self.soup.find(
                    'input', attrs={'name': '_xsrf'})['value']
                new_header = dict(_header)
                new_header['Referer'] = self.url
                params = {"url_token": self.__get_qid(),
                          'pagesize': '50',
                          'offset': i * 50}
                data = {'_xsrf': _xsrf,
                        'method': 'next',
                        'params': json.dumps(params)}
                r = _session.post(_Get_More_Answer_URL, data=data,
                                  headers=_header)
                answer_list = r.json()['msg']
                for answer_html in answer_list:
                    soup = BeautifulSoup(answer_html)
                    # 修正各种建议修改的回答……
                    error_answers = soup.find_all('div', id='answer-status')
                    for each in error_answers:
                        each['class'] = ' zm-editable-content clearfix'
                    answer_url = \
                        self.url + 'answer/' + soup.div['data-atoken']
                    author = soup.find(
                        'h3', class_='zm-item-answer-author-wrap')
                    upvote = _text2int(
                        soup.find('span', class_='count').text)
                    content = soup.find(
                        'div', class_=' zm-editable-content clearfix')
                    content = _answer_content_process(content)
                    author_obj = _parser_author_from_tag(author)
                    yield Answer(answer_url, self, author_obj, upvote, content)

    @property
    def top_answer(self):
        """获取排名第一的答案

        :return: 排名第一的答案对象，能直接获取的属性参见answers方法
        :rtype: Answer
        """
        for a in self.answers:
            return a

    def top_i_answer(self, i):
        """获取排名某一位的答案

        :param int i: 要获取的答案的排名
        :return: 答案对象，能直接获取的属性参见answers方法
        :rtype: Answer
        """
        for j, a in enumerate(self.answers):
            if j == i - 1:
                return a

    def top_i_answers(self, i):
        """获取排名在前几位的答案

        :param int i: 获取高位排名答案数量
        :return: 答案对象生成器，这些对象能直接获取的属性参见answers方法
        :rtype: Answer.iterable
        """
        for j, a in enumerate(self.answers):
            if j <= i - 1:
                yield a

    def __get_qid(self):
        return int(re.match(r'.*/(\d+)', self.url).group(1))


class Author():
    """用户类，用用户主页地址作为参数来构造对象，其他参数可选"""
    def __init__(self, url: str, name: str=None, motto: str=None):
        """

        :param str url: 用户主页地址，形如 http://www.zhihu.com/people/7sdream
        :param str name: 用户名字，可选
        :param str motto: 可选
        :return: Author
        """
        if url is not None:
            if _re_author_url.match(url) is None:
                raise Exception('URL invalid')
            if url.endswith('/') is False:
                url += '/'
        self.url = url
        self.soup = None
        self._nav_list = None
        self._name = name
        self._motto = motto

    def make_soup(self) -> None:
        """**请不要手动调用此方法，当获取需要解析网页的属性时会自动掉用**
        当然你非要调用我也没办法……

        :return: None
        :rtype: None
        """
        if self.soup is None and self.url is not None:
            r = _session.get(self.url)
            self.soup = BeautifulSoup(r.content)
            self._nav_list = self.soup.find(
                'div', class_='profile-navbar clearfix').find_all('a')

    @property
    @_check_soup('_name')
    def name(self):
        """获取用户名字

        :return: 用户名字
        :rtype: str
        """
        if self.url is None:
            return '匿名用户'
        return self.soup.find('div', class_='title-section ellipsis').span.text

    @property
    @_check_soup('_motto')
    def motto(self):
        """获取用户自我介绍？那段话是叫啥……是自我介绍还是签名？？？算了由于历史原因
        我还是把这个属性叫做motto吧……

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
    @_check_soup('_followees_num')
    def followees_num(self):
        """获取追随者数量，就是获取关注此人的人数

        :return: 追随者数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            number = _text2int(
                self.soup.find(
                    'div',
                    class_='zm-profile-side-following zg-clear').a.strong.text)
            return number

    @property
    @_check_soup('_followers_num')
    def followers_num(self):
        """获取关注数量。

        :return: 关注人数
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            number = _text2int(
                self.soup.find(
                    'div', class_='zm-profile-side-following zg-clear')
                .find_all('a')[1].strong.text)
            return number

    @property
    @_check_soup('_agree_num')
    def agree_num(self):
        """获取收到的的赞同数量

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
    @_check_soup('_thanks_num')
    def thanks_num(self):
        """获取收到的感谢数量

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
    @_check_soup('_asks_num')
    def questions_num(self):
        """获取提问数量

        :return: 提问数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[1].span.text)

    @property
    @_check_soup('_answers_num')
    def answers_num(self):
        """获取答案数量

        :return: 答案数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[2].span.text)

    @property
    @_check_soup('_post_num')
    def post_num(self):
        """获取专栏文章数量

        :return: 专栏文章数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[3].span.text)

    @property
    @_check_soup('_collections_num')
    def collections_num(self):
        """获取收藏夹数量

        :return: 收藏夹数量
        :rtype: int
        """
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[4].span.text)

    @property
    def questions(self):
        """获取此人问过的所有问题对象，返回生成器

        :return: 每次迭代返回一个问题对象，获取到的问题对象自带标题，关注人数，答案数量三个属性
        :rtype: Question.Iterable
        """
        if self.url is None or self.questions_num == 0:
            return
        for page_index in range(1, (self.questions_num - 1) // 20 + 2):
            global _session
            html = _session.get(self.url + 'asks?page=' + str(page_index)).text
            soup = BeautifulSoup(html)
            questions_links = soup.find_all('a', class_='question_link')
            question_datas = soup.find_all(
                'div', class_='zm-profile-section-main')
            for link, data in zip(questions_links, question_datas):
                url = _Zhihu_URL + link['href']
                title = link.text
                answers_num = int(
                    _re_get_number.match(data.div.contents[4]).group(1))
                followers_num = int(
                    _re_get_number.match(data.div.contents[6]).group(1))
                q = Question(url, title, followers_num, answers_num)
                yield q

    @property
    def answers(self):
        """获取此人写的所有答案对象，返回生成器

        :return: 此人的所有答案，能直接获取所在问题，答主，赞同数三个属性。
            其中所在问题对象可以直接获取标题。答主对象即为此对象本身。
        :rtype: Answer.iterable
        """
        if self.url is None or self.answers_num == 0:
            return
        self.make_soup()
        for page_index in range(1, (self.answers_num - 1) // 20 + 2):
            global _session
            html = _session.get(
                self.url + 'answers?page=' + str(page_index)).text
            soup = BeautifulSoup(html)
            questions = soup.find_all('a', class_='question_link')
            upvotes = soup.find_all('a', class_='zm-item-vote-count')
            for q, upvote in zip(questions, upvotes):
                answer_url = _Zhihu_URL + q['href']
                question_url = _Zhihu_URL + _re_a2q.match(q['href']).group(1)
                question_title = q.text
                upvote = _text2int(upvote.text)
                yield Answer(answer_url,
                             Question(question_url, question_title),
                             self, upvote)

    @property
    def collections(self):
        """获取此人收藏夹对象集合，返回生成器

        :return: 此人所有的收藏夹， 能直接获取拥有者，收藏夹名字，关注人数三个属性。
            其中拥有者即为此对象本身。
        :rtype: Collection.Iterable
        """
        if self.url is None or self.collections_num == 0:
            return
        else:
            global _session
            collection_num = self.collections_num
            for page_index in range(1, (collection_num - 1) // 20 + 2):
                html = _session.get(
                    self.url + 'collections?page=' + str(page_index)).text
                soup = BeautifulSoup(html)
                collections_names = soup.find_all(
                    'a', class_='zm-profile-fav-item-title')
                collections_followers_nums = soup.find_all(
                    'div', class_='zm-profile-fav-bio')
                for c, f in zip(collections_names, collections_followers_nums):
                    c_url = _Zhihu_URL + c['href']
                    c_name = c.text
                    c_fn = int(_re_get_number.match(f.contents[2]).group(1))
                    yield Collection(c_url, self, c_name, c_fn)


class Answer():
    """答案类，用一个答案的网址作为参数构造对象"""
    def __init__(self, url, question=None, author=None, upvote=None,
                 content=None):
        """

        :param str url: 答案网址，形如
            http://www.zhihu.com/question/28297599/answer/40327808
        :param Question question: 答案所在的问题对象，自己构造对象不需要此参数
        :param Author author: 答案的回答者对象，同上。
        :param int upvote: 此答案的赞同数量，同上。
        :param str content: 此答案内容，同上。
        :return: 答案对象。
        :rtype: Answer
        """
        if _re_ans_url.match(url) is None:
            raise Exception('URL invalid')
        if url.endswith('/') is False:
            url += '/'
        self.url = url
        self.soup = None
        self._question = question
        self._author = author
        self._upvote = upvote
        self._content = content

    def make_soup(self):
        """不要调用！！！不要调用！！！不要调用！！！

        :return: None
        :rtype: None
        """
        if self.soup is None:
            r = _session.get(self.url)
            self.soup = BeautifulSoup(r.content)

    @property
    @_check_soup('_html')
    def html(self):
        """获取网页html源码……话说我写这个属性是为了干啥来着

        :return: 网页源码
        :rtype: str
        """
        return self.soup.prettify()

    @property
    @_check_soup('_author')
    def author(self):
        """获取答案作者对象

        :return: 答案作者对象
        :rtype: Author
        """
        author = self.soup.find('h3', class_='zm-item-answer-author-wrap')
        return _parser_author_from_tag(author)

    @property
    @_check_soup('_question')
    def question(self):
        """获取答案所在问题对象

        :return: 答案所在问题
        :rtype: Question
        """
        question_link = self.soup.find(
            "h2", class_="zm-item-title zm-editable-content").a
        url = _Zhihu_URL + question_link["href"]
        title = question_link.text
        followers_num = _text2int(self.soup.find(
            'div', class_='zh-question-followers-sidebar').div.a.strong.text)
        answers_num = _text2int(_re_get_number.match(self.soup.find(
            'div', class_='zh-answers-title').h3.a.text).group(1))
        return Question(url, title, followers_num, answers_num)

    @property
    @_check_soup('_upvote')
    def upvote(self):
        """获取答案赞同数量

        :return: 答案赞同数量
        :rtype: int
        """
        return _text2int(self.soup.find('span', class_='count').text)

    @property
    @_check_soup('_content')
    def content(self):
        """返回答案内容，以处理过的Html代码形式

        :return: 答案内容
        :rtype: str
        """
        content = self.soup.find('div', class_=' zm-editable-content clearfix')
        content = _answer_content_process(content)
        return content

    def save(self, path=None, filename=None, mode="html"):
        """保存答案为Html文档或markdown文档

        :param str path: 要保存的文件所在的绝对目录或相对目录，不填为当前目录下以问题
            标题命名的目录, 设为"."则为当前目录
        :param str filename: 要保存的文件名，不填则默认为 所在问题标题 - 答主名.html/md
            如果文件已存在，自动在后面加上数字区分。
            自定义文件名时请不要输入后缀 .html 或 .md
        :return: None
        :rtype: None
        """
        if mode not in ["html", "md", "markdown"]:
            return
        if path is None:
            path = os.path.join(
                os.getcwd(), remove_invalid_char(self.question.title))
        if filename is None:
            filename = remove_invalid_char(
                self.question.title + ' - ' + self.author.name)
        if os.path.exists(path) is False:
            os.makedirs(path)
        tempfilepath = os.path.join(path, filename)
        filepath = tempfilepath[:] + '.' + mode
        i = 1
        while os.path.isfile(filepath) is True:
            filepath = tempfilepath + str(i) + '.' + mode
        with open(filepath, 'wb') as f:
            if mode == "html":
                f.write(self.content.encode('utf-8'))
            else:
                import html2text
                X = html2text.HTML2Text()
                X.body_width = 0
                f.write(X.handle(self.content).encode('utf-8'))


class Collection():
    """收藏夹类，用收藏夹主页网址为参数来构造对象
    由于一些原因，没有提供收藏夹答案数量这个属性。"""
    def __init__(self, url, owner=None, name=None, followers_num=None):
        """

        :param str url: 收藏夹主页网址，必须
        :param Author owner: 收藏夹拥有者，可选，最好不要自己设置
        :param str name: 收藏夹标题，可选，可以自己设置
        :param int followers_num: 收藏夹关注人数，可选，可以自己设置
        :return: 收藏夹对象
        :rtype: Collection
        """
        if _re_collection_url.match(url) is None:
            raise Exception('URL invalid')
        else:
            if url.endswith('/') is False:
                url += '/'
            self.url = url
            self.soup = None
            self._name = name
            self._owner = owner
            self._followers_num = followers_num

    def make_soup(self):
        """没用的东西，不要调用。

        :return: None
        :rtype: None
        """
        if self.soup is None:
            global _session
            self.soup = BeautifulSoup(_session.get(self.url).text)

    @property
    @_check_soup('_name')
    def name(self):
        """获取收藏夹名字

        :return: 收藏夹名字
        :rtype: str
        """
        return _re_del_empty_line.match(
            self.soup.find('h2', id='zh-fav-head-title').text).group(1)

    @property
    @_check_soup('_owner')
    def owner(self):
        """获取收藏夹拥有者，返回Author对象

        :return: 收藏夹拥有者
        :rtype: Author
        """
        a = self.soup.find('h2', class_='zm-list-content-title').a
        name = a.text
        url = _Zhihu_URL + a['href']
        motto = self.soup.find(
            'div', id='zh-single-answer-author-info').div.text
        return Author(url, name, motto)

    @property
    @_check_soup('_followers_num')
    def followers_num(self):
        """获取关注此收藏夹的人数

        :return: 关注此收藏夹的人数
        :rtype: int
        """
        href = _re_collection_url_split.match(self.url).group(1)
        return int(self.soup.find('a', href=href + 'followers').text)

    @property
    def questions(self):
        """获取收藏夹内所有问题对象

        :return: 收藏夹内所有问题，以生成器形式返回
        :rtype: Question.Iterable
        """
        self.make_soup()
        # noinspection PyTypeChecker
        for question in self.__page_get_questions(self.soup):
            yield question
        i = 2
        while True:
            global _session
            soup = BeautifulSoup(_session.get(
                self.url[:-1] + '?page=' + str(i)).text)
            for question in self.__page_get_questions(soup):
                if question == 0:
                    return
                yield question
            i += 1

    @property
    def answers(self):
        """获取收藏夹内所有答案对象

        :return: 收藏夹内所有答案，以生成器形式返回
        :rtype: Answer.Iterable
        """
        self.make_soup()
        # noinspection PyTypeChecker
        for answer in self.__page_get_answers(self.soup):
            yield answer
        i = 2
        while True:
            global _session
            soup = BeautifulSoup(_session.get(
                self.url[:-1] + '?page=' + str(i)).text)
            for answer in self.__page_get_answers(soup):
                if answer == 0:
                    return
                yield answer
            i += 1

    @staticmethod
    def __page_get_questions(soup: BeautifulSoup):
        question_tags = soup.find_all("div", class_="zm-item")
        if len(question_tags) == 0:
            yield 0
            return
        else:
            for question_tag in question_tags:
                if question_tag.h2 is not None:
                    question_title = question_tag.h2.a.text
                    question_url = _Zhihu_URL + question_tag.h2.a['href']
                    yield Question(question_url, question_title)

    @staticmethod
    def __page_get_answers(soup: BeautifulSoup):
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
                    question_url = _Zhihu_URL + tag.h2.a['href']
                    question = Question(question_url, question_title)
                answer_url = _Zhihu_URL + url_tag['href']
                h3 = tag.find('h3')
                if h3.text != '匿名用户':
                    author_url = _Zhihu_URL + h3.a['href']
                    author_name = h3.contents[3].text
                    if h3.strong is not None:
                        author_motto = tag.find('h3').strong['title']
                author = Author(author_url, author_name, author_motto)
                upvote = _text2int(tag.find(
                    'a', class_='zm-item-vote-count').text)
                answer = Answer(answer_url, question, author, upvote)
                yield answer


_init()