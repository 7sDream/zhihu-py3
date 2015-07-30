#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import functools
import re
import os

import requests
from bs4 import BeautifulSoup as _Bs

try:
    __import__('lxml')
    BeautifulSoup = lambda makeup: _Bs(makeup, 'lxml')
except ImportError:
    BeautifulSoup = lambda makeup: _Bs(makeup, 'html.parser')

Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}

Zhihu_URL = 'http://www.zhihu.com'
Login_URL = Zhihu_URL + '/login/email'
Captcha_URL_Prefix = Zhihu_URL + '/captcha.gif?r='
Get_Profile_Card_URL = 'http://www.zhihu.com/node/MemberProfileCardV2'
Get_More_Answer_URL = 'http://www.zhihu.com/node/QuestionAnswerListV2'
Get_More_Followers_URL = 'http://www.zhihu.com/node/ProfileFollowersListV2'
Get_More_Followees_URL = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
Cookies_File_Name = 'cookies.json'

Columns_Prefix = 'http://zhuanlan.zhihu.com'
Columns_Data = Columns_Prefix + '/api/columns/{0}'
Columns_Posts_Data = Columns_Prefix + \
    '/api/columns/{0}/posts?limit=10&offset={1}'
Columns_Post_Data = Columns_Prefix + '/api/columns/{0}/posts/{1}'

re_question_url = re.compile(r'^http://www\.zhihu\.com/question/\d+/?$')
re_ans_url = re.compile(
    r'^http://www\.zhihu\.com/question/\d+/answer/\d+/?$')
re_author_url = re.compile(r'^http://www\.zhihu\.com/people/[^/]+/?$')
re_collection_url = re.compile(r'^http://www\.zhihu\.com/collection/\d+/?$')
re_column_url = re.compile(r'^http://zhuanlan\.zhihu\.com/([^/]+)/?$')
re_post_url = re.compile(r'^http://zhuanlan\.zhihu\.com/([^/]+)/(\d+)/?$')
re_topic_url = re.compile(r'^http://www\.zhihu\.com/topic/(\d+)/?$')
re_a2q = re.compile(r'(.*)/a.*')
re_collection_url_split = re.compile(r'.*(/c.*)')
re_get_number = re.compile(r'[^\d]*(\d+).*')
re_del_empty_line = re.compile(r'\n*(.*)\n*')


def check_soup(attr, soup_type='_make_soup'):
    def real(func):
        @functools.wraps(func)
        def wrapper(self):
            # noinspection PyTypeChecker
            value = getattr(self, attr) if hasattr(self, attr) else None
            if value is None:
                if soup_type == '_make_soup':
                    getattr(self, soup_type)()
                elif self.soup is None:
                    getattr(self, soup_type)()
                value = func(self)
                setattr(self, attr, value)
                return value
            else:
                return value
        return wrapper
    return real


def class_common_init(url_re):
    def real(func):
        @functools.wraps(func)
        def wrapper(self, url, *args, **kwargs):
            if url is not None:
                if url_re.match(url) is None:
                    raise ValueError('Invalid URL')
                if url.endswith('/') is False:
                    url += '/'
            if 'session' not in kwargs.keys() or kwargs['session'] is None:
                kwargs['session'] = requests.Session()
            self.soup = None
            return func(self, url, *args, **kwargs)
        return wrapper
    return real


def remove_invalid_char(text):
    """去除字符串中的无效字符，一般用于保存文件时保证文件名的有效性.

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


def parser_author_from_tag(author):
    if author.text == '匿名用户':
        return None, '匿名用户', '', ''
    else:
        author_name = author.contents[3].text
        author_motto = author.strong['title'] \
            if author.strong is not None else ''
        author_url = Zhihu_URL + author.contents[3]['href']
        photo_url = author.a.img['src'].replace('_s', '_r')
        return author_url, author_name, author_motto, photo_url


def answer_content_process(content):
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


def get_path(path, filename, mode, default_path, default_name):
    if path is None:
        path = os.path.join(
            os.getcwd(), remove_invalid_char(default_path))
    if filename is None:
        filename = remove_invalid_char(default_name)
    if os.path.isdir(path) is False:
        os.makedirs(path)
    temp = filename
    i = 0
    while os.path.isfile(os.path.join(path, temp) + '.' + mode):
        i += 1
        temp = filename + str(i)
    return os.path.join(path, temp) + '.' + mode
