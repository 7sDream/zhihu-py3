#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import re
import os

from requests import Session
from bs4 import BeautifulSoup as _Bs
from bs4 import Tag, NavigableString
from requests.packages.urllib3.util import Retry

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

Zhihu_URL = 'https://www.zhihu.com'
Login_URL = Zhihu_URL + '/login/email'
Captcha_URL = Zhihu_URL + '/captcha.gif'
Get_Profile_Card_URL = Zhihu_URL + '/node/MemberProfileCardV2'
Question_Get_More_Answer_URL = Zhihu_URL + '/node/QuestionAnswerListV2'
Answer_Add_Comment_URL = Zhihu_URL + '/node/AnswerCommentAddV2'
Answer_Comment_Box_URL = Zhihu_URL + '/node/AnswerCommentBoxV2'
Get_Answer_Comment_URL = Zhihu_URL + '/r/answers/{0}/comments'
Author_Get_More_Followers_URL = Zhihu_URL + '/node/ProfileFollowersListV2'
Author_Get_More_Followees_URL = Zhihu_URL + '/node/ProfileFolloweesListV2'
Author_Get_More_Follow_Column_URL = Zhihu_URL + \
                                    '/node/ProfileFollowedColumnsListV2'
Author_Get_More_Follow_Topic_URL = Zhihu_URL + \
                                   '/people/{0}/topics'

PROTOCOL = ''

Column_Url = 'http://zhuanlan.zhihu.com'
Column_API = Column_Url + '/api/columns'
Column_Data = Column_API + '/{0}'
Column_Posts_Data = Column_API + '/{0}/posts?limit=10&offset={1}'
Column_Post_Data = Column_Url + '/api/posts/{0}'
Post_Get_Upvoter = Column_Post_Data + '/likers'

Topic_Url = Zhihu_URL + '/topic'
Topic_Get_Children_Url = Topic_Url + '/{0}/organize/entire'
Topic_Get_More_Follower_Url = Topic_Url + '/{0}/followers'
Topic_Questions_Url = Topic_Url + '/{0}/questions'
Topic_Unanswered_Question_Url = Topic_Url + '/{0}/unanswered'
Topic_Top_Answers_Url = Topic_Url + '/{0}/top-answers'
Topic_Hot_Questions_Url = Topic_Url + '/{0}/hot'
Topic_Newest_Url = Topic_Url + '/{0}/newest'

Get_Me_Info_Url = Column_Url + '/api/me'
Upvote_Answer_Url = Zhihu_URL + '/node/AnswerVoteBarV2'
Upvote_Article_Url = Column_API + '/{0}/posts/{1}/rating'
Follow_Author_Url = Zhihu_URL + '/node/MemberFollowBaseV2'
Follow_Question_Url = Zhihu_URL + '/node/QuestionFollowBaseV2'
Follow_Topic_Url = Zhihu_URL + '/node/TopicFollowBaseV2'
Follow_Collection_Url = Zhihu_URL + '/collection/follow'
Unfollow_Collection_Url = Zhihu_URL + '/collection/unfollow'
Thanks_Url = Zhihu_URL + '/answer/thanks'
Cancel_Thanks_Url = Zhihu_URL + '/answer/cancel_thanks'
Send_Message_Url = Zhihu_URL + '/inbox/post'
Unhelpful_Url = Zhihu_URL + '/answer/not_helpful'
Cancel_Unhelpful_Url = Zhihu_URL + '/answer/helpful'
Get_Collection_Url = Zhihu_URL + '/node/AnswerFavlists'

re_question_url = re.compile(
    r'^https?://www\.zhihu\.com/question/\d+(\?sort=created|/?)$')
re_question_url_std = re.compile(r'^https?://www\.zhihu\.com/question/\d+/?')
re_ans_url = re.compile(
    r'^https?://www\.zhihu\.com/question/\d+/answer/\d+/?$')
re_author_url = re.compile(r'^https?://www\.zhihu\.com/(?:people|org)/[^/]+/?$')
re_collection_url = re.compile(r'^https?://www\.zhihu\.com/collection/\d+/?$')
re_column_url = re.compile(r'^http://zhuanlan\.zhihu\.com/([^/]+)/?$')
re_post_url = re.compile(r'^http://zhuanlan\.zhihu\.com/p/(\d+)/?$')
re_topic_url = re.compile(r'^https?://www\.zhihu\.com/topic/(\d+)/?$')
re_a2q = re.compile(r'(.*)/answer/.*')
re_collection_url_split = re.compile(r'.*(/c.*)')
re_get_number = re.compile(r'[^\d]*(\d+).*')
re_del_empty_line = re.compile(r'\n*(.*)\n*')


