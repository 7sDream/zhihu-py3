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
_re_get_munber = re.compile(r'[^\d]*(\d+).*')
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


def _init() -> None:
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


def get_captcha_url() -> str:
    """get captcha image url

    :return: captcha url
    :rtype: str
    """
    return _Captcha_URL_Prefix + str(int(time.time() * 1000))


def login(email: str='', password: str='', captcha: str='',
          savecookies: bool=True) -> tuple:
    """login zhihu.com

    :param email: your email
    :param password: your password
    :param captcha: captcha string
    :param savecookies: if you want save cookies file
    :return: a tuple with 2 elements , first show result(0 for success)
        second show the error message if not success
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


def create_cookies() -> None:
    """create cookies file

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


def remove_invalid_char(text) -> str:
    """remove invalid char from given string, usually use while you want save
files.

    :param text: the string you want process
    :return: the string that deleted invalid char
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
    """Qusetion class, init with a url, another param is optianal"""
    def __init__(self, url: str, title: str=None, followers_num: int=None,
                 answers_num: int=None):
        """
        :param url: question url, like http://www.zhihu.com/question/27936038
        :param title: optional, question title
        :param followers_num: optional, question followers number
        :param answers_num: optional, question answers number
        :return: Question object
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

    def make_soup(self) -> None:
        if self.soup is None:
            r = _session.get(self.url)
            self.soup = BeautifulSoup(r.content)

    @property
    @_check_soup('_html')
    def html(self) -> str:
        """get page html

        :return: the html string
        :rtype: str
        """
        return self.soup.prettify()

    @property
    @_check_soup('_title')
    def title(self) -> str:
        """Get title of the question

        :return: title of question
        :rtype: str
        """
        return self.soup.find('h2', class_='zm-item-title') \
            .text.replace('\n', '')

    @property
    @_check_soup('_details')
    def details(self) -> str:
        """Get detailed description of the question

        :return: question detail
        :rtype: str
        """
        return self.soup.find("div", id="zh-question-detail").div.text

    @property
    @_check_soup('_answers_num')
    def answers_num(self) -> int:
        return int(
            self.soup.find('h3', id='zh-question-answer-num')['data-num'])

    @property
    @_check_soup('_followers_num')
    def followers_num(self) -> int:
        return int(self.soup.find('div', class_='zg-gray-normal').strong.text)

    @property
    @_check_soup('_topics')
    def topics(self) -> list:
        topics_list = []
        for topic in self.soup.find_all('a', class_='zm-item-tag'):
            topics_list.append(topic.text.replace('\n', ''))
        return topics_list

    @property
    def answers(self):
        self.__make_soup()
        for i in range(0, (self.answers_num - 1) // 50 + 1):
            if i == 0:
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
        for a in self.answers:
            return a

    def top_i_answer(self, i):
        for j, a in enumerate(self.answers()):
            if j == i - 1:
                return a

    def top_i_answers(self, i):
        for j, a in enumerate(self.answers()):
            if j <= i - 1:
                yield a

    def __get_qid(self):
        return int(re.match(r'.*/(\d+)', self.url).group(1))


class Author():
    def __init__(self, url: str, name: str=None, motto: str=None):
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
        if self.soup is None and self.url is not None:
            r = _session.get(self.url)
            self.soup = BeautifulSoup(r.content)
            self._nav_list = self.soup.find(
                'div', class_='profile-navbar clearfix').find_all('a')

    @property
    @_check_soup('_name')
    def name(self) -> str:
        if self.url is None:
            return '匿名用户'
        return self.soup.find('div', class_='title-section ellipsis').span.text

    @property
    @_check_soup('_motto')
    def motto(self) -> str:
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
    def followees_num(self) -> int:
        if self.url is None:
            return 0
        else:
            number = int(
                self.soup.find(
                    'div',
                    class_='zm-profile-side-following zg-clear').a.strong.text)
            return number

    @property
    @_check_soup('_followers_num')
    def followers_num(self) -> int:
        if self.url is None:
            return 0
        else:
            number = int(
                self.soup.find(
                    'div', class_='zm-profile-side-following zg-clear')
                .find_all('a')[1].strong.text)
            return number

    @property
    @_check_soup('_agree_num')
    def agree_num(self):
        if self.url is None:
            return 0
        else:
            number = int(self.soup.find(
                'span', class_='zm-profile-header-user-agree').strong.text)
            return number

    @property
    @_check_soup('_thanks_num')
    def thanks_num(self):
        if self.url is None:
            return 0
        else:
            number = int(self.soup.find(
                'span', class_='zm-profile-header-user-thanks').strong.text)
            return number

    @property
    @_check_soup('_asks_num')
    def questions_num(self):
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[1].span.text)

    @property
    @_check_soup('_answers_num')
    def answers_num(self):
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[2].span.text)

    @property
    @_check_soup('_post_num')
    def post_num(self):
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[3].span.text)

    @property
    @_check_soup('_collections_num')
    def collections_num(self):
        if self.url is None:
            return 0
        else:
            return int(self._nav_list[4].span.text)

    @property
    def questions(self):
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
                    _re_get_munber.match(data.div.contents[4]).group(1))
                followers_num = int(
                    _re_get_munber.match(data.div.contents[6]).group(1))
                q = Question(url, title, followers_num, answers_num)
                yield q

    @property
    def answers(self):
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
                    c_fn = int(_re_get_munber.match(f.contents[2]).group(1))
                    yield Collection(c_url, self, c_name, c_fn)


