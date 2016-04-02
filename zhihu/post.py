#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .common import *
from .base import BaseZhihu, JsonAsSoupMixin


class Post(JsonAsSoupMixin, BaseZhihu):

    """专栏文章类，请使用``ZhihuClient.post``方法构造对象."""

    @class_common_init(re_post_url)
    def __init__(self, url, column=None, author=None, title=None,
                 upvote_num=None, comment_num=None, session=None):
        """创建专栏文章类实例.

        :param str url: 文章url
        :param Column column: 文章所属专栏，可选
        :param Author author: 文章作者，可选
        :param str title: 文章标题，可选
        :param int upvote_num: 文章赞同数，可选
        :param int comment_num: 文章评论数，可选
        :param Session session: 使用的网络会话，为空则使用新会话
        :return: 专栏文章对象
        :rtype: Post
        """
        match = re_post_url.match(url)
        self.url = url
        self._session = session
        self._column = column
        self._author = author
        self._title = title
        self._upvote_num = upvote_num
        self._comment_num = comment_num
        self._slug = int(match.group(1))  # 文章编号

    def _make_soup(self):
        if self.soup is None:
            json = self._get_content()
            self._gen_soup(json)

    def _get_content(self):
        origin_host = self._session.headers.get('Host')
        self._session.headers.update(Host='zhuanlan.zhihu.com')
        json = self._session.get(Column_Post_Data.format(self.slug)).json()
        self._session.headers.update(Host=origin_host)
        return json

    @property
    def column_in_name(self):
        """获取文章所在专栏的内部名称（用不到就忽视吧~）

        :return: 专栏的内部名称
        :rtype: str
        """
        self._make_soup()
        if 'column' in self.soup:
            return self.soup['column']['slug']
        else:
            return None

    @property
    def slug(self):
        """获取文章的编号（用不到就忽视吧~）

        :return: 文章编号
        :rtype: int
        """
        return self._slug

    @property
    @check_soup('_column')
    def column(self):
        """获取文章所在专栏.

        :return: 文章所在专栏
        :rtype: Column
        """
        from .column import Column

        if 'column' in self.soup:
            url = Column_Url + '/' + self.soup['column']['slug']
            name = self.soup['column']['name']
            return Column(url, name, session=self._session)
        else:
            return None

    @property
    @check_soup('_author')
    def author(self):
        """获取文章作者.

        :return: 文章作者
        :rtype: Author
        """
        from .author import Author

        url = self.soup['author']['profileUrl']
        name = self.soup['author']['name']
        motto = self.soup['author']['bio']
        template = self.soup['author']['avatar']['template']
        photo_id = self.soup['author']['avatar']['id']
        photo_url = template.format(id=photo_id, size='r')
        return Author(url, name, motto, photo_url=photo_url,
                      session=self._session)

    @property
    @check_soup('_title')
    def title(self):
        """获取文章标题.

        :return: 文章标题
        :rtype: str
        """
        return self.soup['title']

    @property
    @check_soup('_upvote_num')
    def upvote_num(self):
        """获取文章赞同数量.

        :return: 文章赞同数
        :rtype: int
        """
        return int(self.soup['likesCount'])

    @property
    @check_soup('_comment_num')
    def comment_num(self):
        """获取评论数量.

        :return: 评论数量
        :rtype: int
        """
        return self.soup['commentsCount']

    def save(self, filepath=None, filename=None, mode="md"):
        """保存答案为 Html 文档或 markdown 文档.

        :param str filepath: 要保存的文件所在的目录，
            不填为当前目录下以专栏标题命名的目录, 设为"."则为当前目录。
        :param str filename: 要保存的文件名，
            不填则默认为 所在文章标题 - 作者名.html/md。
            如果文件已存在，自动在后面加上数字区分。
            **自定义文件名时请不要输入后缀 .html 或 .md。**
        :param str mode: 保存类型，可选 `html` 、 `markdown` 、 `md` 。
        :return: 无
        :rtype: None
        """
        if mode not in ["html", "md", "markdown"]:
            raise ValueError("`mode` must be 'html', 'markdown' or 'md',"
                             " got {0}".format(mode))
        self._make_soup()
        file = get_path(filepath, filename, mode, self.column.name,
                        self.title + '-' + self.author.name)
        with open(file, 'wb') as f:
            if mode == "html":
                f.write(self.soup['content'].encode('utf-8'))
            else:
                import html2text
                h2t = html2text.HTML2Text()
                h2t.body_width = 0
                f.write(h2t.handle(self.soup['content']).encode('utf-8'))

    @property
    def upvoters(self):
        """获取文章的点赞用户

        :return: 文章的点赞用户，返回生成器。
        """
        from .author import Author, ANONYMOUS
        self._make_soup()
        headers = dict(Default_Header)
        headers['Host'] = 'zhuanlan.zhihu.com'
        json = self._session.get(
            Post_Get_Upvoter.format(self.slug),
            headers=headers
        ).json()
        for au in json:
            try:
                yield Author(
                        au['profileUrl'],
                        au['name'],
                        au['bio'],
                        photo_url=au['avatar']['template'].format(
                                id=au['avatar']['id'], size='r'),
                        session=self._session
                )
            except ValueError:  # invalid url
                yield ANONYMOUS
