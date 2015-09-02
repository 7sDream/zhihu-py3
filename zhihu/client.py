#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = '7sDream'

import time
import json
import requests
import importlib

from .common import *


class ZhihuClient:

    """知乎客户端类，内部维护了自己专用的网络会话，可用cookies或账号密码登录."""

    def __init__(self, cookies=None):
        """创建客户端类实例.

        :param str cookies: 见 :meth:`.login_with_cookies` 中 ``cookies`` 参数
        :return: 知乎客户端对象
        :rtype: ZhihuClient
        """
        self._session = requests.Session()
        self._session.headers.update(Default_Header)
        if cookies is not None:
            assert isinstance(cookies, str)
            self.login_with_cookies(cookies)

    # ===== login staff =====

    @staticmethod
    def _get_captcha_url():
        return Captcha_URL_Prefix + str(int(time.time() * 1000))

    def get_captcha(self):
        """获取验证码数据。

        :return: 验证码图片数据。
        :rtype: bytes
        """
        # some unbelievable zhihu logic
        self._session.get(Zhihu_URL)
        data = {'email': '', 'password': '', 'remember_me': 'true'}
        self._session.post(Login_URL, data=data)

        r = self._session.get(self._get_captcha_url())
        return r.content

    def login(self, email, password, captcha):
        """登陆知乎.

        :param str email: 邮箱
        :param str password: 密码
        :param str captcha: 验证码
        :return:
            ======== ======== ============== ====================
            元素序号 元素类型 意义           说明
            ======== ======== ============== ====================
            0        int      是否成功       0为成功，1为失败
            1        str      失败原因       登录成功则为空字符串
            2        str       cookies字符串 登录失败则为空字符串
            ======== ======== ============== ====================

        :rtype: (int, str, str)
        """
        data = {'email': email, 'password': password,
                'remember_me': 'true', 'captcha': captcha}
        r = self._session.post(Login_URL, data=data)
        j = r.json()
        code = int(j['r'])
        message = j['msg']
        cookies_str = json.dumps(self._session.cookies.get_dict()) \
            if code == 0 else ''
        return code, message, cookies_str

    def login_with_cookies(self, cookies):
        """使用cookies文件或字符串登录知乎

        :param str cookies:
            ============== ===========================
            参数形式       作用
            ============== ===========================
            文件名         将文件内容作为cookies字符串
            cookies字符串  直接提供cookies字符串
            ============== ===========================
        :return: 无
        :rtype: None
        """
        if os.path.isfile(cookies):
            with open(cookies) as f:
                cookies = f.read()
        cookies_dict = json.loads(cookies)
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

    def create_cookies(self, file):
        cookies_str = self.login_in_terminal()
        if cookies_str:
            with open(file, 'w') as f:
                f.write(cookies_str)
            print('cookies file created.')
        else:
            print('can\'t create cookies.')

    # ===== network staff =====

    def set_proxy(self, proxy):
        """设置代理

        :param str proxy: 使用 "http://example.com:port" 的形式
        :return: 无
        :rtype: None

        :说明:
            由于一个 :class:`.ZhihuClient` 对象和它创建出来的其他知乎对象共用
            一个Session，所以调用这个方法也会将所有生成出的知乎类设置上代理。
        """
        self._session.proxies.update({'http': proxy})

    # ===== getter staff ======

    def me(self):
        """获取使用特定cookies的Me实例

        :return: cookies对应的Me对象
        :rtype: Me
        """
        from .me import Me
        headers = dict(Default_Header)
        headers['Host'] = 'zhuanlan.zhihu.com'
        res = self._session.get(Get_Me_Info_Url, headers=headers)
        json_data = res.json()
        url = json_data['profileUrl']
        name = json_data['name']
        motto = json_data['bio']
        photo = json_data['avatar']['template'].format(
            id=json_data['avatar']['id'], size='r')
        return Me(url, name, motto, photo, session=self._session)

    def __getattr__(self, item: str):
        """本函数用于获取各种类，如 `Answer` `Question` 等.

        :支持的形式有:
            1. client.answer()
            2. client.author()
            3. client.collection()
            4. client.column()
            5. client.post()
            6. client.question()
            7. client.topic()

            参数均为对应页面的url，返回对应的类的实例。
        """
        def getter(url):
            return getattr(module, item.capitalize())(url,
                                                      session=self._session)
        attr_list = ['answer', 'author', 'collection',
                     'column', 'post', 'question', 'topic']
        if item.lower() in attr_list:
            module = importlib.import_module('.'+item.lower(), 'zhihu')
            return getter