class Answer():
    def __init__(self, url: str, question: Question=None, author: Author=None,
                 upvote: int=None, content: str=None):
        if _re_ans_url.match(url) is None:
            raise Exception('URL invalid')
        if url.endswith('/') is False:
            url += '/'
        self.url = url
        self.soup = None
        self._qusetion = question
        self._author = author
        self._upvote = upvote
        self._content = content

    def make_soup(self):
        if self.soup is None:
            r = _session.get(self.url)
            self.soup = BeautifulSoup(r.content)

    @property
    @_check_soup('_html')
    def html(self):
        return self.soup.prettify()

    @property
    @_check_soup('_author')
    def author(self):
        author = self.soup.find('h3', class_='zm-item-answer-author-wrap')
        return _parser_author_from_tag(author)

    @property
    @_check_soup('_qusetion')
    def question(self):
        question_link = self.soup.find(
            "h2", class_="zm-item-title zm-editable-content").a
        url = _Zhihu_URL + question_link["href"]
        title = question_link.text
        followers_num = int(self.soup.find(
            'div', class_='zh-question-followers-sidebar').div.a.strong.text)
        answers_num = int(_re_get_munber.match(self.soup.find(
            'div', class_='zh-answers-title').h3.a.text).group(1))
        return Question(url, title, followers_num, answers_num)

    @property
    @_check_soup('_upvote')
    def upvote(self):
        return int(self.soup.find('span', class_='count').text)

    @property
    @_check_soup('_content')
    def content(self):
        content = self.soup.find('div', class_=' zm-editable-content clearfix')
        content = _answer_content_process(content)
        return content

    def save(self, path=None, filename=None):
        if path is None:
            path = os.path.join(
                os.getcwd(), remove_invalid_char(self.question.title))
        if filename is None:
            filename = remove_invalid_char(
                self.question.title + ' - ' + self.author.name)
        if os.path.exists(path) is False:
            os.makedirs(path)
        tempfilepath = os.path.join(path, filename)
        filepath = tempfilepath[:] + '.html'
        i = 1
        while os.path.isfile(filepath) is True:
            filepath = tempfilepath + str(i) + '.html'
        with open(filepath, 'wb') as f:
            f.write(self.content.encode('utf-8'))


class Collection():
    def __init__(self, url: str, owner: Author=None, name: str=None,
                 followers_num: int=None):
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
        if self.soup is None:
            global _session
            self.soup = BeautifulSoup(_session.get(self.url).text)

    @property
    @_check_soup('_name')
    def name(self):
        return _re_del_empty_line.match(
            self.soup.find('h2', id='zh-fav-head-title').text).group(1)

    @property
    @_check_soup('_owner')
    def owner(self):
        a = self.soup.find('h2', class_='zm-list-content-title').a
        name = a.text
        url = _Zhihu_URL + a['href']
        motto = self.soup.find(
            'div', id='zh-single-answer-author-info').div.text
        return Author(url, name, motto)

    @property
    @_check_soup('_followers_num')
    def followers_num(self):
        href = _re_collection_url_split.match(self.url).group(1)
        return int(self.soup.find('a', href=href + 'followers').text)

    @property
    def questions(self):
        self.make_soup()
        # noinspection PyTypeChecker
        for qusetion in self.__page_get_questions(self.soup):
            yield qusetion
        i = 2
        while True:
            global _session
            soup = BeautifulSoup(_session.get(
                self.url[:-1] + '?page=' + str(i)).text)
            for qusetion in self.__page_get_questions(soup):
                if qusetion == 0:
                    return
                yield qusetion
            i += 1

    @property
    def answers(self):
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
                    qusetion_title = question_tag.h2.a.text
                    question_url = _Zhihu_URL + question_tag.h2.a['href']
                    yield Question(question_url, qusetion_title)

    @staticmethod
    def __page_get_answers(soup: BeautifulSoup):
        answer_tags = soup.find_all("div", class_="zm-item")
        if len(answer_tags) == 0:
            yield 0
            return
        else:
            question = None
            for tag in answer_tags:
                author_name = '匿名用户'
                author_motto = ''
                author_url = None
                if tag.h2 is not None:
                    qusetion_title = tag.h2.a.text
                    question_url = _Zhihu_URL + tag.h2.a['href']
                    question = Question(question_url, qusetion_title)

                answer_url = _Zhihu_URL + tag.find(
                    'a', class_='answer-date-link')['href']
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