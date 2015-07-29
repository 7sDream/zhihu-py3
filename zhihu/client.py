#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import time
import json
import requests
import importlib

from .common import *


class ZhihuClient:

    """Zhihu Client, with special account and/or cookies file."""

    def __init__(self, cookies_str=None):
        self._session = requests.Session()
        self._session.headers.update(Default_Header)
        if cookies_str is not None:
            assert isinstance(cookies_str, str)
            self.login_with_cookies(cookies_str)

    # ===== login staff =====

    @staticmethod
    def _get_captcha_url():
        return Captcha_URL_Prefix + str(int(time.time() * 1000))

    def get_captcha(self):
        """获取验证码.

        :return: 验证码图片数据。
        :rtype: bytes
        """
        r = self._session.get(self._get_captcha_url())
        return r.content

    def login(self, email='', password='', captcha=''):
        """登陆知乎.

        :param str email: 邮箱
        :param str password: 密码
        :param str captcha: 验证码
        :return:
            一个三元素元祖
            - 第一个元素代表是否成功（0表示成功）
            - 第二个元素为一个字符串，表示失败原因，若成功则为空字符串
            - 第三个元素为一个字符串，表示获得的cookies，失败为空字符串
        :rtype: (int, str, str)
        """
        data = {'email': email, 'password': password,
                'rememberme': 'y', 'captcha': captcha}
        r = self._session.post(Login_URL, data=data)
        j = r.json()
        code = int(j['r'])
        message = j['msg']
        cookies = json.dumps(self._session.cookies.get_dict()) \
            if code == 0 else ''
        return code, message, cookies

    def login_with_cookies(self, cookies_str):
        """根据cookies字符串登录知乎

        :param cookies_str: cookies 字符串，请传字符串，不要传字典。
        :return: 无
        :rtype: None
        """
        cookies_dict = json.loads(cookies_str)
        self._session.cookies.update(cookies_dict)

    def login_in_terminal(self):
        """不使用cookies，在终端中根据提示登陆知乎

        :return: 如果成功返回cookies字符串
        :rtype: str
        """
        print('====== zhihu login =====')

        email = input('email: ')
        password = input('password: ')

        captcha_data = self.get_captcha()
        with open('captcha.gif', 'wb') as f:
            f.write(captcha_data)

        print('please check captcha.gif for captcha')
        captcha = input('captcha: ')
        os.remove('captcha.gif')

        print('====== logging.... =====')

        code, msg, cookies = self.login(email, password, captcha)

        if code == 0:
            print('login successfully')
        else:
            print('login failed, reason: {0}'.format(msg))

        return cookies

    # ===== getter staff ======

    def __getattr__(self, item: str):
        attr_list = ['answer', 'author', 'collection',
                     'column', 'post', 'question', 'topic']
        if item.lower() in attr_list:
            module = importlib.import_module('.'+item.lower(), 'zhihu')
            return lambda url: \
                getattr(module, item.capitalize())(self._session, url)