def check_soup(attr, soup_type='_make_soup'):
    def real(func):
        @functools.wraps(func)
        def wrapper(self):
            # noinspection PyTypeChecker
            value = getattr(self, attr, None)
            if value is None:
                if soup_type == '_make_soup':
                    getattr(self, soup_type)()
                elif self.soup is None:
                    getattr(self, soup_type)()
                value = func(self)
                setattr(self, attr, value)
            return value

        return wrapper

    return real


def class_common_init(url_re, allowed_none=True, trailing_slash=True):
    def real(func):
        @functools.wraps(func)
        def wrapper(self, url, *args, **kwargs):
            if url is None and not allowed_none:
                raise ValueError('Invalid Url: ' + url)
            if url is not None:
                if url_re.match(url) is None:
                    raise ValueError('Invalid URL: ' + url)
                if not url.endswith('/') and trailing_slash:
                    url += '/'
            if 'session' not in kwargs.keys() or kwargs['session'] is None:
                kwargs['session'] = Session()
                kwargs['session'].mount('https://', Retry(5))
                kwargs['session'].mount('http://', Retry(5))
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
    author_link = author.find('a', class_='author-link')
    if author_link is None:
        return None, '匿名用户', '', ''
    else:
        author_name = author_link.text
        motto_span = author.find('span', class_='bio')
        author_motto = motto_span['title'] \
            if motto_span is not None else ''
        author_url = Zhihu_URL + author_link['href']
        avatar_link = author.find('a', class_='avatar-link')
        photo_url = PROTOCOL + avatar_link.img['src'].replace('_s', '_r')
        return author_url, author_name, author_motto, photo_url


def parser_author_from_comment(author):
    author_avatar = author.find('a', class_='zm-item-link-avatar')
    if author_avatar is None:
        return None, '匿名用户', ''
    else:
        author_link = author.find('a', class_='zg-link')
        author_name = author_link.text
        author_url = author_link['href']
        avatar_link = author.find('img', class_='zm-item-img-avatar')
        photo_url = PROTOCOL + avatar_link['src'].replace('_s', '_r')
        return author_url, author_name,  photo_url


def answer_content_process(content):
    content = clone_bs4_elem(content)
    del content['class']
    soup = BeautifulSoup(
        '<html><head><meta charset="utf-8"></head><body></body></html>')
    soup.body.append(content)
    no_script_list = soup.find_all("noscript")
    for no_script in no_script_list:
        no_script.extract()
    img_list = soup.find_all(
        "img", class_=["origin_image", "content_image"])
    for img in img_list:
        if "content_image" in img['class']:
            img['data-original'] = img['data-actualsrc']
        new_img = soup.new_tag('img', src=PROTOCOL + img['data-original'])
        img.replace_with(new_img)
        if img.next_sibling is None:
            new_img.insert_after(soup.new_tag('br'))
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


def common_follower(url, xsrf, session):
    from .author import Author, ANONYMOUS
    headers = dict(Default_Header)
    headers['Referer'] = url
    data = {'offset': 0, '_xsrf': xsrf}
    gotten_data_num = 20
    offset = 0
    while gotten_data_num == 20:
        data['offset'] = offset
        res = session.post(url, data=data, headers=headers)
        json_data = res.json()['msg']
        gotten_data_num = json_data[0]
        offset += gotten_data_num
        soup = BeautifulSoup(json_data[1])
        follower_divs = soup.find_all('div', class_='zm-profile-card')
        for div in follower_divs:
            if div.a is not None:
                author_name = div.a['title']
                author_url = Zhihu_URL + div.a['href']
                author_motto = div.find('span', class_='bio').text
                author_photo = PROTOCOL + div.img['src'].replace('_m', '_r')
                numbers = [re_get_number.match(a.text).group(1)
                           for a in div.find_all('a', target='_blank')]
                try:
                    yield Author(author_url, author_name, author_motto,
                                 *numbers, photo_url=author_photo,
                                 session=session)
                except ValueError:  # invalid url
                    yield ANONYMOUS
            else:
                yield ANONYMOUS


def clone_bs4_elem(el):
    """Clone a bs4 tag before modifying it.

    Code from `http://stackoverflow.com/questions/23057631/clone-element-with
    -beautifulsoup`
    """
    if isinstance(el, NavigableString):
        return type(el)(el)

    copy = Tag(None, el.builder, el.name, el.namespace, el.nsprefix)
    # work around bug where there is no builder set
    # https://bugs.launchpad.net/beautifulsoup/+bug/1307471
    copy.attrs = dict(el.attrs)
    for attr in ('can_be_empty_element', 'hidden'):
        setattr(copy, attr, getattr(el, attr))
    for child in el.contents:
        copy.append(clone_bs4_elem(child))
    return copy
